from typing import List
from google.genai import types
from services.gemini_client import get_gemini_client
from models.schemas import MenuData

def extract_menu_from_images(image_bytes_list: List[bytes]) -> MenuData:
    """
    Extrae la información completa del menú a partir de fotografías de la carta física.
    """
    client = get_gemini_client()
    
    contents = []
    for img_bytes in image_bytes_list:
        contents.append(
            types.Part.from_bytes(
                data=img_bytes,
                mime_type="image/jpeg"
            )
        )
        
    prompt = (
        "Actúa como un experto en OCR gastronómico y extracción de datos. "
        "Analiza estas fotografías de la carta del restaurante y extrae rigurosamente:\n"
        "1. Nombre del restaurante y breve descripción si aparece.\n"
        "2. Categorías del menú (ej. Entradas, Platos Fuertes, Cocteles).\n"
        "3. Lista de productos por categoría con su nombre exacto, descripción, precio e ingredientes si se detallan.\n\n"
        "REGLA CRÍTICA: NO inventes precios, productos ni ingredientes. Si alguna parte de la imagen es borrosa o difícil de leer con certeza, "
        "asigna 'needs_review': true al ítem correspondiente y extrae lo mejor posible sin adivinar cifras."
    )
    contents.append(prompt)

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MenuData,
            temperature=0.1, # Máxima precisión y fidelidad al texto real
        ),
    )

    return response.parsed
