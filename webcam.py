from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
from PIL import Image
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        # Récupérer l'image envoyée en base64
        data = request.json
        image_data = data['image'].split(',')[1]  # Enlever "data:image/jpeg;base64,"
        
        # Décoder l'image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir en array numpy pour OpenCV
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # ICI : Ajouter votre détection d'objets avec TensorFlow
        # Pour l'instant, on dessine juste un rectangle de test
        height, width = frame.shape[:2]
        cv2.rectangle(frame, (50, 50), (width-50, height-50), (0, 255, 0), 2)
        cv2.putText(frame, "Detection active", (60, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Convertir le résultat en base64 pour renvoyer au client
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'image': f'data:image/jpeg;base64,{img_str}',
            'detections': []  # Ici vous retournerez les objets détectés
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Accessible depuis Windows sur http://localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)