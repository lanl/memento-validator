from mementoweb.validator.pipelines import DefaultPipeline


class TimeGate(DefaultPipeline):

    def __init__(self):
        pass

    def validate(self, uri):
        return []