from flask import Flask, render_template, request, jsonify
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    return file

def wait_for_files_active(files):
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(1)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    system_instruction="always based on the Handbook.pdf and be nice.",
)

def initialize_chat():
    handbook_path = "Handbook.pdf"
    if not os.path.exists(handbook_path):
        print(f"Error: {handbook_path} not found!")
        return None
    
    try:
        files = [upload_to_gemini(handbook_path, mime_type="application/pdf")]
        wait_for_files_active(files)
        
        return model.start_chat(history=[
            {
                "role": "user",
                "parts": [
                    files[0],
                    "you are a chatbot name Mariah, a student companion app where you know the University of the Immaculate Conception's Rules and Regulations or simply known as the Student Handbook based on this PDF",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Hello! I'm Mariah, your UIC student companion. I've been trained on the UIC Student Handbook and I'm ready to help you!"
                ],
            },
        ])
    except Exception as e:
        print(f"Error initializing chat: {str(e)}")
        return None

# Initialize chat session at startup
chat_session = initialize_chat()

@app.route('/')
def home():
    if chat_session is None:
        return "Error: Handbook.pdf not found or failed to initialize chat. Please ensure the file exists in the correct location.", 500
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if chat_session is None:
        return jsonify({
            'response': "Sorry, I'm not able to help right now as I don't have access to the handbook. Please contact support."
        }), 500
    
    user_message = request.json['message']
    try:
        response = chat_session.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({
            'response': f"Sorry, there was an error processing your request: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
