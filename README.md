# Secure Data Hiding in Image using Steganography
A PyQt6 Application for Securely Embedding and Extracting Text from Images

**Overview**

This project is a PyQt6-based desktop application that allows users to encrypt and decrypt text within images. It provides a user-friendly interface for embedding text inside images securely and retrieving it when needed. The encryption process modifies pixel values to encode text, ensuring a hidden yet retrievable message.

**Features**
- **Drag & Drop Image Upload** – Easily add images by dragging them into the app.
- **Text Encryption into Images** – Embed hidden messages securely inside images.
- **Password Protection** – Optionally secure hidden text with a password.
- **Decryption with Password Validation** – Retrieve hidden text by providing the correct password.
- **Intuitive UI** – Dark-themed modern UI built with PyQt6.
- **Standalone Executable** – Package the app into an `.exe` or `.app` using PyInstaller.
- **Cross-Platform Support** – Runs on Windows, macOS, and Linux.

**Installation & Setup**
1. Clone the Repository
   - git clone https://github.com/dragonday3/STEGANOGRAPHY-APPLICATION.git

2. Install Dependencies
   - pip install -r requirements.txt

3. Run the Application
   - python app.py

**Packaging as an Executable**
1. Install PyInstaller
   - pip install pyinstaller

2. Create the Executable
   - pyinstaller --noconsole --onefile --icon=icon.ico app.py

3. The executable will be generated inside the dist/ folder:
   - Windows: `dist/app.exe`
   - macOS/Linux: `dist/app`

**How It Works**
- Encryption Process
  1. Select an image or drag and drop one into the application.
  2. Enter the text to encrypt.
  3. Optionally, provide a password for added security.
  4. Click the "Encrypt Image" button.
  5. The encrypted image is saved as `encrypted.png` in the same directory.

- Decryption Process
  1. Select an encrypted image.
  2. Enter the password (if one was used).
  3. Click "Decrypt Image" to retrieve the hidden text.

# **OUTPUT**
![Image](https://github.com/user-attachments/assets/a3b6d46d-7ab3-4e52-94e4-7b63f5aa1d6f)
![Image](https://github.com/user-attachments/assets/f932bb32-7788-4c5d-927f-7168bb82ec90)
