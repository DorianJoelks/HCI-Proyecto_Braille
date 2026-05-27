"""
Tests para el Motor de Transcripción Braille

Suite de pruebas unitarias para validar la funcionalidad del motor de transcripción.
"""

import unittest
from src.core.transcription_engine import BrailleTranscriptionEngine


class TestBrailleTranscriptionEngine(unittest.TestCase):
    """Tests para el motor de transcripción."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.engine = BrailleTranscriptionEngine()
    
    def test_transcribe_first_series(self):
        """Test transcripción de primera serie (a-j)."""
        # Arrange
        text = "abcdefghij"
        expected = "⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚"
        
        # Act
        result = self.engine.transcribe(text)
        
        # Assert
        self.assertEqual(result, expected)
    
    def test_transcribe_second_series(self):
        """Test transcripción de segunda serie (k-t)."""
        text = "klmnopqrst"
        expected = "⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞"
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_third_series(self):
        """Test transcripción de tercera serie (u-z)."""
        text = "uvxyz"
        expected = "⠥⠧⠭⠽⠵"
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_special_letters(self):
        """Test transcripción de letras especiales (ñ, w)."""
        text = "ñw"
        expected = "⠻⠺"
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_accented_vowels(self):
        """Test transcripción de vocales acentuadas."""
        text = "áéíóúü"
        expected = "⠷⠮⠌⠬⠾⠳"
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_single_digit(self):
        """Test transcripción de un solo dígito."""
        text = "5"
        expected = "⠼ ⠑"  # Signo de número + espacio + patrón de 'e'
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_multiple_digits(self):
        """Test transcripción de múltiples dígitos."""
        text = "123"
        expected = "⠼ ⠁ ⠃ ⠉"  # Signo de número + espacios + abc
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_punctuation(self):
        """Test transcripción de signos de puntuación."""
        text = ".,"
        expected = "⠲⠂"
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_complete_sentence(self):
        """Test transcripción de oración completa."""
        text = "Baño 2"
        # 'B' -> b, 'a' -> a, 'ñ' -> ñ, 'o' -> o, ' ' -> espacio, '2' -> signo + b
        
        result = self.engine.transcribe(text)
        
        # Verificar que contiene los elementos esperados
        self.assertIn('⠃', result)  # b
        self.assertIn('⠁', result)  # a
        self.assertIn('⠻', result)  # ñ
        self.assertIn('⠕', result)  # o
        self.assertIn(' ', result)  # espacio
        self.assertIn('⠼', result)  # signo de número
    
    def test_transcribe_empty_string(self):
        """Test transcripción de cadena vacía."""
        text = ""
        expected = ""
        
        result = self.engine.transcribe(text)
        
        self.assertEqual(result, expected)
    
    def test_transcribe_uppercase_with_capital_indicator(self):
        """Test que mayúsculas se transcriben con el indicador capital (⠨)."""
        # Minúsculas sin indicador
        text_lower = "hola"
        expected_lower = "⠓⠕⠇⠁"
        result_lower = self.engine.transcribe(text_lower)
        self.assertEqual(result_lower, expected_lower)
        
        # Todo en mayúsculas con indicador antes de cada letra
        text_upper = "HOLA"
        expected_upper = "⠨⠓⠨⠕⠨⠇⠨⠁"
        result_upper = self.engine.transcribe(text_upper)
        self.assertEqual(result_upper, expected_upper)
        
        # Caso mixto: primera letra mayúscula
        text_mixed = "Hola"
        expected_mixed = "⠨⠓⠕⠇⠁"
        result_mixed = self.engine.transcribe(text_mixed)
        self.assertEqual(result_mixed, expected_mixed)
        
        # Verificar que lowercase y uppercase son diferentes
        self.assertNotEqual(result_lower, result_upper)
    
    def test_unsupported_character_raises_error(self):
        """Test que caracteres no soportados lanzan error."""
        text = "test@email.com"
        
        with self.assertRaises(ValueError):
            self.engine.transcribe(text)
    
    def test_is_character_supported(self):
        """Test verificación de caracteres soportados."""
        # Caracteres soportados
        self.assertTrue(self.engine.is_character_supported('a'))
        self.assertTrue(self.engine.is_character_supported('ñ'))
        self.assertTrue(self.engine.is_character_supported('5'))
        self.assertTrue(self.engine.is_character_supported('.'))
        
        # Caracteres no soportados
        self.assertFalse(self.engine.is_character_supported('@'))
        self.assertFalse(self.engine.is_character_supported('#'))
    
    def test_get_unsupported_characters(self):
        """Test identificación de caracteres no soportados."""
        text = "Hola@mundo#2024"
        
        unsupported = self.engine.get_unsupported_characters(text)
        
        self.assertIn('@', unsupported)
        self.assertIn('#', unsupported)
        self.assertEqual(len(unsupported), 2)


if __name__ == '__main__':
    unittest.main()
