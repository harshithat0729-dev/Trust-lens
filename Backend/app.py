from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import re
import ipaddress
import pytesseract
import io
from PIL import Image
from pypdf import PdfReader

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
        return jsonify({
        "project": "AI TrustLens",
        "status": "Backend is running!"
    })


@app.route("/api/analyze-message", methods=["POST"])
def analyze_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"message": "Please enter a message."}), 400

    checks = [
        (r"\b(otp|one[- ]time password|verification code)\b",
         "Requests for an OTP or verification code"),
        (r"\b(password|pin|bank details|card number)\b",
         "Mentions passwords or sensitive financial information"),
        (r"\b(won|winner|prize|lottery|claim your reward)\b",
         "Unexpected prize or reward claims"),
        (r"\b(urgent|immediately|act now|limited time)\b",
         "Urgent language that pressures the reader"),
        (r"\b(send money|pay a fee|transfer money)\b",
         "Requests to send money or pay a fee"),
        (r"\b(click here|verify your account|account suspended)\b",
         "Account verification or suspension language")
    ]

    warnings = [
        explanation for pattern, explanation in checks
        if re.search(pattern, message, re.IGNORECASE)
    ]

    return jsonify({
        "status": "Warning signs detected" if warnings
                  else "No common warning signs detected",
        "warning_signs": warnings,
        "explanation": (
            "Verify this message independently before taking action."
            if warnings else
            "No common warning signs were found by these basic checks."
        ),
        "disclaimer": "This rule-based check cannot guarantee whether a message is real or fake."
    })


@app.route("/api/analyze-url", methods=["POST"])
def analyze_url():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"message": "Please enter a URL."}), 400

    url = url.strip()

    # Add HTTPS if the user enters a domain without a scheme.
    candidate = url if "://" in url else "https://" + url
    parsed = urlparse(candidate)
    hostname = parsed.hostname
    warnings = []

    if parsed.scheme not in ("http", "https") or not hostname:
        return jsonify({
            "status": "Invalid URL",
            "warning_signs": ["The URL format is invalid or unsupported."],
            "explanation": "Enter a valid website address beginning with a domain name."
        })

    if parsed.username or parsed.password:
        warnings.append("The URL contains embedded login credentials.")

    try:
        ipaddress.ip_address(hostname)
        warnings.append("The website address uses an IP address instead of a domain name.")
    except ValueError:
        pass

    if parsed.scheme == "http":
        warnings.append("The URL uses HTTP rather than encrypted HTTPS.")

    if hostname.startswith("xn--") or ".xn--" in hostname:
        warnings.append("The domain uses an encoded internationalized name.")

    if re.search(r"@|%40", url, re.IGNORECASE):
        warnings.append("The URL contains an @ symbol, which can sometimes obscure the destination.")

    return jsonify({
        "status": "Warning signs detected" if warnings
                  else "No common warning signs detected",
        "url": url,
        "hostname": hostname,
        "warning_signs": warnings,
        "explanation": (
            "Review this URL carefully before opening it."
            if warnings else
            "These basic checks found no listed warning signs. This does not prove the website is safe."
        ),
        "disclaimer": "This is a basic URL check, not a definitive safety verdict."
    })

@app.route("/api/analyze-file", methods=["POST"])
def analyze_file():
    if "file" not in request.files:
        return jsonify({"message": "Please upload a file."}), 400

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return jsonify({"message": "No file selected."}), 400

    filename = uploaded_file.filename.lower()
    extension = filename.rsplit(".", 1)[-1] if "." in filename else ""

    allowed_extensions = {"png", "jpg", "jpeg", "webp", "pdf", "txt"}

    if extension not in allowed_extensions:
        return jsonify({"message": "Only Image, PDF and TXT files are supported."}), 400

    file_bytes = uploaded_file.read(5 * 1024 * 1024 + 1)

    if not file_bytes:
        return jsonify({"message": "The uploaded file is empty."}), 400

    if len(file_bytes) > 5 * 1024 * 1024:
        return jsonify({"message": "File size must be below 5 MB."}), 400

    try:
        if extension in {"png", "jpg", "jpeg", "webp"}:
            image = Image.open(io.BytesIO(file_bytes))
            image.verify()

            image = Image.open(io.BytesIO(file_bytes))
            extracted_text = pytesseract.image_to_string(image)

        elif extension == "pdf":
            reader = PdfReader(io.BytesIO(file_bytes))

            if reader.is_encrypted:
                return jsonify({"message": "Password-protected PDFs are not supported."}), 400

            extracted_text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            )

        else:
            extracted_text = file_bytes.decode("utf-8-sig")

    except UnicodeDecodeError:
        return jsonify({"message": "TXT file must use UTF-8 encoding."}), 400
    except Exception:
        return jsonify({"message": "Could not read this file. Please try another file."}), 400

    if not extracted_text.strip():
        return jsonify({
            "message": "No readable text found. The image may be unclear or the PDF may be scanned."
        }), 400

    checks = [
        (r"\b(otp|one[- ]time password|verification code)\b",
         "Requests for an OTP or verification code"),
        (r"\b(password|pin|bank details|card number)\b",
         "Mentions passwords or sensitive financial information"),
        (r"\b(won|winner|prize|lottery|claim your reward)\b",
         "Unexpected prize or reward claims"),
        (r"\b(urgent|immediately|act now|limited time)\b",
         "Urgent language that pressures the reader"),
        (r"\b(send money|pay a fee|transfer money)\b",
         "Requests to send money or pay a fee"),
        (r"\b(click here|verify your account|account suspended)\b",
         "Account verification or suspension language")
    ]

    warnings = [
        explanation for pattern, explanation in checks
        if re.search(pattern, extracted_text, re.IGNORECASE)
    ]

    return jsonify({
        "filename": uploaded_file.filename,
        "extracted_text": extracted_text,
        "status": "Warning signs detected" if warnings
                  else "No common warning signs detected",
        "warning_signs": warnings,
        "explanation": "Verify this content independently before taking action.",
        "disclaimer": "This is a basic rule-based check and cannot guarantee whether content is real or fake."
    })
if __name__ == "__main__":
    app.run(debug=True)
