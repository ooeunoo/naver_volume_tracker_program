# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal

import time
from Packages.NaverDeveloper import *
from Packages.NaverAdvertising import *
from Packages.GoogleSheetHandler import *
from Packages.Utilize import *
from Packages.ExcelHandler import *
import logging


class FileProcessThread(QThread):
    finished = pyqtSignal()

    def __init__(self, model, input_file):
        super().__init__()
        self.model = model
        self.input_file = input_file

    def run(self):
        self.model.process_xlsx(self.input_file)
        self.finished.emit()


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.upload_button.clicked.connect(self.upload_and_process_xlsx)

        # 버튼 비활성화 초기 상태 설정
        # self.update_button_state()

        # # 입력 필드의 텍스트가 변경될 때마다 버튼 상태 업데이트
        # self.view.input_nd_client_id.textChanged.connect(self.update_button_state)
        # self.view.input_nd_client_secret.textChanged.connect(self.update_button_state)
        # self.view.input_na_api_key.textChanged.connect(self.update_button_state)
        # self.view.input_na_secret_key.textChanged.connect(self.update_button_state)
        # self.view.input_na_customer_id.textChanged.connect(self.update_button_state)

    def upload_and_process_xlsx(self):
        # 버튼 활성화 여부 확인 후 처리 로직 수행
        if not self.view.upload_button.isEnabled():
            return

        # 파일 업로드 받기
        input_file = self.model.upload_xlsx()

        # 파일이 선택되지 않은 경우 처리 중 상태를 해제하고 종료
        if not input_file:
            return
        
        self.set_progress_guide("파일을 읽는 중...")
        time.sleep(2)  # 그냥 넣음

        # 진행 상황 가이드 업데이트 연결
        self.model.progress_updated.connect(self.set_progress_guide)

        # 파일 처리를 위한 스레드 생성 및 시작
        self.file_process_thread = FileProcessThread(self.model, input_file)
        self.file_process_thread.finished.connect(self.on_processing_finished)
        self.file_process_thread.start()

    def set_progress_guide(self, text):
        self.view.process_guide.setText(text)

    def on_processing_finished(self):
        self.set_progress_guide("파일이 업데이트되엇습니다.")
        logging.info("파일이 업데이트되었습니다.")

    def update_button_state(self):
        pass