class CordException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BoardException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)