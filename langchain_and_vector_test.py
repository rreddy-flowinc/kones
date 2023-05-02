import pdb
from PyPDF2 import PdfReader
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

from langchain.document_loaders import PyPDFLoader
import pdfplumber
#

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
    chunk_size = 2000,
    chunk_overlap  = 300,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)




# build semantic index of documents
embeddings = OpenAIEmbeddings()
docsearch = Milvus.from_texts(texts, embeddings)

docsearch

chain = load_qa_chain(OpenAI(model_name="gpt-3.5-turbo", temperature=0.1), chain_type="stuff")
query = "what is microsoft's total revenue?"
docs = docsearch.similarity_search(query)


print(chain.run(input_documents=docs, question=query))


query = "What was microsoft's gross profit?"
docs = docsearch.similarity_search(query)
print(chain.run(input_documents=docs, question=query))


query = "Who is the CEO or Chief Executive Officer?"
docs = docsearch.similarity_search(query)
print(chain.run(input_documents=docs, question=query))



query = "What is Microsoft's net profit margin? Net profit divided by total revenue."
docs = docsearch.similarity_search(query)
print(chain.run(input_documents=docs, question=query))