# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSettings


class Storage:
    def __init__(self):
        self.storage = QSettings("Storage", " Storage")

    def get_value(self, key):
        return self.storage.value(key, "")

    def save_value(self, key, value):
        self.storage.setValue(key, value)
