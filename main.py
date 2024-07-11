import os
import asyncio
import aiohttp
import requests
import json
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key= GROQ_API_KEY)

async def search_google(query):
    """Realiza una busqueeda en Google usando la API de Serper."""
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query
    })
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: La API de Serper.dev devolvió el código de estado {response.status_code}")
        return {}


            

async def main():
    conversation_history = []

    print("Chatbot: Bienvenido al chatbot. Escribe 'salir' para terminar.")

    while True:
        user_input = input("Usuario: ")

        if user_input.lower() == "salir":
            print("Chatbot: ¡Hasta luego!")
            break

        conversation_history.append(("Usuario", user_input))

        # Aquí es donde deberías procesar la entrada del usuario y generar una respuesta
        response = await process_user_input(user_input, conversation_history)

        conversation_history.append(("Chatbot", response))
        print(f"Chatbot: {response}")


async def process_user_input(user_input, conversation_history):
    # Realizar búsqueda en Google utilizando la API de Serper.dev

    print(f"Chatbot: Buscando en Internet...")
    results = await search_google(user_input)

    # Obtener los primeros 5 enlaces relevantes
    links = results.get("organic", [])[:5]

    # Construir la respuesta con los enlaces
    response = f"\n\n\n\n**Búsqueda en Internet para: '{user_input}'**\n\n"
    # Extraer texto de las páginas web
    page_texts = []
    for link_info in links:
        link = link_info['link']  # Obtener la URL real del diccionario
        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, "html.parser")
            text = soup.get_text()
            page_texts.append(text[:1000])
        except Exception as e:
            response += f"\nNo se pudo extraer el texto de {link}: {e}\n"



    # Integrar con el modelo de lenguaje Groq
    
    conversation_history_str = "\n".join([f"{role}: {message}" for role, message in conversation_history])
    page_texts_str = "\n\n".join(page_texts)
    prompt = f"{conversation_history_str}\nUsuario: {user_input}\nTexto extraído de las páginas web:\n{page_texts_str}\nGroq:"
    stream  = client.chat.completions.create(
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "sos un asistente muy util que entiende pregunatas en español y responde en español."
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama3-8b-8192",
    stream= True
    )

    # Print the incremental deltas returned by the LLM.
    for chunk in stream:
        print(chunk.choices[0].delta.content, end="")

    # Citar fuentes consultadas
    response += "\n\nFuentes consultadas:\n"
    for link_info in links:
        link = link_info['link']
        response += f"- {link}\n"

    return response

if __name__ == "__main__":
    asyncio.run(main())
