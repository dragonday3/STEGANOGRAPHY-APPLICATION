import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, 
    QLineEdit, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QIcon, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect

from encryption import encode_text_in_image
from decryption import decode_text_from_image

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists

class ImageEncryptionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Encryption & Decryption")
        self.setGeometry(100, 100, 700, 400)
        self.setAcceptDrops(True)

        main_layout = QHBoxLayout()

        # Encryption Section (Left)
        encrypt_layout = QVBoxLayout()
        encrypt_layout.setSpacing(10)

        self.label = QLabel("Drag & Drop an image or use the buttons below")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        encrypt_layout.addWidget(self.label)

        self.select_encrypt_image_button = QPushButton("Select Image for Encryption")
        self.select_encrypt_image_button.clicked.connect(self.select_encrypt_image)
        encrypt_layout.addWidget(self.select_encrypt_image_button)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text to encrypt")
        encrypt_layout.addWidget(self.text_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password (optional)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        encrypt_layout.addWidget(self.password_input)

        self.encrypt_button = QPushButton("Encrypt Image")
        self.encrypt_button.clicked.connect(self.encrypt_image)
        encrypt_layout.addWidget(self.encrypt_button)

        encrypt_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        main_layout.addLayout(encrypt_layout)

        # Spacer between encryption and decryption sections
        main_layout.addItem(QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

        # Decryption Section (Right)
        decrypt_layout = QVBoxLayout()
        decrypt_layout.setSpacing(10)

        self.select_decrypt_image_button = QPushButton("Select Image for Decryption")
        self.select_decrypt_image_button.clicked.connect(self.select_decrypt_image)
        decrypt_layout.addWidget(self.select_decrypt_image_button)

        self.decrypt_password_input = QLineEdit(self)
        self.decrypt_password_input.setPlaceholderText("Enter password (optional)")
        self.decrypt_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        decrypt_layout.addWidget(self.decrypt_password_input)

        self.decrypt_button = QPushButton("Decrypt Image")
        self.decrypt_button.clicked.connect(self.decrypt_image)
        decrypt_layout.addWidget(self.decrypt_button)

        self.result_label = QLabel("")
        decrypt_layout.addWidget(self.result_label)

        decrypt_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        main_layout.addLayout(decrypt_layout)

        self.setLayout(main_layout)

        # Center the window on the screen
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        self.encrypt_image_path = None
        self.decrypt_image_path = None

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(34, 34, 34, 255), stop:1 rgba(0, 0, 0, 255));
                color: #ffffff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                border-radius: 15px;
            }

            QPushButton {
                background-color: #3a3a3a;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
                transition: all 0.3s ease;
            }

            QPushButton:hover {
                background-color: #575757;
                cursor: pointer;
            }

            QLineEdit {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 10px;
                color: #ffffff;
                padding: 10px;
                font-size: 14px;
            }

            QLabel {
                font-size: 16px;
                color: #ccc;
                padding: 10px;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """ Accept only image files during drag-and-drop """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """ Handle dropped image file """
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.encrypt_image_path = file_path
                self.label.setText(f"Selected: {os.path.basename(file_path)}")
                self.result_label.clear()  # Clear previous result
            else:
                QMessageBox.warning(self, "Error", "Invalid file type. Please drop an image.")

    def select_encrypt_image(self):
        """ Select image for encryption """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.encrypt_image_path = file_path
            self.label.setText(f"Selected for Encryption: {os.path.basename(file_path)}")
            self.result_label.clear()

    def select_decrypt_image(self):
        """ Select image for decryption """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.decrypt_image_path = file_path
            self.label.setText(f"Selected for Decryption: {os.path.basename(file_path)}")
            self.result_label.clear()

    def encrypt_image(self):
        """ Encrypt text into an image """
        if not self.encrypt_image_path:
            QMessageBox.warning(self, "Error", "Please select an image for encryption.")
            return

        text = self.text_input.text()
        password = self.password_input.text()

        if not text:
            QMessageBox.warning(self, "Error", "Text field cannot be empty.")
            return

        try:
            encrypted_image_path = encode_text_in_image(self.encrypt_image_path, text + password)
            QMessageBox.information(self, "Success", f"Image encrypted!\nSaved at: {encrypted_image_path}")
            self.result_label.clear()
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", f"Failed to encrypt image: {e}")

    def decrypt_image(self):
        """ Decrypt text from an image """
        if not self.decrypt_image_path:
            QMessageBox.warning(self, "Error", "Please select an image for decryption.")
            return

        password = self.decrypt_password_input.text()

        try:
            decrypted_text = decode_text_from_image(self.decrypt_image_path)

            if decrypted_text.endswith(password):
                self.result_label.setText(f"Decrypted Text: {decrypted_text.replace(password, '')}")
            else:
                QMessageBox.warning(self, "Error", "Incorrect password or no hidden text found.")
                self.result_label.clear()
        except Exception as e:
            QMessageBox.critical(self, "Decryption Error", f"Failed to decrypt image: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEncryptionApp()
    window.show()
    sys.exit(app.exec())
