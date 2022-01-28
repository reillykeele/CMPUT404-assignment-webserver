from constants import HttpStatus

class HttpHelper: 
    def get_status_line(httpStatus: HttpStatus) -> str:
        return 'HTTP/1.1 ' + str(httpStatus.value) + ' ' + httpStatus.phrase
    
    def get_location_line(host: str, uri: str) -> str:
        return "Location: http://" + host + uri + '/'

    def get_contenttype_line(contentType: str, encodingType: str = None) -> str:
        contentTypeLine = 'Content-Type: ' + contentType
            
        if encodingType is not None:
            contentTypeLine += '; charset=' + encodingType
        
        return contentTypeLine

    def get_contentlength_line(len) -> str:
        return 'Content-Length: ' + str(len)

    def get_server_line() -> str:
        return 'Server: '