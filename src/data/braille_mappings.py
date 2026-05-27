"""
Módulo de Mapeos Braille

Este módulo contiene todos los mapeos necesarios para la transcripción
de texto español a Braille, incluyendo el alfabeto, números, acentuadas y signos.

Estructura del Cuadratín (6 puntos):
    1 • • 4
    2 • • 5
    3 • • 6
"""

from typing import Dict


class BrailleMappings:
    """Clase que centraliza todos los mapeos del sistema Braille."""
    
    # Signo especial para números
    NUMBER_SIGN: str = "⠼"
    
    # Signo especial para mayúsculas (puntos 4,6)
    CAPITAL_SIGN: str = "⠨"
    
    # Primera Serie (a-j): Puntos 1,2,4,5
    _FIRST_SERIES: Dict[str, str] = {
        'a': '⠁',  # punto 1
        'b': '⠃',  # puntos 1,2
        'c': '⠉',  # puntos 1,4
        'd': '⠙',  # puntos 1,4,5
        'e': '⠑',  # puntos 1,5
        'f': '⠋',  # puntos 1,2,4
        'g': '⠛',  # puntos 1,2,4,5
        'h': '⠓',  # puntos 1,2,5
        'i': '⠊',  # puntos 2,4
        'j': '⠚',  # puntos 2,4,5
    }
    
    # Segunda Serie (k-t): Primera Serie + punto 3
    _SECOND_SERIES: Dict[str, str] = {
        'k': '⠅',  # puntos 1,3
        'l': '⠇',  # puntos 1,2,3
        'm': '⠍',  # puntos 1,3,4
        'n': '⠝',  # puntos 1,3,4,5
        'o': '⠕',  # puntos 1,3,5
        'p': '⠏',  # puntos 1,2,3,4
        'q': '⠟',  # puntos 1,2,3,4,5
        'r': '⠗',  # puntos 1,2,3,5
        's': '⠎',  # puntos 2,3,4
        't': '⠞',  # puntos 2,3,4,5
    }
    
    # Tercera Serie (u-z): Primera Serie + puntos 3,6
    _THIRD_SERIES: Dict[str, str] = {
        'u': '⠥',  # puntos 1,3,6
        'v': '⠧',  # puntos 1,2,3,6
        'x': '⠭',  # puntos 1,3,4,6
        'y': '⠽',  # puntos 1,3,4,5,6
        'z': '⠵',  # puntos 1,3,5,6
    }
    
    # Letras adicionales del español
    _ADDITIONAL_LETTERS: Dict[str, str] = {
        'ñ': '⠻',  # puntos 1,2,4,5,6
        'w': '⠺',  # puntos 2,4,5,6
    }
    
    # Vocales acentuadas
    _ACCENTED_VOWELS: Dict[str, str] = {
        'á': '⠷',  # puntos 1,2,3,5,6
        'é': '⠮',  # puntos 2,3,4,6
        'í': '⠌',  # puntos 3,4
        'ó': '⠬',  # puntos 3,4,6
        'ú': '⠾',  # puntos 2,3,4,5,6
        'ü': '⠳',  # puntos 1,2,5,6
    }
    
    # Signos de puntuación básicos
    _PUNCTUATION: Dict[str, str] = {
        '.': '⠲',  # puntos 2,5,6
        ',': '⠂',  # punto 2
        ';': '⠆',  # puntos 2,3
        ':': '⠒',  # puntos 2,5
        '¿': '⠢',  # puntos 2,6
        '?': '⠦',  # puntos 2,3,6
        '¡': '⠖',  # puntos 2,3,5
        '!': '⠖',  # puntos 2,3,5
        '(': '⠐⠣',  # puntos 5 + 1,2,6
        ')': '⠐⠜',  # puntos 5 + 3,4,5
        '-': '⠤',  # puntos 3,6
        ' ': ' ',  # espacio
    }
    
    # Números (mapean a primera serie con signo de número)
    _NUMBERS: Dict[str, str] = {
        '1': '⠁',
        '2': '⠃',
        '3': '⠉',
        '4': '⠙',
        '5': '⠑',
        '6': '⠋',
        '7': '⠛',
        '8': '⠓',
        '9': '⠊',
        '0': '⠚',
    }
    
    @classmethod
    def get_alphabet_mapping(cls) -> Dict[str, str]:
        """
        Obtiene el mapeo completo del alfabeto español a Braille.
        
        Returns:
            Dict[str, str]: Diccionario con el mapeo de letras a Braille
        """
        alphabet = {}
        alphabet.update(cls._FIRST_SERIES)
        alphabet.update(cls._SECOND_SERIES)
        alphabet.update(cls._THIRD_SERIES)
        alphabet.update(cls._ADDITIONAL_LETTERS)
        alphabet.update(cls._ACCENTED_VOWELS)
        return alphabet
    
    @classmethod
    def get_number_mapping(cls) -> Dict[str, str]:
        """
        Obtiene el mapeo de números a Braille.
        
        Returns:
            Dict[str, str]: Diccionario con el mapeo de números a Braille
        """
        return cls._NUMBERS.copy()
    
    @classmethod
    def get_punctuation_mapping(cls) -> Dict[str, str]:
        """
        Obtiene el mapeo de signos de puntuación a Braille.
        
        Returns:
            Dict[str, str]: Diccionario con el mapeo de signos a Braille
        """
        return cls._PUNCTUATION.copy()
    
    @classmethod
    def get_complete_mapping(cls) -> Dict[str, str]:
        """
        Obtiene el mapeo completo de todos los caracteres soportados.
        
        Returns:
            Dict[str, str]: Diccionario con todos los mapeos
        """
        complete = {}
        complete.update(cls.get_alphabet_mapping())
        complete.update(cls.get_punctuation_mapping())
        return complete
