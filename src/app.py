import os
import streamlit as st
import tempfile
from rag_engine import RAGEngine
from ui.styles import apply_custom_styles
from ui.components import render_header, render_sidebar

st.set_page_config(page_title="Semantic Search", page_icon="🔍", layout="wide")
apply_custom_styles()

if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()

render_header()
render_sidebar(st.session_state.rag_engine, st.session_state.processed_files)

st.markdown("---")

uploaded_files = st.file_uploader(
    "Upload your documents", 
    type=['pdf', 'txt', 'docx'], 
    accept_multiple_files=True,
    help="Supported formats: PDF, TXT, DOCX"
)

if uploaded_files:
    files_to_process = []
    temp_files = []
    
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.processed_files:
            try:
                suffix = os.path.splitext(uploaded_file.name)[1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    temp_files.append(tmp_file.name)
                files_to_process.append(tmp_file.name)
                st.session_state.processed_files.add(uploaded_file.name)
            except Exception as e:
                st.error(f"Error preparing file {uploaded_file.name}: {e}")

    if files_to_process:
        with st.spinner(f"Processing {len(files_to_process)} file(s)..."):
            try:
                chunks = st.session_state.rag_engine.process_files(files_to_process)
                st.success(f"Processed {len(files_to_process)} file(s) into {chunks} chunks")
                st.rerun()
            except Exception as e:
                st.error(f"Error processing files: {e}")
            finally:
                for tf in temp_files:
                    if os.path.exists(tf):
                        os.remove(tf)
    else:
        if len(uploaded_files) > 0:
            st.info("Files already processed")

st.markdown("---")

if prompt := st.chat_input("Ask a question about your documents..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        result_placeholder = st.empty()
        full_completion = ""
        
        try:
            stream = st.session_state.rag_engine.answer_question(prompt)
            for chunk in stream:
                full_completion += chunk.content
                result_placeholder.write(full_completion)
        except Exception as e:
            st.error(f"Error: {e}")
