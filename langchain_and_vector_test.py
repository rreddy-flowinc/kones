import pdb
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

reader = PdfReader('./source_pdf/ms10k.pdf')


raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text


text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)


embeddings = OpenAIEmbeddings()

docsearch = Milvus.from_texts(texts, embeddings)

docsearch

chain = load_qa_chain(OpenAI(), chain_type="stuff")
query = "what is microsoft's total revenue?"
docs = docsearch.similarity_search(query)


print(chain.run(input_documents=docs, question=query))


# query = "What was the cost of training the GPT4all model?"
# docs = docsearch.similarity_search(query)
# chain.run(input_documents=docs, question=query)
