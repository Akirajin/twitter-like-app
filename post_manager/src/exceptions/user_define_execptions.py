class Error(Exception):
    """Base class for other exceptions"""
    pass


class MessageTooLong(Error):
    """Message should be less or equal than 777"""
    pass


class UserNotFound(Error):
    """Username not found"""
    pass


class DailyPostLimitReached(Error):
    """Post should be created only 5 per day"""
    pass
