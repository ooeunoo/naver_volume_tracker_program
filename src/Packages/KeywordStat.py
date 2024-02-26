import hashlib
import hmac
import base64
import requests
import time
import pandas as pd


class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(
            bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256
        )

        hash.hexdigest()
        return base64.b64encode(hash.digest())


class KeywordStat:
    base_url = "https://api.naver.com"
    endpoint = "/keywordstool"

    def __init__(self, api_key, secret_key, customer_id):
        self.api_key = api_key
        self.secret_key = secret_key
        self.customer_id = customer_id

    def set_lazy_initialize(self, api_key, secret_key,customer_id):
        self.api_key = api_key
        self.secret_key = secret_key
        self.customer_id = customer_id

    def get_header(self, method, uri, api_key, secret_key, customer_id):
        timestamp = str(round(time.time() * 1000))
        signature = Signature.generate(timestamp, method, uri, secret_key)

        return {
            "Content-Type": "application/json; charset=UTF-8",
            "X-Timestamp": timestamp,
            "X-API-KEY": api_key,
            "X-Customer": str(customer_id),
            "X-Signature": signature,
        }

    def get_stat(self, keyword):

        params = {"hintKeywords": [keyword.replace(" ", "")], "showDetail": "1"}

        r = requests.get(
            self.base_url + self.endpoint,
            params=params,
            headers=self.get_header(
                "GET", self.endpoint, self.api_key, self.secret_key, self.customer_id
            ),
        )

        return pd.DataFrame(r.json()["keywordList"])


# 테스트용 코드
if __name__ == "__main__":
    pass
