"""
Hello World with python cgi
"""

from urllib.parse import parse_qsl
from pprint import pformat


def app(env, resp):
    """
    CGI method, prints:
    `Hello World!
    $REQUEST_METHOD:
    $HTTP_PARAMS`
    """
    data = "Hello World!\n"
    data += env['REQUEST_METHOD'] + ':\n'
    if env['REQUEST_METHOD'] == 'POST':
        if env['QUERY_STRING'] != '':
            for chank in parse_qsl(env['QUERY_STRING']):
                data += ' = '.join(chank) + '<br>'
    elif env['REQUEST_METHOD'] == 'GET':
        data += pformat(env['wsgi.input'].read())
    else:
        data += 'UNSUPPORTED PARSING'

    data = bytes(data, 'ascii')
    resp("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data))),
    ])
    return iter([data])
