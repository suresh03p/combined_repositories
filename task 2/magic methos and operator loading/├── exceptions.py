class LibraryException(Exception):
    """Base library exception"""
    pass


class BookNotFoundError(LibraryException):
    pass


class MemberNotFoundError(LibraryException):
    pass


class BookUnavailableError(LibraryException):
    pass