# 1. Importamos las librerías 
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont # Librería Pillow para manipular imágenes
import io # Para manejar datos binarios en memoria
import json
import textwrap # Para ajustar automáticamente el texto largo

# 2. Configuración inicial
load_dotenv() # Carga las variables de entorno desde el archivo .env
app = Flask(__name__) # Inicializa la aplicación Flask
CORS(app) # Habilita Cross-Origin Resource Sharing para permitir peticiones desde el frontend

# 3. Configurar la API de Gemini
try:
    # Lee la clave API desde las variables de entorno para mayor seguridad
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    print(f"Error configurando Gemini: {e}")
    model = None # Si falla, el modelo será None y las rutas devolverán un error

# --- RUTA 1: PARA OBTENER UNA CITA ---
@app.route("/api/get-quote", methods=["GET"])
def get_quote():
    # Verifica si el modelo de IA se inicializó correctamente
    if not model:
        return jsonify({"error": "El modelo de IA no está configurado"}), 500
    
   
    try:
        # Prompt detallado pidiendo a Gemini que responda en formato JSON
        prompt = "Genera una cita corta e inspiradora de un personaje célebre de la historia (filósofo, científico, artista, etc.). Devuelve tu respuesta en un formato JSON válido con las claves 'quote' y 'author'. Ejemplo: {\"quote\": \"La imaginación es más importante que el conocimiento.\", \"author\": \"Albert Einstein\"}"
        response = model.generate_content(prompt)
        
        # Lógica para limpiar la respuesta de Gemini y extraer solo el JSON
        raw_text = response.text
        json_start = raw_text.find('{')
        json_end = raw_text.rfind('}') + 1

        if json_start != -1 and json_end != -1:
            clean_json_str = raw_text[json_start:json_end]
            result = json.loads(clean_json_str) # Convierte el string limpio a un objeto Python
            return jsonify(result) # Devuelve una respuesta JSON válida al frontend
        else:
            raise json.JSONDecodeError("No se encontró un objeto JSON en la respuesta.", raw_text, 0)

    except json.JSONDecodeError as e:
        # Manejo de error si la respuesta de Gemini no es un JSON válido
        return jsonify({"error": "La respuesta de Gemini no fue un JSON válido", "raw": str(e)}), 500
    except Exception as e:
        # Manejo de cualquier otro error durante la generación
        return jsonify({"error": f"Error al generar la cita: {str(e)}"}), 500

# --- RUTA 2: PARA CREAR Y ENVIAR LA IMAGEN ---
@app.route("/api/create-image", methods=["POST"])
def create_image():
    # ... (El código de esta ruta no necesita cambios) ...
    try:
        # Obtiene los datos JSON enviados desde el frontend
        data = request.json
        quote_text = data.get("quote", "Una cita inspiradora vive aquí.")
        author_text = data.get("author", "Anónimo")

        # Configuración de la imagen a generar
        img_width, img_height = 1080, 1080
        background_color = (25, 25, 25)
        text_color = (240, 240, 240)
        author_color = (200, 200, 200)
        font_path = os.path.join("fonts", "arial.ttf") # Ruta a la fuente

        # Crea un lienzo de imagen en blanco con Pillow
        img = Image.new('RGB', (img_width, img_height), color=background_color)
        draw = ImageDraw.Draw(img)

         # Carga las fuentes con el tamaño deseado
        quote_font = ImageFont.truetype(font_path, size=80)
        author_font = ImageFont.truetype(font_path, size=50)

        # Usa textwrap para dividir la cita en múltiples líneas si es muy larga
        lines = textwrap.wrap(quote_text, width=25)
        
        # Calcula la posición inicial para centrar el texto verticalmente
        total_text_height = len(lines) * 80
        y_text = (img_height - total_text_height) / 2 - 50

        # Dibuja cada línea de la cita en la imagen
        for line in lines:
            line_width = draw.textlength(line, font=quote_font)
            draw.text(((img_width - line_width) / 2, y_text), line, font=quote_font, fill=text_color)
            y_text += 90

        # Dibuja el autor debajo de la cita
        author_width = draw.textlength(f"— {author_text}", font=author_font)
        draw.text(((img_width - author_width) / 2, y_text + 20), f"— {author_text}", font=author_font, fill=author_color)

        # Guarda la imagen generada en un buffer en memoria, no en un archivo físico
        img_buffer = io.BytesIO()
        img.save(img_buffer, 'PNG')
        img_buffer.seek(0)

        # Envía el buffer como un archivo descargable al frontend
        return send_file(img_buffer, mimetype='image/png', as_attachment=True, download_name='cita_generada.png')

    except Exception as e:
        return jsonify({"error": f"Error al crear la imagen: {str(e)}"}), 500
    
# 4. Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)