import json
import asyncio
import aiofiles






class Profit:

    def __init__(self, history_path: str):
        self.path = history_path
        self.polldata: list = None
        self.pricelist: list = None



    @classmethod
    async def read_history(self) -> dict:

        async with aiofiles.open(self.path, mode='r', encoding='utf-8') as f:
            data = await f.read()

        for _ in range(5):
            try:
                return json.loads(data)
            except json.decoder.JSONDecodeError:
                asyncio.sleep(0.1)
        else:
            raise Exception(f"Couldn't load {self.path}")




    async def initialize(self):
        self.history = await self.read_history()

        # reduce the size of the history


        self.polldata = []
        if 'offerData' in self.polldata:
            self.polldata = self.polldata['offerData']







profit = Profit(history_path='./tests/providipresents')
