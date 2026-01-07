"""
Main window for VaultBurn - Secure File Deletion Application
"""

import sys
import os
import logging
import argparse
import signal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QTabWidget, QFileDialog, QMessageBox, QHeaderView,
    QTextEdit, QGroupBox, QLineEdit
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QFont, QIcon, QDragEnterEvent, QDropEvent

# Import from local modules
from utils import human_size, setup_logging
from file_operations import secure_delete, generate_key, encrypt_file, decrypt_file
from styles import (
    APP_STYLESHEET, TABLE_STYLESHEET, ADD_BUTTON_STYLE,
    NORMAL_BUTTON_STYLE, DELETE_BUTTON_STYLE, WARNING_BUTTON_STYLE,
    TITLE_LABEL_STYLE, INFO_LABEL_STYLE, HINT_LABEL_STYLE,
    STATUS_LABEL_READY_STYLE, STATUS_LABEL_ACTIVE_STYLE, COPYRIGHT_LABEL_STYLE
)


class SecureDeleteApp(QWidget):
    """Main application window for VaultBurn."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("VaultBurn - Secure File Deletion System")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #1e1e2e; color: #e0e0e0;")
        
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Setup logging
        self.log_file = setup_logging()
        logging.info("VaultBurn application started")
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        self.is_drag_over = False
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget {
                background-color: #1e1e2e;
            }
            
            QTabWidget::pane {
                border: 2px solid #3d3d5c;
                background-color: #1e1e2e;
                border-radius: 5px;
                top: 0px;
                padding: 5px;
            }
            
            QTabBar {
                background-color: transparent;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d3d5c, stop:1 #2d2d44);
                color: #b0b0b0;
                padding: 15px 30px;
                margin-right: 5px;
                margin-bottom: 2px;
                border: 2px solid #3d3d5c;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a5a8a, stop:1 #4a4a6a);
                color: #ffffff;
                border-color: #5a5a8a;
                border-bottom: 2px solid #1e1e2e;
                margin-bottom: 0px;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a4a6a, stop:1 #3a3a5a);
                color: #e0e0e0;
            }
        """)
        
        # Create main tab
        self.main_tab = QWidget()
        self.setup_main_tab()
        
        # Create logs tab
        self.logs_tab = QWidget()
        self.setup_logs_tab()
        
        # Create encryption tab
        self.encrypt_tab = QWidget()
        self.setup_encrypt_tab()
        
        # Add tabs
        self.tab_widget.addTab(self.main_tab, "🔥 Delete Files")
        self.tab_widget.addTab(self.encrypt_tab, "🔐 Encrypt/Decrypt")
        self.tab_widget.addTab(self.logs_tab, "📋 Activity Logs")
        
        # Ensure tabs are visible
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(False)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def setup_main_tab(self):
        """Setup the main file deletion tab."""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.main_tab.setLayout(self.layout)

        # Title Label
        title_label = QLabel("🔥 Secure File Deletion System")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL_STYLE)
        self.layout.addWidget(title_label)

        # Info Label
        info_label = QLabel("⚠️ Files will be permanently and securely deleted (3-pass overwrite)")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet(INFO_LABEL_STYLE)
        self.layout.addWidget(info_label)

        # Drag and drop hint
        drag_hint = QLabel("💡 Tip: You can also drag and drop files/folders directly into this window")
        drag_hint.setAlignment(Qt.AlignCenter)
        drag_hint.setStyleSheet(HINT_LABEL_STYLE)
        self.layout.addWidget(drag_hint)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["File Name", "Size", "Full Path"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(TABLE_STYLESHEET)
        self.layout.addWidget(self.table)

        # Button layouts
        top_btn_layout = QHBoxLayout()
        top_btn_layout.setSpacing(10)

        self.add_btn = QPushButton("+ Add Files")
        self.add_btn.setObjectName("addButton")
        self.add_btn.setStyleSheet(ADD_BUTTON_STYLE)
        
        self.add_dir_btn = QPushButton("+ Add Directory")
        self.add_dir_btn.setObjectName("addButton")
        self.add_dir_btn.setStyleSheet(ADD_BUTTON_STYLE)
        
        self.remove_btn = QPushButton("- Remove Selected")
        self.remove_btn.setStyleSheet(NORMAL_BUTTON_STYLE)
        
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setStyleSheet(NORMAL_BUTTON_STYLE)

        top_btn_layout.addWidget(self.add_btn)
        top_btn_layout.addWidget(self.add_dir_btn)
        top_btn_layout.addWidget(self.remove_btn)
        top_btn_layout.addWidget(self.clear_btn)

        self.layout.addLayout(top_btn_layout)

        # Delete buttons layout
        delete_btn_layout = QHBoxLayout()
        delete_btn_layout.setSpacing(10)

        self.delete_selected_btn = QPushButton("🔥 Secure Delete Selected")
        self.delete_selected_btn.setObjectName("deleteButton")
        self.delete_selected_btn.setStyleSheet(DELETE_BUTTON_STYLE)
        
        self.delete_all_btn = QPushButton("💥 Secure Delete All")
        self.delete_all_btn.setObjectName("warningButton")
        self.delete_all_btn.setStyleSheet(WARNING_BUTTON_STYLE)

        delete_btn_layout.addStretch()
        delete_btn_layout.addWidget(self.delete_selected_btn)
        delete_btn_layout.addWidget(self.delete_all_btn)
        delete_btn_layout.addStretch()

        self.layout.addLayout(delete_btn_layout)

        # Status bar
        self.status_label = QLabel("Ready | 0 files")
        self.status_label.setStyleSheet(STATUS_LABEL_READY_STYLE)
        self.layout.addWidget(self.status_label)

        # Copyright footer
        copyright_label = QLabel("© 2025 InnoVista Dev. All rights reserved.")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet(COPYRIGHT_LABEL_STYLE)
        self.layout.addWidget(copyright_label)

        # Connect buttons
        self.add_btn.clicked.connect(self.add_files)
        self.add_dir_btn.clicked.connect(self.add_directory)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.clear_btn.clicked.connect(self.clear_all)
        self.delete_selected_btn.clicked.connect(self.delete_selected)
        self.delete_all_btn.clicked.connect(self.delete_all)
        
        self.update_status()

    def setup_logs_tab(self):
        """Setup the logs viewing tab."""
        logs_layout = QVBoxLayout()
        logs_layout.setContentsMargins(20, 20, 20, 20)
        logs_layout.setSpacing(15)
        self.logs_tab.setLayout(logs_layout)

        # Logs title
        logs_title = QLabel("📋 Activity Logs")
        logs_title_font = QFont("Segoe UI", 18, QFont.Bold)
        logs_title.setFont(logs_title_font)
        logs_title.setAlignment(Qt.AlignCenter)
        logs_title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:0.5 #357abd, stop:1 #4a90e2);
                border-radius: 10px;
                font-size: 20px;
            }
        """)
        logs_layout.addWidget(logs_title)

        # Logs info
        logs_info = QLabel(f"📁 Log file location: {self.log_file}")
        logs_info.setAlignment(Qt.AlignCenter)
        logs_info.setStyleSheet("""
            QLabel {
                color: #b0b0b0;
                font-size: 11px;
                padding: 8px;
                background-color: #2a2a3e;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
        """)
        logs_layout.addWidget(logs_info)

        # Logs text area
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a2a;
                color: #e0e0e0;
                border: 2px solid #3d3d5c;
                border-radius: 10px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                padding: 10px;
            }
        """)
        logs_layout.addWidget(self.logs_text)

        # Refresh logs button
        refresh_btn = QPushButton("🔄 Refresh Logs")
        refresh_btn.setStyleSheet(ADD_BUTTON_STYLE)
        refresh_btn.clicked.connect(self.refresh_logs)
        logs_layout.addWidget(refresh_btn, alignment=Qt.AlignCenter)

        # Load initial logs
        self.refresh_logs()

    def refresh_logs(self):
        """Refresh and display the current logs."""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs_content = f.read()
                    self.logs_text.setPlainText(logs_content)
                    # Scroll to bottom
                    cursor = self.logs_text.textCursor()
                    cursor.movePosition(cursor.End)
                    self.logs_text.setTextCursor(cursor)
            else:
                self.logs_text.setPlainText("No logs available yet.")
        except Exception as e:
            self.logs_text.setPlainText(f"Error reading logs: {e}")

    def setup_encrypt_tab(self):
        """Setup the encryption/decryption tab."""
        encrypt_layout = QVBoxLayout()
        encrypt_layout.setContentsMargins(20, 20, 20, 20)
        encrypt_layout.setSpacing(15)
        self.encrypt_tab.setLayout(encrypt_layout)

        # Title
        encrypt_title = QLabel("🔐 File Encryption & Decryption")
        encrypt_title_font = QFont("Segoe UI", 18, QFont.Bold)
        encrypt_title.setFont(encrypt_title_font)
        encrypt_title.setAlignment(Qt.AlignCenter)
        encrypt_title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8e44ad, stop:0.5 #3498db, stop:1 #8e44ad);
                border-radius: 10px;
                font-size: 20px;
            }
        """)
        encrypt_layout.addWidget(encrypt_title)

        # Info
        info_text = QLabel("🔒 Encrypt files to share securely with friends using a unique key")
        info_text.setAlignment(Qt.AlignCenter)
        info_text.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-size: 11px;
                padding: 8px;
                background-color: #2a2a3e;
                border-radius: 5px;
                font-style: italic;
            }
        """)
        encrypt_layout.addWidget(info_text)

        # Encryption Group
        encrypt_group = QGroupBox("🔐 Encrypt File")
        encrypt_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #8e44ad;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        encrypt_group_layout = QVBoxLayout()
        
        # File selection for encryption
        self.encrypt_file_label = QLabel("No file selected")
        self.encrypt_file_label.setStyleSheet("""
            QLabel {
                color: #b0b0b0;
                padding: 10px;
                background-color: #2a2a3e;
                border: 2px dashed #5a5a7a;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
        """)
        encrypt_group_layout.addWidget(self.encrypt_file_label)
        
        encrypt_btn_layout = QHBoxLayout()
        self.select_encrypt_btn = QPushButton("📁 Select File to Encrypt")
        self.select_encrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8e44ad, stop:1 #6c3483);
                color: white;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #7d3c98);
            }
        """)
        self.select_encrypt_btn.clicked.connect(self.select_file_to_encrypt)
        
        self.do_encrypt_btn = QPushButton("🔒 Encrypt & Generate Key")
        self.do_encrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: 2px solid #2ecc71;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
            QPushButton:disabled {
                background: #4a4a6a;
                border: 2px solid #5a5a7a;
                color: #888;
            }
        """)
        self.do_encrypt_btn.clicked.connect(self.encrypt_selected_file)
        self.do_encrypt_btn.setEnabled(False)
        
        encrypt_btn_layout.addWidget(self.select_encrypt_btn)
        encrypt_btn_layout.addWidget(self.do_encrypt_btn)
        encrypt_group_layout.addLayout(encrypt_btn_layout)
        
        # Key display
        self.key_display = QTextEdit()
        self.key_display.setReadOnly(True)
        self.key_display.setMaximumHeight(100)
        self.key_display.setPlaceholderText("Your encryption key will appear here after encrypting...")
        self.key_display.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a2a;
                color: #2ecc71;
                border: 2px solid #3d3d5c;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                padding: 10px;
            }
        """)
        encrypt_group_layout.addWidget(QLabel("🔑 Encryption Key (Share this with your friend):"))
        encrypt_group_layout.addWidget(self.key_display)
        
        self.copy_key_btn = QPushButton("📋 Copy Key to Clipboard")
        self.copy_key_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 2px solid #5dade2;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
        """)
        self.copy_key_btn.clicked.connect(self.copy_key_to_clipboard)
        encrypt_group_layout.addWidget(self.copy_key_btn)
        
        encrypt_group.setLayout(encrypt_group_layout)
        encrypt_layout.addWidget(encrypt_group)

        # Decryption Group
        decrypt_group = QGroupBox("🔓 Decrypt File")
        decrypt_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        decrypt_group_layout = QVBoxLayout()
        
        # File selection for decryption
        self.decrypt_file_label = QLabel("No encrypted file selected")
        self.decrypt_file_label.setStyleSheet("""
            QLabel {
                color: #b0b0b0;
                padding: 10px;
                background-color: #2a2a3e;
                border: 2px dashed #5a5a7a;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
        """)
        decrypt_group_layout.addWidget(self.decrypt_file_label)
        
        self.select_decrypt_btn = QPushButton("📁 Select Encrypted File")
        self.select_decrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 2px solid #5dade2;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
        """)
        self.select_decrypt_btn.clicked.connect(self.select_file_to_decrypt)
        decrypt_group_layout.addWidget(self.select_decrypt_btn)
        
        # Key input
        decrypt_group_layout.addWidget(QLabel("🔑 Enter Decryption Key:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Paste the encryption key from your friend here...")
        self.key_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a3e;
                color: #e0e0e0;
                border: 2px solid #3d3d5c;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        decrypt_group_layout.addWidget(self.key_input)
        
        self.do_decrypt_btn = QPushButton("🔓 Decrypt File")
        self.do_decrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #d35400);
                color: white;
                border: 2px solid #f39c12;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
            }
            QPushButton:disabled {
                background: #4a4a6a;
                border: 2px solid #5a5a7a;
                color: #888;
            }
        """)
        self.do_decrypt_btn.clicked.connect(self.decrypt_selected_file)
        self.do_decrypt_btn.setEnabled(False)
        decrypt_group_layout.addWidget(self.do_decrypt_btn)
        
        decrypt_group.setLayout(decrypt_group_layout)
        encrypt_layout.addWidget(decrypt_group)

        encrypt_layout.addStretch()

    def select_file_to_encrypt(self):
        """Select a file to encrypt."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        if file_path:
            self.selected_encrypt_file = file_path
            self.encrypt_file_label.setText(f"📄 {os.path.basename(file_path)}")
            self.encrypt_file_label.setStyleSheet("""
                QLabel {
                    color: #2ecc71;
                    padding: 10px;
                    background-color: #1a2a1a;
                    border: 2px solid #27ae60;
                    border-radius: 5px;
                    font-family: 'Courier New', monospace;
                }
            """)
            self.do_encrypt_btn.setEnabled(True)
            logging.info(f"Selected file for encryption: {file_path}")

    def encrypt_selected_file(self):
        """Encrypt the selected file."""
        if not hasattr(self, 'selected_encrypt_file'):
            QMessageBox.warning(self, "No File", "Please select a file to encrypt first.")
            return
        
        try:
            # Generate key
            key = generate_key()
            self.current_key = key
            
            # Encrypt file
            encrypted_path = encrypt_file(self.selected_encrypt_file, key)
            
            if encrypted_path:
                # Display key
                key_str = key.decode('utf-8')
                self.key_display.setPlainText(key_str)
                
                QMessageBox.information(
                    self,
                    "✅ Encryption Successful",
                    f"File encrypted successfully!\n\n"
                    f"Encrypted file: {os.path.basename(encrypted_path)}\n\n"
                    f"⚠️ IMPORTANT:\n"
                    f"1. Copy the encryption key above\n"
                    f"2. Share both the encrypted file AND the key with your friend\n"
                    f"3. Keep the key safe - it cannot be recovered!",
                    QMessageBox.Ok
                )
                
                # Reset
                self.encrypt_file_label.setText("No file selected")
                self.encrypt_file_label.setStyleSheet("""
                    QLabel {
                        color: #b0b0b0;
                        padding: 10px;
                        background-color: #2a2a3e;
                        border: 2px dashed #5a5a7a;
                        border-radius: 5px;
                        font-family: 'Courier New', monospace;
                    }
                """)
                self.do_encrypt_btn.setEnabled(False)
                self.refresh_logs()
            else:
                QMessageBox.critical(
                    self,
                    "❌ Encryption Failed",
                    "Failed to encrypt the file. Check the logs for details.",
                    QMessageBox.Ok
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Encryption error: {str(e)}")
            logging.error(f"Encryption error: {e}")

    def copy_key_to_clipboard(self):
        """Copy encryption key to clipboard."""
        key_text = self.key_display.toPlainText()
        if key_text and key_text != "Your encryption key will appear here after encrypting...":
            clipboard = QApplication.clipboard()
            clipboard.setText(key_text)
            QMessageBox.information(
                self,
                "✅ Copied",
                "Encryption key copied to clipboard!\nYou can now share it with your friend.",
                QMessageBox.Ok
            )
        else:
            QMessageBox.warning(
                self,
                "No Key",
                "No encryption key to copy. Encrypt a file first.",
                QMessageBox.Ok
            )

    def select_file_to_decrypt(self):
        """Select an encrypted file to decrypt."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Encrypted File",
            "",
            "Encrypted Files (*.encrypted);;All Files (*.*)"
        )
        if file_path:
            self.selected_decrypt_file = file_path
            self.decrypt_file_label.setText(f"🔒 {os.path.basename(file_path)}")
            self.decrypt_file_label.setStyleSheet("""
                QLabel {
                    color: #3498db;
                    padding: 10px;
                    background-color: #1a1a2a;
                    border: 2px solid #2980b9;
                    border-radius: 5px;
                    font-family: 'Courier New', monospace;
                }
            """)
            self.do_decrypt_btn.setEnabled(True)
            logging.info(f"Selected file for decryption: {file_path}")

    def decrypt_selected_file(self):
        """Decrypt the selected file."""
        if not hasattr(self, 'selected_decrypt_file'):
            QMessageBox.warning(self, "No File", "Please select an encrypted file first.")
            return
        
        key_str = self.key_input.text().strip()
        if not key_str:
            QMessageBox.warning(
                self,
                "No Key",
                "Please enter the decryption key.",
                QMessageBox.Ok
            )
            return
        
        try:
            # Convert key string to bytes
            key = key_str.encode('utf-8')
            
            # Decrypt file
            decrypted_path = decrypt_file(self.selected_decrypt_file, key)
            
            if decrypted_path:
                QMessageBox.information(
                    self,
                    "✅ Decryption Successful",
                    f"File decrypted successfully!\n\n"
                    f"Decrypted file: {os.path.basename(decrypted_path)}\n"
                    f"Location: {os.path.dirname(decrypted_path)}",
                    QMessageBox.Ok
                )
                
                # Reset
                self.decrypt_file_label.setText("No encrypted file selected")
                self.decrypt_file_label.setStyleSheet("""
                    QLabel {
                        color: #b0b0b0;
                        padding: 10px;
                        background-color: #2a2a3e;
                        border: 2px dashed #5a5a7a;
                        border-radius: 5px;
                        font-family: 'Courier New', monospace;
                    }
                """)
                self.key_input.clear()
                self.do_decrypt_btn.setEnabled(False)
                self.refresh_logs()
            else:
                QMessageBox.critical(
                    self,
                    "❌ Decryption Failed",
                    "Failed to decrypt the file.\n\n"
                    "Possible reasons:\n"
                    "• Wrong decryption key\n"
                    "• File is corrupted\n"
                    "• File is not encrypted\n\n"
                    "Check the logs for more details.",
                    QMessageBox.Ok
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Decryption Error",
                f"Error decrypting file:\n{str(e)}\n\n"
                f"Make sure you're using the correct key.",
                QMessageBox.Ok
            )
            logging.error(f"Decryption error: {e}")
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events for file/folder drops."""
        if event.mimeData().hasUrls():
            # Check if any of the URLs are local files or directories
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    self.is_drag_over = True
                    self.update_drag_style()
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        """Handle drag leave events."""
        self.is_drag_over = False
        self.update_drag_style()

    def dropEvent(self, event: QDropEvent):
        """Handle drop events for file/folder drops."""
        self.is_drag_over = False
        self.update_drag_style()
        
        if event.mimeData().hasUrls():
            files_to_add = []
            directories_to_add = []
            
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    path = url.toLocalFile()
                    if os.path.isfile(path):
                        files_to_add.append(path)
                    elif os.path.isdir(path):
                        directories_to_add.append(path)
            
            # Add individual files
            for file_path in files_to_add:
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
            
            # Add files from directories
            for dir_path in directories_to_add:
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
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
            
            self.update_status()
            event.acceptProposedAction()
        else:
            event.ignore()

    def update_drag_style(self):
        """Update the widget style based on drag state."""
        if self.is_drag_over:
            self.main_tab.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2a2a3e, stop:1 #3d3d5c);
                    color: #e0e0e0;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    border: 3px solid #4a90e2;
                    border-radius: 15px;
                }
            """)
        else:
            self.main_tab.setStyleSheet("")

    def update_status(self):
        """Update the status label with file count and total size."""
        count = self.table.rowCount()
        total_size = 0
        for row in range(count):
            path = self.table.item(row, 2).text()
            if os.path.exists(path):
                total_size += os.path.getsize(path)
        
        if count == 0:
            self.status_label.setText("Ready | 0 files")
            self.status_label.setStyleSheet(STATUS_LABEL_READY_STYLE)
        else:
            self.status_label.setText(
                f"📋 {count} file{'s' if count != 1 else ''} | 💾 Total size: {human_size(total_size)}"
            )
            self.status_label.setStyleSheet(STATUS_LABEL_ACTIVE_STYLE)

    def add_files(self):
        """Add files to the deletion list."""
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
        
        self.update_status()

    def add_directory(self):
        """Add all files from a directory to the deletion list."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
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
            
            self.update_status()

    def is_already_added(self, path):
        """Check if a file path is already in the table."""
        for row in range(self.table.rowCount()):
            if self.table.item(row, 2).text() == path:
                return True
        return False

    def remove_selected(self):
        """Remove selected files from the deletion list."""
        rows = sorted(
            set(index.row() for index in self.table.selectedIndexes()),
            reverse=True
        )
        for row in rows:
            self.table.removeRow(row)
        
        self.update_status()

    def clear_all(self):
        """Clear all files from the deletion list."""
        self.table.setRowCount(0)
        self.update_status()

    def delete_selected(self):
        """Securely delete selected files."""
        rows = sorted(
            set(index.row() for index in self.table.selectedIndexes()),
            reverse=True
        )
        if not rows:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select files to delete first.",
                QMessageBox.Ok
            )
            return

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("⚠️ Confirm Deletion")
        msg_box.setText(f"🔥 {len(rows)} file(s) will be permanently destroyed.")
        msg_box.setInformativeText("This cannot be undone. The files will be overwritten 3 times before deletion.\n\nAre you sure you want to continue?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Style the message box
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d44;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #4a4a6a;
                color: white;
                border: 2px solid #5a5a7a;
                border-radius: 5px;
                padding: 8px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5a5a8a;
            }
        """)

        if msg_box.exec_() != QMessageBox.Yes:
            return

        for row in rows:
            path = self.table.item(row, 2).text()
            secure_delete(path)
            self.table.removeRow(row)
        
        self.update_status()
        
        QMessageBox.information(
            self,
            "✅ Deletion Complete",
            f"Successfully deleted {len(rows)} file(s).",
            QMessageBox.Ok
        )
        
        # Refresh logs to show the deletion activity
        self.refresh_logs()

    def delete_all(self):
        """Securely delete all files in the list."""
        if self.table.rowCount() == 0:
            QMessageBox.information(
                self,
                "No Files",
                "No files to delete.",
                QMessageBox.Ok
            )
            return

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("💥 Confirm Deletion of ALL Files")
        msg_box.setText(f"🔥 ALL {self.table.rowCount()} file(s) will be permanently destroyed!")
        msg_box.setInformativeText("This cannot be undone. The files will be overwritten 3 times before deletion.\n\nAre you ABSOLUTELY SURE you want to continue?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Style the message box
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d44;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #4a4a6a;
                color: white;
                border: 2px solid #5a5a7a;
                border-radius: 5px;
                padding: 8px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5a5a8a;
            }
        """)

        if msg_box.exec_() != QMessageBox.Yes:
            return

        count = self.table.rowCount()
        for row in reversed(range(count)):
            path = self.table.item(row, 2).text()
            secure_delete(path)
            self.table.removeRow(row)
        
        self.update_status()
        
        QMessageBox.information(
            self,
            "✅ Deletion Complete",
            f"Successfully deleted all {count} file(s).",
            QMessageBox.Ok
        )
        
        # Refresh logs to show the deletion activity
        self.refresh_logs()
