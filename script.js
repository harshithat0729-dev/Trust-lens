const urlInput = document.getElementById("urlInput");
const messageInput = document.getElementById("messageInput");

const analyzeUrlButton = document.getElementById("analyzeUrlButton");
const analyzeMessageButton = document.getElementById("analyzeMessageButton");

const resultBox = document.getElementById("result");

function showMessage(message) {
    resultBox.textContent = message;
    resultBox.hidden = false;
    resultBox.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}

async function analyzeData(endpoint, payload, label) {
    showMessage(`Analyzing ${label}...`);

    try {
        const response = await fetch(
            `http://127.0.0.1:5000/api/${endpoint}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            showMessage(data.message || "Analysis failed.");
            return;
        }

        const warnings = data.warning_signs?.length
            ? data.warning_signs.map(item => "- " + item).join("\n")
            : "No common warning signs detected.";

        showMessage(
            `Status: ${data.status}\n\n` +
            `Warning Signs:\n${warnings}\n\n` +
            `Explanation: ${data.explanation}\n\n` +
            `${data.disclaimer || ""}`
        );
    } catch (error) {
        showMessage(
            "Cannot connect to the backend. Check whether Flask is running."
        );
        console.error(error);
    }
}

analyzeMessageButton.addEventListener("click", function () {
    const message = messageInput.value.trim();
    const fileInput = document.getElementById("fileInput");
    if (!message) {
        showMessage("Please paste a message to continue.");
        return;
    }

    analyzeData("analyze-message", { message }, "message");
});

analyzeUrlButton.addEventListener("click", function () {
    const url = urlInput.value.trim();

    if (!url) {
        showMessage("Please enter a website URL to continue.");
        return;
    }

    analyzeData("analyze-url", { url }, "URL");
});
async function analyzeUploadedFile() {
    const file = fileInput.files[0];

    if (!file) {
        showMessage("Please select an Image, PDF or TXT file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showMessage("Analyzing uploaded file...");

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/analyze-file",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            showMessage(data.message || "File analysis failed.");
            return;
        }

        const warnings = data.warning_signs?.length
            ? data.warning_signs.map(item => "- " + item).join("\n")
            : "No common warning signs detected.";

        showMessage(
            `File: ${data.filename}\n\n` +
            `Extracted Text:\n${data.extracted_text}\n\n` +
            `Status: ${data.status}\n\n` +
            `Warning Signs:\n${warnings}\n\n` +
            `Explanation: ${data.explanation}\n\n` +
            `${data.disclaimer || ""}`
        );

    } catch (error) {
        showMessage("Cannot connect to backend. Check whether Flask is running.");
        console.error(error);
    }
}

fileInput.addEventListener("change", analyzeUploadedFile);