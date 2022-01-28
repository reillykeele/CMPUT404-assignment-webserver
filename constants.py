from enum import IntEnum

class HttpStatus(IntEnum):
    # From https://github.com/python/cpython/blob/3.10/Lib/http/__init__.py
    def __new__(self, value, phrase):
        obj = int.__new__(self, value)
        obj._value_ = value

        obj.phrase = phrase
        return obj

    # 200
    OK = 200, 'OK'

    # 300
    MOVED_PERMANENTLY = 301, 'Moved Permanently'

    # 400 
    BAD_REQUEST = 400, 'Bad Request'
    NOT_FOUND = 404, 'Not Found'
    METHOD_NOT_ALLOWED = 405, 'Method Not Allowed'
    

    # 500
    INTERNAL_SERVER_ERROR = 500, 'Internal Server Error'
    HTTP_VERSION_NOT_SUPPORTED = 505, 'HTTP Version Not Supported'


class HttpMethod:
    Get = 'GET'
    Post = 'POST'
    Put = 'PUT'
    Delete = 'DELETE'    

class Encoding:
    DEFAULT = 'utf-8'
    TEXT = "ISO-8859-1"

class ContentType:
    Default = 'application/octet-stream'    
    JSON = 'application/json'
    JavaScript = 'application/javascript'    
    PDF = 'application/pdf'
    HTML = 'text/html'
    CSS = 'text/html'
    JPEG = 'image/jpeg'
    PNG = 'image/png'
    