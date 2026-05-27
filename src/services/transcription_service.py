"""
Servicio de Transcripción Braille

Esta capa de servicio actúa como intermediaria entre los controladores
y la lógica de negocio, implementando el patrón Service Layer.
"""

from typing import Dict, Any
from src.core.transcription_engine import BrailleTranscriptionEngine
from src.core.signage_generator import BrailleSignageGenerator
from io import BytesIO


class TranscriptionService:
    """Servicio para gestionar la transcripción y generación de señalética."""
    
    def __init__(self):
        """Inicializa el servicio con sus dependencias."""
        self._engine = BrailleTranscriptionEngine()
        self._generator = BrailleSignageGenerator()
    
    def transcribe_text(self, text: str) -> Dict[str, Any]:
        """
        Transcribe texto español a Braille.
        
        Args:
            text (str): Texto a transcribir
            
        Returns:
            Dict[str, Any]: Resultado con texto Braille o error
        """
        if not text or not text.strip():
            return {
                'success': False,
                'error': 'El texto no puede estar vacío'
            }
        
        try:
            # Validar caracteres soportados
            unsupported = self._engine.get_unsupported_characters(text)
            if unsupported:
                return {
                    'success': False,
                    'error': f'Caracteres no soportados: {", ".join(unsupported)}'
                }
            
            # Realizar transcripción
            braille_text = self._engine.transcribe(text)
            
            return {
                'success': True,
                'original_text': text,
                'braille_text': braille_text
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def generate_signage(self, original_text: str, braille_text: str) -> Dict[str, Any]:
        """
        Genera un documento PDF con señalética Braille.
        
        Args:
            original_text (str): Texto original
            braille_text (str): Texto en Braille
            
        Returns:
            Dict[str, Any]: Resultado con buffer PDF o error
        """
        try:
            pdf_buffer = self._generator.generate_pdf(original_text, braille_text)
            
            return {
                'success': True,
                'pdf_buffer': pdf_buffer,
                'filename': 'senaletica_braille.pdf'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al generar señalética: {str(e)}'
            }
    
    def validate_text(self, text: str) -> Dict[str, Any]:
        """
        Valida si un texto puede ser transcrito.
        
        Args:
            text (str): Texto a validar
            
        Returns:
            Dict[str, Any]: Resultado de validación
        """
        if not text or not text.strip():
            return {
                'valid': False,
                'message': 'El texto está vacío'
            }
        
        unsupported = self._engine.get_unsupported_characters(text)
        
        if unsupported:
            return {
                'valid': False,
                'message': f'Caracteres no soportados encontrados',
                'unsupported_chars': unsupported
            }
        
        return {
            'valid': True,
            'message': 'El texto es válido para transcripción'
        }
