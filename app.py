import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Agente IA Interno", page_icon="🤖")
st.title("🤖 Asistente de IA Documental")
st.markdown("Sube un documento PDF y hazme preguntas sobre su contenido.")

with st.sidebar:
    st.header("Configuración")
    cohere_api_key = st.text_input("Tu Cohere API Key", type="password")
    uploaded_file = st.file_uploader("Sube tu archivo PDF", type="pdf")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if uploaded_file and cohere_api_key and st.session_state.rag_chain is None:
    with st.spinner("Procesando el documento..."):
        os.environ["COHERE_API_KEY"] = cohere_api_key
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        loader = PyPDFLoader(tmp_file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        embeddings = CohereEmbeddings(model="embed-multilingual-v3.0")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        
        llm = ChatCohere(model="command-r-plus-08-2024") 
        
        template = '''Eres un asistente de IA interno de la empresa.
        Usa los siguientes fragmentos de contexto para responder la pregunta del usuario.
        Si no sabes la respuesta, di amablemente que no tienes esa información.
        Mantén tu respuesta clara, directa y profesional.

        Contexto:
        {context}

        Pregunta: {question}
        '''
        prompt = ChatPromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        st.session_state.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        st.success("¡Documento procesado y listo!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    if not st.session_state.rag_chain:
        st.error("Por favor, sube un documento e ingresa tu API Key primero.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                respuesta = st.session_state.rag_chain.invoke(prompt)
                st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
