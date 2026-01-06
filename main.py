"""
VaultBurn - Secure File Deletion Application
Main entry point for the application.
"""
import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
import os

# Import utilities and main window
from utils import setup_logging
from ui.main_window import SecureDeleteApp


def main():
    """Main entry point for VaultBurn application."""
    # Setup logging
    log_file = setup_logging()
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create splash screen
    splash_path = os.path.join(os.path.dirname(__file__), 'assets', 'splashscreen.png')
    if os.path.exists(splash_path):
        splash_pixmap = QPixmap(splash_path)
        splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
        splash.show()
        app.processEvents()
    else:
        splash = None
    
    # Create main window
    window = SecureDeleteApp()
    
    # Set window icon if available
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    
    # Show main window after splash screen delay
    if splash:
        QTimer.singleShot(300, lambda: (splash.close(), window.show()))
    else:
        window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
