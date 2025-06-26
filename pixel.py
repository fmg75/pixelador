import streamlit as st
from PIL import Image
import io

def pixelar_imagen(imagen, factor_pixel=10, bn=False, rotacion=0):
    """
    Pixela una imagen aplicando un efecto de baja resolución
    """
    try:
        if rotacion != 0:
            imagen = imagen.rotate(-rotacion, expand=True)
        
        if bn:
            imagen = imagen.convert('L').convert('RGB')
        
        ancho_original, alto_original = imagen.size
        ancho_pequeno = max(1, ancho_original // factor_pixel)
        alto_pequeno = max(1, alto_original // factor_pixel)
        
        imagen_pequena = imagen.resize((ancho_pequeno, alto_pequeno), Image.NEAREST)
        imagen_pixelada = imagen_pequena.resize((ancho_original, alto_original), Image.NEAREST)
        
        return imagen_pixelada
        
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.set_page_config(
        page_title="🎨 Pixel Art Generator",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS minimalista
    st.markdown("""
    <style>
    /* Ocultar sidebar completamente */
    .css-1d391kg {display: none;}
    
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Contenedor principal centrado */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Espaciado minimalista */
    .stSelectbox, .stSlider, .stCheckbox {
        margin-bottom: 0.5rem;
    }
    
    /* Título minimalista */
    h1 {
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título
    st.markdown("#Pixelsdor")
    
    # Controles en una fila horizontal
    col_upload, col_rotate, col_pixel, col_bw = st.columns([3, 1, 2, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "Sube tu imagen",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            label_visibility="collapsed"
        )
    
    # Solo mostrar controles si hay imagen
    if uploaded_file is not None:
        imagen_original = Image.open(uploaded_file)
        if imagen_original.mode != 'RGB':
            imagen_original = imagen_original.convert('RGB')
        
        with col_rotate:
            rotacion = st.selectbox(
                "Rotación",
                [0, 90, 180, 270],
                format_func=lambda x: f"{x}°",
                label_visibility="collapsed"
            )
        
        with col_pixel:
            factor_pixel = st.slider(
                "Factor de pixelado",
                2, 50, 10,
                label_visibility="collapsed"
            )
        
        with col_bw:
            bn_enabled = st.checkbox("B&W", label_visibility="collapsed")
        
        # Procesar imagen
        imagen_pixelada = pixelar_imagen(imagen_original, factor_pixel, bn_enabled, rotacion)
        
        if imagen_pixelada:
            st.markdown("---")
            
            # Mostrar imágenes lado a lado
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("**Original**")
                imagen_preview = imagen_original
                if rotacion != 0:
                    imagen_preview = imagen_original.rotate(-rotacion, expand=True)
                st.image(imagen_preview, use_container_width=True)
            
            with col2:
                st.markdown("**Pixelado**")
                st.image(imagen_pixelada, use_container_width=True)
            
            # Botón de descarga centrado
            st.markdown("---")
            col_center = st.columns([2, 1, 2])[1]
            
            with col_center:
                buf = io.BytesIO()
                imagen_pixelada.save(buf, format='PNG')
                byte_im = buf.getvalue()
                
                original_name = uploaded_file.name.rsplit('.', 1)[0]
                suffix = "_BW" if bn_enabled else ""
                download_name = f"{original_name}_pixel_{factor_pixel}x{suffix}.png"
                
                st.download_button(
                    "💾 Descargar",
                    data=byte_im,
                    file_name=download_name,
                    mime="image/png",
                    use_container_width=True,
                    type="primary"
                )
    
    else:
        # Mensaje minimalista de bienvenida
        st.markdown("---")
        col_welcome = st.columns([1, 2, 1])[1]
        
        with col_welcome:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #666;">
                <h3 style="color: #888; font-weight: 300;">Arrastra una imagen aquí</h3>
                <p>O usa el botón de arriba para seleccionar un archivo</p>
                <small>PNG, JPG, JPEG, GIF, BMP</small>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()