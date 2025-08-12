import os, glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

KB_DIR = "data"
INDEX_DIR = "kb_index"

def _load_docs():
    docs = []
    pdfs = glob.glob(os.path.join(KB_DIR, "*.pdf"))
    mds  = glob.glob(os.path.join(KB_DIR, "*.md"))
    for p in pdfs:
        docs.extend(PyPDFLoader(p).load())
    for m in mds:
        docs.extend(TextLoader(m, encoding="utf-8").load())
    return docs

def _ensure_index():
    if not os.path.isdir(INDEX_DIR) or not os.listdir(INDEX_DIR):
        docs = _load_docs()
        if not docs:
            print("Warning: No documents found in data/ directory")
            return
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
        chunks = splitter.split_documents(docs)
        vs = FAISS.from_documents(chunks, OpenAIEmbeddings())
        os.makedirs(INDEX_DIR, exist_ok=True)
        vs.save_local(INDEX_DIR)

def _load_index():
    return FAISS.load_local(INDEX_DIR, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

def ingest_faq_node(state):
    print(f"\n=== ingest_faq_node ===")
    print(f"Input state keys: {list(state.keys())}")
    
    # This node only adds the retriever. It doesn't need to modify other state.
    try:
        _ensure_index()
        vs = _load_index()
        retriever = vs.as_retriever(search_kwargs={"k": 4})
        print("Successfully created FAQ retriever.")
        return {"faq_retriever": retriever}
    except Exception as e:
        print(f"Error loading FAQ index: {str(e)}")
        return {"faq_retriever": None}
