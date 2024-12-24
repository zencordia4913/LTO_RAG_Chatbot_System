import os
import fitz  # PyMuPDF
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
import gradio as gr

# Path to the dataset folder
DATASET_PATH = r"C:\Users\LEGION\Desktop\Project\AI351\PROJECT\Dataset"

# Chunking parameters
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split text into chunks with specified chunk size and overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks


def extract_text_from_pdfs(folder_path):
    texts = []
    metadata = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                folder_name = os.path.basename(root)
                print(f"Extracting text from {pdf_path}...")

                doc = fitz.open(pdf_path)
                for page_num, page in enumerate(doc, start=1):
                    text = page.get_text()
                    if text.strip():
                        chunks = chunk_text(text)
                        for chunk in chunks:
                            texts.append(chunk)
                            metadata.append(
                                {
                                    "source": pdf_path,
                                    "folder": folder_name,
                                    "title": file,
                                    "page": page_num,
                                }
                            )
    return texts, metadata


# Initialize the system
print("Initializing the RAG system...")
documents, metadatas = extract_text_from_pdfs(DATASET_PATH)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(documents, embeddings, metadatas=metadatas)
llm = Ollama(model="llama3.2")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
)


def rag_query(query):
    """Function to process the query and return the answer with references."""
    try:
        result = qa.invoke({"query": query})
        answer = result["result"]
        source_documents = result["source_documents"]

        # Format the references
        references = []
        for i, doc in enumerate(source_documents, start=1):
            metadata = doc.metadata
            source_info = f"Source {i}: {metadata['title']} (Page {metadata['page']}, Folder: {metadata['folder']})"
            references.append(source_info)

        return answer, "\n".join(references)
    except Exception as e:
        return str(e), ""


# Gradio Interface
iface = gr.Interface(
    fn=rag_query,
    inputs=gr.Textbox(label="Enter your query"),
    outputs=[gr.Textbox(label="Answer"), gr.Textbox(label="References")],
    title="RAG System with LLaMA 3.2",
    description="Ask questions and get answers with references based on PDF documents.",
)

if __name__ == "__main__":
    iface.launch()
