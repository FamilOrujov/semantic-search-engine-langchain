import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import OllamaEmbeddings 
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate



st.title("Semantic Search Engine")
st.header("Upload a file to get started", divider="green")

# text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)

# Embedding model
embedding_model = OllamaEmbeddings(model="mxbai-embed-large")

# If you want to use OpenAI embeddings
#embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Vector Store
vector_store = Chroma(
    collection_name="my_docs",
    embedding_function=embedding_model,
    persist_directory="./chroma/db"
)

# LLM Model
llm = ChatOllama(model="gemma3:1b")

# If you want to use OpenAI LLM (always use gpt-4.1-nano for faster and cheaper )
#llm = ChatOpenAI(model="gpt-4.1-nano")


uploaded_file = st.file_uploader("Select a file:")


if uploaded_file is not None:
    with st.spinner("Processing file..."):
        try:
            print("FIle info: ", uploaded_file)

            # save the file in memory
            temp_file_path = uploaded_file.name

            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

                
            # PDF file loader
            loader = PyPDFLoader(temp_file_path)
            docs = loader.load()
            #print("Docs: ",docs)

            # create chunks
            chunks = text_splitter.split_documents(docs)
            print("Chunks created: ", len(chunks), "from ", len(docs), "documents")

            for i, chunk in enumerate(chunks):
                print(f"Chunks {i} is of size ", len(chunk.page_content))

            
            # create embeddings (analyze embeddings for testing)
            #emb1 = embedding_model.embed_documents([chunks[0].page_content])
            #print(emb1)
            

            # Index embeddings
            chroma_ids = vector_store.add_documents(documents=chunks)
            print("Chroma ids: ", chroma_ids)


            # Similarity search -> if you want to use it for testing
            #result = vector_store.similarity_search(
            #    query="What is the main topic of the document?",
            #    k=2
            #)
            #print("Result: ", result)



            # Create retriever 
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )

            if prompt := st.chat_input("Prompt"):
                print(prompt)

                docs_retrieved = retriever.invoke(prompt)

                # Create a prompt template
                system_prompt = """
                You are a helpful assistant that can answer questions about the following question: 
                {question}, only using the following information {document}.
                If you don't know the answer, just say that I have not enough information 
                to answer the question.
                """

                prompt_template = ChatPromptTemplate.from_messages(
                    [
                        ("system", system_prompt)
                    ]
                )

                final_prompt = prompt_template.invoke({
                    "question": prompt,
                    "document": docs_retrieved
                })

                

                # UI container
                result_placeholder = st.empty()

                # Create completion
                #completion = llm.invoke(final_prompt)
                #print("Completion: ", completion.content)

                # Streaming the completion result
                full_completion = ""
                for chunk in llm.stream(final_prompt):
                    full_completion += chunk.content
                    result_placeholder.write(full_completion)



        except Exception as e:
            print(e)


        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


