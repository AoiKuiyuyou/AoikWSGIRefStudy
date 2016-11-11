# coding: utf-8
from __future__ import absolute_import

import aoiktracecall.config
import aoiktracecall.trace


# Only `aoiktracecall` modules are imported here.
# Other modules should be imported after `trace_calls_in_specs` is called.


# Set `FIGLET_WIDTH` to control how figlet wraps
aoiktracecall.config.set_config('FIGLET_WIDTH', 150)


# Trace specs
trace_specs = [
    ('aoiktracecall([.].+)?', False),

    ('.+[.]copy', False),

    ('.+[.]__setattr__', True),

    ('.+[.]service_actions', False),

    ('.+[.]log_request', {'hide_below'}),

    ('socket.IntEnum', False),

    ('socket._intenum_converter', False),

    ('socket[.].+[.]getsockname', False),

    ('socket[.].+[.]getpeername', False),

    ('(socket|SocketServer)[.].+[.]fileno', False),

    ('socket._realsocket', False),

    # `SocketIO` is in Python 3
    ('socket[.]SocketIO[.]readinto', {'highlight'}),

    ('socket[.]SocketIO[.]write', {'highlight'}),

    ('socket[.]SocketIO[.]flush', {'highlight'}),

    ('socket[.]SocketIO[.]close', {'highlight'}),

    ('socket[.]SocketIO[.]__(?!init)[^.]+__', False),

    ('socket[.]SocketIO[.].+', True),

    ('socket[.].+[.]__init__', {'highlight'}),

    ('socket[.].+[.]__[^.]+__', False),

    ('socket([.].+)?', {'highlight'}),

    ('selectors.ABCMeta', False),

    ('selectors.Mapping', False),

    ('selectors.SelectSelector', False),

    ('selectors.DefaultSelector.__init__', {'highlight'}),

    ('selectors.DefaultSelector.select', 'hide_tree'),

    ('selectors.DefaultSelector.register', {'highlight'}),

    ('selectors[.].+[.]__[^.]+__', False),

    ('selectors([.].+)?', True),

    # `socketserver` is in Python 3.
    # `SocketServer` is in Python 2.
    ('(socketserver|SocketServer)._eintr_retry', False),

    ('(socketserver|SocketServer)._ServerSelector', False),

    ('(socketserver|SocketServer)[.].+[.]__(?!init)[^.]+__', False),

    ('(socketserver|SocketServer)([.].+)?', {'highlight'}),

    # `http` is in Python 3
    ('http[.].+[.]__(?!init)[^.]+__', False),

    ('http([.].+)?', {'highlight'}),

    # `BaseHTTPServer` is in Python 2
    ('BaseHTTPServer[.].+[.]__(?!init)[^.]+__', False),

    ('BaseHTTPServer([.].+)?', {'highlight'}),

    ('wsgiref.simple_server.ServerHandler.setup_environ', {
        'highlight', 'hide_below'
    }),

    # Remove 'hide_below' to see the parsing details
    ('wsgiref.simple_server.WSGIRequestHandler.parse_request', {
        'highlight', 'hide_below'
    }),

    ('wsgiref.simple_server.WSGIRequestHandler.get_environ', {
        'highlight', 'hide_below'
    }),

    ('wsgiref[.].+[.]__(?!init)[^.]+__', False),

    ('wsgiref([.].+)?', {'highlight'}),

    # `email` is used for parsing HTTP headers in Python 3
    ('email[.].+[.]__(?!init)[^.]+__', False),

    ('email([.].+)?', {'highlight'}),

    # `mimetools` is used for parsing HTTP headers in Python 2
    ('mimetools[.].+[.]__(?!init)[^.]+__', False),

    ('mimetools([.].+)?', {'highlight'}),

    ('__main__[.].+[.]__(?!init)[^.]+__', False),

    ('__main__([.].+)?', {'highlight'}),
]


# Trace calls in specs
aoiktracecall.trace.trace_calls_in_specs(specs=trace_specs)


# Import modules after `trace_calls_in_specs` is called
from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIRequestHandler
from wsgiref.simple_server import WSGIServer


def CustomApp(environ, start_response):
    """
    This WSGI application echoes request body in response body.
    """
    # Get `Context-Length` header value
    content_length_text = environ['CONTENT_LENGTH']

    # If header value is empty
    if not content_length_text:
        # Set content length be 0
        content_length = 0

    # If header value is not empty
    else:
        # Convert to int
        content_length = int(content_length_text)

    # Get input file
    input_file = environ['wsgi.input']

    # Read request body
    request_body = input_file.read(content_length)

    # Send response status line and headers
    start_response('200 OK', [('Content-Length', str(len(request_body)))])

    # Return response body
    return [request_body]


def main():
    try:
        # Create server
        server = make_server(
            host='127.0.0.1',
            port=8000,
            app=CustomApp,
            server_class=WSGIServer,
            handler_class=WSGIRequestHandler,
        )

        # Serve forever
        server.serve_forever()

    # If have `KeyboardInterrupt`
    except KeyboardInterrupt:
        # Ignore
        pass


# Trace calls in this module
aoiktracecall.trace.trace_calls_in_this_module()


# If is run as main module
if __name__ == '__main__':
    # Call main function
    exit(main())
