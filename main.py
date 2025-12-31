import sys
import os
import signal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt5.QtCore import Qt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def human_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def secure_delete(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        print(nonce)
        encrypted = aesgcm.encrypt(nonce, data, None)

        with open(file_path, "wb") as f:
            f.write(nonce + encrypted)
            f.flush()
            os.fsync(f.fileno())

        # os.remove(file_path)

        del key
        del data
        del encrypted

        return True
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
        return False


class SecureDeleteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure File Deletion")
        self.resize(800, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["File Name", "Size", "Full Path"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Files")
        self.remove_btn = QPushButton("Remove Selected")
        self.clear_btn = QPushButton("Clear All")
        self.delete_selected_btn = QPushButton("Secure Delete Selected")
        self.delete_all_btn = QPushButton("Secure Delete All")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.delete_selected_btn)
        btn_layout.addWidget(self.delete_all_btn)

        self.layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.add_files)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.clear_btn.clicked.connect(self.clear_all)
        self.delete_selected_btn.clicked.connect(self.delete_selected)
        self.delete_all_btn.clicked.connect(self.delete_all)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        for file_path in files:
            if not self.is_already_added(file_path):
                row = self.table.rowCount()
                self.table.insertRow(row)

                name_item = QTableWidgetItem(os.path.basename(file_path))
                size_item = QTableWidgetItem(
                    human_size(os.path.getsize(file_path))
                )
                path_item = QTableWidgetItem(file_path)

                name_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)
                size_item.setFlags(size_item.flags() ^ Qt.ItemIsEditable)
                path_item.setFlags(path_item.flags() ^ Qt.ItemIsEditable)

                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, size_item)
                self.table.setItem(row, 2, path_item)

    def is_already_added(self, path):
        for row in range(self.table.rowCount()):
            if self.table.item(row, 2).text() == path:
                return True
        return False

    def remove_selected(self):
        rows = sorted(
            set(index.row() for index in self.table.selectedIndexes()),
            reverse=True
        )
        for row in rows:
            self.table.removeRow(row)

    def clear_all(self):
        self.table.setRowCount(0)

    def delete_selected(self):
        rows = sorted(
            set(index.row() for index in self.table.selectedIndexes()),
            reverse=True
        )
        if not rows:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Selected files will be permanently destroyed.\nThis cannot be undone.\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        for row in rows:
            path = self.table.item(row, 2).text()
            secure_delete(path)
            self.table.removeRow(row)

    def delete_all(self):
        if self.table.rowCount() == 0:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "ALL listed files will be permanently destroyed.\nThis cannot be undone.\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        for row in reversed(range(self.table.rowCount())):
            path = self.table.item(row, 2).text()
            secure_delete(path)
            self.table.removeRow(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    def sigint_handler(signum, frame):
        app.quit()
    
    signal.signal(signal.SIGINT, sigint_handler)
    
    window = SecureDeleteApp()
    window.show()
    sys.exit(app.exec_())
