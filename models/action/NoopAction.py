from models.action.Action import Action


class NoopAction(Action):
    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        return None
