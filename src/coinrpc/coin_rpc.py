import itertools
from types import TracebackType
from typing import Any, List, Optional, Type, Union

import httpx
import json
from typing_extensions import Literal

from ._exceptions import ImproperlyConfigured, RPCError
from ._types import (
    BestBlockHash,
    coinRPCResponse,
    Block,
    BlockchainInfo,
    BlockCount,
    BlockHash,
    BlockHeader,
    BlockStats,
    ChainTips,
    ConnectionCount,
    Difficulty,
    MempoolInfo,
    MiningInfo,
    NetworkHashps,
    NetworkInfo,
    RawTransaction,
    SendToAddress,
    ListRecievedByAddress,
    ListUnspent,
)

# Neat trick found in asyncio library for task enumeration
# https://github.com/python/cpython/blob/3.8/Lib/asyncio/tasks.py#L31
_next_rpc_id = itertools.count(1).__next__


class coinRPC:
    __slots__ = ("_url", "_client")
    """
    For list of all available commands, visit:
    https://developer.bitcoin.org/reference/rpc/index.html
    """

    def __init__(
        self,
        url: str,
        rpc_user: str,
        rpc_password: str,
        **options: Any,
    ) -> None:
        self._url = url
        self._client = self._configure_client(rpc_user, rpc_password, **options)

    async def __aenter__(self) -> "coinRPC":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        await self.aclose()

    @staticmethod
    def _configure_client(
        rpc_user: str, rpc_password: str, **options: Any
    ) -> httpx.AsyncClient:
        """
        Configure `httpx.AsyncClient`. If you choose to provide additional options, it
        is your responsibility to conform to the `httpx.AsyncClient` interface.
        """
        auth = (rpc_user, rpc_password)
        headers = {"content-type": "application/json"}

        options = dict(options)
        if not options:
            return httpx.AsyncClient(auth=auth, headers=headers)

        if "auth" in options:
            raise ImproperlyConfigured("Authentication cannot be set via options!")

        if "headers" in options:
            _additional_headers = dict(options.pop("headers"))
            headers.update(_additional_headers)
            # guard against content-type overwrite
            headers["content-type"] = "application/json"

        if "timeout" in options:
            return httpx.AsyncClient(
                auth=auth, headers=headers, timeout=options.pop("timeout"), **options
            )
        else:
            return httpx.AsyncClient(auth=auth, headers=headers, timeout=5, **options)

    @property
    def url(self) -> str:
        return self._url

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    async def aclose(self) -> None:
        await self.client.aclose()

    async def req(
        self,
        method: str,
        params: List[Union[str, int, List[str], None]],
        **kwargs: Any,
    ) -> coinRPCResponse:
        """
        Pass keyword arguments to directly modify the constructed request -
            see `httpx.Request`.
        """
        req = self.client.post(
            url=self.url,
            content=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": _next_rpc_id(),
                    "method": method,
                    "params": params,
                }
            ),
            **kwargs,
        )
        resp = json.loads((await req).content)

        if resp["error"] is not None:
            raise RPCError(resp["error"]["code"], resp["error"]["message"])
        else:
            return resp["result"]

    async def getmempoolinfo(self) -> MempoolInfo:
        """https://developer.bitcoin.org/reference/rpc/getmempoolinfo.html"""
        return await self.req("getmempoolinfo", [])

    async def getmininginfo(self) -> MiningInfo:
        """https://developer.bitcoin.org/reference/rpc/getmininginfo.html"""
        return await self.req("getmininginfo", [])

    async def getnetworkinfo(self) -> NetworkInfo:
        """https://developer.bitcoin.org/reference/rpc/getnetworkinfo.html"""
        return await self.req("getnetworkinfo", [])

    async def getblockchaininfo(self) -> BlockchainInfo:
        """https://developer.bitcoin.org/reference/rpc/getblockchaininfo.html"""
        return await self.req("getblockchaininfo", [])

    async def getconnectioncount(self) -> ConnectionCount:
        """https://developer.bitcoin.org/reference/rpc/getconnectioncount.html"""
        return await self.req("getconnectioncount", [])

    async def getchaintips(self) -> ChainTips:
        """https://developer.bitcoin.org/reference/rpc/getchaintips.html"""
        return await self.req("getchaintips", [])

    async def getdifficulty(self) -> Difficulty:
        """https://developer.bitcoin.org/reference/rpc/getdifficulty.html"""
        return await self.req("getdifficulty", [])

    async def getbestblockhash(self) -> BestBlockHash:
        """https://developer.bitcoin.org/reference/rpc/getbestblockhash.html"""
        return await self.req("getbestblockhash", [])

    async def getblockhash(self, height: int) -> BlockHash:
        """https://developer.bitcoin.org/reference/rpc/getblockhash.html"""
        return await self.req("getblockhash", [height])

    async def getblockcount(self) -> BlockCount:
        """https://developer.bitcoin.org/reference/rpc/getblockcount.html"""
        return await self.req("getblockcount", [])

    async def getblockheader(
        self, block_hash: str, verbose: bool = True
    ) -> BlockHeader:
        """https://developer.bitcoin.org/reference/rpc/getblockheader.html"""
        return await self.req("getblockheader", [block_hash, verbose])

    async def getblockstats(
        self, hash_or_height: Union[int, str], *keys: str
    ) -> BlockStats:
        """
        https://developer.bitcoin.org/reference/rpc/getblockstats.html

        Enter `keys` as positional arguments to return only the provided `keys`
            in the response.
        """
        return await self.req("getblockstats", [hash_or_height, list(keys) or None])

    async def getblock(self, block_hash: str, verbosity: Literal[0, 1, 2] = 1) -> Block:
        """
        https://developer.bitcoin.org/reference/rpc/getblock.html

        :param verbosity: 0 for hex-encoded block data, 1 for block data with
            transactions list, 2 for block data with each transaction.
        """
        return await self.req("getblock", [block_hash, verbosity])

    async def getrawtransaction(
        self, txid: str, verbose: bool = True, block_hash: Optional[str] = None
    ) -> RawTransaction:
        """
        https://developer.bitcoin.org/reference/rpc/getrawtransactiono.html

        :param txid: If transaction is not in mempool, block_hash must also be provided.
        :param verbose: True for JSON, False for hex-encoded string
        :param block_hash: see ^txid
        :param timeout: If doing a lot of processing, no timeout may come in handy
        """
        return await self.req("getrawtransaction", [txid, verbose, block_hash])

    async def getnetworkhashps(
        self, nblocks: int = -1, height: Optional[int] = None
    ) -> NetworkHashps:
        """
        https://developer.bitcoin.org/reference/rpc/getnetworkhashps.html

        :param nblocks: -1 for estimated hash power since last difficulty change,
            otherwise as an average over last provided number of blocks
        :param height: If not provided, get estimated hash power for the latest block
        :param timeout: If doing a lot of processing, no timeout may come in handy
        """
        return await self.req("getnetworkhashps", [nblocks, height])

    async def sendtoaddress(
        self,
        address: str,
        amount: float,
        comment: Optional[str] = None,
        comment_to: Optional[str] = None,
        subtractfeefromamount: Optional[bool] = True,
        avoid_reuse: Optional[bool] = True,
    ) -> SendToAddress:
        """
        https://developer.bitcoin.org/reference/rpc/sendtoaddress.html

        :param address: The coin address to send to.
        :param amount: The amount in coin to send. eg 0.1
        :param: comment: A comment used to store what the transaction is for.
            This is not part of the transaction, just kept in your wallet.
        :param: comment_to: A comment to store the name of the person or organization
            to which you're sending the transaction. This is not part of the transaction, just kept in your wallet.
        :param: subtractfeefromamount: The fee will be deducted from the amount being sent.
            The recipient will receive less coins than you enter in the amount field.
        :param: avoid_reuse: (only available if avoid_reuse wallet flag is set) Avoid spending from dirty addresses; addresses are considered
            dirty if they have previously been used in a transaction.
        """
        return await self.req(
            "sendtoaddress",
            [address, amount, comment, comment_to, subtractfeefromamount, avoid_reuse],
        )

    async def getnewaddress(
        self, label: Optional[str] = None, address_type: Optional[str] = "bech32"
    ) -> str:
        """
        https://developer.bitcoin.org/reference/rpc/getnewaddress.html

        :param label: The label name for the address to be linked to.
            It can also be set to the empty string “” to represent the default label.
            The label does not need to exist, it will be created if there is no label by the given name.
        :param address_type: The address type to use. Options are “legacy”, “p2sh-segwit”, and “bech32”.
        """
        return await self.req("getnewaddress", [label, address_type])

    async def importpubkey(
        self, pubkey: str, label: Optional[str], rescan: Optional[bool] = True
    ) -> None:
        """
        https://developer.bitcoin.org/reference/rpc/importpubkey.html

        :param pubkey: The hex-encoded public key.
        :param lable: An optional label.
        :param rescan: Rescan the wallet for transactions
        """
        return await self.req("importpubkey", [label, rescan])

    async def listreceivedbyaddress(
        self,
        include_watchonly: Optional[bool],
        address_filter: Optional[str],
        include_empty: Optional[bool] = False,
        minconf: Optional[int] = 1,
    ) -> List[ListRecievedByAddress]:
        """
        https://developer.bitcoin.org/reference/rpc/listreceivedbyaddress.html

        :param minconf: The minimum number of confirmations before payments are included.
        :param include_empty: Whether to include addresses that haven't received any payments.
        :param include_watchonly: Whether to include watch-only addresses
        :param address_filter If present, only return information on this address.
        """
        return await self.req(
            "listreceivedbyaddress",
            [minconf, include_empty, include_watchonly, address_filter],
        )

    async def listunspent(
        self,
        minconf: Optional[int] = 1,
        maxconf: Optional[int] = 9999999,
        addresses: Optional[list] = [],
        include_unsafe: Optional[bool] = True,
        query_options: Optional[dict] = {},
    ) -> List[ListUnspent]:
        """
        https://developer.bitcoin.org/reference/rpc/listunspent.html?highlight=listunspent

        :param minconf: The minimum number of confirmations before payments are included.
        :param maxconf: The maximum confirmations to filter
        :param addresses: The peercoin addresses to filter
        :param include_unsafe: Include outputs that are not safe to spend
        :param query_options: JSON with query options, see bitcoin docs for more info.
        """
        return await self.req(
            "listunspent",
            [minconf, maxconf, addresses, include_unsafe, query_options],
        )

    async def createrawtransaction(
        self,
        inputs: List(dict),
        outputs: List(dict),
        locktime: Optional(int),
        # replaceable: Optional(bool) not supported in Peercoin
    ) -> str:
        """
        https://developer.bitcoin.org/reference/rpc/createrawtransaction.html

        :param inputs: The of inputs
        :param outputs: The list of outputs
        :param locktime: Raw locktime. Non-0 value also locktime-activates inputs.
        """
        return await self.reqt("createrawtransaction", [inputs, outputs, locktime])
