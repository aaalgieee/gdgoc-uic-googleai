# UIC Student Handbook Chatbot (Mariah)

A Flask-based chatbot that uses Google's Gemini AI to answer questions about the University of the Immaculate Conception's Student Handbook.

## Prerequisites

- Python 3.8 or higher
- Google AI API key (Gemini)
- UIC Student Handbook PDF file

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd gdgoc-uic-googleai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask google-generativeai python-dotenv
```

4. Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

5. Place the `Handbook.pdf` file in the project root directory.

## Running the Application

1. Make sure your virtual environment is activated.

2. Start the Flask server:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Features

- Interactive chat interface
- Responses based on the UIC Student Handbook
- Powered by Google's Gemini AI model
- Real-time conversation history

## Troubleshooting

- If you see an error about missing `Handbook.pdf`, ensure the file is placed in the project root directory.
- If you get API errors, verify your Gemini API key in the `.env` file.
- Make sure all dependencies are installed correctly using the requirements above.

## Note

This is a demo application. The responses are generated based on the content of the UIC Student Handbook only.
