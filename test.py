import asyncio

from coinrpc import coinRPC


async def main():
    async with coinRPC("http://localhost:9904", "user", "pass", timeout=12) as rpc:
        #rpc.settimeout(10)
        print(await rpc.getnewaddress())


if __name__ == "__main__":
    asyncio.run(main())