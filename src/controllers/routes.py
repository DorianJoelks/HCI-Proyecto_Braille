"""
Controlador de Rutas Web

Este módulo define las rutas y controladores de la aplicación Flask,
siguiendo el patrón MVC (Model-View-Controller).
"""

from flask import Blueprint, render_template, request, jsonify, send_file
from src.services.transcription_service import TranscriptionService


# Crear blueprint para organizar rutas
main_bp = Blueprint('main', __name__)

# Instanciar servicio (Dependency Injection simple)
transcription_service = TranscriptionService()


@main_bp.route('/')
def index():
    """
    Renderiza la página principal de la aplicación.
    
    Returns:
        str: HTML de la página principal
    """
    return render_template('index.html')


@main_bp.route('/api/transcribe', methods=['POST'])
def transcribe():
    """
    Endpoint para transcribir texto a Braille.
    
    Espera JSON con formato: {"text": "texto a transcribir"}
    
    Returns:
        JSON: Resultado de la transcripción
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({
            'success': False,
            'error': 'Formato de solicitud inválido. Se requiere el campo "text".'
        }), 400
    
    text = data['text']
    result = transcription_service.transcribe_text(text)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@main_bp.route('/api/validate', methods=['POST'])
def validate():
    """
    Endpoint para validar si un texto puede ser transcrito.
    
    Espera JSON con formato: {"text": "texto a validar"}
    
    Returns:
        JSON: Resultado de la validación
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({
            'valid': False,
            'message': 'Formato de solicitud inválido'
        }), 400
    
    text = data['text']
    result = transcription_service.validate_text(text)
    
    return jsonify(result), 200


@main_bp.route('/api/generate-signage', methods=['POST'])
def generate_signage():
    """
    Endpoint para generar señalética Braille en formato PDF.
    
    Espera JSON con formato: {
        "original_text": "texto original",
        "braille_text": "texto en braille"
    }
    
    Returns:
        PDF: Archivo PDF con la señalética
    """
    data = request.get_json()
    
    if not data or 'original_text' not in data or 'braille_text' not in data:
        return jsonify({
            'success': False,
            'error': 'Se requieren los campos "original_text" y "braille_text"'
        }), 400
    
    original_text = data['original_text']
    braille_text = data['braille_text']
    
    result = transcription_service.generate_signage(original_text, braille_text)
    
    if result['success']:
        pdf_buffer = result['pdf_buffer']
        filename = result['filename']
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    else:
        return jsonify(result), 500


@main_bp.errorhandler(404)
def not_found(error):
    """
    Manejador de errores 404.
    
    Returns:
        JSON: Mensaje de error
    """
    return jsonify({
        'success': False,
        'error': 'Recurso no encontrado'
    }), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """
    Manejador de errores 500.
    
    Returns:
        JSON: Mensaje de error
    """
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500
