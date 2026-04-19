from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

DOCS_DIR = "docs"
CHROMA_DIR = "chroma_db"

def build_vectorstore():
    """Belgeleri okur, chunk'lar ve ChromaDB'ye kaydeder."""
    print("Belgeler yükleniyor...")
    loader = DirectoryLoader(
        DOCS_DIR,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"{len(documents)} belge yüklendi.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"{len(chunks)} chunk oluşturuldu.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print("ChromaDB oluşturuldu!")
    return vectorstore

def get_vectorstore():
    """Mevcut ChromaDB'yi yükler, yoksa oluşturur."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    if os.path.exists(CHROMA_DIR):
        return Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )
    else:
        return build_vectorstore()

def get_context(query: str, k: int = 3) -> str:
    """Sorguya en yakın belge parçalarını döndürür."""
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    return context


if __name__ == "__main__":
    build_vectorstore()
    print("\nTest sorgusu yapılıyor...")
    context = get_context("leaving home and feeling lost")
    print("Bulunan context:")
    print(context)