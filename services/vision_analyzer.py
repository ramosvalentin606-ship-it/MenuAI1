from typing import List
from google.genai import types
from services.gemini_client import get_gemini_client
from models.schemas import VisualIdentity

def analyze_restaurant_images(image_bytes_list: List[bytes]) -> VisualIdentity:
    """
    Recibe una lista de bytes de imágenes del restaurante y retorna un objeto VisualIdentity validado.
    """
    client = get_gemini_client()
    
    # Preparar las partes de contenido con las imágenes
    contents = []
    for img_bytes in image_bytes_list:
        contents.append(
            types.Part.from_bytes(
                data=img_bytes,
                mime_type="image/jpeg"
            )
        )
    
    prompt = (
        "Analiza detalladamente estas fotografías del restaurante (fachada, interior, iluminación, mobiliario, detalles). "
        "Extrae estrictamente las características visuales que definen su identidad para el diseño de su carta o menú. "
        "Identifica colores dominantes y de acento en formato HEX real, materiales predominantes, iluminación y estilo de diseño general. "
        "No inventes características que no se puedan inferir de las imágenes."
    )
    contents.append(prompt)

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=VisualIdentity,
            temperature=0.2, # Baja temperatura para mayor precisión y consistencia objetiva
        ),
    )

    # El SDK parseará y validará automáticamente el JSON hacia el schema de Pydantic
    return response.parsed
