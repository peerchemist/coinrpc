# *coin-python-async-rpc
Lightweight *coin async JSON-RPC Python client.

Serves as a tiny layer between an application and a Bitcoin daemon, its primary usage
is querying the current state of Bitcoin blockchain, network stats, transactions...

If you want more complete *Bit*coin experience in Python, consult
[python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib).

## Installation
```bash
$ pip install bitcoinrpc
```

## Supported methods
Here is a list of supported methods, divided by their categories. Should you need
method not implemented, wrap the call in `coinRPC.acall(<your_method>, ...)` coroutine.

### Blockchain

|   Method   |   Supported?     |
|------------|:----------------:|
| `getbestblockhash` | ✔ |
| `getblock` | ✔ |
| `getblockchaininfo` | ✔ |
| `getblockcount` | ✔ |
| `getblockhash` | ✔ |
| `getblockheader` | ✔ |
| `getblockstats` | ✔ |
| `getchaintips` | ✔ |
| `getdifficulty` | ✔ |
| `getmempoolinfo` | ✔ |
| `getnetworkhashps` | ✔ |

### Mining

|   Method   |   Supported?     |
|------------|:----------------:|
| `getmininginfo` | ✔ |

### Network

|   Method   |   Supported?     |
|------------|:----------------:|
| `getconnectioncount` | ✔ |
| `getnetworkinfo` | ✔ |

### Raw transactions

|   Method   |   Supported?     |
|------------|:----------------:|
| `getrawtransaction` | ✔ |

## Usage
Minimal illustration (assuming Python 3.8+, where you can run `async` code in console)

```
$ python -m asyncio
>>> import asyncio
>>>
>>> from bitcoinrpc import coinRPC
>>> rpc = coinRPC("http://localhost:18443" "rpc_user", "rpc_passwd")
>>> await rpc.getconnectioncount()
10
>>> await rpc.aclose()  # Clean-up resource
```

You can also use the `coinRPC` as an asynchronous context manager, which does
all the resource clean-up automatically, as the following example shows:

```python
import asyncio

from bitcoinrpc import coinRPC


async def main():
    async with coinRPC("http://localhost:9902", "rpc_user", "rpc_password") as rpc:
        print(await rpc.getconnectioncount())


if __name__ == "__main__":
    asyncio.run(main())
```

Running this script yields:
```
$ python rpc_minimal.py
10
```

## License
MIT
