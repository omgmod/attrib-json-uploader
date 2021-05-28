
class AbstractModel:

    def __init__(self, raw_json):
        self.raw_json = raw_json

    def clean(self):
        """
            Returns the clean representation of the model.
        """
        pass
