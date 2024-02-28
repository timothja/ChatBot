import os
import openai

from flask import Flask, request
from flask import render_template
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
app = Flask(__name__)


openai.api_key = API_KEY

user_messages = []
bot_messages = []

# ############ lorem ipsum ############

# import lorem

# for i in range(0, 10):
#     user_messages.append(lorem.paragraph())
#     bot_messages.append(lorem.paragraph())

# ############ lorem ipsum ############

    
def chatcompletion(user_input, chat_history):
    client = openai.OpenAI(
        api_key=API_KEY,
    )

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        messages = [
            {"role": "system", "content": f"You are a helpful and enthusiastic ChatBot. Do not hesitate to ask questions if you require more information. Here is the chat history: {chat_history}"},
            {"role": "user", "content": f"{user_input}"},
        ]
    )

    chatgpt_output = chat_completion.choices[0].message.content

    return chatgpt_output



@app.route("/", methods=['GET', 'POST'])
def home():
    global user_messages
    global bot_messages

    if request.method == 'POST':
        button_text = request.form.get('button_text')
        text_input = request.form.get('text_input')
        chat_history = request.form.get('history')
        user_input = request.form.get('text_input')

        if button_text == 'clear':
            chat_history = ''
            chat_history_html_formatted = ''
            user_messages = []
            bot_messages = []

        elif button_text == 'submit':
            if text_input == '':
                chat_history_html_formatted = chat_history.replace('\n', '<br>')
                return render_template("index.html", chat_history=chat_history, chat_history_html_formatted=chat_history_html_formatted, user_messages=user_messages, bot_messages=bot_messages)

            chatgpt_output = chatcompletion(user_input, chat_history)

            chat_history += f'User: {text_input}\n'
            chat_history += f'\nAssistant: {chatgpt_output}\n'
            
            user_messages.append(text_input)
            bot_messages.append(chatgpt_output)

            # print(user_messages)
            # print(bot_messages)
            
            chat_history_html_formatted = chat_history.replace('\n', '<br>')

        return render_template("index.html", chat_history=chat_history, chat_history_html_formatted=chat_history_html_formatted, user_messages=user_messages, bot_messages=bot_messages)

    else:    
        chat_history = ''
        chat_history_html_formatted = ''

        return render_template("index.html", chat_history=chat_history, chat_history_html_formatted=chat_history_html_formatted, user_messages=user_messages, bot_messages=bot_messages)



if __name__ == "__main__":
    app.run(debug=True)

