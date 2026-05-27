"""
Test para verificar que el indicador de mayúsculas se incluye en el PDF
"""
import unittest
from src.core.signage_generator import BrailleSignageGenerator
from src.core.transcription_engine import BrailleTranscriptionEngine


class TestPDFCapitalIndicator(unittest.TestCase):
    """Verifica que el generador de PDF maneja correctamente el indicador de mayúsculas."""
    
    def setUp(self):
        self.engine = BrailleTranscriptionEngine()
        self.generator = BrailleSignageGenerator()
    
    def test_capital_indicator_in_braille_to_dots_mapping(self):
        """Verifica que el indicador de mayúsculas ⠨ está en el mapeo."""
        capital_sign = '⠨'
        self.assertIn(capital_sign, self.generator._BRAILLE_TO_DOTS)
        self.assertEqual(self.generator._BRAILLE_TO_DOTS[capital_sign], [4, 6])
    
    def test_pdf_generation_with_capitals(self):
        """Verifica que se puede generar PDF con texto que contiene mayúsculas."""
        original_text = "Buenas Tardes Estimada"
        braille_text = self.engine.transcribe(original_text)
        
        # Verificar que el texto Braille contiene indicadores de mayúsculas
        self.assertIn('⠨', braille_text)
        
        # Generar PDF (no debe lanzar excepciones)
        try:
            pdf_buffer = self.generator.generate_pdf(original_text, braille_text)
            self.assertIsNotNone(pdf_buffer)
            self.assertGreater(pdf_buffer.getbuffer().nbytes, 0)
            print(f"\n✅ PDF generado exitosamente")
            print(f"   Texto original: {original_text}")
            print(f"   Texto Braille: {braille_text}")
            print(f"   Tamaño PDF: {pdf_buffer.getbuffer().nbytes} bytes")
        except KeyError as e:
            self.fail(f"Falta mapeo para el carácter: {e}")
    
    def test_all_braille_characters_mapped(self):
        """Verifica que todos los caracteres generados por el motor están mapeados."""
        test_cases = [
            "Hola",
            "HOLA",
            "HoLa",
            "Buenas Tardes Estimada",
            "2025",
            "abc 123 ñáéíóú"
        ]
        
        unmapped_chars = set()
        
        for text in test_cases:
            braille_text = self.engine.transcribe(text)
            for char in braille_text:
                if char != ' ' and char not in self.generator._BRAILLE_TO_DOTS:
                    unmapped_chars.add(char)
        
        if unmapped_chars:
            self.fail(f"Caracteres Braille sin mapear: {unmapped_chars}")
        else:
            print(f"\n✅ Todos los caracteres Braille tienen mapeo en el generador de PDF")


if __name__ == '__main__':
    unittest.main(verbosity=2)
