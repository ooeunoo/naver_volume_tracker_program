# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QAction,
    QMainWindow,
)
from PyQt5.QtCore import QSettings

from Packages.NaverDeveloper import *
from Packages.KeywordStat import *
from Packages.GoogleSheetHandler import *
from Packages.Utilize import *
from Packages.ExcelHandler import *
from Features.Storage import *


class View(QMainWindow):
    def __init__(self, storage):
        super().__init__()

        self.storage = storage
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.setWindowTitle("네이버 키워드 검색량 조회")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: white;")

        self.init_ui()

    def generate_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("background-color: white; padding: 10px; Color: green")
        return button

    def generate_label_and_text_field(self, label_text):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(line_edit)
        return layout, line_edit

    def init_ui(self):
        self.upload_button = self.generate_button("엑셀 파일 업로드")
        self.process_guide = QLabel("파일을 업로드해주세요.")
        self.process_guide.setStyleSheet("background-color: white; color: blue")

        # 환경변수 정보
        layout_nd_client_id, self.input_nd_client_id = (
            self.generate_label_and_text_field("NAVER_DEVELOPER_CLIENT_ID: ")
        )
        layout_nd_client_secret, self.input_nd_client_secret = (
            self.generate_label_and_text_field("NAVER_DEVELOPER_CLIENT_SECRET: ")
        )
        layout_na_api_key, self.input_na_api_key = self.generate_label_and_text_field(
            "NAVER_AD_API_KEY: "
        )
        layout_na_secret_key, self.input_na_secret_key = (
            self.generate_label_and_text_field("NAVER_AD_SECRET_KEY: ")
        )
        layout_na_customer_id, self.input_na_customer_id = (
            self.generate_label_and_text_field("NAVER_AD_CUSTOMER_ID: ")
        )

        layout = QVBoxLayout()
        layout.addLayout(layout_nd_client_id)
        layout.addLayout(layout_nd_client_secret)
        layout.addLayout(layout_na_api_key)
        layout.addLayout(layout_na_secret_key)
        layout.addLayout(layout_na_customer_id)

        layout.addWidget(self.upload_button)
        layout.addWidget(self.process_guide)

        # Add menu bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")
        settings_action = QAction("Settings", self)
        settings_menu.addAction(settings_action)

        self.widget.setLayout(layout)
        self.load_storage()

    def load_storage(self):
        self.input_nd_client_id.setText(self.storage.get_value(KEY["ND_CLIENT_ID"]))
        self.input_nd_client_secret.setText(
            self.storage.get_value(KEY["ND_CLIENT_SECRET"])
        )
        self.input_na_api_key.setText(self.storage.get_value(KEY["NA_API_KEY"]))
        self.input_na_secret_key.setText(self.storage.get_value(KEY["NA_SECRET_KEY"]))
        self.input_na_customer_id.setText(self.storage.get_value(KEY["NA_CUSTOMER_ID"]))

    def save_storage(self):
        self.storage.save_value(KEY["ND_CLIENT_ID"], self.input_nd_client_id.text())
        self.storage.save_value(
            KEY["ND_CLIENT_SECRET"], self.input_nd_client_secret.text()
        )
        self.storage.save_value(KEY["NA_API_KEY"], self.input_na_api_key.text())
        self.storage.save_value(KEY["NA_SECRET_KEY"], self.input_na_secret_key.text())
        self.storage.save_value(KEY["NA_CUSTOMER_ID"], self.input_na_customer_id.text())

    # 사용자가 애플리케이션을 종료할 때 설정값을 저장
    def closeEvent(self, event):
        self.save_storage()
        event.accept()
