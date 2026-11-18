
from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

API_URL = "https://api.dharun.dev/v1/translate"

LANGUAGES = {
    "en": "English",
    "as": "Assamese",
    "bn": "Bengali",
    "brx": "Bodo",
    "doi": "Dogri",
    "gu": "Gujarati",
    "hi": "Hindi",
    "kn": "Kannada",
    "ks": "Kashmiri",
    "kok": "Konkani",
    "mai": "Maithili",
    "ml": "Malayalam",
    "mni": "Manipuri",
    "mr": "Marathi",
    "ne": "Nepali",
    "or": "Odia",
    "pa": "Punjabi",
    "sa": "Sanskrit",
    "sat": "Santali",
    "sd": "Sindhi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu"
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Language Translation Tool</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef3ff;
            margin: 0;
            padding: 25px 12px;
        }

        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        h1 {
            text-align: center;
            color: #2457c5;
        }

        p {
            color: #555;
        }

        .subtitle {
            text-align: center;
        }

        label {
            display: block;
            margin-top: 18px;
            font-weight: bold;
        }

        textarea, select {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 15px;
        }

        textarea {
            height: 130px;
            resize: vertical;
        }

        button {
            width: 100%;
            padding: 13px;
            margin-top: 20px;
            background: #2457c5;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #173f99;
        }

        .result {
            margin-top: 25px;
            padding: 18px;
            background: #edf7ee;
            border-radius: 10px;
        }

        .result p {
            color: #222;
            overflow-wrap: anywhere;
        }

        .error {
            margin-top: 20px;
            padding: 12px;
            background: #ffe9e9;
            color: #b00020;
            border-radius: 8px;
        }

        .copy-btn {
            background: #16834a;
        }

        .copy-btn:hover {
            background: #106337;
        }

        footer {
            text-align: center;
            margin-top: 25px;
            color: #777;
            font-size: 13px;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>Language Translation Tool</h1>

    <p class="subtitle">
        Translate your text into different Indian languages
    </p>

    <form method="POST">

        <label>Enter Your Text:</label>

        <textarea name="text"
        placeholder="Type your text here..."
        maxlength="2000"
        required>{{ original_text }}</textarea>

        <label>Source Language:</label>

        <select name="source" required>
            {% for code, name in languages.items() %}
            <option value="{{ code }}"
            {% if source_lang == code %}selected{% endif %}>
                {{ name }}
            </option>
            {% endfor %}
        </select>

        <label>Target Language:</label>

        <select name="target" required>
            {% for code, name in languages.items() %}
            <option value="{{ code }}"
            {% if target_lang == code %}selected{% endif %}>
                {{ name }}
            </option>
            {% endfor %}
        </select>

        <button type="submit">
            Translate
        </button>

    </form>

    {% if translated_text %}

    <div class="result">

        <h3>Translated Text:</h3>

        <p id="translation">{{ translated_text }}</p>

        <button type="button"
                class="copy-btn"
                onclick="copyTranslation()">
            Copy Translation
        </button>

    </div>

    {% endif %}

    {% if error %}

    <div class="error">
        {{ error }}
    </div>

    {% endif %}

    <footer>
        Developed as part of CodeAlpha AI Internship
    </footer>

</div>

<script>
function copyTranslation() {

    var text = document.getElementById(
        "translation"
    ).innerText;

    navigator.clipboard.writeText(text)
        .then(function() {
            alert("Translation copied successfully!");
        })
        .catch(function() {
            alert("Unable to copy. Please copy manually.");
        });
}
</script>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    translated_text = ""
    error = ""
    original_text = ""

    source_lang = "en"
    target_lang = "hi"

    if request.method == "POST":

        original_text = request.form.get(
            "text", ""
        ).strip()

        source_lang = request.form.get(
            "source", "en"
        )

        target_lang = request.form.get(
            "target", "hi"
        )

        if not original_text:

            error = "Please enter some text."

        elif len(original_text) > 2000:

            error = "Text cannot exceed 2000 characters."

        elif (source_lang not in LANGUAGES
              or target_lang not in LANGUAGES):

            error = "Please select valid languages."

        elif source_lang == target_lang:

            error = "Please select two different languages."

        else:

            try:

                params = {
                    "text": original_text,
                    "from": source_lang,
                    "to": target_lang
                }

                response = requests.get(
                    API_URL,
                    params=params,
                    timeout=30
                )

                data = response.json()

                if response.ok:

                    translated_text = data.get(
                        "data", {}
                    ).get("translation", "")

                    if not translated_text:
                        error = "Translation was not received."

                else:

                    error = data.get(
                        "error", {}
                    ).get(
                        "message",
                        "Translation service error."
                    )

            except requests.exceptions.Timeout:

                error = (
                    "Request timed out. Please try again."
                )

            except requests.exceptions.ConnectionError:

                error = (
                    "Internet connection problem. "
                    "Please check your network."
                )

            except requests.exceptions.RequestException:

                error = (
                    "Unable to contact translation service."
                )

            except ValueError:

                error = (
                    "Invalid response received from translation API."
                )

            except Exception:

                error = (
                    "Something went wrong. Please try again."
                )

    return render_template_string(
        HTML,
        languages=LANGUAGES,
        translated_text=translated_text,
        original_text=original_text,
        source_lang=source_lang,
        target_lang=target_lang,
        error=error
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
