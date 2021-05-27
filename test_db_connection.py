from sqlalchemy import create_engine, text
import paramiko
import sshtunnel

from Config import Config


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
    engine = create_engine(f"mysql+mysqldb://{db_user}:{db_pass}@127.0.0.1:{port}/{db_name}", echo=True, future=True)

    with engine.connect() as connection:
        result = connection.execute(text("select * from units"))
        print(result.all())




