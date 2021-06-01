from typing import Set, Tuple, Dict, AnyStr, List

import paramiko
import sshtunnel
from sqlalchemy import create_engine, text, insert, Table, MetaData, Column, Integer, String
from sqlalchemy.engine import Connection

from Config import Config

metadata = MetaData()

units_table = Table(
    "stats_units",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('reference', String(100)),
    Column('CONSTNAME', String(100)),
    Column('short_constname', String(100)),
    Column('faction', String(10)),
    Column('type', String(20)),
    Column('version_id', Integer),
    Column('json', String),
)

entities_table = Table(
    "stats_entities",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('reference', String(100)),
    Column('faction', String(10)),
    Column('type', String(20)),
    Column('version_id', Integer),
    Column('json', String),
)

weapons_table = Table(
    "stats_weapons",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('reference', String(200)),
    Column('type', String(100)),
    Column('version_id', Integer),
    Column('json', String),
)

upgrades_table = Table(
    "stats_upgrades",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('reference', String(200)),
    Column('faction', String(50)),
    Column('CONSTNAME', String(100)),
    Column('version_id', Integer),
    Column('json', String),
)

slot_items_table = Table(
    "stats_slot_items",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('reference', String(200)),
    Column('version_id', Integer),
    Column('json', String),
)

def rds_connection_wrapper(function):
    def wrap_function(*args, **kwargs):
        aws_config = Config.get_instance()['AWS']
        db_host = aws_config['DB_HOST']
        db_port = aws_config['DB_PORT']
        db_user = aws_config['DB_USER']
        db_pass = aws_config['DB_PASS']
        db_name = aws_config['DB_NAME']

        private_key = paramiko.RSAKey.from_private_key_file(f"./{aws_config['EC2_KEY']}")

        # https://stackoverflow.com/questions/58373690/connecting-to-mysql-database-via-ssh-over-a-jump-host-using-python-3
        # https://stackoverflow.com/questions/45213676/access-remote-db-via-ssh-tunnel-python-3
        with sshtunnel.SSHTunnelForwarder(
                (aws_config['EC2_HOST'], int(aws_config['EC2_PORT'])),
                ssh_username=aws_config['EC2_USER'],
                ssh_pkey=private_key,
                remote_bind_address=(db_host, int(db_port))
        ) as tunnel:
            port = tunnel.local_bind_port
            engine = create_engine(f"mysql+mysqldb://{db_user}:{db_pass}@127.0.0.1:{port}/{db_name}", echo=True,
                                   future=True)

            with engine.connect() as connection:
                kwargs['connection'] = connection
                return function(*args, **kwargs)

    return wrap_function


class WarcpDataService:

    @rds_connection_wrapper
    def get_version(self, connection: Connection = None,) -> AnyStr:
        result = connection.execute(text("SELECT id, version FROM versions order by id desc limit 1")).fetchone()
        if result is None:
            raise Exception("No version found")
        version_id, version = result
        print(f"Using version id {version_id} of {version}")
        return version_id

    @rds_connection_wrapper
    def insert_units(self, data: List[Dict], version_id: int, connection: Connection = None) -> None:
        """"""
        stmt_input = []
        for unit in data:
            stmt_input.append({
                'reference': unit['reference'],
                'CONSTNAME': f"{unit['faction']}.{unit['constname']}",
                'short_constname': unit['constname'],
                'faction': unit['faction'],
                'type': unit['type'],
                'version_id': version_id,
                'json': unit,
            })
        
        connection.execute(units_table.insert(), stmt_input)
        connection.commit()

    @rds_connection_wrapper
    def insert_entities(self, data: List[Dict], version_id: int, connection: Connection = None) -> None:
        """"""
        stmt_input = []
        for entity in data:
            stmt_input.append({
                'reference': entity['reference'],
                'faction': entity.get('faction'),
                'type': entity['type'],
                'version_id': version_id,
                'json': entity,
            })

        connection.execute(entities_table.insert(), stmt_input)
        connection.commit()

    @rds_connection_wrapper
    def insert_weapons(self, data: List[Dict], version_id: int, connection: Connection = None) -> None:
        stmt_input = []
        for weapon in data:
            stmt_input.append({
                'reference': weapon['reference'],
                'type': weapon['type'],
                'version_id': version_id,
                'json': weapon,
            })

        connection.execute(weapons_table.insert(), stmt_input)
        connection.commit()

    @rds_connection_wrapper
    def insert_upgrades(self, data: List[Dict], version_id: int, connection: Connection = None) -> None:
        stmt_input = []
        for upgrade in data:
            stmt_input.append({
                'reference': upgrade['reference'],
                'faction': upgrade.get('faction'),
                'CONSTNAME': upgrade.get('constname'),
                'version_id': version_id,
                'json': upgrade,
            })

        connection.execute(upgrades_table.insert(), stmt_input)
        connection.commit()

    @rds_connection_wrapper
    def insert_slot_items(self, data: List[Dict], version_id: int, connection: Connection = None) -> None:
        stmt_input = []
        for slot_item in data:
            stmt_input.append({
                'reference': slot_item['reference'],
                'version_id': version_id,
                'json': slot_item,
            })

        connection.execute(slot_items_table.insert(), stmt_input)
        connection.commit()

    @rds_connection_wrapper
    def get_base_constnames(self,
                            connection: Connection = None,
                            ) -> Tuple[Set[AnyStr], Dict[AnyStr, Set[AnyStr]], Dict[AnyStr, Set[AnyStr]], Dict[AnyStr, Set[AnyStr]]]:
        # Get Faction constnames
        result = connection.execute(text("select CONSTNAME from factions")).all()
        faction_constnames = {x['CONSTNAME'] for x in result}
        print(faction_constnames)

        # Get units by faction
        units_by_faction = WarcpDataService._get_constnames_by_faction(connection, faction_constnames, 'units')

        # Get docmarkers by faction
        docmarkers_by_faction = WarcpDataService._get_constnames_by_faction(connection, faction_constnames, 'doctrineabilities', tier=True)

        # Get upgrades by faction
        upgrades_by_faction = WarcpDataService._get_constnames_by_faction(connection, faction_constnames, 'upgrades')

        # Merge in units_modified to units
        units_modified_by_faction = WarcpDataService._get_constnames_by_faction(connection, faction_constnames, 'units_modified')
        WarcpDataService._merge_constnames_by_faction(faction_constnames, units_by_faction, units_modified_by_faction)

        # Merge in upgrades_modified to upgrades
        upgrades_modified_by_faction = WarcpDataService._get_constnames_by_faction(connection, faction_constnames, 'upgrades_modified')
        WarcpDataService._merge_constnames_by_faction(faction_constnames, upgrades_by_faction, upgrades_modified_by_faction)

        return faction_constnames, units_by_faction, upgrades_by_faction, docmarkers_by_faction

    @staticmethod
    def _get_constnames_by_faction(connection: Connection,
                                   faction_constnames: Set[AnyStr],
                                   tablename: AnyStr,
                                   tier=False
                                   ) -> Dict[AnyStr, Set[AnyStr]]:
        by_faction = {}
        for faction in faction_constnames:
            result = connection.execute(
                text(f"select CONSTNAME from {tablename} where CONSTNAME like '{faction}%' {'and tier > 0' if tier else ''}"))
            by_faction[faction] = {x['CONSTNAME'] for x in result}
        return by_faction

    @staticmethod
    def _merge_constnames_by_faction(faction_constnames: Set[AnyStr],
                                     by_faction: Dict[AnyStr, Set[AnyStr]],
                                     modified_by_faction: Dict[AnyStr, Set[AnyStr]],
                                     ) -> None:
        if len(modified_by_faction) > 0:
            for faction in faction_constnames:
                if faction in modified_by_faction:
                    units_modified = modified_by_faction[faction]
                    by_faction[faction].update(units_modified)
