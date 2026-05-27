#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Pruebas Finales para Merge a Main
Verifica todas las funcionalidades antes de fusionar develop con main
"""

from src.core.transcription_engine import BrailleTranscriptionEngine
import sys

def print_header(title):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def test_case(engine, text, description=""):
    """Ejecuta un caso de prueba y muestra los resultados."""
    try:
        result = engine.transcribe(text)
        status = "✓ PASS"
        error = None
    except Exception as e:
        result = None
        status = "✗ FAIL"
        error = str(e)
    
    print(f"{status} | {description if description else text}")
    print(f"     Input:  '{text}'")
    if result:
        print(f"     Output: '{result}'")
        print(f"     Repr:   {repr(result)}")
    else:
        print(f"     ERROR:  {error}")
    print()
    
    return status == "✓ PASS"

def main():
    """Ejecuta todas las pruebas finales."""
    engine = BrailleTranscriptionEngine()
    passed = 0
    total = 0
    
    print_header("PRUEBAS FINALES PARA MERGE - SISTEMA TRANSCRIPCIÓN BRAILLE")
    
    # ========== PRUEBAS SOLICITADAS POR EL USUARIO ==========
    print_header("1. PRUEBAS ESPECÍFICAS DEL USUARIO")
    
    user_tests = [
        ("Buenas tardes!", "Saludo con mayúscula inicial y exclamación"),
        ("nov 2025", "Texto con año"),
        ("Niño", "Palabra con ñ y mayúscula"),
        ("FIS-EPN", "Siglas en mayúsculas con guion"),
        ("20,15", "Número decimal con coma"),
        ("46.37", "Número decimal con punto"),
        ("25-11-2025", "Fecha completa con guiones"),
        ("sandía", "Vocal acentuada (í)"),
    ]
    
    for text, desc in user_tests:
        total += 1
        if test_case(engine, text, desc):
            passed += 1
    
    # ========== PRUEBAS DE MAYÚSCULAS ==========
    print_header("2. PRUEBAS DE MAYÚSCULAS (Indicador ⠨)")
    
    uppercase_tests = [
        ("HOLA", "Todo en mayúsculas"),
        ("Hola", "Primera letra mayúscula"),
        ("HoLa", "Mayúsculas mezcladas"),
        ("Hola Mundo", "Múltiples palabras con mayúsculas"),
        ("STOP", "Palabra en mayúsculas"),
    ]
    
    for text, desc in uppercase_tests:
        total += 1
        if test_case(engine, text, desc):
            passed += 1
    
    # ========== PRUEBAS DE NÚMEROS ==========
    print_header("3. PRUEBAS DE NÚMEROS (Indicador ⠼ con espacios)")
    
    number_tests = [
        ("0", "Número cero"),
        ("5", "Un solo dígito"),
        ("123", "Múltiples dígitos"),
        ("2025", "Año 2025"),
        ("0123456789", "Todos los dígitos"),
        ("12.5", "Decimal con punto"),
        ("12,5", "Decimal con coma"),
        ("3.1416", "Número PI"),
        ("19,99", "Precio con coma"),
    ]
    
    for text, desc in number_tests:
        total += 1
        if test_case(engine, text, desc):
            passed += 1
    
    # ========== PRUEBAS DE CARACTERES ESPECIALES ==========
    print_header("4. PRUEBAS DE CARACTERES ESPECIALES DEL ESPAÑOL")
    
    special_tests = [
        ("ñ", "Letra ñ minúscula"),
        ("Ñ", "Letra ñ mayúscula"),
        ("niño", "Palabra con ñ"),
        ("Ñoño", "Ñ mayúscula y minúscula"),
        ("mañana", "Ñ en medio de palabra"),
        ("áéíóú", "Todas las vocales acentuadas"),
        ("Ángel", "Vocal acentuada con mayúscula"),
        ("María José", "Nombres con acentos"),
        ("ü", "Vocal con diéresis"),
    ]
    
    for text, desc in special_tests:
        total += 1
        if test_case(engine, text, desc):
            passed += 1
    
    # ========== PRUEBAS DE PUNTUACIÓN ==========
    print_header("5. PRUEBAS DE PUNTUACIÓN")
    
    punctuation_tests = [
        (".,;:", "Puntuación básica"),
        ("¿Cómo?", "Signos de interrogación"),
        ("¡Hola!", "Signos de exclamación"),
        ("(test)", "Paréntesis"),
        ("Pregunta: ¿Cómo estás?", "Oración con puntuación"),
        ("Hola, ¿cómo estás?", "Múltiples signos"),
    ]
    
    for text, desc in punctuation_tests:
        total += 1
        if test_case(engine, text, desc):
            passed += 1
    
    # ========== PRUEBAS MIXTAS COMPLEJAS ==========
    print_header("6. PRUEBAS MIXTAS COMPLEJAS")
    
    complex_tests = [
        ("Año 2025", "Mayúscula + número"),
        ("Teléfono: 555-1234", "Texto con números y guiones"),
        ("Dirección 123, Quito", "Dirección completa"),
        ("abc123xyz", "Letras y números mezclados"),
        ("FIS-EPN 2025", "Siglas con año"),
        ("Información123, ¿verdad?", "Caso complejo del test"),
        ("PI: 3.1416", "Constante matemática"),
    ]
    
    for text, desc in complex_tests:
        total += 1
        if test_case(engine, text, desc):
            passed += 1
    
    # ========== RESUMEN FINAL ==========
    print_header("RESUMEN DE PRUEBAS")
    
    print(f"Total de pruebas ejecutadas: {total}")
    print(f"Pruebas exitosas:            {passed}")
    print(f"Pruebas fallidas:            {total - passed}")
    print(f"Tasa de éxito:               {(passed/total)*100:.1f}%")
    print()
    
    if passed == total:
        print("✓✓✓ TODAS LAS PRUEBAS PASARON ✓✓✓")
        print("El sistema está listo para merge a main")
        print()
        return 0
    else:
        print("✗✗✗ ALGUNAS PRUEBAS FALLARON ✗✗✗")
        print("Revisar los errores antes de hacer merge")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
