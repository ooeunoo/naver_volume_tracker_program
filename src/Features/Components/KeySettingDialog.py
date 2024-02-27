# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QFormLayout,QLineEdit

class KeySettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)

        # Create form layout
        form_layout = QFormLayout()

        # 환경변수 정보 입력창
        self.input_nd_client_id = QLineEdit()
        self.input_nd_client_secret = QLineEdit()
        self.input_na_api_key = QLineEdit()
        self.input_na_secret_key = QLineEdit()
        self.input_na_customer_id = QLineEdit()
        self.input_cg_key = QLineEdit()


        form_layout.addRow("NAVER_DEVELOPER_CLIENT_ID: ", self.input_nd_client_id)
        form_layout.addRow("NAVER_DEVELOPER_CLIENT_SECRET: ", self.input_nd_client_secret)
        form_layout.addRow("NAVER_AD_API_KEY: ", self.input_na_api_key)
        form_layout.addRow("NAVER_AD_SECRET_KEY: ", self.input_na_secret_key)
        form_layout.addRow("NAVER_AD_CUSTOMER_ID: ", self.input_na_customer_id)
        form_layout.addRow("CHAT_GPT_API_KEY: ", self.input_cg_key)
        # form_layout.addRow("CHAT_GPT_API_KEY: ", self.input_cg_key)

        layout.addLayout(form_layout)

        # 저장 및 취소 버튼
        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            parent=self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    # 현재 설정값을 가져오는 메서드
    def get_settings(self):
        return (
            self.input_nd_client_id.text(),
            self.input_nd_client_secret.text(),
            self.input_na_api_key.text(),
            self.input_na_secret_key.text(),
            self.input_na_customer_id.text(),
            self.input_cg_key.text(),
            # self.input_t_data.text(),
        )

    def is_enable_key(self):
        nd_client_id, nd_client_secret, na_api_key, na_secret_key, na_customer_id, cg_key, t_data = self.get_settings()

        # 빈칸이 하나라도 있는지 확인
        if nd_client_id and nd_client_secret and na_api_key and na_secret_key and na_customer_id and cg_key:
            return True
        else:
            return False        

    # 모달 다이얼로그 실행 후, 사용자가 저장을 눌렀을 때 호출되는 메서드
    def accept(self):
        super().accept()
