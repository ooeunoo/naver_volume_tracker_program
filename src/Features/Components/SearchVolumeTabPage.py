# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QRadioButton, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QCoreApplication
from Packages.ExcelHandler import ExcelHandler
from Packages.NaverDeveloper import NaverDeveloper
from Packages.NaverAdvertising import NaverAdvertising
from Packages.ChatGptHandler import ChatGptHandler
from Utils.Constants import KEY
from Utils.Helpers import *
from enum import Enum
import pandas as pd
import json
import ast
import re

header_mapping = {
    '키워드': 0,
    '메인 키워드': 1,
    "전체 상품수": 2, 
    "해외 상품수": 3, 
    "해외 상품 비율": 4, 
    "1월": 5, 
    "2월": 6, 
    "3월": 7,
    "4월": 8,
    "5월": 9,
    "6월": 10,
    "7월": 11,
    "8월": 12,
    "9월": 13,
    "10월": 14,
    "11월": 15,
    "12월": 16
}

class KeywordType(Enum):
    MAIN = "MAIN"
    ORIGIN = "ORIGIN"


class SearchVolumeTabPage(QWidget):
    
    def __init__(self, storage):
        super().__init__()
        self.keywords = []
        self.select_keyword = "ORIGIN"  # 기본값은 ORIGIN

        self.storage = storage
        self.naver_developer_instance = NaverDeveloper(self.storage.get_value(KEY["ND_CLIENT_ID"]), self.storage.get_value(KEY["ND_CLIENT_SECRET"]))
        self.naver_advertising_instance =  NaverAdvertising(self.storage.get_value(KEY["NA_API_KEY"]), self.storage.get_value(KEY["NA_SECRET_KEY"]), self.storage.get_value(KEY["NA_CUSTOMER_ID"]))
        self.chat_gpt_instance = ChatGptHandler(self.storage.get_value(KEY['C_G_KEY']))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()


        # 엑셀 파일 업로드 버튼 생성
        self.upload_button = QPushButton("엑셀 파일 업로드")
        self.upload_button.clicked.connect(self.upload_excel)
        layout.addWidget(self.upload_button)

        # 테이블 생성
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(17)  # 열 수 설정
        self.table_widget.setHorizontalHeaderLabels(["키워드", "메인 키워드", "전체 상품수", "해외 상품수", "해외 상품 비율", "1월", "2월", "3월","4월","5월","6월","7월","8월", "9월", "10월", "11월","12월"])  # 헤더 설정

        layout.addWidget(self.table_widget)

        # 메인 키워드 예측 버튼 생성
        self.query_main_keyword_button = QPushButton("메인 키워드 자동 예측하기")
        self.query_main_keyword_button.clicked.connect(self.query_main_keyword)
        layout.addWidget(self.query_main_keyword_button)

        # 키워드 선택 버튼 생성
        self.keyword_radio_button = QRadioButton("수집 키워드 선택 (선택 시 메인 키워드 기준)")
        self.keyword_radio_button.toggled.connect(lambda: self.on_radio_button_toggled(self.keyword_radio_button))

        # 진행 버튼 생성
        self.process_button = QPushButton("진행")
        self.process_button.clicked.connect(self.process_task)

        process_layout = QHBoxLayout()
        process_layout.addWidget(self.keyword_radio_button)
        process_layout.addWidget(self.process_button)
        layout.addLayout(process_layout)

        # 내보내기 버튼 생성
        self.export_button = QPushButton("내보내기")
        self.export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

        # 업로드 전 숨김
        self.table_widget.hide()
        self.query_main_keyword_button.hide()
        self.keyword_radio_button.hide()
        self.process_button.hide()
        self.export_button.hide()

    def on_radio_button_toggled(self, radio_button):
        self.select_keyword = KeywordType.MAIN if  radio_button.isChecked() else KeywordType.ORIGIN

    def query_main_keyword(self):
        # 전체 ROW 수 
        row_count = self.table_widget.rowCount()

        if row_count == 0:
            return

        keyword_row_mapper = {}
        real_question = []
        for row, index in enumerate(range(row_count)):
            keyword = self.table_widget.item(index, 0).text()

            if keyword == None:
                continue
            
            keyword_row_mapper[keyword] = row
            real_question.append(keyword)

        # 저장된 학습 데이터 불러오기
        train_data = self.storage.get_value(KEY['T_DATA'])
        train_data_json = json.loads(train_data)
        train_data_question = [list(item.keys())[0] for item in train_data_json]
        train_data_answer = [{"original": key, "main": value} for item in train_data_json for key, value in item.items()]

        try:
            forms = self.chat_gpt_instance.generate_train_form(train_data_question, train_data_answer, real_question)
            result = self.chat_gpt_instance.ask_keyword_question(forms)
            result_json_array =  extract_json_list(result.replace("'", '"') )
        except Exception as e:
            self._alert_event(f"ChatGPT 답변 오류: {e}")
            print(e)
            return


        # 테이블 업데이트
        for index, item in enumerate(result_json_array):
            original_keyword = item['original']  
            main_keyword = item['main']  

            item = QTableWidgetItem(str(main_keyword))
            self.table_widget.setItem(keyword_row_mapper[original_keyword], 1, item)
            # 이벤트 루프 처리하여 UI 업데이트
            QCoreApplication.processEvents()


    def upload_excel(self):
        # 파일 업로드 다이얼로그 열기
        file_name, _ = QFileDialog.getOpenFileName(self, "Excel 파일 선택", "", "Excel 파일 (*.xlsx *.xls)")

        # 파일이 선택되었다면 파일 위치를 버튼 텍스트로 업데이트하고 테이블 표시
        if file_name:
            self.upload_button.setText(f"파일 위치: {file_name}")
            data = self.set_keywords(file_name)
            self.table_widget.show()  # 테이블 표시
            self.query_main_keyword_button.show() # 메인 키워드 예측 버튼 표시
            self.keyword_radio_button.show() # 키워드 선택 버튼 표시
            self.process_button.show()  # 진행 버튼 표시
            self.export_button.show()  # 내보내기 버튼 표시
        else:
            self.table_widget.hide()  # 파일이 선택되지 않은 경우 테이블 숨김
            self.query_main_keyword_button.hide() # 파일이 선택되징 않은 경우 메인 키워드 예측 버튼 숨김
            self.keyword_radio_button.hide()  # 파일이 선택되지 않은 경우 키워드 선택 버튼 숨김
            self.process_button.hide()  # 파일이 선택되지 않은 경우 진행 버튼 숨김
            self.export_button.hide()  # 파일이 선택되지 않은 경우 내보내기 버튼 숨김

    def set_keywords(self, file_name):
        excelHandler = ExcelHandler(file_name)
        keywords = excelHandler.get_all_keywords()
        self.table_widget.setRowCount(len(keywords))  # 행 수 설정
        for i, (index, keyword) in enumerate(keywords):
            item = QTableWidgetItem(keyword)
            self.table_widget.setItem(i, 0, item)
            main_keyword_item = QTableWidgetItem()  # 메인 키워드 입력 아이템 생성
            self.table_widget.setItem(i, 1, main_keyword_item)  # 메인 키워드 열에 아이템 설정
            # 예상 키워드 값이 변경되는 이벤트를 감지하여 버튼 상태 업데이트
            item.setTextAlignment(Qt.AlignCenter)  # 텍스트 가운데 정렬

        self.keywords = keywords
        return keywords

    def process_task(self):
        # 전체 ROW 수 및 선택 열 인덱스
        row_count = self.table_widget.rowCount()
        selected_column_index = 1 if self.select_keyword == KeywordType.MAIN else 0 

        # 데이터가 없다면 진행하지않음
        if row_count == 0:
            return

        for row, index in enumerate(range(row_count)):
            keyword = self.table_widget.item(index, selected_column_index).text()

            # 키워드가 비워져있다면 패스
            if keyword == None:
                continue

            volumes = self._get_monthly_volumes(keyword, '2023-01-01', '2024-01-01')
            total_items, total_cbshop_items = self._get_total_items_and_cbshop_items(keyword)
            data = self._fill_data(volumes, total_items, total_cbshop_items)
       
            # 테이블 업데이트
            for header, value in data.items():
                if header in header_mapping:
                    col = header_mapping[header]
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row, col, item)
            # 이벤트 루프 처리하여 UI 업데이트
                    QCoreApplication.processEvents()

    def export_to_excel(self):
        # 파일 저장 다이얼로그 열기
        file_name, _ = QFileDialog.getSaveFileName(self, "저장할 파일 선택", "", "Excel 파일 (*.xlsx *.xls)")

        # 파일 이름이 주어지지 않은 경우 또는 사용자가 취소한 경우
        if not file_name:
            return

        # 테이블 데이터를 pandas DataFrame으로 변환
        data = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)

        df = pd.DataFrame(data, columns=list(header_mapping.keys()))  # 헤더 이름을 사용하여 DataFrame 생성
        
        # DataFrame을 Excel 파일로 저장
        df.to_excel(file_name, index=False)

    def _get_monthly_volumes(self, keyword, start_date, end_date):
        try:
            ratios = self.naver_developer_instance.get_ratio(keyword, start_date, end_date)
            stats = self.naver_advertising_instance.get_stat(keyword)

            if ratios.empty:
                return pd.DataFrame()

            keyword_percent = ratios.loc[ratios['title'] == keyword, 'ratio'].iloc[-1]
            monthly_pc_qc_cnt = 10 if stats.iloc[0, 1] == "< 10" else stats.iloc[0, 1]
            monthly_mobile_qc_cnt = 10 if stats.iloc[0, 2] == "< 10" else stats.iloc[0, 2]
            total_count = monthly_pc_qc_cnt + monthly_mobile_qc_cnt

            keyword_one_percent = total_count / keyword_percent

            trend_fin = ratios.copy()
            trend_fin.loc[trend_fin["title"] == keyword, ("검색수")] = (
                keyword_one_percent * trend_fin.loc[trend_fin["title"] == keyword, "ratio"]
            )

            ratios_fin = trend_fin.astype({("검색수"): "int64"})
            return ratios_fin
        except Exception as e:
            print(e)
            return pd.DataFrame()
      

    def _get_total_items_and_cbshop_items(self, keyword):
        try:
            total_items = self.naver_developer_instance.get_total_count(keyword)
            
            total_exclude_cbshop_items = self.naver_developer_instance.get_exclude_cbshop_count(keyword)
            total_cbshop_items = total_items - total_exclude_cbshop_items
            return (total_items, total_cbshop_items)
        except Exception as e:
            return (None, None)

    def _fill_data(self, volumes, total_items, total_cbshop_items):
        cbshop_ratio = None if total_cbshop_items == None or total_items == None else total_cbshop_items / total_items * 100

        result = {
            "전체 상품수": '-' if total_items == None else total_items,
            "해외 상품수": '-' if total_cbshop_items == None else total_cbshop_items,
            "해외 상품 비율": '-' if cbshop_ratio == None else "{:.2f}%".format(cbshop_ratio),
        }


        for month in  ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]:
            try:
                if volumes.empty:
                    month_volume = '-'
                else:
                    month_volume = volumes.loc[
                        volumes["period"] == f"2023-{month[:-1].zfill(2)}-01",
                        "검색수",
                    ].values[0]
            except IndexError:
                month_volume = "-"
            result[month] = month_volume

        return result




    # Alert
    def _alert_event(self, message) :
        QMessageBox.critical(self,'Error', message)