import pandas as pd
import spacy
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Load medical data from CSV
medical_data = pd.read_csv("medical_data.csv")

# Create a mapping of conditions to specialists
specialist_mapping = {
    "Cardiology": "Cardiologist",
    "Neurology": "Neurologist",
    "Gastroenterology": "Gastroenterologist",
    "Respiratory": "Pulmonologist",
    "Dermatology": "Dermatologist",
    "Orthopedics": "Orthopedic Surgeon",
    "Endocrinology": "Endocrinologist",
    "Hematology": "Hematologist",
    "Oncology": "Oncologist",
    "Psychiatry": "Psychiatrist",
    "Infectious Disease": "Infectious Disease Specialist",
    "Allergy": "Allergist",
    "Urology": "Urologist",
    "Gynecology": "Gynecologist",
    "Ophthalmology": "Ophthalmologist",
    "Rheumatology": "Rheumatologist",
    "Nephrology": "Nephrologist",
    "Pediatrics": "Pediatrician",
    "ENT": "ENT Specialist"
}

# Basic conversation handling (add more phrases as needed)
greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
farewells = ["bye", "goodbye", "see you", "take care"]
general_conversation = {
    "how are you": "I'm a bot, but I'm doing well! How about you?",
    "what's your name": "I'm your health diagnosis assistant.",
    "thank you": "You're welcome! I'm here to help."
}

# Function to process user symptoms and handle normal conversations
def process_symptoms(user_input):
    user_input_lower = user_input.lower()  # Convert input to lowercase
    doc = nlp(user_input_lower)  # Process the input using NLP
    extracted_symptoms = [token.text for token in doc if token.is_alpha]  # Extract only words

    # Check for greetings or farewells
    if any(greeting in user_input_lower for greeting in greetings):
        return "Hello! How can I assist you today?"
    elif any(farewell in user_input_lower for farewell in farewells):
        return "Goodbye! Take care and stay healthy!"
    
    # Handle general conversations
    for phrase, response in general_conversation.items():
        if phrase in user_input_lower:
            return response
    
    # Medical diagnosis if no normal conversation is detected
    potential_diagnoses = []
    
    # Iterate over each medical field and check for matching symptoms
    for _, row in medical_data.iterrows():
        symptoms = row['Symptoms'].lower().split(', ')  # Get symptoms for this medical field
        matched_symptoms = [symptom for symptom in extracted_symptoms if symptom in symptoms]
        
        # If we find any matching symptoms, append the diagnosis to the result
        if matched_symptoms:
            potential_diagnoses.append({
                "field": row['Field'],
                "matched_symptoms": matched_symptoms,
                "conditions": row['Conditions'].split(', ')
            })
    
    # If no matching symptoms are found
    if not potential_diagnoses:
        return "Sorry, I couldn't match your symptoms to any known medical conditions."
    
    # Generate a response for medical diagnosis
    response = "Based on your symptoms, you may have the following conditions:\n"
    for diagnosis in potential_diagnoses:
        response += f"\nMedical Field: {diagnosis['field']}"
        response += f"\nMatched Symptoms: {', '.join(diagnosis['matched_symptoms'])}"
        response += f"\nPotential Conditions: {', '.join(diagnosis['conditions'])}\n"
        
        # Add doctor recommendation based on the medical field
        specialist = specialist_mapping.get(diagnosis['field'], "General Practitioner")
        response += f"Recommended Doctor: {specialist}\n"
    
    return response

# Function to handle the "Send" button click (simulate chat)
def diagnose():
    user_input = symptom_input.get("1.0", tk.END).strip()
    if user_input:
        # Display the user's input in the chat window
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + "\n\n")
        
        diagnosis = process_symptoms(user_input)
        
        # Display the bot's response in the chat window
        chat_window.insert(tk.END, "Bot: " + diagnosis + "\n\n")
        chat_window.config(state=tk.DISABLED)
        
        # Clear the text input after the message is sent
        symptom_input.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter your symptoms.")

# Create the main application window
app = tk.Tk()
app.title("Health Diagnosis Chatbot")
app.geometry("600x800")  # Adjust window size for laptop/chat-like app

# Set background and text colors
app.configure(bg="#f0f4f7")

# Create a frame for the chat window
chat_frame = tk.Frame(app, bg="#e0e0e0")
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a scrolled text widget for chat history
chat_window = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, bg="#ffffff", fg="#333333", font=("Arial", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_window.config(state=tk.DISABLED)  # Make chat window read-only

# Create a frame for the input box and button
input_frame = tk.Frame(app, bg="#f0f4f7")
input_frame.pack(fill=tk.X, padx=10, pady=5)

# Create a scrolled text widget for user input
symptom_input = tk.Text(input_frame, height=3, bg="#ffffff", fg="#333333", font=("Arial", 12), wrap=tk.WORD)
symptom_input.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5, expand=True)

# Create a send button to simulate sending messages in chat
send_button = tk.Button(input_frame, text="Send", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=diagnose)
send_button.pack(side=tk.RIGHT, padx=10)

# Start the GUI event loop
app.mainloop()
