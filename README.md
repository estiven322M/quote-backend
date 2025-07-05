# Generador de Citas con IA 

[![Ver Demo](https://img.shields.io/badge/Ver_Demo-En_Vivo-brightgreen)](https://front-quote-generator.netlify.app/)

Aplicación web full-stack que genera citas inspiradoras utilizando la API de Google Gemini y permite crear una imagen personalizada con la cita para descargar y compartir.



### Descripción del Proyecto

Este proyecto es una aplicación web completa construida desde cero, que integra un frontend interactivo con un backend robusto para comunicarse con una API de inteligencia artificial. La aplicación permite a los usuarios obtener citas célebres y generar dinámicamente imágenes con ellas, listas para ser compartidas en redes sociales.

---

### 🔧 Tecnologías Utilizadas (Backend)

* **Lenguaje:** Python 3
* **Framework:** Flask
* **APIs:** Google Gemini API
* **Librerías Clave:**
    * `Pillow (PIL)`: Para la generación de imágenes.
    * `Flask-CORS`: Para permitir la comunicación con el frontend.
    * `python-dotenv`: Para la gestión segura de claves de API.
* **Servidor de Producción:** Gunicorn
* **Plataforma de Despliegue:** Render

### ⚙️ Endpoints de la API

* `GET /api/get-quote`: Genera y devuelve una nueva cita en formato JSON.
* `POST /api/create-image`: Recibe una cita y un autor, y devuelve una imagen PNG generada.

### 🚀 Instalación y Uso Local (Backend)

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/quote-backend.git](https://github.com/tu-usuario/quote-backend.git)
    cd quote-backend
    ```
2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Crear el archivo `.env`** en la raíz del proyecto y añadir la clave de API:
    ```
    GOOGLE_API_KEY="TU_CLAVE_API_AQUI"
    ```
5.  **Ejecutar el servidor:**
    ```bash
    python app.py
    ```
El servidor estará disponible en `http://127.0.0.1:5000`.

### 💻 Tecnologías Utilizadas (Frontend)

* **Lenguajes:** HTML5, CSS3, JavaScript (ES6+)
* **Librerías:** Font Awesome (para íconos)
* **APIs Nativas del Navegador:** `fetch` para peticiones asíncronas, `Blob` y `URL.createObjectURL` para la descarga de archivos.
* **Plataforma de Despliegue:** Netlify

### Uso Local (Frontend)

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/quote-frontend.git](https://github.com/tu-usuario/quote-frontend.git)
    cd quote-frontend
    ```
2.  **Abrir `index.html`** directamente en tu navegador web.

*(**Nota:** Para que funcione localmente, el servidor backend debe estar corriendo en `http://127.0.0.1:5000`)*.
