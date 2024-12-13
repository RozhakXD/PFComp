import time, os
from flask import Blueprint, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from .utils import compress_pdf, schedule_file_deletion

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/v1/compress', methods=['POST', 'GET'])
def compress_pdf_route():
    if request.method != 'GET':
        files = request.files.get('file')
        if not files or not files.filename.endswith('.pdf'):
            return jsonify(
                message='Invalid file. Please upload a PDF file!',
                status='error'
            ), 400
        file_name = secure_filename(files.filename)
        upload_path = os.path.join('app/static/uploads', file_name)
        files.save(upload_path)

        compressed_file_name = f'PFComp_{file_name.replace(".pdf", "")}_{int(time.time())}.pdf'
        compressed_file_path = os.path.join('app/static/uploads', compressed_file_name)

        success = compress_pdf(upload_path, compressed_file_path, quality='ebook')
        os.remove(upload_path)
        if not success:
            return jsonify(
                message='Compression failed! Please try again.',
                status='error'
            ), 500
        
        schedule_file_deletion(compressed_file_path, delay=1800)

        return jsonify(
            message='Compression successful!',
            status='success',
            download_url=f'/downloads/{compressed_file_name}'
        )
    else:
        return jsonify(
            message='Invalid request method!',
            status='error'
        ), 405

@main.route('/downloads/<filename>')
def downloads_files(filename):
    directory = os.path.abspath(os.path.join('app/static/uploads'))
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        return jsonify(
            message='File not found!',
            status='error'
        ), 404
    return send_from_directory(directory, filename, as_attachment=True)