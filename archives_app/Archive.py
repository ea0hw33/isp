from dataclasses import dataclass

list_of_archives = []
dict_of_archive_names = {}

@dataclass
class Archive:
    id: int
    progress: int
    status: str
