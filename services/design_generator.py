from google.genai import types
from services.gemini_client import get_gemini_client
from models.schemas import VisualIdentity, MenuData, DesignSpec

def generate_design_spec(visual_identity: VisualIdentity, menu_data: MenuData) -> DesignSpec:
    """
    Genera la especificación de diseño (DesignSpec) basada en la identidad visual del local
    y el volumen de contenido del menú.
    """
    client = get_gemini_client()
    
    prompt = f"""
    Basándote en la identidad visual del restaurante y la estructura del menú provistas, genera la especificación de diseño (DesignSpec).
    
    Identidad Visual del Restaurante:
    - Estilo: {visual_identity.style}
    - Mood: {visual_identity.mood}
    - Colores Primarios: {visual_identity.primary_colors}
    - Colores Secundarios: {visual_identity.secondary_colors}
    - Colores de Acento: {visual_identity.accent_colors}
    - Estilo Tipográfico sugerido: {visual_identity.typography_style}
    
    Instrucciones para la especificación:
    1. Selecciona colores HEX limpios y contrastados para el fondo, títulos, textos y precios, inspirados o adaptados de los colores primarios/secundarios del local.
    2. Elige tipografías de Google Fonts reales y profesionales que concuerden con el estilo (ej. 'Playfair Display', 'Montserrat', 'Inter', 'Lora', 'Oswald').
    3. Define si el layout debe ser de 1 o 2 columnas según la cantidad de categorías y elementos del menú.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DesignSpec,
            temperature=0.3,
        ),
    )

    return response.parsed
