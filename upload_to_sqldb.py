import json

from services.WarcpDataService import WarcpDataService
from utils.FileUtils import FileUtils


def parse_weapons_in_batches(weapons):
    number = len(weapons)
    batch = (number // 80) + 1

    start = 0
    end = batch
    result = []
    for i in range(0, 80):
        section = weapons[start:end]
        weapons_string = json.dumps(section)

        replaced_weapons_string = weapons_string.replace('\\', '/').replace('//', '/')

        try:
            result.extend(json.loads(replaced_weapons_string))
        except json.decoder.JSONDecodeError:
            print(replaced_weapons_string)
            raise
        print(f"Finished index [{start}:{end}]")
        start = end + 1
        end = end + batch + 1
    print("finished")

    return result


CLEAN_JSON_RELATIVE_PATH = './json/clean'

# Load json file
units_json = FileUtils.read_json_file(f"{CLEAN_JSON_RELATIVE_PATH}/units.json")
entities_json = FileUtils.read_json_file(f"{CLEAN_JSON_RELATIVE_PATH}/entities.json")
weapons_json = FileUtils.read_json_file(f"{CLEAN_JSON_RELATIVE_PATH}/weapons.json")
upgrades_json = FileUtils.read_json_file(f"{CLEAN_JSON_RELATIVE_PATH}/upgrades.json")
slot_items_json = FileUtils.read_json_file(f"{CLEAN_JSON_RELATIVE_PATH}/slot_items.json")

# Get latest version from db
warcp_data_service = WarcpDataService()
version_id = warcp_data_service.get_version()

units_json = json.loads(json.dumps(units_json).replace('\\', '/').replace('//', '/'))
entities_json = json.loads(json.dumps(entities_json).replace('\\', '/').replace('//', '/'))
weapons_json = json.loads(json.dumps(weapons_json).replace('\\', '/').replace('//', '/'))
upgrades_json = json.loads(json.dumps(upgrades_json).replace('\\', '/').replace('//', '/'))
slot_items_json = json.loads(json.dumps(slot_items_json).replace('\\', '/').replace('//', '/'))

# pass to data service to insert
# for idx, unit in enumerate(units_json):
warcp_data_service.insert_units(units_json, version_id)
warcp_data_service.insert_entities(entities_json, version_id)
warcp_data_service.insert_weapons(weapons_json, version_id)
warcp_data_service.insert_upgrades(upgrades_json, version_id)
warcp_data_service.insert_slot_items(slot_items_json, version_id)

print(f"Uploaded {len(units_json)} unit stats records for version {version_id}")
print(f"Uploaded {len(entities_json)} entity stats records for version {version_id}")
print(f"Uploaded {len(weapons_json)} weapon stats records for version {version_id}")
print(f"Uploaded {len(upgrades_json)} upgrade stats records for version {version_id}")
print(f"Uploaded {len(slot_items_json)} slot_item stats records for version {version_id}")
