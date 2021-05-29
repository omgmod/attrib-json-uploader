import json
import os
import shutil
from typing import AnyStr, Dict, Any


class FileUtils:

    @staticmethod
    def read_json_file(filename: AnyStr) -> Dict[Any, Any]:
        """
            Open and read a json file's contents as a dict
        """
        file = open(filename, mode='r')
        file_contents = json.load(file)
        file.close()

        return file_contents

    @staticmethod
    def clear_directory_of_filetype(folderpath: AnyStr, filetype: AnyStr) -> None:
        print(f"Begin removing all {filetype} files from {folderpath}")
        for file in os.listdir(folderpath):
            if not file.endswith(filetype):
                continue
            os.remove(os.path.join(folderpath, file))
        print(f"Finished removing all {filetype} files from {folderpath}")

    @staticmethod
    def copy_directory(source_directory_path, destination_directory_path):
        print(f"Copying contents of {source_directory_path} to {destination_directory_path}")
        for filename in os.listdir(source_directory_path):
            shutil.copy2(os.path.join(source_directory_path, filename), os.path.join(destination_directory_path, filename))
