from cgi import parse_qsl, escape
from pprint import pformat

def app(env, resp):
    data = "Hello World!\n"
    data += env['REQUEST_METHOD'] + ':\n'
    if env['REQUEST_METHOD'] == 'POST':
        if env['QUERY_STRING'] != '':
            for ch in parse_qsl(env['QUERY_STRING']):
                data += ' = '.join(ch) + '<br>'
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
