from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_answer(context, question, history):
    history_text = ""

    for message in history:
        history_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
        Use ONLY the provided context to answer the question.

        If the answer is not in the context, say:
        "I could not find that information in the uploaded PDF."

        Conversation History:
        {history_text}

        Context:
        {context}

        Question:
        {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text