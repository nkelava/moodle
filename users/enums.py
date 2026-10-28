from enum import Enum


# Create your forms here.

class RoleChoices(Enum):
    PROFESSOR = 'professor'
    STUDENT = 'student'


class StatusChoices(Enum):
    NONE = 'none'
    FULL_TIME = 'full time'
    PART_TIME = 'part time'


