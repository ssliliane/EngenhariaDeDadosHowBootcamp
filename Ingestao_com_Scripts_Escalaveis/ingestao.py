from abc import ABC, abstractmethod
from genericpath import exists
import json
import os
from typing import List
import requests
import logging
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi(ABC):

    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    @abstractmethod
    def _get_endpoint(self,**kwargs) -> str:
        pass

    def get_data(self,**kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

class DaySummaryApi(MercadoBitcoinApi):

    type = "day-summary"
    def _get_endpoint(self, data: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{data.year}/{data.month}/{data.day}"

class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint

class DataWriter:
    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename),exist_ok=True)
        #'a' de append para só adicionar as linhas e não sobrescrever o que já estiver no arquivos
        with open(self.filename, "a") as f:
            f.write(row)

    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)

class DataIngestor(ABC):
    def __init__(self, writer, coins: List[str], default_start_date: datetime.date) -> None:
        self.default_start_date = default_start_date
        self.coins = coins
        self.writer = writer

    @abstractmethod
    def ingest(self) -> None:
        pass

class DaySummaryIngestor(DataIngestor):
     
    def ingest(self) -> None:
        date = self.default_start_date
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(data=date)
                self.writer(coin=coin, api=api.type).write(data)

        
print(DaySummaryApi(coin='BTC').get_data(data=datetime.date(2021,6,21)))

print(TradesApi('BTC').get_data())
print(TradesApi('BTC').get_data(date_from=datetime.datetime(2021,6,21)))
print(TradesApi('BTC').get_data(date_from=datetime.datetime(2021,6,21), date_to=datetime.datetime(2021,6,22)))

data = DaySummaryApi('BTC').get_data(data=datetime.date(2021,6,21))
writer = DataWriter('day_summary.json')
writer.write(data)

data = DaySummaryApi('BTC').get_data(data=datetime.date(2021,6,22))
writer = DataWriter('day_summary.json')
writer.write(data)

data = TradesApi('BTC').get_data()
writer = DataWriter('trades.json')
writer.write(data)

ingestor = DaySummaryIngestor(writer=DataWriter, coins=['BTC','LTC','ETH'],default_start_date=datetime.date(2021,6,21))
ingestor.ingest()