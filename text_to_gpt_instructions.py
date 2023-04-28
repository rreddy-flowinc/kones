import os
import openai
import pdb
from dotenv import load_dotenv

from pathlib import Path
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


current_directory = Path.cwd()
input_text_path = current_directory / Path(f"source_text/output.txt")

contents = None
with open(input_text_path) as f:
    contents = f.read()


def ask_question(question, inputtext):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Answer the following question based on these texts:\n\n{inputtext}\n\nQuestion: {question} \n ",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text.strip()


def ask_question2(question, inputtext):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": f"Answer the following question based on this input content: \n\n{inputtext} \n\n, Please return the output in JSON:\n\nQuestion: {question} \n "}
        ]
    )
    return response.choices[0].message.content.strip()


json_formatted = ask_question2("What are the wire instructions in this document", contents)
instructions = json.loads(json_formatted)

# {'Wire Transfer Information': {'Amount Due': '$145,010.00', 'Bank Name': 'First Republic Bank', 'Account Name': 'Buiet Venture II LP', 'ABA Routing Number': '432-010-312', 'SWIFT Code': '', 'Account Number': '312391293912', 'Ref/OBI': 'CC - Adrian Bortiz', 'Due Date': 'September 1, 2021'}}

# reply_content = completion.choices[0].message.content
pdb.set_trace();

