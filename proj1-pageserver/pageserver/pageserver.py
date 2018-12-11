"""
  A trivial web server in Python.

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible
"""

"""
SOURCES
Python endswith function - https://www.tutorialspoint.com/python/string_endswith.htm
Checking if a file exists - https://www.guru99.com/python-check-if-file-exists.html
reading a file - https://www.guru99.com/reading-and-writing-files-in-python.html
Source path joining - https://piazza.com/class/jmgzw525226r7?cid=38
"""
import config    # Configure from .ini files and command line
import logging   # Better than print statements
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
# Logging level may be overridden by configuration 

import socket    # Basic TCP/IP communication on the internet
import _thread   # Response computation runs concurrently with main program
import os
import os.path
from os import path

DOCROOT = "."   # Overridden by configuration

def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)    # A real server would have multiple listeners
    return serversocket


def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        log.info("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept()
        _thread.start_new_thread(func, (clientsocket,))

# HTTP response codes, as the strings we will actually send.
# See:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# or    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
##
STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"


def respond(sock):
    """
    This server responds only to GET requests (not PUT, POST, or UPDATE).
    Any valid GET request is answered with an ascii graphic of a cat.
    """
    sent = 0
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    log.info("--- Received request ----")
    log.info("Request was {}\n***\n".format(request))
    parts = request.split()
    source_path = os.path.join(DOCROOT, parts[1].strip("/"))
    text = ""

    if len(parts) > 1 and parts[0] == "GET":
        #make sure its an html or css file
        if parts[1].endswith(".html") or parts[1].endswith(".css"):
            
            #return forbidden if any of these are found in the file address
            if "//" in source_path or "~" in source_path or ".." in source_path: 
                transmit(STATUS_FORBIDDEN, sock)

            #if the file doesn't (not) exists, then return error   
            if not os.path.isfile(source_path):
                transmit(STATUS_NOT_FOUND, sock)

            #if it does exist, business as usual
            #open and read the file then transmit
            else:
                transmit(STATUS_OK, sock)
                file = open(source_path, 'r', encoding='utf-8')
                text = file.read()
                transmit(text,sock)
            
        else:
            log.info("Unhandled request: {}".format(request))
            transmit(STATUS_NOT_IMPLEMENTED, sock)
            transmit("\nI don't handle this request: {}\n".format(request), sock)

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return


def transmit(msg, sock):
    """It might take several sends to get the whole message out"""
    sent = 0
    while sent < len(msg):
        buff = bytes(msg[sent:], encoding="utf-8")
        sent += sock.send(buff)

###
#
# Run from command line
#
###


def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    # Defaults from configuration files;
    #   on conflict, the last value read has precedence
    options = config.configuration()
    # We want: PORT, DOCROOT, possibly LOGGING

    if options.PORT <= 1000:
        log.warning(("Port {} selected. " +
                         " Ports 0..1000 are reserved \n" +
                         "by the operating system").format(options.port))

    return options


def main():
    global DOCROOT
    options = get_options()
    port = options.PORT
    DOCROOT = options.DOCROOT
    if options.DEBUG:
        log.setLevel(logging.DEBUG)
    sock = listen(port)
    log.info("Listening on port {}".format(port))
    log.info("Socket is {}".format(sock))
    serve(sock, respond)


if __name__ == "__main__":
    main()
