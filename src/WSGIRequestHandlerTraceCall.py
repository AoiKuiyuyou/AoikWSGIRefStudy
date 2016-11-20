# coding: utf-8
from __future__ import absolute_import

import aoiktracecall.config
import aoiktracecall.trace


# Only `aoiktracecall` modules are imported here.
# Other modules should be imported after `trace_calls_in_specs` is called.


# Set configs
aoiktracecall.config.set_configs({
    # Whether wrap callables using wrapper class instead of wrapper function.
    #
    # Wrapper class is more adaptive to various types of callables but will
    # break if the code that was using the original function requires a real
    # function, instead of a callable. Known cases include PyQt slot functions.
    #
    'WRAP_USING_WRAPPER_CLASS': True,

    # Whether wrap base class attributes in a subclass.
    #
    # If enabled, wrapper attributes will be added to a subclass even if the
    # wrapped original attributes are defined in a base class.
    #
    # This helps in the case that base class attributes are implemented in C
    # extensions thus can not be traced directly.
    #
    'WRAP_BASE_CLASS_ATTRIBUTES': True,

    # Whether highlight title shows `self` argument's class instead of called
    # function's defining class.
    #
    # This helps reveal the real type of the `self` argument on which the
    # function is called.
    #
    'HIGHLIGHT_TITLE_SHOW_SELF_CLASS': True,

    # Highlight title line character count max
    'HIGHLIGHT_TITLE_LINE_CHAR_COUNT_MAX': 265,

    # Whether show function's file path and line number in pre-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_PRE_CALL': True,

    # Whether show function's file path and line number in post-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_POST_CALL': False,

    # Whether show `printing_handler`'s debug info
    'PRINTING_HANDLER_SHOW_DEBUG_INFO': False,
})


# Create trace specs.
#
# The order of the specs determines the matching precedence, with one exception
# that URI patterns consisting of only alphanumerics, underscores, and dots are
# considered as exact URI matching, and will have higher precedence over all
# regular expression matchings. The rationale is that a spec with exact URI
# matching is more specific therefore should not be shadowed by any spec with
# regular expression matching that has appeared early.
#
trace_specs = [
    # ----- aoiktracecall -----
    # Not trace `aoiktracecall`
    ('aoiktracecall([.].+)?', False),

    # ----- * -----
    # Tracing `__setattr__` will reveal instances' attribute assignments.
    # Notice Python 2 old-style classes have no `__setattr__` attribute.
    ('.+[.]__setattr__', True),

    # Not trace most of double-underscore functions.
    # Tracing double-underscore functions is likely to break code, e.g. tracing
    # `__str__` or `__repr__` may cause infinite recursion.
    ('.+[.]__(?!init|call)[^.]+__', False),

    # ----- socket.SocketIO (Python 3) -----
    # Highlight
    ('socket[.]SocketIO[.](__init__|readinto|write|flush|close)', {
        'highlight'
    }),

    # Hide details
    ('socket.SocketIO.fileno', False),

    # Show all
    ('socket[.]SocketIO[.].+', True),

    # ----- socket -----
    # Notice in Python 2, class `socket._socketobject`'s instance methods
    # - recv
    # - recvfrom
    # - recv_into
    # - recvfrom_into
    # - send
    # - sendto
    # are dynamically generated in `_socketobject.__init__`. The approach of
    # wrapping class attributes is unable to trace these methods.

    # Hide details
    ('socket[.].+[.]fileno', False),

    # Hide details.
    # This function is in Python 3.
    ('socket._intenum_converter', False),

    # Hide to avoid infinite recursion in `__repr__` in Python 3
    ('socket[.].+[.]getpeername', False),

    # Hide to avoid infinite recursion in `__repr__` in Python 3
    ('socket[.].+[.]getsockname', False),

    # Highlight all
    ('socket([.].+)?', {'highlight'}),

    # ----- select (Python 2) -----
    # Highlight
    ('select.select', {'highlight'}),

    # Show all
    ('select([.].+)?', True),

    # ----- selectors (Python 3) -----
    # Highlight
    ('selectors[.].+[.](__init__|register|select|_select)', {'highlight'}),

    # Show all
    ('selectors([.].+)?', True),

    # ----- SocketServer (Python 2), socketserver (Python 3) -----
    # Hide details
    ('SocketServer._eintr_retry', False),

    # Hide details
    ('socketserver[.].+[.]service_actions', False),

    # Hide details
    ('(socketserver|SocketServer)[.].+[.]fileno', False),

    # Highlight all
    ('(socketserver|SocketServer)([.].+)?', {'highlight'}),

    # ----- mimetools -----
    # `mimetools` is used for parsing HTTP headers in Python 2.

    # Highlight all
    ('mimetools([.].+)?', {'highlight'}),

    # ----- email -----
    # `email` is used for parsing HTTP headers in Python 3.

    # Highlight all
    ('email([.].+)?', {'highlight'}),

    # ----- BaseHTTPServer (Python 2), http.server (Python 3) -----
    # Hide details
    ('(BaseHTTPServer|http[.]server)[.].+[.](parse_request|log_request)', {
        'highlight', 'hide_below'
    }),

    # ----- BaseHTTPServer (Python 2) -----
    # Highlight all
    ('BaseHTTPServer([.].+)?', {'highlight'}),

    # ----- http (Python 3) -----
    # Highlight all
    ('http([.].+)?', {'highlight'}),

    # ----- wsgiref -----
    # Hide details
    ('wsgiref.simple_server.ServerHandler.setup_environ', {
        'highlight', 'hide_below'
    }),

    # Hide details
    ('wsgiref.simple_server.WSGIRequestHandler.get_environ', {
        'highlight', 'hide_below'
    }),

    # Highlight all
    ('wsgiref([.].+)?', {'highlight'}),

    # ----- __main__ -----
    # Highlight all
    ('__main__([.].+)?', {'highlight'}),
]


# Create printing handler filter function
def printing_handler_filter_func(info):
    # Get onwrap URI
    onwrap_uri = info['onwrap_uri']

    # If is this URI
    if onwrap_uri == '__main__.CustomApp':
        # Get arguments inspect info
        arguments_inspect_info = info['arguments_inspect_info']

        # Get `environ` argument info
        arg_info = arguments_inspect_info.fixed_arg_infos['environ']

        # Hide details
        arg_info.value = '{...}'

    # Return info dict
    return info


# Trace calls according to trace specs.
#
# This function will hook the module importing system in order to intercept and
# process newly imported modules. Callables in these modules which are matched
# by one of the trace specs will be wrapped to enable tracing.
#
# Already imported modules will be processed as well. But their callables may
# have been referenced elsewhere already, making the tracing incomplete. This
# explains why import hook is needed and why modules must be imported after
# `trace_calls_in_specs` is called.
#
aoiktracecall.trace.trace_calls_in_specs(
    specs=trace_specs,
    printing_handler_filter_func=printing_handler_filter_func,
)

# Remove to avoid being traced
del printing_handler_filter_func


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

        # Run server
        server.serve_forever()

    # If have `KeyboardInterrupt`
    except KeyboardInterrupt:
        # Stop gracefully
        return


# Trace calls in this module.
#
# Calling this function is needed because at the point `trace_calls_in_specs`
# is called, this module is being initialized, therefore callables defined
# after the call point are not accessible to `trace_calls_in_specs`.
#
aoiktracecall.trace.trace_calls_in_this_module()


# If is run as main module
if __name__ == '__main__':
    # Call main function
    exit(main())
