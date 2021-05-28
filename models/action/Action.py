from models.AbstractModel import AbstractModel


class Action(AbstractModel):

    def __init__(self, raw_json):
        """

        """
        super().__init__(raw_json)

    @staticmethod
    def get_reference_with_depth(path, depth):
        return path.split('\\')[depth].replace('.lua]]', '')