# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QFileDialog,
)
from PyQt5.QtCore import QThread, pyqtSignal, QObject

import pandas as pd
import time
import sys
from Packages.NaverDeveloper import *
from Packages.KeywordStat import *
from Packages.GoogleSheetHandler import *
from Packages.Utilize import *
from Packages.ExcelHandler import *
from datetime import datetime
import os
import logging
from config.config import *

# 로그 설정
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class FileProcessThread(QThread):
    finished = pyqtSignal()

    def __init__(self, model, input_file):
        super().__init__()
        self.model = model
        self.input_file = input_file

    def run(self):
        self.model.process_xlsx(self.input_file)
        self.finished.emit()


class Model(QObject):
    progress_updated = pyqtSignal(str)

    def __init__(self, naver_developer, keyword_stat, utilize):
        super().__init__()
        self.naver_developer = naver_developer
        self.keyword_stat = keyword_stat
        self.utilize = utilize

    def upload_xlsx(self):
        """xlsx 파일 업로드를 처리하는 함수"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Excel 파일 업로드", "", "Excel files (*.xlsx)"
        )
        return file_path

    def process_xlsx(self, input_file):
        """xlsx 파일 처리 함수"""
        if not input_file:
            return

        excelHandler = ExcelHandler(
            input_file,
        )

        task_keywords = excelHandler.get_all_keywords()
        self.progress_updated.emit(f"키워드 가져오는 중...")

        update_cells = {}

        for row, keyword in task_keywords:
            self.progress_updated.emit(f"월별 거래량 가져오는 중...")
            volume = self.get_monthly_volume(keyword, "2023-01-01", "2024-01-01")

            self.progress_updated.emit(f"전체 상품 수 가져오는 중...")
            total_items = self.naver_developer.get_total_count(keyword)

            self.progress_updated.emit(f"전체 해외 상품 수 가져오는 중...")
            total_exclude_cbshop_items = self.naver_developer.get_exclude_cbshop_count(
                keyword
            )
            total_cbshop_items = total_items - total_exclude_cbshop_items

            self.progress_updated.emit(f"엑셀 데이터 업데이트 중...")

            if volume.empty:
                continue
            else:
                update_cells[row] = {
                    "전체 상품수": total_items,
                    "해외 상품수": total_cbshop_items,
                    "해외 상품 비율": "{:.2f}%".format(
                        total_cbshop_items / total_items * 100
                    ),
                    "업데이트": str(utilize.get_time()),
                }
                months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
                for month in months:
                    try:
                        search_volume = volume.loc[volume["period"] == f"2023-{month[:-1].zfill(2)}-01", "검색수"].values[0]
                    except IndexError:
                        search_volume = "N/A"
                    update_cells[row][month] = search_volume

        excelHandler.bulk_update_cells(update_cells)

    def get_monthly_volume(self, keyword, start_date, end_date):
        logging.info(f"{keyword} 작업 중...")

        ratios = self.naver_developer.get_ratio(keyword, start_date, end_date)
        stat = self.keyword_stat.get_stat(keyword)
            

        if ratios.empty:
            return pd.DataFrame()

        keyword_percent = ratios.loc[ratios["title"] == keyword, "ratio"].iloc[-1]
        
        monthly_pc_qc_cnt = 10 if stat.iloc[0, 1] == "< 10" else stat.iloc[0, 1]
        monthly_mobile_qc_cnt = 10 if stat.iloc[0, 2] == "< 10" else stat.iloc[0, 2]
        total_count = monthly_pc_qc_cnt + monthly_mobile_qc_cnt

        keyword_one_percent = total_count / keyword_percent

        trend_fin = ratios.copy()
        trend_fin.loc[trend_fin["title"] == keyword, ("검색수")] = (
            keyword_one_percent * trend_fin.loc[trend_fin["title"] == keyword, "ratio"]
        )

        ratios_fin = trend_fin.astype({("검색수"): "int64"})
        return ratios_fin


class View(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("네이버 키워드 검색량 조회")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: white;")

        self.init_ui()

    def generate_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("background-color: white; padding: 10px; Color: green")
        return button

    def init_ui(self):
        self.upload_button = self.generate_button("엑셀 파일 업로드")
        self.process_guide = QLabel("파일을 업로드해주세요.")
        self.process_guide.setStyleSheet("background-color: white; color: blue")

        layout = QVBoxLayout()
        layout.addWidget(self.upload_button)
        layout.addWidget(self.process_guide)

        self.setLayout(layout)


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.upload_button.clicked.connect(self.upload_and_process_xlsx)

    def upload_and_process_xlsx(self):
        input_file = self.model.upload_xlsx()
        if not input_file:  # 파일이 선택되지 않은 경우 처리 중 상태를 해제하고 종료
            return

        self.view.process_guide.setText("파일을 읽는 중...")
        time.sleep(2)  # 그냥 넣음

        self.model.progress_updated.connect(
            self.update_progress
        )  # 진행 상황 업데이트 연결

        # 파일 처리를 위한 스레드 생성 및 시작
        self.file_process_thread = FileProcessThread(self.model, input_file)
        self.file_process_thread.finished.connect(self.on_processing_finished)
        self.file_process_thread.start()

    def update_progress(self, text):
        self.view.process_guide.setText(text)

    def on_processing_finished(self):
        self.view.process_guide.setText("파일이 업데이트되었습니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.info('프로그램이 실행되었습니다.')

    naverDeveloper = NaverDeveloper(
       NAVER_DEVELOPER_CLIENT_ID,
       NAVER_DEVELOPER_CLIENT_SECRET,
    )
    keywordStat = KeywordStat(
        NAVER_AD_API_KEY,
        NAVER_AD_SECRET_KEY,
        NAVER_AD_CUSTOMER_ID,
    )
    utilize = Utilize()

    model = Model(naverDeveloper, keywordStat, utilize)
    view = View()
    presenter = Presenter(model, view)

    view.show()

    sys.exit(app.exec_())
