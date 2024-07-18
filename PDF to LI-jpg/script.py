import sys
import os
import fitz  # PyMuPDF
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt

def pdf_to_long_image(pdf_path, output_image_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    max_width = max(image.width for image in images)
    total_height = sum(image.height for image in images)

    long_image = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for image in images:
        long_image.paste(image, (0, y_offset))
        y_offset += image.height

    long_image.save(output_image_path)

class PDFConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pdf_files = []
        
    def initUI(self):
        self.setWindowTitle('PDF to Long Image Converter')
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        
        self.convert_button = QPushButton('Convert Loaded PDFs')
        self.convert_button.clicked.connect(self.convert_loaded_pdfs)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.convert_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path.endswith('.pdf'):
                self.pdf_files.append(file_path)
                self.text_edit.append(f'Added: {file_path}')
        
    def convert_loaded_pdfs(self):
        if self.pdf_files:
            for pdf_file in self.pdf_files:
                try:
                    output_image_path = f"{os.path.splitext(pdf_file)[0]}.png"
                    pdf_to_long_image(pdf_file, output_image_path)
                    self.text_edit.append(f"Converted {pdf_file} to {output_image_path}")
                except Exception as e:
                    self.text_edit.append(f"Failed to convert {pdf_file}: {e}")
        else:
            self.text_edit.append("No PDFs loaded to convert")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = PDFConverter()
    converter.show()
    sys.exit(app.exec_())
