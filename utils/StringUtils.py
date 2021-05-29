
class StringUtils:

    @staticmethod
    def remove_bracket_wrapping(text):
        return text.replace('[[', '').replace(']]', '')

    @staticmethod
    def remove_file_endings(text):
        return text.replace('.lua', '').replace('.rgd', '')

    @staticmethod
    def remove_bracket_file_endings(text):
        return StringUtils.remove_file_endings(StringUtils.remove_bracket_wrapping(text))
