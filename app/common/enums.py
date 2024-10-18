from enum import Enum


class Status(Enum):
    in_queue = "In Queue"
    run = "Run"
    completed = "Completed"
    failed = "Failed"
