import streamlit as st

def render_header():
    st.title("🔍 Semantic Search Engine")
    st.caption("Upload documents and ask questions using AI")

def render_sidebar(rag_engine, processed_files_set):
    with st.sidebar:
        st.header("📊 Status")
        doc_count = rag_engine.get_document_count()
        file_count = len(processed_files_set)
        
        col1, col2 = st.columns(2)
        col1.metric("Files", file_count)
        col2.metric("Chunks", doc_count)
        
        st.markdown("---")
        
        st.header("🗑️ Reset Database")
        st.caption("Clear all indexed documents")
        if st.button("Reset", type="secondary", use_container_width=True):
            rag_engine.reset_database()
            processed_files_set.clear()
            st.success("Database cleared!")
            st.rerun()
        
        st.markdown("---")
        
        st.header("ℹ️ About")
        st.markdown("""
        Upload **PDF**, **TXT**, or **DOCX** files and ask questions about their content.
        
        **Tech Stack:**
        - LangChain
        - Ollama  
        - ChromaDB
        """)
