import streamlit as st
from PIL import Image
import io

def pixelar_imagen(imagen, factor_pixel=10, bn=False, rotacion=0):
    """
    Pixela una imagen aplicando un efecto de baja resolución
    
    Args:
        imagen (PIL.Image): Imagen PIL
        factor_pixel (int): Factor de pixelado (mayor número = más pixelado)
        bn (bool): Convertir a blanco y negro
        rotacion (int): Grados de rotación (0, 90, 180, 270)
    
    Returns:
        PIL.Image: Imagen pixelada
    """
    try:
        # Aplicar rotación si es necesario
        if rotacion != 0:
            imagen = imagen.rotate(-rotacion, expand=True)
        
        # Convertir a B&W si se solicita
        if bn:
            imagen = imagen.convert('L').convert('RGB')
        
        # Obtener dimensiones originales
        ancho_original, alto_original = imagen.size
        
        # Calcular nuevas dimensiones (más pequeñas)
        ancho_pequeno = max(1, ancho_original // factor_pixel)
        alto_pequeno = max(1, alto_original // factor_pixel)
        
        # Redimensionar a tamaño pequeño usando NEAREST para mantener bordes duros
        imagen_pequena = imagen.resize((ancho_pequeno, alto_pequeno), Image.NEAREST)
        
        # Volver a escalar al tamaño original para crear el efecto pixelado
        imagen_pixelada = imagen_pequena.resize((ancho_original, alto_original), Image.NEAREST)
        
        return imagen_pixelada
        
    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")
        return None

def main():
    st.set_page_config(
        page_title="🎨 Pixel Art Generator",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado para sidebar fijo y compacto
    st.markdown("""
    <style>
    /* Sidebar fijo y compacto */
    .css-1d391kg {
        position: fixed !important;
        top: 0 !important;
        height: 100vh !important;
        width: 280px !important;
        z-index: 999999 !important;
    }
    
    /* Contenido principal con margen */
    .main .block-container {
        padding-left: 300px !important;
        max-width: none !important;
    }
    
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Sidebar más compacto */
    .css-1d391kg .css-1v3fvcr {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Espaciado de elementos del sidebar */
    .css-1d391kg .stSelectbox > div {
        margin-bottom: 0.5rem !important;
    }
    
    .css-1d391kg .stSlider > div {
        margin-bottom: 0.5rem !important;
    }
    
    .css-1d391kg .stCheckbox > div {
        margin-bottom: 0.5rem !important;
    }
    
    /* Botón de descarga más prominente */
    .download-btn {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        color: white !important;
        margin-top: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar compacto y fijo
    with st.sidebar:
        st.markdown("### 🎨 Pixel Art Generator")
        
        # Subir imagen
        uploaded_file = st.file_uploader(
            "📁 Imagen",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Arrastra o selecciona una imagen"
        )
        
        if uploaded_file is not None:
            # Cargar imagen
            imagen_original = Image.open(uploaded_file)
            
            # Convertir a RGB si es necesario
            if imagen_original.mode != 'RGB':
                imagen_original = imagen_original.convert('RGB')
            
            st.markdown("---")
            
            # Controles compactos
            rotacion = st.selectbox(
                "🔄 Rotación",
                [0, 90, 180, 270],
                format_func=lambda x: f"{x}°" if x != 0 else "0°"
            )
            
            factor_pixel = st.slider(
                "🔲 Pixelado",
                min_value=2,
                max_value=50,
                value=10,
                help="Mayor valor = más pixelado"
            )
            
            bn_enabled = st.checkbox("⚫ Blanco y Negro")
            
            # Información compacta
            st.markdown("---")
            efectivo_w = imagen_original.size[0] // factor_pixel
            efectivo_h = imagen_original.size[1] // factor_pixel
            st.caption(f"📐 Original: {imagen_original.size[0]}×{imagen_original.size[1]}")
            st.caption(f"🎯 Efectivo: {efectivo_w}×{efectivo_h}")
            
            # Procesar imagen
            imagen_pixelada = pixelar_imagen(imagen_original, factor_pixel, bn_enabled, rotacion)
            
            if imagen_pixelada:
                st.markdown("---")
                
                # Botón de descarga en sidebar
                buf = io.BytesIO()
                imagen_pixelada.save(buf, format='PNG')
                byte_im = buf.getvalue()
                
                original_name = uploaded_file.name.rsplit('.', 1)[0]
                suffix = "_BW" if bn_enabled else ""
                download_name = f"{original_name}_pixel_{factor_pixel}x{suffix}.png"
                
                st.download_button(
                    label="💾 Descargar",
                    data=byte_im,
                    file_name=download_name,
                    mime="image/png",
                    use_container_width=True,
                    type="primary"
                )
        else:
            st.markdown("---")
            st.markdown("""
            **📋 Instrucciones:**
            1. Sube una imagen
            2. Ajusta los controles
            3. Descarga el resultado
            
            **💡 Consejos:**
            - Factor 2-8: Sutil
            - Factor 10-20: Retro
            - Factor 25+: Máximo pixel
            """)
    
    # Contenido principal
    if uploaded_file is not None and 'imagen_pixelada' in locals():
        st.markdown("## 🖼️ Resultado")
        
        # Mostrar imágenes
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("### 📸 Original")
            # Aplicar solo rotación para vista previa original
            imagen_preview = imagen_original
            if rotacion != 0:
                imagen_preview = imagen_original.rotate(-rotacion, expand=True)
            st.image(imagen_preview, use_container_width=True)
        
        with col2:
            st.markdown("### 🎮 Pixelado")
            st.image(imagen_pixelada, use_container_width=True)
    
    else:
        # Pantalla de bienvenida
        st.markdown("## 🎨 Pixel Art Generator")
        st.markdown("### Convierte tus imágenes en arte pixelado con estilo retro")
        
        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
                <h3>🚀 ¡Comienza ahora!</h3>
                <p>Sube una imagen usando el panel lateral y experimenta con diferentes estilos de pixelado.</p>
                <p><strong>Formatos soportados:</strong> PNG, JPG, JPEG, GIF, BMP</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Ejemplo visual
            st.markdown("### 🎯 Ejemplo de resultados")
            
            # Crear ejemplos con diferentes factores
            import numpy as np
            
            # Crear imagen de ejemplo
            ejemplo_base = np.zeros((100, 100, 3), dtype=np.uint8)
            for i in range(0, 100, 10):
                for j in range(0, 100, 10):
                    color = [(i+j) % 200 + 55, (i*2+j) % 200 + 55, (j*2+i) % 200 + 55]
                    ejemplo_base[i:i+10, j:j+10] = color
            
            col_ej1, col_ej2, col_ej3 = st.columns(3)
            
            with col_ej1:
                st.markdown("**Factor 5x**")
                ejemplo_5 = Image.fromarray(ejemplo_base).resize((20, 20), Image.NEAREST).resize((100, 100), Image.NEAREST)
                st.image(ejemplo_5, width=150)
            
            with col_ej2:
                st.markdown("**Factor 10x**")
                ejemplo_10 = Image.fromarray(ejemplo_base).resize((10, 10), Image.NEAREST).resize((100, 100), Image.NEAREST)
                st.image(ejemplo_10, width=150)
            
            with col_ej3:
                st.markdown("**Factor 20x**")
                ejemplo_20 = Image.fromarray(ejemplo_base).resize((5, 5), Image.NEAREST).resize((100, 100), Image.NEAREST)
                st.image(ejemplo_20, width=150)

if __name__ == "__main__":
    main()