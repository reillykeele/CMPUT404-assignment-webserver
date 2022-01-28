from http import HTTPStatus

class HttpHelper: 
    def get_status_line(httpStatus: HTTPStatus) -> str:
        return 'HTTP/1.1 ' + str(httpStatus.value) + ' ' + httpStatus.phrase
    
    def get_location_line(host: str, uri: str) -> str:
        return "Location: http://" + host + uri + '/'

    def get_contenttype_line(contentType: str) -> str:
        return 'Content-Type: ' + contentType

    def get_contentlength_line(len) -> str:
        return 'Content-Length: ' + str(len)