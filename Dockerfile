# Usar una imagen base oficial de Python (python:3.11-slim es eficiente)
FROM python:3.11-slim

# Establecer metadata del contenedor
LABEL maintainer="Proyecto Braille <info@braille.com>"
LABEL description="Sistema de Transcripción Braille - Aplicación Web"

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar archivo de dependencias primero (aprovecha el caché de Docker)
COPY requirements.txt ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Crear directorio para logs
RUN mkdir -p logs

# Exponer el puerto de Flask
EXPOSE 5000

# Variables de ambiente por defecto
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

# Comando de inicio: correr la aplicación
CMD ["python", "app.py"]
