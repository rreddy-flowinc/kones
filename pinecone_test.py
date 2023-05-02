import pdb
from PyPDF2 import PdfReader
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings, SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone

from dotenv import load_dotenv


from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
load_dotenv()

import pinecone
import os

# initialize pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)


index_name = "langchain-demo"
# pinecone.create_index(index_name, dimension=1536,
#                           metric="cosine", pods=1, pod_type="p1.x1")

from langchain.document_loaders import PyPDFLoader
import pdfplumber
#

PINECONE_API_KEY="a62035e1-b729-47c4-b933-fd8a40d22831"
PINECONE_ENV="us-west1-gcp-free"

# from pymilvus import Milvus as pm
#
# host = '127.0.0.1'
# port = '19530'
# client = pm(host, port)
# client.drop_collection('LangChainCollection')
# pdb.set_trace()

reader = PdfReader('./source_pdf/ms10k.pdf')
# reader = pdfplumber.open('./source_pdf/ms10k.pdf')

raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text
# reader.close()


text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

# build semantic index of documents
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_texts(texts, embeddings, index_name=index_name)

docsearch

chain = load_qa_chain(ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), chain_type="stuff")
def generate_answer(chain, query):
    docs = docsearch.similarity_search(query)
    return chain.run(input_documents=docs, question=query)

print(generate_answer(chain, query="what is microsoft's total revenue?"))
print(generate_answer(chain, query="What was microsoft's gross profit?"))
print(generate_answer(chain, query="Who is the CEO or Chief Executive Officer?"))
print(generate_answer(chain, query="What is Microsoft's net profit margin? Net profit divided by total revenue."))
