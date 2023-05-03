from dataclasses import dataclass


@dataclass
class Archive:

    id : int
    progress : int
    status : str


