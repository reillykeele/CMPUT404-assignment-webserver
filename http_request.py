from config import Config
from constants import Encoding, HttpStatus
from http_helper import HttpHelper

class HttpRequest:    
    def __init__(self, httpMethod, httpVersion, uri, headers):
        self.httpMethod = httpMethod
        self.httpVersion = httpVersion
        self.uri = uri
        self.headers = headers    

    def __init__(self, request):        
        self.request = request
        req = request.recv(Config.BUFFER_SIZE).decode(Encoding.DEFAULT).split('\r\n')

        # parse method, http version        
        try:
            self.httpMethod, self.uri, self.httpVersion = req[0].split(' ')        
        except:
            return self.respond(HttpStatus.BAD_REQUEST)

        # parse headers 
        self.headers = {}
        for line in req[1:]:            
            if not line: continue
            key, val = line.split(': ')
            self.headers[key] = val            

    def __str__(self) -> str:
        return self.httpMethod + ' ' + self.uri + ' ' + self.httpVersion + '\n' + str(self.headers)

    def respond(self, status: HttpStatus, body: bytearray = b'', additionalHeaders = []) -> bool:    
        headers = [HttpHelper.get_status_line(status), HttpHelper.get_contentlength_line(len(body))]

        # include any additional headers that were supplied (ex. Location)
        if len(additionalHeaders) > 0:
            headers.extend(additionalHeaders)

        # Create our message, encode it as a byte array, and send it 
        message = '\r\n'.join(headers) + '\r\n\r\n'

        print(message)
        self.request.sendall(bytearray(message, Encoding.DEFAULT) + body)
        return True
