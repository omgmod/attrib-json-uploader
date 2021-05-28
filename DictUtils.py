class DictUtils:

    @staticmethod
    def add_to_dict_if_in_source(key, source, target):
        if key in source:
            target[key] = source[key]

