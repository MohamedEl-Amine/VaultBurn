"""
UI Styles and themes for VaultBurn application.
"""

# Main application stylesheet
APP_STYLESHEET = """
    QWidget {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #1e1e2e, stop:1 #2d2d44);
        color: #e0e0e0;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    QTabWidget::pane {
        border: 2px solid #3d3d5c;
        background-color: #2a2a3e;
        border-radius: 10px;
    }
    
    QTabBar::tab {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #3a3a5a, stop:1 #2a2a4a);
        color: #b0b0b0;
        padding: 12px 25px;
        margin-right: 2px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-size: 13px;
        font-weight: bold;
    }
    
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4a90e2, stop:1 #357abd);
        color: white;
    }
    
    QTabBar::tab:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4a4a6a, stop:1 #3a3a5a);
        color: white;
    }
"""

# Table widget stylesheet
TABLE_STYLESHEET = """
    QTableWidget {
        background-color: #252535;
        alternate-background-color: #2a2a3e;
        border: 2px solid #4a90e2;
        border-radius: 10px;
        gridline-color: #4a90e2;
        color: #e0e0e0;
        font-size: 13px;
    }
    
    QTableWidget::item {
        padding: 8px;
    }
    
    QTableWidget::item:selected {
        background-color: #5e5ea8;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #4a90e2;
        color: #ffffff;
        padding: 10px;
        border: none;
        border-right: 1px solid #357abd;
        font-weight: bold;
        font-size: 13px;
    }
"""

# Button styles
ADD_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4a90e2, stop:1 #357abd);
        color: white;
        border: 2px solid #5a9af2;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 13px;
        font-weight: bold;
        min-width: 120px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #5aa0f2, stop:1 #458acd);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #357abd, stop:1 #2a6aa8);
    }
"""

NORMAL_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4a4a6a, stop:1 #3a3a5a);
        color: white;
        border: 2px solid #5a5a7a;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 13px;
        font-weight: bold;
        min-width: 120px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #5a5a8a, stop:1 #4a4a7a);
        border: 2px solid #6a6a9a;
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #3a3a5a, stop:1 #2a2a4a);
    }
"""

DELETE_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #e74c3c, stop:1 #c0392b);
        color: white;
        border: 2px solid #e85c4c;
        border-radius: 8px;
        padding: 12px 25px;
        font-size: 14px;
        font-weight: bold;
        min-width: 180px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f75c4c, stop:1 #d0493b);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #c0392b, stop:1 #a02919);
    }
"""

WARNING_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f39c12, stop:1 #d68910);
        color: white;
        border: 2px solid #f3ac22;
        border-radius: 8px;
        padding: 12px 25px;
        font-size: 14px;
        font-weight: bold;
        min-width: 180px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f3ac22, stop:1 #e69920);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #d68910, stop:1 #b67700);
    }
"""

# Label styles
TITLE_LABEL_STYLE = """
    QLabel {
        color: #ffffff;
        padding: 15px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #e74c3c, stop:0.5 #f39c12, stop:1 #e74c3c);
        border-radius: 10px;
        font-size: 22px;
    }
"""

INFO_LABEL_STYLE = """
    QLabel {
        color: #f39c12;
        font-size: 12px;
        padding: 8px;
        background-color: #2a2a1a;
        border-radius: 5px;
        border: 1px solid #f39c12;
    }
"""

HINT_LABEL_STYLE = """
    QLabel {
        color: #4a90e2;
        font-size: 11px;
        padding: 5px;
        background-color: transparent;
        font-style: italic;
    }
"""

STATUS_LABEL_READY_STYLE = """
    QLabel {
        color: #4a90e2;
        font-size: 13px;
        padding: 10px;
        background-color: #1a1a2a;
        border-radius: 5px;
        border: 1px solid #3d3d5c;
    }
"""

STATUS_LABEL_ACTIVE_STYLE = """
    QLabel {
        color: #2ecc71;
        font-size: 13px;
        padding: 10px;
        background-color: #1a1a2a;
        border-radius: 5px;
        border: 1px solid #2ecc71;
    }
"""

COPYRIGHT_LABEL_STYLE = """
    QLabel {
        color: #6a6a8a;
        font-size: 11px;
        padding: 10px;
        background-color: transparent;
        font-style: italic;
    }
"""
