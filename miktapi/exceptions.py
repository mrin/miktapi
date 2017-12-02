class UnpackerException(Exception):
    pass


class BufferFull(UnpackerException):
    pass


class OutOfData(UnpackerException):
    pass


class UnpackValueError(UnpackerException, ValueError):
    pass


class UnknownControlByteError(UnpackValueError):
    pass


class PackException(Exception):
    pass


class ParseException(Exception):
    pass
