import streamlit as st
from PIL import Image
import io

# Importar los servicios desarrollados en la Etapa 3
from services.vision_analyzer import analyze_restaurant_images
from services.menu_parser import extract_menu_from_images
from services.design_generator import generate_design_spec

# Configuración de la página
st.set_page_config(
    page_title="MenuAI — Menús profesionales con IA",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estados de sesión para retener resultados entre interacciones
if "visual_identity" not in st.session_state:
    st.session_state.visual_identity = None
if "menu_data" not in st.session_state:
    st.session_state.menu_data = None
if "design_spec" not in st.session_state:
    st.session_state.design_spec = None

def main():
    # Header Principal
    st.title("MenuAI")
    st.markdown("### Convierte la identidad de tu restaurante en un menú profesional.")
    st.markdown("---")

    # Contenedor de Estado de Configuración (Sidebar)
    with st.sidebar:
        st.header("⚙️ Configuración")
        st.info(
            "**Instrucciones:**\n\n"
            "1. Sube entre 1 y 10 fotos del interior, fachada o detalles de tu restaurante.\n"
            "2. Sube la(s) fotografía(s) de tu carta actual.\n"
            "3. Haz clic en **Generar menú con IA** para procesar la identidad y el contenido."
        )
        st.markdown("---")
        st.markdown("🚀 **Versión MVP 1.0** — Optimizado para restaurantes.")

    # Layout en dos columnas principales para la subida de archivos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. 🏢 Fotografías del Restaurante")
        st.markdown("Sube imágenes de la fachada, interior, mesas, barra o iluminación (máx. 10).")
        restaurant_files = st.file_uploader(
            "Selecciona imágenes del local",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="restaurant_images"
        )
        
        if restaurant_files:
            st.success(f"✅ {len(restaurant_files)} imagen(es) de restaurante cargada(s).")
            # Mostrar vista previa en miniatura horizontal
            cols_prev = st.columns(min(len(restaurant_files), 4))
            for idx, file in enumerate(restaurant_files[:4]):
                with cols_prev[idx]:
                    image = Image.open(file)
                    st.image(image, use_container_width=True)

    with col2:
        st.subheader("2. 📄 Fotografías del Menú Actual")
        st.markdown("Sube las fotografías de tu carta física actual.")
        menu_files = st.file_uploader(
            "Selecciona imágenes del menú",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="menu_images"
        )
        
        if menu_files:
            st.success(f"✅ {len(menu_files)} imagen(es) de menú cargada(s).")
            cols_menu_prev = st.columns(min(len(menu_files), 4))
            for idx, file in enumerate(menu_files[:4]):
                with cols_menu_prev[idx]:
                    image = Image.open(file)
                    st.image(image, use_container_width=True)

    st.markdown("---")

    # Botón de Ejecución Principal
    st.subheader("3. ⚡ Generación Automática")
    
    can_generate = bool(restaurant_files and menu_files)
    
    if not can_generate:
        st.warning("⚠️ Por favor, sube al menos una fotografía del restaurante y una fotografía del menú para continuar.")

    generate_btn = st.button(
        "✨ Generar menú con IA",
        type="primary",
        use_container_width=True,
        disabled=not can_generate
    )

    if generate_btn:
        try:
            # Convertir archivos subidos a bytes en memoria
            restaurant_bytes = [f.read() for f in restaurant_files]
            menu_bytes = [f.read() for f in menu_files]

            with st.status("🧠 Procesando con inteligencia artificial...", expanded=True) as status:
                
                # Paso 1: Analizar identidad visual
                st.write("🏢 Analizando identidad visual y estilo del restaurante...")
                st.session_state.visual_identity = analyze_restaurant_images(restaurant_bytes)
                
                # Paso 2: Extraer contenido del menú
                st.write("📄 Extrayendo platos, categorías y precios de la carta (OCR)...")
                st.session_state.menu_data = extract_menu_from_images(menu_bytes)
                
                # Paso 3: Generar especificación de diseño
                st.write("🎨 Sintetizando especificación de diseño profesional...")
                st.session_state.design_spec = generate_design_spec(
                    st.session_state.visual_identity,
                    st.session_state.menu_data
                )
                
                status.update(label="¡Análisis y diseño completados con éxito!", state="complete", expanded=False)
            
            st.success("¡Información procesada correctamente! Revisa los resultados extraídos a continuación antes de renderizar.")

        except Exception as e:
            st.error(f"Ocurrió un error durante el procesamiento con Gemini: {str(e)}")

    # Visualización de Resultados Extraídos (Human-in-the-Loop Validation)
    if st.session_state.visual_identity and st.session_state.menu_data:
        st.markdown("---")
        st.header("📋 Resumen del Análisis e Información Extraída")
        
        tab1, tab2, tab3 = st.tabs(["🎨 Identidad Visual", "🍽️ Contenido del Menú", "📐 Especificación de Diseño"])

        with tab1:
            vi = st.session_state.visual_identity
            st.markdown(f"**Estilo:** {vi.style}")
            st.markdown(f"**Atmósfera (Mood):** {vi.mood}")
            st.markdown(f"**Iluminación:** {vi.lighting}")
            st.markdown(f"**Tipografía sugerida:** {vi.typography_style}")
            
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                st.markdown("**Colores Primarios:**")
                st.write(vi.primary_colors)
            with col_c2:
                st.markdown("**Colores Secundarios:**")
                st.write(vi.secondary_colors)
            with col_c3:
                st.markdown("**Colores de Acento:**")
                st.write(vi.accent_colors)
            
            st.markdown(f"**Materiales detectados:** {', '.join(vi.materials)}")

        with tab2:
            menu = st.session_state.menu_data
            st.subheader(f"Restaurante: {menu.restaurant.name or 'Sin nombre detectado'}")
            if menu.restaurant.description:
                st.caption(menu.restaurant.description)
            
            for cat in menu.categories:
                with st.expander(f"📂 {cat.name} ({len(cat.items)} ítems)"):
                    for item in cat.items:
                        review_badge = " ⚠️ *[Needs Review]*" if item.needs_review else ""
                        st.markdown(f"- **{item.name}** — `{item.price}`{review_badge}")
                        if item.description:
                            st.caption(f"  _{item.description}_")
                        if item.ingredients:
                            st.caption(f"  *Ingredientes: {', '.join(item.ingredients)}*")

        with tab3:
            ds = st.session_state.design_spec
            st.json(ds.model_dump())

        st.markdown("---")
        st.info("🔜 En las siguientes etapas conectaremos el motor de renderizado HTML y la exportación a PDF profesional.")

if __name__ == "__main__":
    main()
