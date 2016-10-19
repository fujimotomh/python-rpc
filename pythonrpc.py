from __future__ import print_function
import io
import time
import requests
import pickle
from six.moves.BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class RPCServer(HTTPServer):

    def __init__(self, func, local=False, port=8080, verbose=False):
        self.func = func
        self.verbose = verbose

        if local:
            ip = '127.0.0.1'
        else:
            ip = '0.0.0.0'

        super(RPCServer, self).__init__((ip, port), RPCHandler)


class RPCHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        start = time.clock()

        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('access-control-allow-origin', '*')
        self.end_headers()

        args, kwargs = pickle.load(self.rfile)
        out = self.server.func(*args, **kwargs)

        pickle.dump(out, self.wfile)

        if self.server.verbose:
            print("finished POST")
            print("ms/call: {:.3f}".format((time.clock() - start) * 1000))


class RPCClient(object):

    def __init__(self, addr):
        self.addr = addr

    def __call__(self, *args, **kwargs):
        up = io.BytesIO()
        pickle.dump((args, kwargs), up)

        post = requests.post(self.addr, data=up.getvalue(), \
                headers={'content-type': 'application/octet-stream', 
                        'access-control-allow-origin': '*'})

        down = io.BytesIO(post.content)
        out = pickle.load(down)

        return out
