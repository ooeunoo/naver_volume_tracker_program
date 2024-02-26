# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
)
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QSettings

import pandas as pd
import time
import sys
from Packages.NaverDeveloper import *
from Packages.NaverAdvertising import *
from Packages.GoogleSheetHandler import *
from Packages.Utilize import *
from Packages.ExcelHandler import *
from Features.Model import *
from Features.Presenter import *
from Features.View import *
from Features.Storage import *

from datetime import datetime
import os
import logging

# 로그 설정
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.info("프로그램이 실행되었습니다.")

    naverDeveloper = NaverDeveloper(
        None,
        None,
    )
    keywordStat = NaverAdvertising(
        None,
        None,
        None,
    )
    utilize = Utilize()
    storage = Storage()

    model = Model(naverDeveloper, keywordStat, utilize)
    view = View(storage)
    presenter = Presenter(model, view)

    view.show()
    sys.exit(app.exec_())
