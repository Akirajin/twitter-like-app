

class Error(Exception):
    """Base class for other exceptions"""
    pass


class NonAlphanumericError(Error):
    """Non alphanumeric"""
    pass


class UserNameTooLongError(Error):
    pass


class UserNameAlreadyTaken(Error):
    """Username is already taken"""
    pass


class UserNotFound(Error):
    """Username not found"""
    pass


class FollowingHimselfError(Error):
    """Cannot follow yourself"""
    pass
