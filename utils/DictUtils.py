class DictUtils:

    @staticmethod
    def add_to_dict_if_in_source(source, target, key, target_key=None):
        if key in source:
            if target_key:
                target[target_key] = source[key]
            else:
                target[key] = source[key]

