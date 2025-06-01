# Imagen base de Python
FROM python:3.10-slim

# Crear directorio en el contenedor
WORKDIR /app

# Copiar archivos del backend
COPY backend/ ./backend/

# Copiar frontend también (por si se usa en algún momento)
COPY frontend/ ./frontend/

# Instalar herramientas necesarias para compilar PyAudio
RUN apt-get update && apt-get install -y gcc libportaudio2 libasound2-dev portaudio19-dev libffi-dev

# Copiar e instalar dependencias
COPY backend/requirements25.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt


# Exponer el puerto de Flask
EXPOSE 5000

# Comando para ejecutar el backend
CMD ["python", "./backend/app.py"]

# Instalar dependencias del sistema necesarias para PyAudio, OpenCV y GTK
RUN apt-get update && apt-get install -y \
    gcc \
    libportaudio2 \
    libasound2-dev \
    portaudio19-dev \
    libffi-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*


