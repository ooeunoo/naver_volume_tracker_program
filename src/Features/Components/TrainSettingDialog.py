from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt

from Utils.Constants import *
import json

class TrainSettingDialog(QDialog):
    def __init__(self, parent=None, storage=None ):
        super().__init__(parent)
        self.storage = storage
        self.setWindowTitle("Settings")
        

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Number of columns
        self.table_widget.setHorizontalHeaderLabels(["키워드", "메인 키워드"])  # Set headers

        # Add rows with editable cells
        self.load_data()
        self.add_row_with_button()

        layout.addWidget(self.table_widget)

        # Add save button
        save_button = QPushButton("저장하기")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Resize dialog
        self.resize(1000, 1000)  # Set width and height

    def add_row(self, keyword, main_keyword):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        keyword_item = QTableWidgetItem(keyword)
        self.table_widget.setItem(row_position, 0, keyword_item)

        main_keyword_item = QTableWidgetItem(main_keyword)
        self.table_widget.setItem(row_position, 1, main_keyword_item)

    def add_row_with_button(self):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        button = QPushButton("+")
        button.clicked.connect(lambda _, row=row_position: self.add_new_row(row))
        self.table_widget.setCellWidget(row_position, 0, button)

         # Disable input in the second column
        item = QTableWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Disable editing
        self.table_widget.setItem(row_position, 1, item)

    def add_new_row(self, row):
        self.table_widget.removeRow(row)  # Remove current row
        self.add_row("", "")  # Add empty row

        # Move + button to the next row
        next_row = row + 1
        self.add_row_with_button()

    def load_data(self):
        data = self.storage.get_value(KEY["T_DATA"])
        try:
            data_json_array = json.loads(data)
            for item in data_json_array:
                keyword = list(item.keys())[0]
                main_keyword = item[keyword]
                self.add_row(keyword, main_keyword)
        except:
            pass


    def save_data(self):
        data = []
        for row in range(self.table_widget.rowCount()):
            keyword_item = self.table_widget.item(row, 0)
            main_keyword_item = self.table_widget.item(row, 1)
            if keyword_item and main_keyword_item:
                keyword = keyword_item.text()
                main_keyword = main_keyword_item.text()
                if keyword == "" or main_keyword == "":
                    continue
                data.append({keyword: main_keyword})

        result = json.dumps(data, indent=4)
        self.storage.save_value(KEY['T_DATA'], result)

        return result

# 테스트용 코드
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = TrainSettingDialog()
    dialog.exec_()
