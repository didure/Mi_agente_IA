# 🤖 Asistente de IA Documental (RAG)

## 🎯 Resumen del Proyecto
Este repositorio contiene la implementación de un agente de Inteligencia Artificial que soluciona la pérdida de tiempo en la búsqueda de información interna en empresas. A través de la arquitectura **RAG (Generación Aumentada por Recuperación)**, este agente permite subir documentos corporativos (PDF) y realizar consultas en lenguaje natural, garantizando que las respuestas se basen únicamente en la información proporcionada.

## 🏗️ Arquitectura del Sistema
1.  **Interfaz de Usuario (UI):** Construida de manera ágil con Streamlit.
2.  **Procesamiento:** `PyPDFLoader` para extraer el texto y `RecursiveCharacterTextSplitter` para fragmentarlo en bloques de 1000 caracteres.
3.  **Base de Datos Vectorial:** ChromaDB para almacenamiento local y búsqueda eficiente.
4.  **Modelo y Embeddings:** Cohere (`embed-multilingual-v3.0` y `command-r-plus-08-2024`).
5.  **Orquestación:** Tubería construida con LangChain (LCEL).

## 🚀 Instrucciones de Ejecución Local
Sigue estos pasos para probar el proyecto en tu máquina:

1. Clona el repositorio e ingresa a la carpeta del proyecto.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación de Streamlit:
   ```bash
   streamlit run app.py
   ```
   *(La aplicación se abrirá en el navegador. Podrás introducir tu API Key de Cohere directamente en la barra lateral).*

## 💬 Ejemplos de Preguntas y Respuestas

*   **Pregunta:** "¿Cuál es la política de trabajo remoto?"
    *   **Respuesta:** "Según el manual de políticas, los empleados pueden trabajar de forma remota hasta 3 días a la semana, previa coordinación con su supervisor."
*   **Pregunta:** "¿Qué lenguajes de programación se usan en el back-end de la empresa?"
    *   **Respuesta:** "De acuerdo con la documentación adjunta, el back-end está construido utilizando Python con el framework FastAPI."

## Respuestas del agente ante una pregunta que no tiene que ver con su función:
<img width="1408" height="615" alt="image" src="https://github.com/user-attachments/assets/b508c31e-c596-4f45-b4dc-b4124a60581d" />

## Respuestas del agente ante una pregunta que si se encuentra en la política.
<img width="1411" height="762" alt="image" src="https://github.com/user-attachments/assets/77d1b9b0-961f-4a9d-9932-c4f0fab5194c" />



