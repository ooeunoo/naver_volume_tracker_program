from PyQt5.QtCore import QSettings

KEY = {
    "ND_CLIENT_ID": "ND_CLIENT_ID",
    "ND_CLIENT_SECRET": "ND_CLIENT_SECRET",
    "NA_API_KEY": "NA_API_KEY",
    "NA_SECRET_KEY": "NA_SECRET_KEY",
    "NA_CUSTOMER_ID": "NA_CUSTOMER_ID",
}


class Storage:
    def __init__(self):
        self.storage = QSettings("Storage", " Storage")

    def get_value(self, key):
        return self.storage.value(key, "")

    def save_value(self, key, value):
        self.storage.setValue(key, value)
