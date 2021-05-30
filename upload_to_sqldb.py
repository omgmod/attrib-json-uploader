
from services.WarcpDataService import WarcpDataService
from utils.FileUtils import FileUtils

CLEAN_JSON_RELATIVE_PATH = './json/clean'

# Load json file
units_json = FileUtils.read_json_file(f"{CLEAN_JSON_RELATIVE_PATH}/units.json")
entities_json = FileUtils.read_json_file(f"{CLEAN_JSON_RELATIVE_PATH}/entities.json")

# Get latest version from db
warcp_data_service = WarcpDataService()
version_id = warcp_data_service.get_version()

# pass to data service to insert
# for idx, unit in enumerate(units_json):
warcp_data_service.insert_units(units_json, version_id)
warcp_data_service.insert_entities(entities_json, version_id)

print(f"Uploaded {len(units_json)} unit stats records for version {version_id}")
print(f"Uploaded {len(entities_json)} entity stats records for version {version_id}")
