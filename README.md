# 🛡️ AI TrustLens – Your Digital Safety Companion

## 🌐 Project Overview

AI TrustLens is a web-based digital safety application that helps users identify potential scam and phishing warning signs in website URLs, text messages, images, PDF documents, and TXT files.

It uses rule-based detection and OCR technology to analyze suspicious content and provide understandable warnings.

## 🎯 Problem Statement

Online scams, phishing links, fake prize notifications, and fraudulent messages are increasing. Many users struggle to identify suspicious content and may unknowingly share personal or financial information.

## 💡 Proposed Solution

AI TrustLens provides a simple platform where users can submit suspicious links, messages, or files and receive warning signs with safety explanations.

## ✨ Key Features

- 🔗 Website URL analysis
- 💬 Suspicious message analysis
- 🖼️ Image upload with OCR text extraction
- 📄 PDF text extraction and analysis
- 📝 TXT file analysis
- ⚠️ Rule-based scam warning detection
- 🔐 Online safety recommendations

## 🛠️ Technologies Used

**Frontend**
- HTML5
- CSS3
- JavaScript

**Backend**
- Python
- Flask
- Flask-CORS

**File Processing**
- Pytesseract
- Tesseract OCR
- Pillow
- pypdf

## 📂 Project Structure

```text
AI Trust-Lens/
├── Backend/
│   └── app.py
├── Frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/harshithat0729-dev/Trust-lens.git
cd Trust-lens
```

Create a Python virtual environment:

```bash
py -m venv Backend/.venv
```

Install dependencies:

```bash
Backend/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

Install Tesseract OCR separately for image text extraction.

## ▶️ Run the Application

Start the backend:

```bash
cd Backend
.venv/Scripts/python.exe app.py
```

Open the frontend using VS Code Live Server.

Backend:

`http://127.0.0.1:5000`

Frontend:

`http://127.0.0.1:5500/Frontend/index.html`

## 🧪 Testing

The application has been manually tested with:
- Suspicious and normal messages.
- HTTP and HTTPS URLs.
- Scam-related images.
- PDF documents containing suspicious content.
- TXT files containing suspicious messages.

## ⚠️ Limitations

- Uses basic rule-based detection.
- Does not use a trained machine-learning model.
- Cannot guarantee whether content is safe or fraudulent.
- OCR accuracy depends on image quality.
- URL analysis does not verify live website reputation.

## 🚀 Future Enhancements

- Machine-learning-based scam classification.
- Live malicious URL reputation checking.
- Improved OCR for scanned PDFs.
- Multilingual scam detection.
- Downloadable analysis reports.
- Automated testing.

## 🔒 Disclaimer

AI TrustLens provides basic warning indicators for educational and awareness purposes. Its results are not definitive security verdicts. Always independently verify suspicious messages, websites, and payment requests.

---

**AI TrustLens – Think Before You Trust.** 🛡️
