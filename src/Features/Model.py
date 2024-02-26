# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject

import pandas as pd
import time
from Packages.NaverDeveloper import *
from Packages.KeywordStat import *
from Packages.GoogleSheetHandler import *
from Packages.Utilize import *
from Packages.ExcelHandler import *
import logging


class Model(QObject):
    progress_guide = pyqtSignal(str)

    def __init__(self, naverDeveloper, keywordStat, utilize):
        super().__init__()
        self.naverDeveloper = naverDeveloper
        self.keywordStat = keywordStat
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
        self.progress_guide.emit(f"키워드 가져오는 중...")

        update_cells = {}

        for row, keyword in task_keywords:
            time.sleep(0.5)
            self.progress_guide.emit(f"월별 거래량 가져오는 중...")
            try:
                volume = self.get_monthly_volume(keyword, "2023-01-01", "2024-01-01")
            except Exception as e:
                print(e)
                logging.warning(f"{keyword} 월별 거래량 가져오기 실패: {e}")
                volume = pd.DataFrame()

            self.progress_guide.emit(f"전체 상품 수 가져오는 중...")
            self.progress_guide.emit(f"전체 해외 상품 수 가져오는 중...")

            try:
                total_items = self.naverDeveloper.get_total_count(keyword)
                total_exclude_cbshop_items = (
                    self.naverDeveloper.get_exclude_cbshop_count(keyword)
                )
                total_cbshop_items = total_items - total_exclude_cbshop_items
            except Exception as e:
                logging.warning(f"{keyword} 상품 수 가져오기 실패: {e}")
                continue

            self.progress_guide.emit(f"엑셀 데이터 업데이트 중...")

            if volume.empty:
                continue
            else:
                update_cells[row] = {
                    "전체 상품수": total_items,
                    "해외 상품수": total_cbshop_items,
                    "해외 상품 비율": "{:.2f}%".format(
                        total_cbshop_items / total_items * 100
                    ),
                    "업데이트": str(self.utilize.get_time()),
                }
                months = [
                    "1월",
                    "2월",
                    "3월",
                    "4월",
                    "5월",
                    "6월",
                    "7월",
                    "8월",
                    "9월",
                    "10월",
                    "11월",
                    "12월",
                ]
                for month in months:
                    try:
                        search_volume = volume.loc[
                            volume["period"] == f"2023-{month[:-1].zfill(2)}-01",
                            "검색수",
                        ].values[0]
                    except IndexError:
                        search_volume = "N/A"
                    update_cells[row][month] = search_volume

        excelHandler.bulk_update_cells(update_cells)

    def get_monthly_volume(self, keyword, start_date, end_date):
        logging.info(f"{keyword} 작업 중...")
        ratios = self.naverDeveloper.get_ratio(keyword, start_date, end_date)
        stat = self.keywordStat.get_stat(keyword)

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
