# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QLineEdit
)
from PyQt5.QtCore import Qt

from Packages.ExcelHandler import *

class MainKeywordTabPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 엑셀 파일 업로드 버튼 생성
        self.upload_button = QPushButton("엑셀 파일 업로드")
        self.upload_button.clicked.connect(self.upload_excel)
        layout.addWidget(self.upload_button)

        # 테이블 생성
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # 열 수 설정
        self.table_widget.setHorizontalHeaderLabels(["키워드", "메인 키워드"])  # 헤더 설정

        layout.addWidget(self.table_widget)

        # 진행 버튼 생성
        self.process_button = QPushButton("진행")
        self.process_button.clicked.connect(self.process_task)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

        # 테이블 초기 상태는 숨김
        self.table_widget.hide()
        self.process_button.hide()

        # 테이블 스타일 설정
        # self.table_widget.verticalHeader().setVisible(False)


    def upload_excel(self):
        # 파일 업로드 다이얼로그 열기
        file_name, _ = QFileDialog.getOpenFileName(self, "Excel 파일 선택", "", "Excel 파일 (*.xlsx *.xls)")

        # 파일이 선택되었다면 파일 위치를 버튼 텍스트로 업데이트하고 테이블 표시
        if file_name:
            self.upload_button.setText(f"파일 위치: {file_name}")
            data = self.set_keywords(file_name)
            self.table_widget.show()  # 테이블 표시
            self.process_button.show()  # 진행 버튼 표시
        else:
            self.table_widget.hide()  # 파일이 선택되지 않은 경우 테이블 숨김
            self.process_button.hide()  # 파일이 선택되지 않은 경우 진행 버튼 숨김

   
    def set_keywords(self, file_name):
        excelHandler = ExcelHandler(file_name)
        keywords = excelHandler.get_all_keywords()
        self.table_widget.setRowCount(len(keywords))  # 행 수 설정
        for i, (index, keyword) in enumerate(keywords):
            item = QTableWidgetItem(keyword)
            self.table_widget.setItem(i, 0, item)
            predict_keyword = QLineEdit()  # 예상 키워드 입력 위젯 생성
            self.table_widget.setCellWidget(i, 1, predict_keyword)  # QLineEdit을 셀에 추가
            # 예상 키워드 값이 변경되는 이벤트를 감지하여 버튼 상태 업데이트
            item.setTextAlignment(Qt.AlignCenter)  # 텍스트 가운데 정렬
        return keywords

    def process_task(self):
        # 여기에 임시로 생성된 {keyword: predict_keyword, .. } 형식의 데이터를 사용하여 예상 키워드를 설정하는 코드를 추가하세요.
        pass
