# *coinrpc
Lightweight *coin async JSON-RPC Python client.

It will work with most modern Satoshi clients.

Serves as a tiny layer between an application and a *coin daemon, its primary usage
is querying the current state of blockchain, network stats, transactions and sending the transactions.

If you want more complete *coin experience in Python, consult
[python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib).

## Installation

```bash
$ pip install coinrpc
```

## Supported methods
Here is a list of supported methods, divided by their categories. Should you need
method not implemented, wrap the call in `coinRPC.req(<your_method>, ...)` coroutine.

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


### Wallet RPCs

|   Method   |   Supported?     |
|------------|:----------------:|
| `sendtoaddress` | ✔ |
| `getnewaddress` | ✔ |
| `importpubkey`  | ✔ |
| `listreceivedbyaddress`  | ✔ |
| `listunspent`  | ✔ |

## Usage
Minimal illustration (assuming Python 3.8+, where you can run `async` code in console)

```
$ python -m asyncio
>>> import asyncio
>>>
>>> from coinrpc import coinRPC
>>> rpc = coinRPC("http://localhost:9904" "rpc_user", "rpc_passwd")
>>> await rpc.getconnectioncount()
10
>>> await rpc.aclose()  # Clean-up resource
```

You can also use the `coinRPC` as an asynchronous context manager, which does
all the resource clean-up automatically, as the following example shows:

```python
import asyncio

from coinrpc import coinRPC


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
