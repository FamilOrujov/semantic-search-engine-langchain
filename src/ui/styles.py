CUSTOM_CSS = """
<style>
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
    }
    
    .stMetric {
        background-color: #262626;
        padding: 1rem;
        border-radius: 8px;
    }
    
    [data-testid="stMainBlockContainer"] {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    [data-testid="stChatInput"] {
        max-width: 800px;
        margin: 0 auto;
    }
</style>
"""

def apply_custom_styles():
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
