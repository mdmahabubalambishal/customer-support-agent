import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader


def setup_vectorstore():
    # সব .txt files load করো data/ folder থেকে
    loader = DirectoryLoader(
        "data/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"📄 {len(documents)} files loaded")

    # Chunk করো
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["---", "\n\n", "\n", " "]
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ {len(chunks)} chunks created")

    # Multilingual embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # ChromaDB তে store করো
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print(f"✅ VectorStore ready with {len(chunks)} chunks!")
    return vectorstore


def update_vectorstore(new_file_path: str):
    """নতুন knowledge file যোগ করলে এটা call করো"""
    loader = TextLoader(new_file_path, encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    vectorstore.add_documents(chunks)
    print(f"✅ {len(chunks)} new chunks added!")


if __name__ == "__main__":
    # chroma_db না থাকলে নতুন বানাও
    if os.path.exists("./chroma_db"):
        print("⚠️ chroma_db already exists. Delete it first to rebuild.")
    else:
        setup_vectorstore()