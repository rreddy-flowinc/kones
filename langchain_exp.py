import os
import json
import pandas as pd
import langchain
import pypdf

from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from pydantic import BaseModel, Field, validator
from typing import List
from io import StringIO

import multiprocessing
multiprocessing.set_start_method('fork')



loader = PyPDFLoader("./source_pdf/ms10k.pdf")
pages = loader.load_and_split()

print(pages[0].page_content)


def extract_fields(page):
    template = """
    You are a legal analyst who is knowledgeable about contracts generally, but specifically in financial
    contracts related to investment fund subscription.

    Given a page of an unfilled fund subscription document, extract the following data for each field:

    name: The name of the field, 
    field_type: The field type, such as "text" or "checkbox", 
    description: A description of what is meant to be filled in the field

    Page: 

    {page}

    Respond as a list of JSON objects parsable by Python json.loads

    """
    
    llm = ChatOpenAI(temperature=0, request_timeout=300, max_retries=10)

    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(template)
        ],
        input_variables=["page"]
    )

    model_input = prompt.format_prompt(page=page)

    model_output = llm(model_input.to_messages()).content
    return json.loads(model_output)


page_contents = [page.page_content for page in pages]

pool = multiprocessing.Pool()
field_extractions = pool.map(extract_fields, page_contents)
field_extractions = [i for field_list in field_extractions for i in field_list]


with open('ilpa_extractions.json', 'w') as outfile:
    json.dump(field_extractions, outfile)