from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

def generate_meme(image_path, top_text, bottom_text, text_color):
    try:
        img = Image.open(image_path)
    except Exception as e:
        return None, str(e)

    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Load the "Impact" font (you can specify the path to the font file if needed)
    font = ImageFont.truetype("impact.ttf", size=40)  # Adjust the font size as needed

    # Convert user-inputted text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # Calculate text bounding boxes
    top_text_bbox = draw.multiline_textbbox((0, 0), top_text, font=font)
    bottom_text_bbox = draw.multiline_textbbox((0, 0), bottom_text, font=font)

    # Calculate text positions
    top_text_x = (width - top_text_bbox[2]) / 2
    top_text_y = 10
    bottom_text_x = (width - bottom_text_bbox[2]) / 2
    bottom_text_y = height - bottom_text_bbox[3] - 10

    # Add top and bottom text to the image with the specified text color
    if top_text:
        draw.multiline_text((top_text_x, top_text_y), top_text, fill=text_color, font=font)
    if bottom_text:
        draw.multiline_text((bottom_text_x, bottom_text_y), bottom_text, fill=text_color, font=font)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'meme.jpg')
    img.save(output_path)

    return output_path, None

@app.route('/', methods=['GET', 'POST'])
def meme_generator():
    meme_image = None
    error = None
    text_color = "#FFFFFF"  # Default text color (white)

    if request.method == 'POST':
        top_text = request.form['top_text']
        bottom_text = request.form['bottom_text']
        image = request.files['image']
        text_color = request.form['text_color']

        if image.filename != '':
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.jpg')
            image.save(image_path)

            meme_image, error = generate_meme(image_path, top_text, bottom_text, text_color)

    return render_template('meme.html', meme_image=meme_image, error=error, text_color=text_color)

if __name__ == '__main__':
    app.run(debug=True)
