import pandas as pd
import urllib.request
import json
import time


class NaverDeveloper:
    datalab_url = "https://openapi.naver.com/v1/datalab/search"
    search_url = "https://openapi.naver.com/v1/search"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def set_lazy_initialize(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret



    def get_ratio(self, keyword, start_date, end_date):
        response_results_all = pd.DataFrame()

        body_dict = {}  # 검색 정보를 저장할 변수
        body_dict["startDate"] = start_date
        body_dict["endDate"] = end_date
        body_dict["timeUnit"] = "month"
        body_dict["keywordGroups"] = [{"groupName": keyword, "keywords": [keyword]}]
        # body_dict['device']='mo'

        body = str(body_dict).replace("'", '"')  # ' 문자로는 에러가 발생해서 " 로 변환
        request = urllib.request.Request(self.datalab_url)
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)
        request.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        
        if rescode == 200:
            response_body = response.read()
            response_json = json.loads(response_body)
        else:
            print("Error Code:" + rescode)

        response_results = pd.DataFrame()
        for data in response_json["results"]:
            result = pd.DataFrame(data["data"])
            result["title"] = data["title"]

            response_results = pd.concat([response_results, result])
        response_results_all = pd.concat([response_results_all, response_results])
        return response_results_all

    def get_total_count(self, keyword):
        query = urllib.parse.quote(keyword)
        total_count_request = urllib.request.Request(
            self.search_url + "/shop?query=" + query
        )
        total_count_request.add_header("X-Naver-Client-Id", self.client_id)
        total_count_request.add_header("X-Naver-Client-Secret", self.client_secret)

        response = urllib.request.urlopen(total_count_request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            response_json = json.loads(response_body)
        else:
            print("Error Code:" + rescode)

        return response_json["total"]

    def get_exclude_cbshop_count(self, keyword):
        query = urllib.parse.quote(keyword)
        total_count_request = urllib.request.Request(
            self.search_url + "/shop?query=" + query + "&exclude=" + "cbshop"
        )
        total_count_request.add_header("X-Naver-Client-Id", self.client_id)
        total_count_request.add_header("X-Naver-Client-Secret", self.client_secret)

        response = urllib.request.urlopen(total_count_request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            response_json = json.loads(response_body)
        else:
            print("Error Code:" + rescode)

        return response_json["total"]


if __name__ == "__main__":
    pass