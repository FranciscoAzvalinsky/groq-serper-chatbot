import pytest
from unittest.mock import patch
from main import process_user_input  # Importa la función principal desde tu archivo

# Prueba para verificar que se devuelven los enlaces relevantes
def test_search_returns_relevant_links():
    user_input = "prueba de búsqueda"
    conversation_history = []
    with patch("serpapi.GoogleSearch.get_dict") as mock_search:
        mock_search.return_value = {
            "organic_results": [
                {"link": "https://example.com/1"},
                {"link": "https://example.com/2"},
                {"link": "https://example.com/3"},
                {"link": "https://example.com/4"},
                {"link": "https://example.com/5"},
            ]
        }
        response = process_user_input(user_input, conversation_history)
        for link in ["https://example.com/1", "https://example.com/2", "https://example.com/3", "https://example.com/4", "https://example.com/5"]:
            assert link in response

# Prueba para verificar que se extrae el texto de las páginas web
def test_extract_page_text():
    user_input = "prueba de extracción de texto"
    conversation_history = []
    with patch("requests.get") as mock_get:
        mock_get.return_value.content = b"<html><body>Texto de prueba</body></html>"
        response = process_user_input(user_input, conversation_history)
        assert "Texto de prueba" in response

# Prueba para verificar que se genera una respuesta coherente con Groq
def test_generate_coherent_response():
    user_input = "prueba de respuesta coherente"
    conversation_history = [("Usuario", "Hola"), ("Chatbot", "¡Hola! ¿En qué puedo ayudarte?")]
    with patch("groq.Client.stream") as mock_stream:
        mock_stream.return_value = ["Esta es una ", "respuesta de prueba "]
        response = process_user_input(user_input, conversation_history)
        assert "Esta es una respuesta de prueba" in response
