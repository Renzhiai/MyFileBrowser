# coding = utf-8
# !/usr/bin/python
from config import C
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)


@app.errorhandler(500)
def internal_server_error(e):
    return '文件路径不存在'

# root路径最后带斜杆
if not C.ROOT_PATH.endswith(os.sep):
    ROOT_PATH = C.ROOT_PATH + os.sep

@app.route('/', methods=['GET', 'POST'])
@app.route('/<current_relative_path>', methods=['GET', 'POST'])
def index(current_relative_path=None):

    if current_relative_path:
        current_absolute_path = os.path.join(ROOT_PATH, current_relative_path)
    else:
        current_absolute_path = ROOT_PATH
    result = []
    for file_name in os.listdir(current_absolute_path):
        file_absolute_path = os.path.join(current_absolute_path, file_name)
        is_dir = os.path.isdir(file_absolute_path)
        file_relative_path = file_absolute_path.replace(ROOT_PATH, '')
        result.append([file_name, file_relative_path, is_dir])
    return render_template('index.html', data=result)


@app.route('/download/<file_path>')
def download_file(file_path):
    file_path = os.path.join(ROOT_PATH, file_path)
    head, tail = os.path.split(file_path)
    return send_from_directory(head, tail, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
