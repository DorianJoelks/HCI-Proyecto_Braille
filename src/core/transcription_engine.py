"""
Motor de Transcripción Braille

Este módulo contiene la lógica principal para transcribir texto español a Braille,
siguiendo las reglas del sistema Braille Español.
"""

from typing import List
import re
from src.data.braille_mappings import BrailleMappings


class BrailleTranscriptionEngine:
    """Motor principal de transcripción de texto español a Braille."""
    
    # Constantes de validación
    MAX_TEXT_LENGTH = 500  # Límite máximo de caracteres
    MAX_CONSECUTIVE_SPACES = 2  # Máximo de espacios consecutivos permitidos
    
    def __init__(self):
        """Inicializa el motor de transcripción con los mapeos necesarios."""
        self._alphabet = BrailleMappings.get_alphabet_mapping()
        self._numbers = BrailleMappings.get_number_mapping()
        self._punctuation = BrailleMappings.get_punctuation_mapping()
        self._number_sign = BrailleMappings.NUMBER_SIGN
        self._capital_sign = BrailleMappings.CAPITAL_SIGN
    
    def transcribe(self, text: str) -> str:
        """
        Transcribe un texto completo de español a Braille.
        
        Técnicas de prueba aplicadas:
        - Partición de Equivalencias: Letras (a-z), números (0-9), puntuación, acentos
        - Análisis de Valores Límite: Texto vacío, longitud máxima (500 caracteres)
        - Pruebas de Robustez: Múltiples espacios, puntuación duplicada, mayúsculas
        
        Mayúsculas en Braille:
        - Se indica con el signo ⠨ (puntos 4,6) antes de la letra
        - Ejemplo: "Hola" → "⠨⠓⠕⠇⠁"
        
        Args:
            text (str): Texto en español a transcribir
            
        Returns:
            str: Texto transcrito a Braille
            
        Raises:
            ValueError: Si el texto contiene caracteres no soportados o excede límites
        """
        # Validación 1: Texto vacío
        if not text or not text.strip():
            return ""
        
        # Validación 2: Límite de longitud
        if len(text) > self.MAX_TEXT_LENGTH:
            raise ValueError(
                f"El texto excede el límite máximo de {self.MAX_TEXT_LENGTH} caracteres. "
                f"Longitud actual: {len(text)}"
            )
        
        # Normalización: Eliminar espacios al inicio y final
        text = text.strip()
        
        # Normalización: Reducir múltiples espacios consecutivos a uno solo
        text = self._normalize_spaces(text)
        
        # Validación 3: Verificar caracteres no soportados antes de procesar
        unsupported = self.get_unsupported_characters(text)
        if unsupported:
            raise ValueError(
                f"El texto contiene caracteres no soportados: {', '.join(repr(c) for c in unsupported)}"
            )
        
        result_chars: List[str] = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # Procesar números (pueden ser múltiples dígitos)
            if char.isdigit():
                number_sequence, digits_processed = self._process_number_sequence(text, i)
                result_chars.append(number_sequence)
                i += digits_processed
                continue
            
            # Procesar letras (manteniendo mayúsculas)
            char_lower = char.lower()
            if char_lower in self._alphabet:
                # Si es mayúscula, agregar el signo de mayúscula antes
                if char.isupper():
                    result_chars.append(self._capital_sign)
                result_chars.append(self._alphabet[char_lower])
            # Procesar signos de puntuación
            elif char in self._punctuation:
                # Evitar puntuación duplicada consecutiva (excepto espacios)
                if char != ' ' and result_chars and result_chars[-1] == self._punctuation[char]:
                    # Saltar puntuación duplicada
                    i += 1
                    continue
                result_chars.append(self._punctuation[char])
            # Espacio (ya manejado en _punctuation, pero por claridad)
            elif char == ' ':
                result_chars.append(' ')
            
            i += 1
        
        # Post-procesamiento: Limpiar espacios múltiples en el resultado
        result = ''.join(result_chars)
        result = re.sub(r' {2,}', ' ', result)  # Reducir múltiples espacios a uno
        result = result.strip()  # Eliminar espacios al inicio/final
        
        return result
    
    def _normalize_spaces(self, text: str) -> str:
        """
        Normaliza espacios en el texto.
        
        - Reduce múltiples espacios consecutivos a uno solo
        - Elimina espacios antes/después de puntuación
        
        Args:
            text (str): Texto a normalizar
            
        Returns:
            str: Texto con espacios normalizados
        """
        # Reducir múltiples espacios a uno solo
        text = re.sub(r' {2,}', ' ', text)
        
        # Eliminar espacios antes de puntuación de cierre
        text = re.sub(r' +([.,;:?!)])', r'\1', text)
        
        # Eliminar espacios después de puntuación de apertura
        text = re.sub(r'([¿¡(]) +', r'\1', text)
        
        return text
    
    def _process_number_sequence(self, text: str, start_index: int) -> tuple[str, int]:
        """
        Procesa una secuencia de números según las reglas Braille.
        
        Maneja:
        - Números enteros: 123 → ⠼ ⠁ ⠃ ⠉ (con espacios entre dígitos)
        - Números con punto decimal: 12.5 → ⠼ ⠁ ⠃ ⠲ ⠑
        - Números con coma decimal: 12,5 → ⠼ ⠁ ⠃ ⠂ ⠑
        
        Args:
            text (str): Texto completo
            start_index (int): Índice donde comienza la secuencia numérica
            
        Returns:
            tuple[str, int]: (Secuencia en Braille, cantidad de caracteres procesados)
        """
        braille_numbers = [self._number_sign]
        digits_processed = 0
        i = start_index
        
        while i < len(text):
            char = text[i]
            
            # Procesar dígitos
            if char.isdigit():
                braille_numbers.append(' ')  # Espacio antes de cada dígito
                braille_numbers.append(self._numbers[char])
                digits_processed += 1
                i += 1
            # Procesar separadores decimales (punto o coma)
            elif char in ['.', ','] and i + 1 < len(text) and text[i + 1].isdigit():
                # Verificar que hay un dígito después del separador
                braille_numbers.append(' ')  # Espacio antes del separador
                braille_numbers.append(self._punctuation[char])
                digits_processed += 1
                i += 1
            else:
                # Fin de la secuencia numérica
                break
        
        return ''.join(braille_numbers), digits_processed
    
    def is_character_supported(self, char: str) -> bool:
        """
        Verifica si un carácter es soportado por el sistema.
        
        Técnica: Partición de Equivalencias
        - Clase 1: Letras del alfabeto (a-z, ñ, vocales acentuadas)
        - Clase 2: Números (0-9)
        - Clase 3: Puntuación soportada
        - Clase 4: Espacios en blanco
        
        Args:
            char (str): Carácter a verificar
            
        Returns:
            bool: True si el carácter es soportado, False en caso contrario
        """
        # Normalizar a minúsculas para verificación
        char_lower = char.lower()
        
        return (char_lower in self._alphabet or 
                char in self._punctuation or 
                char.isdigit() or
                char.isspace())
    
    def get_unsupported_characters(self, text: str) -> List[str]:
        """
        Identifica caracteres no soportados en un texto.
        
        Técnica: Análisis de Valores Frontera
        - Identifica caracteres especiales no soportados
        - Ordena alfabéticamente para mejor legibilidad
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            List[str]: Lista de caracteres no soportados (sin duplicados, ordenados)
        """
        unsupported = set()
        
        for char in text:
            if not self.is_character_supported(char):
                unsupported.add(char)
        
        return sorted(unsupported)
    
    def validate_text_length(self, text: str) -> bool:
        """
        Valida que el texto no exceda el límite máximo.
        
        Técnica: Análisis de Valores Límite
        - Valor mínimo: 0 caracteres (válido)
        - Valor máximo: MAX_TEXT_LENGTH caracteres (válido)
        - Valor límite superior: MAX_TEXT_LENGTH + 1 (inválido)
        
        Args:
            text (str): Texto a validar
            
        Returns:
            bool: True si la longitud es válida, False en caso contrario
        """
        return len(text) <= self.MAX_TEXT_LENGTH
    
    def get_validation_errors(self, text: str) -> List[str]:
        """
        Obtiene una lista de errores de validación para un texto.
        
        Técnica: Pruebas de Robustez
        - Valida múltiples condiciones
        - Retorna todos los errores encontrados
        
        Args:
            text (str): Texto a validar
            
        Returns:
            List[str]: Lista de mensajes de error (vacía si no hay errores)
        """
        errors = []
        
        # Error 1: Texto vacío después de normalizar
        if not text or not text.strip():
            errors.append("El texto está vacío o solo contiene espacios")
            return errors  # No tiene sentido validar más si está vacío
        
        # Error 2: Excede longitud máxima
        if not self.validate_text_length(text):
            errors.append(
                f"El texto excede el límite de {self.MAX_TEXT_LENGTH} caracteres "
                f"(actual: {len(text)})"
            )
        
        # Error 3: Caracteres no soportados
        unsupported = self.get_unsupported_characters(text)
        if unsupported:
            chars_display = ', '.join(repr(c) for c in unsupported[:10])  # Mostrar máximo 10
            if len(unsupported) > 10:
                chars_display += f" y {len(unsupported) - 10} más"
            errors.append(f"Caracteres no soportados: {chars_display}")
        
        return errors
