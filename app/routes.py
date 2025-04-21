import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from .utils import process_image_external, image_gen_replica

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    output_file = ''
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            print(file.filename)
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            try:
                # Send the file to an external conversion service
                output_path = image_gen_replica(upload_path)
                output_file = output_path.split('/')[-1]
                print("Done!", output_path)
            except Exception as e:
                flash(f"Image conversion failed: {str(e)}")

    return render_template('index.html', output_image=output_file)
