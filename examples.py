from __future__ import print_function
import os
import time
from httprpc import RPCServer, RPCClient


# send class objects and keywords


class ListHolder(object):

    def __init__(self, data):
        self.data = data


def func(a, b, kw=9):
    return (a + sum(b.data)) * kw

newpid = os.fork()

if newpid == 0:
    # server
    try:
        server = RPCServer(func, port=2345, verbose=True)
        server.handle_request() # handle one request, alternative is server.serve_forever()
    except Exception:
        print("server start failed, the server may already be running")

    exit()
else:
    # client
    time.sleep(3)

    rpcfunc = RPCClient('http://127.0.0.1:2345')

    out = rpcfunc(1, ListHolder([1, 1]), kw=3)
    assert out == func(1, ListHolder([1, 1]), kw=3)


# use libraries (e.g. numpy) on server

try:
    newpid = os.fork()

    if newpid == 0:
        # server
        import numpy as np

        def mat_mul(A, B):
            mat_A = np.array(A)
            mat_B = np.array(B)
            mat_AB = np.dot(A, B)
            return mat_AB.tolist()
        
        try:
            server = RPCServer(mat_mul, port=2345, verbose=True)
            server.handle_request() # handle one request, alternative is server.serve_forever()
        except Exception:
            print("server start failed, the server may already be running")

        exit()
    else:
        # client
        time.sleep(3)

        rpcfunc = RPCClient('http://127.0.0.1:2345')

        A = [[1, 2],
             [3, 4]]
        B = [[4, 3],
             [2, 1]]
        out = rpcfunc(A, B)

        import numpy as np
        local = np.dot(np.array(A), np.array(B)).tolist()
        assert out == local
except ImportError:
    pass


# use RPCServer with local flag for interprocess communication

newpid = os.fork()

if newpid == 0:
    # server

    counter = 0

    def add_to_counter(inc):
        global counter
        counter += inc
        return counter

    try:
        server = RPCServer(add_to_counter, local=True, port=2345, verbose=True)
        for _ in range(5):
            server.handle_request()
    except Exception:
        print("server start failed, the server may already be running")

    exit()
else:
    # client
    time.sleep(3)

    add_to_counter = RPCClient('http://127.0.0.1:2345')

    adds = [3, 5, 235, 12, 0]

    for add in adds:
        end = add_to_counter(add)

    assert end == sum(adds)
