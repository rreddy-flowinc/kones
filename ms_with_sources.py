import pdb
from PyPDF2 import PdfReader
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings, SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus

from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from langchain.chat_models import ChatOpenAI

from pymilvus import Collection, utility, connections
# Get an existing collection.


from langchain.document_loaders import PyPDFLoader
import pdfplumber
#
#
# from pymilvus import Milvus as pm
#
# host = '127.0.0.1'
# port = '19530'
# client = pm(host, port)
# client.drop_collection('LangChainCollection')
#
#
# connections.connect(
#   alias="default",
#   host='localhost',
#   port='19530'
# )
#
# collection = Collection("book")
# collection.create_index(
#   field_name="book_intro",
#   index_params=index_params
# )
#
# pdb.set_trace()
#
# utility.index_building_progress("book")
index_params = {
  "metric_type":"IP",
  "index_type":"IVF_FLAT",
  "params":{"nlist":1024}
}

pdf_name = "ms10k.pdf"
reader = PdfReader(f"./source_pdf/{pdf_name}")
# reader = pdfplumber.open('./source_pdf/ms10k.pdf')
#
# raw_text = ''
# for i, page in enumerate(reader.pages):
#     text = page.extract_text()
#     if text:
#         raw_text += text
# reader.close()


text_splitter = CharacterTextSplitter(chunk_size=2000, separator="\n", chunk_overlap =200, length_function=len)
docs, metadatas = [], []
for i, page in enumerate(reader.pages):
    splits = text_splitter.split_text(page.extract_text())
    docs.extend(splits)
    metadatas.extend([{"source": f"{pdf_name}-page-${i}"}] * len(splits))
    # print(f"Split {page['source']} into {len(splits)} chunks")

#
# text_splitter = CharacterTextSplitter(
#     separator = "\n",
#     chunk_size = 1000,
#     chunk_overlap  = 100,
#     length_function = len,
# )
# texts = text_splitter.split_text(raw_text)

# build semantic index of documents
embeddings = OpenAIEmbeddings()
docsearch = Milvus.from_texts(docs, embeddings, collection_name="TestCollection", index_params=index_params, metadatas=metadatas)

docsearch

chain = load_qa_with_sources_chain(ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), chain_type="stuff")
def generate_answer(chain, query):
    docs = docsearch.similarity_search(query)
    return chain.run(input_documents=docs, question=query)

print(generate_answer(chain, query="what is microsoft's total revenue?"))
print(generate_answer(chain, query="What was microsoft's gross profit?"))
print(generate_answer(chain, query="Who is the CEO or Chief Executive Officer?"))
print(generate_answer(chain, query="What is Microsoft's net profit margin? Net profit margin is net profit divided by total revenue."))
