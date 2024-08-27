<h1 align="center">🎥 YouTube Video Downloader 🎥</h1>

<p align="center">
  A simple web app to download YouTube videos using Flask.<br>
  Простое веб-приложение для скачивания видео с YouTube на Flask.
</p>

---

## 🛠️ Requirements / Требования

- **Python 3.x**
- **Flask**
- **yt-dlp**
- **FFmpeg**: Required for merging video and audio streams.  
  **FFmpeg**: Требуется для объединения видео- и аудиопотоков.

---

## 🚀 Installation / Установка

1. **Clone the repository** / **Клонируйте репозиторий**:
   ```bash git clone https://github.com/hdream10/youtube-downloader.git```
   ```bash cd youtube-downloader```

2. **Install dependencies** / **Установите зависимости**:
   ```bash pip install -r requirements.txt```

3. **Ensure FFmpeg is installed** / **Убедитесь, что FFmpeg установлен**:
   - [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system's PATH.

---

## 🎯 Usage / Использование

1. **Run the Flask app** / **Запустите Flask приложение**:
   ```bash python app.py```

2. **Open in browser** / **Откройте в браузере**:
   - The front-end interface is served via the `index.html` file in the `static` directory.  
     Интерфейс обслуживается через файл `index.html` в каталоге `static`.
   - Open the `index.html` file directly in your browser to access the application.  
     Откройте файл `index.html` напрямую в вашем браузере, чтобы получить доступ к приложению.
   - Use the provided form in the browser to enter a YouTube URL and initiate the download.  
     Используйте предоставленную форму в браузере, чтобы ввести ссылку на YouTube и начать загрузку.

---

## ⚙️ Configuration / Конфигурация

- **Download Directory / Каталог загрузки**:
  - By default, videos are saved in the `downloads` directory. You can change this in the `app.py` file.  
    По умолчанию видео сохраняются в каталоге `downloads`. Вы можете изменить это в файле `app.py`.

- **Video Quality / Качество видео**:
  - Modify the `ydl_opts` dictionary in the `app.py` file to change the video quality settings.  
    Измените словарь `ydl_opts` в файле `app.py`, чтобы изменить настройки качества видео.