"""
Aplicación Principal Flask

Este módulo configura e inicializa la aplicación Flask,
registra blueprints y configura middleware.
"""

import os
from flask import Flask
from src.controllers.routes import main_bp


def create_app(config_name: str = 'development') -> Flask:
    """
    Factory para crear y configurar la aplicación Flask.
    
    Args:
        config_name (str): Nombre de la configuración a usar
        
    Returns:
        Flask: Aplicación Flask configurada
    """
    app = Flask(__name__,
                template_folder='src/templates',
                static_folder='src/static')
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_AS_ASCII'] = False  # Soporte para caracteres Unicode (Braille)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Límite de 16MB
    
    # Configuración específica por ambiente
    if config_name == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    elif config_name == 'testing':
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
    else:  # development
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    
    # Logging básico
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/braille_app.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Aplicación Braille iniciada')
    
    return app


def main():
    """Punto de entrada principal de la aplicación."""
    # Obtener configuración del ambiente
    config = os.environ.get('FLASK_ENV', 'development')
    
    # Crear aplicación
    app = create_app(config)
    
    # Obtener configuración del servidor
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = app.config['DEBUG']
    
    # Iniciar servidor
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
