from mementoweb.validator.errors import DefaultError
import typing

class DefaultPipeline:

    def validate(self, uri: str) -> typing.List[DefaultError]:
        return []
