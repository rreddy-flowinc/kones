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

first_half = contents[0:(len(contents) // 2)]
second_half = contents[(len(contents) // 2):]


def assess_bucket_size(input):
    GPT_TOTAL_WORD_COUNT = 500
    words = len(input.strip().split(" "))
    return words // (GPT_TOTAL_WORD_COUNT + 1)


def convert_chunk_to_user_input(chunk):
    dictionary = {"role": "user"}
    dictionary["content"] = f"Answer the following question based on this continuation of input content: \n\n{chunk} \n\n"
    return dictionary

def convert_chunk_to_question(chunk, question):
    dictionary = {"role": "user"}
    dictionary["content"] = f"Answer the following question based on this final input content: \n\n{chunk} \n\n, Please return the output in JSON:\n\nQuestion: {question} \n "
    return dictionary

def chunk_text(text):
    """
    Splits the given text into 83 evenly chunked parts.

    Args:
        text (str): The text to split.

    Returns:
        list: A list of strings representing the 83 chunks of text.
    """

    bucket_size = assess_bucket_size(text)
    # Calculate the length of each chunk.
    chunk_size = len(text) // bucket_size

    # Split the text into chunks of the calculated size.
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # If there are any leftover characters, add them to the last chunk.
    if len(chunks) > bucket_size:
        chunks[bucket_size - 1] += chunks[bucket_size]
        chunks = chunks[:bucket_size]

    input_prompts = [convert_chunk_to_user_input(c) for c in chunks[0:-1]]
    last_prompt = convert_chunk_to_question(chunks[-1], "What is the GROSS PROFIT for the year? Please respond in JSON format")

    return (input_prompts + [last_prompt])



print(chunk_text(contents))

# pdb.set_trace()


# def create_chunks():
#
# #     create input / tokenlimit+1 dicts with role user, content, push into array.
# # iterate through the
#


def ask_question2(all_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chunk_text(all_text)
    )
    return response.choices[0].message.content.strip()


json_formatted1 = ask_question2(contents)
pdb.set_trace()
json_formatted = ask_question2("What is the current commitment", contents)
instructions = json.loads(json_formatted)

ask_question2("Give me the current total capital calls", "", contents)

{'Wire Transfer Information': {'Amount Due': '$145,010.00', 'Bank Name': 'First Republic Bank',
                               'Account Name': 'Buiet Venture II LP', 'ABA Routing Number': '432-010-312',
                               'SWIFT Code': '', 'Account Number': '312391293912', 'Ref/OBI': 'CC - Adrian Bortiz',
                               'Due Date': 'September 1, 2021'}}
{'Amount Due': '$145,010.00', 'Bank Name': 'First Republic Bank', 'Account Name': 'Buiet Venture II LP',
 'ABA Routing Number': '432-010-312', 'SWIFT Code': None, 'Account Number': '312391293912',
 'Ref/OBI': 'CC - Adrian Bortiz', 'Due Date': 'September 1, 2021'}
{'Wire Transfer Information': {'Amount Due': '$145,010.00', 'Bank Name': 'First Republic Bank',
                               'Account Name': 'Buiet Venture II LP', 'ABA Routing Number': '432-010-312',
                               'SWIFT Code': None, 'Account Number': '312391293912', 'Ref/OBI': 'CC - Adrian Bortiz',
                               'Due Date': 'September 1, 2021'}}
{'Amount Due': '$145,010.00', 'Bank Name': 'First Republic Bank', 'Account Name': 'Buiet Venture II LP',
 'ABA Routing Number': '432-010-312', 'SWIFT Code': '', 'Account Number': '312391293912',
 'Ref/OBI': 'CC - Adrian Bortiz', 'Due Date': 'September 1, 2021'}
{'Wire Transfer Information': {'Amount Due': '$145,010.00', 'Bank Name': 'First Republic Bank',
                               'Account Name': 'Buiet Venture II LP', 'ABA Routing Number': '432-010-312',
                               'SWIFT Code': None, 'Account Number': '312391293912', 'Ref/OBI': 'CC - Adrian Bortiz',
                               'Due Date': 'September 1, 2021'}}
# reply_content = completion.choices[0].message.content
pdb.set_trace();
