#  Pixelador

Una aplicación web simple y elegante para convertir imágenes en arte pixelado con estilo retro.

## ✨ Características

- 📁 **Subida de imágenes**: Soporta PNG, JPG, JPEG, GIF, BMP
- 🔄 **Rotación**: Gira tus imágenes (0°, 90°, 180°, 270°)
- 🔲 **Pixelado ajustable**: Factor de 2x a 50x
- ⚫ **Modo B&W**: Convierte a escala de grises
- 💾 **Descarga directa**: Guarda tu creación en PNG
- 🎮 **Interfaz limpia**: Diseño minimalista y responsive

## 🚀 Demo en vivo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tu-app-url.streamlit.app)

## 🛠️ Instalación local

### Requisitos previos
- Python 3.7 o superior
- pip

### Pasos

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/fmg75/pixelador.git
   cd pixel-art-generator
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**
   ```bash
   streamlit run app.py
   ```

4. **Abre tu navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📋 Uso

1. **Sube una imagen** usando el panel lateral
2. **Ajusta la rotación** si es necesario
3. **Selecciona el factor de pixelado** (2-50)
4. **Activa B&W** si quieres escala de grises
5. **Descarga** tu imagen pixelada

## 🎯 Consejos

- **Factor bajo (2-8)**: Efecto sutil
- **Factor medio (10-20)**: Estilo retro clásico  
- **Factor alto (25-50)**: Máximo pixelado
- **Mejor calidad**: Usa imágenes con buena resolución

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🔧 Tecnologías

- **Streamlit** - Framework web
- **Pillow (PIL)** - Procesamiento de imágenes
- **Python** - Lenguaje de programación

---

**Hecho con ❤️**