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
        layout="wide"
    )
    
    # Ocultar elementos de Streamlit por defecto
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    st.title("Pixelador")
    
    # Sidebar para controles
    st.sidebar.header("⚙️ Controles")
    
    # Subir imagen
    uploaded_file = st.sidebar.file_uploader(
        "📁 Sube tu imagen",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp']
    )
    
    if uploaded_file is not None:
        # Cargar imagen
        imagen_original = Image.open(uploaded_file)
        
        # Convertir a RGB si es necesario
        if imagen_original.mode != 'RGB':
            imagen_original = imagen_original.convert('RGB')
        
        # Controles
        st.sidebar.markdown("---")
        
        # Rotación
        rotacion = st.sidebar.selectbox(
            "🔄 Rotación",
            [0, 90, 180, 270],
            index=0,
            format_func=lambda x: f"{x}°" if x != 0 else "Sin rotación"
        )
        
        # Factor de pixelado
        factor_pixel = st.sidebar.slider(
            "🔲 Factor de Pixelado",
            min_value=2,
            max_value=50,
            value=10
        )
        
        # Blanco y negro
        bn_enabled = st.sidebar.checkbox("⚫ Blanco y Negro")
        
        # Procesar imagen
        imagen_pixelada = pixelar_imagen(imagen_original, factor_pixel, bn_enabled, rotacion)
        
        if imagen_pixelada:
            # Layout de columnas
            col1, col2 = st.columns(2, gap="medium")
            
            with col1:
                st.subheader("📸 Original")
                # Aplicar solo rotación para vista previa original
                imagen_preview = imagen_original
                if rotacion != 0:
                    imagen_preview = imagen_original.rotate(-rotacion, expand=True)
                st.image(imagen_preview, use_container_width=True)
            
            with col2:
                st.subheader("🎮 Pixelado")
                st.image(imagen_pixelada, use_container_width=True)
            
            # Botón de descarga centrado
            st.markdown("---")
            col_center = st.columns([1, 1, 1])[1]
            
            with col_center:
                # Convertir imagen a bytes para descarga
                buf = io.BytesIO()
                imagen_pixelada.save(buf, format='PNG')
                byte_im = buf.getvalue()
                
                # Generar nombre de archivo
                original_name = uploaded_file.name.rsplit('.', 1)[0]
                suffix = "_BW" if bn_enabled else ""
                download_name = f"{original_name}_pixel_{factor_pixel}x{suffix}.png"
                
                st.download_button(
                    label="💾 Descargar",
                    data=byte_im,
                    file_name=download_name,
                    mime="image/png",
                    use_container_width=True
                )
    
    else:
        # Mensaje de bienvenida limpio
        st.markdown("---")
        col_welcome = st.columns([1, 2, 1])[1]
        
        with col_welcome:
            st.markdown("""
            ### 🚀 Instrucciones
            
            1. **📁 Sube** una imagen
            2. **🔄 Rota** si es necesario  
            3. **🔲 Ajusta** el pixelado
            4. **💾 Descarga** tu creación
            """)

if __name__ == "__main__":
    main()