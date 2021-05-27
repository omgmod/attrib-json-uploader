import configparser


class Config:
    __instance = None

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance is not None:
            raise Exception("Singletons should be instantiated only once")
        else:
            Config.__instance = configparser.ConfigParser()
            Config.__instance.read(Config.CONFIG_PATH)

    CONFIG_PATH = './config.ini'
