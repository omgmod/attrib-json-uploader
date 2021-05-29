
class StringUtils:

    @staticmethod
    def remove_bracket_wrapping(text):
        return text.replace('[[', '').replace(']]', '')
