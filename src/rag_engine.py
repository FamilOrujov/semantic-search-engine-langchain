import os
import docx2txt
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

class RAGEngine:
    def __init__(self, persist_directory="./chroma/db", embedding_model_name="mxbai-embed-large", llm_model_name="gemma3:4b"):
        self.persist_directory = os.path.abspath(persist_directory)
        
        try:
            self.embedding_model = OllamaEmbeddings(model=embedding_model_name)
            self.llm = ChatOllama(model=llm_model_name)
        except Exception as e:
            raise RuntimeError(
                f"Failed to connect to Ollama. Make sure Ollama is running and models are installed:\n"
                f"  ollama pull {embedding_model_name}\n"
                f"  ollama pull {llm_model_name}\n"
                f"Original error: {e}"
            )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=75,
            add_start_index=True
        )
        
        self.vector_store = Chroma(
            collection_name="my_docs",
            embedding_function=self.embedding_model,
            persist_directory=self.persist_directory
        )
        
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

    def _clean_text(self, text):
        if not text: return text
        parts = text.split()
        if not parts: return text
        single_chars = sum(1 for p in parts if len(p) == 1)
        ratio = single_chars / len(parts)
        if ratio > 0.4:
            cleaned = text.replace("  ", " %TEMP% ").replace(" ", "").replace("%TEMP%", " ")
            return cleaned
        return text

    def process_files(self, file_paths):
        all_docs = []
        for file_path in file_paths:
            ext = os.path.splitext(file_path)[1].lower()
            docs = []
            try:
                if ext == ".pdf":
                    loader = PDFPlumberLoader(file_path)
                    docs = loader.load()
                elif ext == ".txt":
                    loader = TextLoader(file_path)
                    docs = loader.load()
                elif ext == ".docx":
                    text = docx2txt.process(file_path)
                    docs = [Document(page_content=text, metadata={"source": file_path})]
                else:
                    continue
                
                for doc in docs:
                    doc.page_content = self._clean_text(doc.page_content)
                all_docs.extend(docs)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

        if not all_docs:
            return 0

        chunks = self.text_splitter.split_documents(all_docs)
        if chunks:
            self.vector_store.add_documents(documents=chunks)
        return len(chunks)

    def answer_question(self, question):
        docs_retrieved = self.retriever.invoke(question)
        
        if not docs_retrieved:
            return iter([type('obj', (object,), {'content': "I don't have any documents to search. Please upload some files first."})()])

        context_str = "\n\n---\n\n".join([d.page_content for d in docs_retrieved])
        
        system_prompt = """Answer the question using ONLY the context below. If the answer is not in the context, say "I don't have enough information in the documents."

Context:
{context}"""
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}")
        ])
        
        final_prompt = prompt_template.invoke({
            "question": question,
            "context": context_str
        })
        
        return self.llm.stream(final_prompt)

    def reset_database(self):
        import shutil
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        self.vector_store = Chroma(
            collection_name="my_docs",
            embedding_function=self.embedding_model,
            persist_directory=self.persist_directory
        )
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

    def get_document_count(self):
        try:
            data = self.vector_store.get()
            return len(data['ids'])
        except:
            return 0
