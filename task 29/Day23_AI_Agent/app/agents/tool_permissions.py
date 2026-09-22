from enum import StrEnum


class Permission(StrEnum):
    READ = "read"
    COMPUTE = "compute"


DEFAULT_PERMISSIONS = frozenset({Permission.READ, Permission.COMPUTE})
