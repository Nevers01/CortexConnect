from dataclasses import dataclass


@dataclass
class Server:
    id: int | None
    name: str
    type: str
    host: str
    port: int
    username: str
    password: str = ""
    notes: str = ""