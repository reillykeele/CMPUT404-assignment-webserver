#  coding: utf-8 
from distutils.command.config import config
import socketserver
from config import Config
from constants import ContentType, HttpMethod, HttpStatus
from http_helper import HttpHelper
from http_request import HttpRequest
import mimetypes
import os

# Copyright 2022 Reilly Keele
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):               
        # Create a request              
        httpRequest = HttpRequest(self.request)        

        # Check if we can service the request
        if httpRequest.httpVersion != 'HTTP/1.1':            
            return httpRequest.respond(HttpStatus.HTTP_VERSION_NOT_SUPPORTED)

        if httpRequest.httpMethod != HttpMethod.Get:             
            return httpRequest.respond(HttpStatus.METHOD_NOT_ALLOWED)

        # Service the request         
        try:
            path = os.path.join(Config.ROOT, httpRequest.uri[1:])                     
            if os.path.relpath(path)[:len(Config.ROOT[2:])] != Config.ROOT[2:] or not os.path.exists(path):
                return httpRequest.respond(HttpStatus.NOT_FOUND)
            elif os.path.isdir(path):
                if path[-1] != '/':
                    headers = [HttpHelper.get_location_line(httpRequest.headers['Host'], httpRequest.uri)]
                    return httpRequest.respond(HttpStatus.MOVED_PERMANENTLY, additionalHeaders=headers)

                path = os.path.join(path, 'index.html')            
                if not os.path.exists(path):
                    return httpRequest.respond(HttpStatus.NOT_FOUND)
                    
            contentType, contentEncoding = mimetypes.guess_type(path)
            body = b'' if contentType is None else self.create_message_body(path)

            if contentType is None: 
                contentType = ContentType.Default

            headers = [HttpHelper.get_contenttype_line(contentType, contentEncoding), HttpHelper.get_server_line()]
            return httpRequest.respond(HttpStatus.OK, body, additionalHeaders=headers)
        except:
            return httpRequest.respond(HttpStatus.INTERNAL_SERVER_ERROR)

    def create_message_body(self, path) -> bytearray:                
        with open(path, 'rb') as file:
            body = file.read()
            return bytearray(body)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
