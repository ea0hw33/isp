from dataclasses import dataclass


@dataclass
class User:
    username: str
    login: str
    password: str
