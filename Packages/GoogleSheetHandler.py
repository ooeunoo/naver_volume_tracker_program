import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.cell import Cell


class GoogleSheetHandler:
    def __init__(self, credentials_file, sheet_name):
        self.credentials_file = credentials_file
        self.sheet_name = sheet_name
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file, self.scope
        )
        self.client = gspread.authorize(self.credentials)
        self.spreadsheet = self.client.open(self.sheet_name)
        self.worksheet = self.spreadsheet.worksheet("검색량")

    def get_incomplete_keywords(self):
        incomplete_keywords = []
        rows = self.worksheet.get_all_values()
        for i, row in enumerate(
            rows[1:], start=2
        ):  # 첫 번째 행은 헤더이므로 건너뜁니다.
            if not row[-2]:  # 완료 컬럼이 비어 있는 경우
                keyword = row[0]  # 키워드를 가져옵니다.
                incomplete_keywords.append(
                    (i, keyword)
                )  # 행과 키워드를 함께 추가합니다.
        return incomplete_keywords

    def bulk_update_cells(self, data):
        cells = []
        for row_key, row_data in data.items():
            row_index = int(row_key)
            for column_name, value in row_data.items():
                print(row_index)
                cells.append(
                    Cell(
                        row=row_index,
                        col=self._get_column_index(column_name),
                        value=value,
                    )
                )

        self.worksheet.update_cells(cells)

    def _get_column_index(self, column_name):
        # 컬럼명을 받아 해당 컬럼의 인덱스를 반환
        col_names = self.worksheet.row_values(1)
        try:
            return col_names.index(column_name) + 1
        except ValueError:
            raise ValueError(f"컬럼 '{column_name}'을(를) 시트에서 찾을 수 없습니다.")


# 예시 사용법
# 테스트용 코드
if __name__ == "__main__":
    credentials_file = "Packages/service_account.json"
    sheet_name = "naver_search_volume"

    google_sheet_handler = GoogleSheetHandler(credentials_file, sheet_name)

    json_data = {"2": {"JAN": 213}, "3": {"JAN": 424, "FEB": 123}}
    google_sheet_handler.bulk_update_cells(json_data)
