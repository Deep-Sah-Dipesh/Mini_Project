from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from PIL import Image
import io
import base64

import pickle

with open("oo.pkl", "rb") as f:
    data = pickle.load(f)  # pickle.load()
    model = data["model"]
    processor = data["processor"]
    tokenizer = data["tokenizer"]

print("Model, processor, and tokenizer loaded successfully!")


app = Flask(__name__)
CORS(app)

braille_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
    ' ': ' ', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙',
    '5': '⠼⠑', '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚'
}

def text_to_braille(text):
    return ''.join(braille_dict.get(char.lower(), '?') for char in text)

@app.route("/generate", methods=["POST"])
def generate_caption_and_braille():
    try:
        image_data = request.json.get("image")
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        inputs = processor(images=image, return_tensors="pt").pixel_values

        outputs = model.generate(inputs)
        caption = tokenizer.decode(outputs[0], skip_special_tokens=True)

        braille_text = text_to_braille(caption)

        return jsonify({
            "caption": caption,
            "braille": braille_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
