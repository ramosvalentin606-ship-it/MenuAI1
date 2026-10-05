from typing import List, Optional
from pydantic import BaseModel, Field


# ==========================================
# 1. VISUAL IDENTITY SCHEMAS
# ==========================================

class VisualIdentity(BaseModel):
    style: str = Field(
        description="Estilo arquitectónico/diseño del restaurante (ej. industrial contemporáneo, rústico, minimalista, tropical)."
    )
    mood: str = Field(
        description="Atmósfera o vibra que transmite el lugar (ej. cálido y acogedor, sofisticado, jovial, elegante)."
    )
    primary_colors: List[str] = Field(
        default_factory=list,
        description="Lista de 1 a 3 códigos HEX primarios predominantes en el espacio (ej. ['#1E1E1E', '#2B2B2B'])."
    )
    secondary_colors: List[str] = Field(
        default_factory=list,
        description="Lista de 1 a 3 códigos HEX secundarios que complementan el espacio (ej. ['#F2E9DC'])."
    )
    accent_colors: List[str] = Field(
        default_factory=list,
        description="Lista de 1 a 2 códigos HEX de acento utilizados en detalles o iluminación (ej. ['#C89B3C'])."
    )
    materials: List[str] = Field(
        default_factory=list,
        description="Materiales visibles en la decoración/arquitectura (ej. madera, concreto, metal negro, ladrillo)."
    )
    lighting: str = Field(
        description="Tipo de iluminación predominante (ej. cálida tenue, luz natural brillante, neón industrial)."
    )
    typography_style: str = Field(
        description="Estilo tipográfico sugerido acorde a la marca (ej. serif elegante, sans-serif moderna, manuscrita vintage)."
    )
    layout_style: str = Field(
        description="Distribución visual recomendada para el menú (ej. minimalista, columnas clásicas, editorial con imágenes)."
    )
    image_style: str = Field(
        description="Estilo fotográfico ideal para acompañar el menú (ej. fotografía limpia con luz natural, claroscuro gastronómico)."
    )
    graphic_elements: List[str] = Field(
        default_factory=list,
        description="Elementos gráficos decorativos coherentes con el espacio (ej. líneas finas, patrones botánicos, bordes geométricos)."
    )
    design_keywords: List[str] = Field(
        default_factory=list,
        description="Palabras clave de diseño que resumen la esencia visual (ej. ['elegante', 'minimalista', 'urbano'])."
    )


# ==========================================
# 2. MENU CONTENT SCHEMAS
# ==========================================

class MenuItem(BaseModel):
    name: str = Field(description="Nombre exacto del plato o bebida tal como aparece en el menú.")
    description: Optional[str] = Field(
        default="",
        description="Descripción del plato. Si no existe en el menú físico, dejar cadena vacía."
    )
    price: str = Field(
        description="Precio del producto (ej. '$25.000', '25.000', '12.50'). Mantener el formato original si existe."
    )
    ingredients: List[str] = Field(
        default_factory=list,
        description="Lista de ingredientes explícitamente detallados en el menú. Si no están indicados, dejar lista vacía."
    )
    needs_review: bool = Field(
        default=False,
        description="Establecer en True únicamente si el texto o precio era difícil de leer, borracho o ambiguo en la imagen."
    )


class MenuCategory(BaseModel):
    name: str = Field(description="Nombre de la categoría (ej. 'Entradas', 'Platos Fuertes', 'Coctelería', 'Postres').")
    items: List[MenuItem] = Field(default_factory=list, description="Lista de platos/bebidas dentro de la categoría.")


class RestaurantInfo(BaseModel):
    name: str = Field(
        default="",
        description="Nombre oficial del restaurante extraído de la carta o marca. Si no es visible, dejar vacíos."
    )
    description: Optional[str] = Field(
        default="",
        description="Slogan, subtítulo o breve descripción del restaurante presente en la carta."
    )


class MenuData(BaseModel):
    restaurant: RestaurantInfo
    categories: List[MenuCategory] = Field(default_factory=list)


# ==========================================
# 3. DESIGN SPEC SCHEMAS
# ==========================================

class ColorPaletteSpec(BaseModel):
    background: str = Field(description="Color HEX para el fondo del menú (ej. '#FDFBF7' o '#121212').")
    primary: str = Field(description="Color HEX para títulos principales y nombre del restaurante.")
    secondary: str = Field(description="Color HEX para subtítulos, nombres de platos y bordes.")
    accent: str = Field(description="Color HEX para precios, destacados y elementos decorativos.")
    text_muted: str = Field(description="Color HEX para descripciones e ingredientes secundarios (ej. '#666666').")


class TypographySpec(BaseModel):
    heading: str = Field(description="Nombre de la tipografía de Google Fonts para títulos (ej. 'Playfair Display', 'Montserrat').")
    body: str = Field(description="Nombre de la tipografía de Google Fonts para descripciones (ej. 'Inter', 'Lora').")
    price: str = Field(description="Nombre de la tipografía de Google Fonts para precios (ej. 'Oswald', 'Montserrat').")


class LayoutSpec(BaseModel):
    columns: int = Field(default=2, description="Número de columnas sugerido para el diseño (1 o 2).")
    category_style: str = Field(description="Estilo visual de los títulos de categoría (ej. 'centered_lines', 'underlined', 'boxed').")
    product_style: str = Field(description="Estilo visual de la línea de producto (ej. 'dotted_leader', 'clean_spaced', 'card').")


class SpacingSpec(BaseModel):
    section: str = Field(default="24px", description="Margen vertical entre categorías.")
    product: str = Field(default="12px", description="Espaciado vertical entre ítems de comida.")
    page: str = Field(default="32px", description="Padding interno de la página.")


class DesignSpec(BaseModel):
    template: str = Field(default="modern_restaurant", description="Nombre de la plantilla a utilizar.")
    page_size: str = Field(default="A4", description="Tamaño de la página (A4 o Letter).")
    orientation: str = Field(default="portrait", description="Orientación (portrait o landscape).")
    colors: ColorPaletteSpec
    typography: TypographySpec
    layout: LayoutSpec
    spacing: SpacingSpec
    decorative_elements: List[str] = Field(
        default_factory=list,
        description="Lista de clases o modificadores estéticos (ej. ['border_frame', 'subtle_shadow', 'uppercase_headers'])."
    )
