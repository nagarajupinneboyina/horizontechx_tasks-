import tkinter as tk
from tkinter import scrolledtext
import re
import nltk

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------------------------
# Download NLTK stopwords
# -------------------------------------------------
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


# -------------------------------------------------
# FAQ Data
# Topic: Python Programming
# -------------------------------------------------
faqs = [
    {
        "question": "What is Python?",
        "answer": "Python is a high-level, interpreted programming language known for its simple and readable syntax."
    },
    {
        "question": "How do I install Python?",
        "answer": "You can download Python from the official Python website and install it on your computer."
    },
    {
        "question": "What is a variable in Python?",
        "answer": "A variable is a name used to store a value in Python. Example: age = 20."
    },
    {
        "question": "What are Python data types?",
        "answer": "Common Python data types include int, float, string, boolean, list, tuple, set, dictionary, and complex."
    },
    {
        "question": "What is a list in Python?",
        "answer": "A list is an ordered and mutable collection of elements. Example: numbers = [1, 2, 3]."
    },
    {
        "question": "What is a tuple in Python?",
        "answer": "A tuple is an ordered collection that cannot be changed after it is created. Example: numbers = (1, 2, 3)."
    },
    {
        "question": "What is a dictionary in Python?",
        "answer": "A dictionary stores data as key-value pairs. Example: student = {'name': 'John', 'age': 20}."
    },
    {
        "question": "What is a set in Python?",
        "answer": "A set is an unordered collection of unique elements. Example: numbers = {1, 2, 3}."
    },
    {
        "question": "What is a function in Python?",
        "answer": "A function is a reusable block of code designed to perform a particular task."
    },
    {
        "question": "How do I create a function in Python?",
        "answer": "Use the def keyword. Example: def greet(): print('Hello')."
    },
    {
        "question": "What is a loop in Python?",
        "answer": "A loop is used to repeatedly execute a block of code. Python provides for and while loops."
    },
    {
        "question": "What is an if statement?",
        "answer": "An if statement is used to execute code when a specified condition is true."
    },
    {
        "question": "What is the difference between list and tuple?",
        "answer": "A list is mutable, meaning it can be changed. A tuple is immutable, meaning it cannot be changed after creation."
    },
    {
        "question": "What is the len function?",
        "answer": "The len() function returns the number of items or characters in an object."
    },
    {
        "question": "What is the print function?",
        "answer": "The print() function displays output on the screen."
    },
    {
        "question": "How do I take input in Python?",
        "answer": "Use the input() function. Example: name = input('Enter your name: ')."
    },
    {
        "question": "What is Python used for?",
        "answer": "Python is used for web development, data science, artificial intelligence, machine learning, automation, and software development."
    },
    {
        "question": "Is Python easy to learn?",
        "answer": "Yes. Python is considered beginner-friendly because it has simple and readable syntax."
    },
    {
        "question": "What is indentation in Python?",
        "answer": "Indentation is the whitespace at the beginning of a line. Python uses indentation to define blocks of code."
    },
    {
        "question": "What is an exception in Python?",
        "answer": "An exception is an error that occurs during program execution. Exceptions can be handled using try and except."
    }
]


# -------------------------------------------------
# Text Preprocessing
# -------------------------------------------------
def preprocess_text(text):
    """
    Convert text to lowercase, remove punctuation,
    remove stopwords, and return cleaned text.
    """

    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Split into words
    words = text.split()

    # Remove stopwords
    words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(words)


# -------------------------------------------------
# Prepare FAQ Questions
# -------------------------------------------------
questions = [
    faq["question"]
    for faq in faqs
]

processed_questions = [
    preprocess_text(question)
    for question in questions
]


# -------------------------------------------------
# TF-IDF Vectorizer
# -------------------------------------------------
vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(processed_questions)


# -------------------------------------------------
# Find Best FAQ
# -------------------------------------------------
def get_answer(user_question):
    """
    Find the most relevant FAQ using cosine similarity.
    """

    cleaned_question = preprocess_text(user_question)

    # Convert user question into TF-IDF vector
    user_vector = vectorizer.transform([cleaned_question])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        user_vector,
        faq_vectors
    )

    # Find highest similarity score
    best_match_index = similarity_scores.argmax()

    best_score = similarity_scores[0][best_match_index]

    # Minimum confidence threshold
    threshold = 0.20

    if best_score >= threshold:
        return faqs[best_match_index]["answer"]

    return (
        "Sorry, I could not find a suitable answer to your question. "
        "Please try asking about Python programming, variables, "
        "lists, tuples, dictionaries, functions, loops, or data types."
    )


# -------------------------------------------------
# Chatbot GUI
# -------------------------------------------------
def send_message():
    user_question = user_input.get().strip()

    if user_question == "":
        return

    # Display user message
    chat_area.config(state=tk.NORMAL)

    chat_area.insert(
        tk.END,
        "You: " + user_question + "\n"
    )

    # Get chatbot response
    answer = get_answer(user_question)

    # Display chatbot response
    chat_area.insert(
        tk.END,
        "Bot: " + answer + "\n\n"
    )

    chat_area.config(state=tk.DISABLED)

    # Clear input box
    user_input.delete(0, tk.END)

    # Scroll to bottom
    chat_area.see(tk.END)


# -------------------------------------------------
# Allow Enter Key to Send Message
# -------------------------------------------------
def enter_pressed(event):
    send_message()


# -------------------------------------------------
# Create Main Window
# -------------------------------------------------
root = tk.Tk()

root.title("AI-Based FAQ Chatbot")
root.geometry("700x600")
root.resizable(False, False)


# -------------------------------------------------
# Title
# -------------------------------------------------
title_label = tk.Label(
    root,
    text="AI-Based FAQ Chatbot",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=10)


# -------------------------------------------------
# Subtitle
# -------------------------------------------------
subtitle_label = tk.Label(
    root,
    text="Ask questions about Python programming",
    font=("Arial", 11)
)

subtitle_label.pack(pady=5)


# -------------------------------------------------
# Chat Display Area
# -------------------------------------------------
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=75,
    height=25,
    font=("Arial", 11)
)

chat_area.pack(padx=15, pady=10)

chat_area.config(state=tk.NORMAL)

chat_area.insert(
    tk.END,
    "Bot: Hello! Welcome to the Python FAQ Chatbot.\n"
)

chat_area.insert(
    tk.END,
    "Bot: Ask me a question about Python.\n\n"
)

chat_area.config(state=tk.DISABLED)


# -------------------------------------------------
# Input Frame
# -------------------------------------------------
input_frame = tk.Frame(root)

input_frame.pack(pady=10)


# -------------------------------------------------
# User Input
# -------------------------------------------------
user_input = tk.Entry(
    input_frame,
    width=55,
    font=("Arial", 12)
)

user_input.grid(
    row=0,
    column=0,
    padx=5
)


# -------------------------------------------------
# Send Button
# -------------------------------------------------
send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    command=send_message,
    width=10
)

send_button.grid(
    row=0,
    column=1,
    padx=5
)


# -------------------------------------------------
# Enter Key Binding
# -------------------------------------------------
user_input.bind(
    "<Return>",
    enter_pressed
)


# -------------------------------------------------
# Start Application
# -------------------------------------------------
root.mainloop()