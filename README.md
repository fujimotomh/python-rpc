# python-rpc
Simple Python to Python remote procedure calls using http and pickle

This code demonstrates a remote procedure call server and client in 60 lines of [source](https://github.com/fujimotomh/python-rpc/blob/master/pythonrpc.py). An example usage is to have tensorflow on an AWS server and clients running python without the library. Another use is for interprocess communication.

The signatures of functions are unchanged, allowing for seamless use of remote procedure calls.

# Requirements
- [Requests](http://docs.python-requests.org/en/master/)
	- `pip install requests`

# Basic Usage

On the server:

```python
from pythonrpc import RPCServer

def func(*args, **kwargs):
	# do something
    return out

server = RPCServer(func, port=2345)
server.serve_forever()

# or

def keep_serving():
	# do something
	return bool

while keep_serving():
	server.handle_request()
```

On the client:

```python
from pythonrpc import RPCClient

rpcfunc = RPCClient(server_addr)

out = rpcfunc(*args, **kwargs)
```

For more see [examples.py](https://github.com/fujimotomh/python-rpc/blob/master/examples.py)

# Roadmap
- Benchmark performance
- Add documentation
