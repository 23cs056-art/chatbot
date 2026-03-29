from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Chatbot is running"
from groq import Groq
import re

app = Flask(__name__)

GROQ_API_KEY = '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'
client = Groq(api_key=GROQ_API_KEY)

with open("knowledge.txt", 'r', encoding='utf-8') as file:
    knowledge = file.read()

# Extract keywords from knowledge base for validation
KNOWLEDGE_KEYWORDS = {
    'normalization', 'redundancy', 'integrity', 'anomaly', 'anomalies',
    'normal form', '1nf', '2nf', '3nf', 'bcnf', 'denormalization',
    'relation', 'attribute', 'tuple', 'domain', 'primary key', 'candidate key',
    'super key', 'composite key', 'foreign key', 'database', 'table',
    'column', 'row', 'insertion', 'deletion', 'update', 'functional dependency',
    'transitive', 'partial', 'duplicate', 'data'
}


@app.route('/')
def home():
    return render_template('index.html')

def is_question_related_to_knowledge(question):
    """
    Check if the user's question is related to the knowledge base.
    Returns True if question contains relevant keywords, False otherwise.
    """
    question_lower = question.lower()
    
    # Check if question contains any knowledge-related keywords
    for keyword in KNOWLEDGE_KEYWORDS:
        if keyword in question_lower:
            return True
    
    return False

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if user_message.lower() in ['hi', 'hello', 'hey']:
        return jsonify({'response': 'Hello! I am an NormaBot chatbot 🤖 I can help you understand Database Normalization concepts!'})

    # Check if question is related to knowledge base
    if not is_question_related_to_knowledge(user_message):
        return jsonify({'response': 'Sorry, I can only answer questions related to Database Normalization. Please ask me about normalization concepts, normal forms, database design, or related topics!'})
    
    completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
    "role": "user",
    "content": f"""
You are a helpful AI tutor chatbot.

Your job is to give SHORT and INTERACTIVE answers.

RULES:
- Remember you will not answer anything which is not in the knowledge base{knowledge}.
- Do NOT give long paragraphs
- Give only basic explanation first
- Keep answer within 4-6 lines
- Always include 2-3 simple examples
- After answering, suggest next options to explore

FORMAT:
1. Definition (short)
2. Examples (bullet points)
3. Ask user what they want next (like types, applications, advantages, etc.) (bullet points)

Knowledge:
{knowledge}

Question: {user_message}

If answer not found, say: Sorry, I don't know the answer for this question.
"""
}],

 )
    
    bot_reply = completion.choices[0].message.content.strip()

    return jsonify({'response': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
