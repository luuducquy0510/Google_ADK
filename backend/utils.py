from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.text_splitter import TokenTextSplitter
import tempfile

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from langchain.schema import Document



def clean_metadata_keys(doc: Document):
    new_metadata = {}
    for k, v in doc.metadata.items():
        # Keep only clean keys
        if "." in k or not k.replace("_", "").isalnum():
            k = k.replace(".", "_")
        new_metadata[k] = v
    return Document(page_content=doc.page_content, metadata=new_metadata)

# Function to extract chunks from PDF
def extract_chunks_from_pdf(file_bytes) -> list[Document]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    pages = loader.load()

    splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(pages)
    cleaned_chunks = [clean_metadata_keys(doc) for doc in chunks]
    return cleaned_chunks

# Function to insert chunks into Milvus
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def insert_chunks_into_milvus(docs):
    vector_store = Milvus(
        embedding_function=embedding_model,
        connection_args={"host": "localhost", "port": "19530"},
        collection_name="pdf_documents",
        auto_id=True
    )
    vector_store.add_documents(docs)


