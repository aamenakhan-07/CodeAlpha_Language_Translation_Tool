Language Translation Tool

A simple web-based Language Translation Tool developed using Python and Flask. It allows users to translate text between English and supported Indian languages through a translation API.

Features

- Simple and user-friendly interface.
- Supports English and multiple Indian languages.
- Select source and target languages.
- Displays translated text instantly.
- Copy translated text with the Copy button.
- Handles empty input and translation errors.

Technologies Used

- Python
- Flask
- HTML
- CSS
- Requests
- India API (powered by AI4Bharat IndicTrans2)

Installation and Setup

1. Clone this repository:
   
   "git clone https://github.com/aamenakhan-07/CodeAlpha_Language_Translation_Tool.git"

2. Open the project folder.

3. Install the required libraries:
   
   "pip install -r requirements.txt"

4. Run the application:
   
   "python app.py"

5. Open this address in your browser:
   
   "http://127.0.0.1:5000"

Project Structure

Language_Translation_Tool/
│
├── app.py
├── requirements.txt
└── README.md

How It Works

1. Enter the text you want to translate.
2. Select the source language.
3. Select the target language.
4. Click the Translate button.
5. View and copy the translated result.

API Information

This project uses the India API translation endpoint, powered by AI4Bharat IndicTrans2, to translate supported Indian languages.

API Documentation: https://api.dharun.dev/docs/translate

Developer

Developed as part of the CodeAlpha Artificial Intelligence Internship.

Note

An active internet connection is required for translation because the application uses an external translation API.
