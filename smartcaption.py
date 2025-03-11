# Import necessary libraries for screen capture, OCR, HTTP requests, GUI, and image processing
import pyautogui  # For capturing screenshots
import pytesseract  # For optical character recognition (OCR)
import requests  # For making API calls
from tkinter import Tk, Label, Button, StringVar  # For creating a GUI with dynamic text
from PIL import Image  # For handling image files

# Set the path to the Tesseract-OCR executable (required for pytesseract to work)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to capture text from Live Captions on the screen
def capture_live_caption():
    """
    Captures a screenshot of the Live Captions area and extracts text using OCR.
    Returns the extracted text or a fallback message if no text is found.
    """
    # Define coordinates and size of the Live Captions region (x, y, width, height)
    x, y, width, height = 470, 1030, 980, 100  # Based on user's screen setup
    # Capture the screenshot of the specified region
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    # Save the screenshot as an image file for OCR processing
    screenshot.save("caption.png")
    # Use OCR to extract text from the saved image
    text = pytesseract.image_to_string(Image.open("caption.png"))
    # Return the stripped text, or a default message if no text is detected
    return text.strip() if text else "No text found."

# Function to get an answer from Hugging Face Inference API
def get_answer_from_ai(question):
    """
    Sends a question to the Hugging Face Inference API and retrieves an answer.
    Uses an expanded context for more detailed answers.
    Returns the answer or an error message if the request fails.
    """
    try:
        # API endpoint for the question-answering model
        url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
        # Authentication header with the user's Hugging Face API key
        headers = {
            "Authorization": "Bearer YOUR-API"  # User's token
        }
        # Expanded context with more detailed information
        context = (
            "SQL is Structured Query Language, a standard language used for managing and manipulating relational databases. "
            "It allows users to create, read, update, and delete data efficiently. "
            "OOP is Object-Oriented Programming, a programming paradigm based on the concept of objects, which can contain data and code. "
            "Python is a high-level, interpreted programming language known for its readability and versatility."
        )
        # Payload for the API request, including the question and context
        data = {
            "inputs": {
                "question": question,
                "context": context
            }
        }
        # Send POST request to the Hugging Face API
        response = requests.post(url, json=data, headers=headers)
        # Print debug information to the console
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the answer from the JSON response
            answer = response.json().get("answer", "No answer found.")
            return f"SmartCaption: {answer}"
        # Return an error message if the request fails
        return f"SmartCaption: {question} (Failed to get answer - Status: {response.status_code})"
    except Exception as e:
        # Return any exception details if the request fails
        return f"Error: {str(e)}"

# Main function to orchestrate the program flow and update the GUI
def start_program():
    """
    Captures text from Live Captions, gets an answer from the API, and updates the answer label in the main window.
    """
    # Get the question from Live Captions
    question = capture_live_caption()
    print(f"Question from Live Captions: {question}")  # Log the question to console
    # Get the answer from the AI API
    answer = get_answer_from_ai(question)
    # Update the answer label with the new text
    answer_text.set(answer)

# Set up the main GUI window with a button and dynamic answer label
root = Tk()
root.title("SmartCaption")  # Set main window title
root.geometry("400x200")  # Set main window size (increased to fit longer answers)

# Create a StringVar to dynamically update the answer text
answer_text = StringVar()
answer_text.set("Press the button to get an answer.")  # Initial text

# Create a label to display the answer, with text wrapping
answer_label = Label(root, textvariable=answer_text, wraplength=380, justify="left")
answer_label.pack(pady=10)  # Add padding around the label

# Create a button to trigger the start_program function
btn = Button(root, text="Get Question from Live Captions", command=start_program)
btn.pack(pady=10)  # Add padding around the button

root.mainloop()  # Start the main Tkinter event loop
