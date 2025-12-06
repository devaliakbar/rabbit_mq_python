from dataclasses import dataclass


@dataclass
class StatusRes:
    status: str = "Success"
