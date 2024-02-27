# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QAction,QTabWidget,
    QMainWindow,QApplication
)
from PyQt5.QtCore import QSettings
import sys

from Packages.NaverDeveloper import *
from Packages.NaverAdvertising import *
from Packages.GoogleSheetHandler import *
from Packages.Utilize import *
from Packages.ExcelHandler import *
from Features.Storage import *
from Features.Components.KeySettingDialog import *
from Features.Components.TrainSettingDialog import *
from Features.Components.MainKeywordTabPage import *
from Features.Components.SearchVolumeTabPage import *
from Utils.Constants import *


class View(QMainWindow):
    def __init__(self, storage):
        super().__init__()

        self.storage = storage
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
       
        self.init_screen()
        self.init_ui()

    def init_screen(self):
        self.setWindowTitle("네이버 키워드 검색량 조회")
        self.setStyleSheet("background-color: white;")

        window_width, window_height = 1200, 1200
        self.resize(window_width, window_height)

        # Get screen dimensions
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()

        # Calculate window position to center it on the screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.move(x, y)


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

        self.tab_widget = QTabWidget()

        # Create tabs for different functionalities
        self.main_keyword_tab = MainKeywordTabPage()
        self.search_volume_tab = SearchVolumeTabPage(self.storage)

        # Add tabs to the tab widget
        # self.tab_widget.addTab(self.main_keyword_tab, "메인 키워드 추정")
        self.tab_widget.addTab(self.search_volume_tab, "검색량 조회")

        # Add tab widget to the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.widget.setLayout(layout)

        # Initialize UI for each tab
        # self.init_main_keyword_tab()
        self.init_search_volume_tab()

        # Add menu bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("설정")


        # Settings action
        key_info_action = QAction("키정보", self)
        key_info_action.triggered.connect(self.open_key_settings_dialog)
        settings_menu.addAction(key_info_action)

        train_action = QAction("학습시키기", self)
        train_action.triggered.connect(self.open_train_settings_dialog)  
        settings_menu.addAction(train_action)

        # Tab navigation actions
        # main_keyword_action = QAction("메인 키워드 추정", self)
        # main_keyword_action.triggered.connect(self.switch_to_main_keyword_tab)
        search_volume_action = QAction("검색량 조회", self)
        search_volume_action.triggered.connect(self.switch_to_search_volume_tab)

    # def load_storage(self):
    #     self.input_nd_client_id.setText(self.storage.get_value(KEY["ND_CLIENT_ID"]))
    #     self.input_nd_client_secret.setText(
    #         self.storage.get_value(KEY["ND_CLIENT_SECRET"])
    #     )
    #     self.input_na_api_key.setText(self.storage.get_value(KEY["NA_API_KEY"]))
    #     self.input_na_secret_key.setText(self.storage.get_value(KEY["NA_SECRET_KEY"]))
    #     self.input_na_customer_id.setText(self.storage.get_value(KEY["NA_CUSTOMER_ID"]))

    def init_main_keyword_tab(self):
        # Initialize UI for the "메인 키워드 추정" tab
        layout = QVBoxLayout(self.main_keyword_tab)
        label = QLabel("This is the Main Keyword Estimation tab")
        layout.addWidget(label)
        self.main_keyword_tab.setLayout(layout)

    def init_search_volume_tab(self):
        # Initialize UI for the "검색량 조회" tab
        layout = QVBoxLayout(self.search_volume_tab)
        label = QLabel("This is the Search Volume Lookup tab")
        layout.addWidget(label)
        self.search_volume_tab.setLayout(layout)

    def switch_to_main_keyword_tab(self):
        self.tab_widget.setCurrentWidget(self.main_keyword_tab)

    def switch_to_search_volume_tab(self):
        self.tab_widget.setCurrentWidget(self.search_volume_tab)

    def open_key_settings_dialog(self):
        dialog = KeySettingDialog(self)
        # 현재 설정된 값으로 설정 다이얼로그 초기화
        dialog.input_nd_client_id.setText(self.storage.get_value(KEY["ND_CLIENT_ID"]))
        dialog.input_nd_client_secret.setText(self.storage.get_value(KEY["ND_CLIENT_SECRET"]))
        dialog.input_na_api_key.setText(self.storage.get_value(KEY["NA_API_KEY"]))
        dialog.input_na_secret_key.setText(self.storage.get_value(KEY["NA_SECRET_KEY"]))
        dialog.input_na_customer_id.setText(self.storage.get_value(KEY["NA_CUSTOMER_ID"]))
        dialog.input_cg_key.setText(self.storage.get_value(KEY["C_G_KEY"]))

        # 사용자가 저장을 눌렀을 때 설정값을 저장
        if dialog.exec_() == QDialog.Accepted:
            (
                nd_client_id,
                nd_client_secret,
                na_api_key,
                na_secret_key,
                na_customer_id,
                cg_key,
            ) = dialog.get_settings()
            self.storage.save_value(KEY["ND_CLIENT_ID"], nd_client_id)
            self.storage.save_value(KEY["ND_CLIENT_SECRET"], nd_client_secret)
            self.storage.save_value(KEY["NA_API_KEY"], na_api_key)
            self.storage.save_value(KEY["NA_SECRET_KEY"], na_secret_key)
            self.storage.save_value(KEY["NA_CUSTOMER_ID"], na_customer_id)
            self.storage.save_value(KEY["C_G_KEY"], cg_key)

    def open_train_settings_dialog(self):
        dialog = TrainSettingDialog(parent=self, storage=self.storage)
        dialog.exec_()

        # 현재 설정된 값으로 설정 다이얼로그 초기화



    # 사용자가 애플리케이션을 종료할 때 설정값을 저장
    def closeEvent(self, event):
        event.accept()
