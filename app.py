from flask import Flask, request, send_file, jsonify
import yt_dlp
import re
import os
import uuid
import logging
import threading
import time

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DOWNLOAD_DIR = 'downloads'
EXPIRY_TIME = 24 * 60 * 60  # 24 hours
SERVER_URL = "http://127.0.0.1:3000"
PORT = 3000


def create_unique_directory(base_path=DOWNLOAD_DIR):
    unique_dir = os.path.join(base_path, str(uuid.uuid4()))
    os.makedirs(unique_dir, exist_ok=True)
    app.logger.debug(f"Created unique directory: {unique_dir}")
    return unique_dir


def sanitize_filename(filename):
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename).strip('-')
    return filename


def download_video(url, download_dir):
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Получаем оригинальное название и расширение
            original_filename = sanitize_filename(info_dict['title'])
            ext = info_dict.get('ext', 'mp4')

            # Формируем путь к финальному файлу
            temp_file_path = os.path.join(
                download_dir, f"{original_filename}.{ext}")

            # Переименовываем файл, если требуется
            # yt-dlp может создавать файл с разным именем, поэтому убедимся, что его переименовали
            for temp_file in os.listdir(download_dir):
                if temp_file.endswith(f".{ext}"):
                    original_file_path = os.path.join(download_dir, temp_file)
                    if temp_file_path != original_file_path:
                        os.rename(original_file_path, temp_file_path)
                        app.logger.debug(f"Renamed file to: {temp_file_path}")
                    break

            app.logger.debug(f"Video downloaded to: {temp_file_path}")
            return temp_file_path
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        raise e


def delete_expired_files():
    while True:
        now = time.time()
        for dirpath, _, files in os.walk(DOWNLOAD_DIR):
            for file in files:
                file_path = os.path.join(dirpath, file)
                if os.path.getmtime(file_path) < now - EXPIRY_TIME:
                    os.remove(file_path)
                    app.logger.debug(f"Removed file: {file_path}")

            # Remove empty directories
            for dirpath, dirs, _ in os.walk(DOWNLOAD_DIR, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(dirpath, dir)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        app.logger.debug(
                            f"Removed empty directory: {dir_path}")

        time.sleep(3600)  # Check every hour


def start_cleanup_thread():
    thread = threading.Thread(target=delete_expired_files, daemon=True)
    thread.start()


@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')

    if not url:
        app.logger.error("URL is required")
        return "URL is required", 400

    download_dir = create_unique_directory()

    try:
        output_file = download_video(url, download_dir)

        # Generate full URL for downloading the file
        full_url = f"{SERVER_URL}/{output_file}"

        # Returning URL that points to the downloadable file
        return jsonify({'download_url': full_url}), 200

    except Exception as e:
        app.logger.error(f"Error processing download request: {str(e)}")
        return f"Error: {str(e)}", 500


@app.route('/downloads/<uniqdir>/<filename>')
def serve_file(uniqdir, filename):
    full_url = f"{uniqdir}/{filename}"
    file_path = os.path.join(DOWNLOAD_DIR, full_url)

    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404


@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == "__main__":
    start_cleanup_thread()
    app.run(port = PORT)
