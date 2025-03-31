from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rotate', methods=['POST'])
def rotate_pdf():
    if 'pdf' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['pdf']
    direction = int(request.form.get('direction', 90))  # 기본은 오른쪽 90도

    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(direction)
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='rotated.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
