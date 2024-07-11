# Chatbot con Búsqueda en Internet y Respuestas en Streaming

Este proyecto es un chatbot que funciona desde la consola, mantiene la memoria de la conversación durante su ejecución, y tiene la capacidad de realizar búsquedas en Internet para enriquecer sus respuestas. Además, proporciona respuestas en streaming y cita las fuentes de donde extrajo la información.

## Requisitos previos

- Python 3.6 o superior
- Una clave de API válida para Serper.dev (https://serper.dev/)
- Una clave de API válida para Groq (https://www.groq.ai/)

## Instalación

1. Clona este repositorio:

        `git clone https://github.com/FranciscoAzvalinsky/groq-serper-chatbot`

2. Navega al directorio del proyecto:

        `cd groq-serper-chatbot`

3. Crea un archivo `.env` en el directorio raíz del proyecto y agrega tus claves de API:

        `SERPER_API_KEY=tu-clave-de-api-serper GROQ_API_KEY=tu-clave-de-api-groq`


4. Instala las dependencias necesarias:

        `pip install -r requirements.txt`


5. Para ejecutar el chatbot, simplemente ejecuta el siguiente comando:

        `python main.py`


Esto iniciará el chatbot en la consola. Puedes interactuar con él haciendo preguntas y recibirá respuestas en streaming basadas en la información recopilada de Internet y el modelo de lenguaje Groq.

## Pruebas automatizadas

Este proyecto si bien incluye un archivo de pruebas automatizadas para verificar la funcionalidad de cada componente, no se ha testeado su eficacia en ellas mismas.

PD: Esto se debe a que no pude solucionar un problema con el entorno virtual y la libreria de pytest, y dado que nunca antes utilice python, carezco del conocimiento para resolverlo. Entiendo que esto resta puntos en el proyecto.

