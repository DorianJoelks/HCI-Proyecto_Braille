"""
Generador de Señalética Braille

Este módulo genera documentos PDF de alta calidad con representaciones
visuales del Braille para impresión de señalética.
"""

from io import BytesIO
from typing import Tuple
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, grey


class BrailleSignageGenerator:
    """Genera documentos PDF con señalética Braille."""
    
    # Constantes de diseño (en mm)
    BRAILLE_DOT_RADIUS = 1.5  # Radio del punto Braille
    BRAILLE_DOT_SPACING_H = 2.5  # Espaciado horizontal entre puntos
    BRAILLE_DOT_SPACING_V = 2.5  # Espaciado vertical entre puntos
    BRAILLE_CELL_WIDTH = 7.0  # Ancho de una celda Braille
    BRAILLE_CELL_HEIGHT = 10.0  # Alto de una celda Braille
    MARGIN_TOP = 50  # Margen superior
    MARGIN_LEFT = 30  # Margen izquierdo
    LINE_SPACING = 15  # Espaciado entre líneas
    TEXT_BRAILLE_SPACING = 8  # Espacio entre texto tinta y Braille
    
    # Mapeo de caracteres Braille Unicode a patrones de puntos
    _BRAILLE_TO_DOTS = {
        '⠁': [1], '⠃': [1, 2], '⠉': [1, 4], '⠙': [1, 4, 5],
        '⠑': [1, 5], '⠋': [1, 2, 4], '⠛': [1, 2, 4, 5], '⠓': [1, 2, 5],
        '⠊': [2, 4], '⠚': [2, 4, 5], '⠅': [1, 3], '⠇': [1, 2, 3],
        '⠍': [1, 3, 4], '⠝': [1, 3, 4, 5], '⠕': [1, 3, 5], '⠏': [1, 2, 3, 4],
        '⠟': [1, 2, 3, 4, 5], '⠗': [1, 2, 3, 5], '⠎': [2, 3, 4], '⠞': [2, 3, 4, 5],
        '⠥': [1, 3, 6], '⠧': [1, 2, 3, 6], '⠭': [1, 3, 4, 6], '⠽': [1, 3, 4, 5, 6],
        '⠵': [1, 3, 5, 6], '⠻': [1, 2, 4, 5, 6], '⠺': [2, 4, 5, 6],
        '⠷': [1, 2, 3, 5, 6], '⠮': [2, 3, 4, 6], '⠌': [3, 4], '⠬': [3, 4, 6],
        '⠾': [2, 3, 4, 5, 6], '⠳': [1, 2, 5, 6], '⠲': [2, 5, 6], '⠂': [2],
        '⠆': [2, 3], '⠒': [2, 5], '⠢': [2, 6], '⠦': [2, 3, 6],
        '⠖': [2, 3, 5], '⠤': [3, 6], '⠼': [3, 4, 5, 6], '⠣': [1, 2, 6],
        '⠜': [3, 4, 5], '⠐': [5], '⠨': [4, 6], ' ': []
    }
    
    def __init__(self, page_size: Tuple[float, float] = A4):
        """
        Inicializa el generador de señalética.
        
        Args:
            page_size: Tamaño de página (por defecto A4)
        """
        self.page_size = page_size
    
    def generate_pdf(self, original_text: str, braille_text: str) -> BytesIO:
        """
        Genera un documento PDF con el texto original y su transcripción Braille.
        
        Args:
            original_text (str): Texto original en español
            braille_text (str): Texto transcrito a Braille
            
        Returns:
            BytesIO: Buffer con el contenido del PDF
        """
        buffer = BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=self.page_size)
        
        # Configurar título del documento
        pdf_canvas.setTitle("Señalética Braille")
        
        # Posición inicial
        x_pos = self.MARGIN_LEFT * mm
        y_pos = self.page_size[1] - (self.MARGIN_TOP * mm)
        
        # Dibujar texto original
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.setFillColor(black)
        pdf_canvas.drawString(x_pos, y_pos, original_text)
        
        # Mover posición para Braille
        y_pos -= (self.TEXT_BRAILLE_SPACING * mm)
        
        # Dibujar representación Braille
        self._draw_braille_text(pdf_canvas, braille_text, x_pos, y_pos)
        
        # Agregar información del cuadratín (leyenda)
        self._draw_legend(pdf_canvas)
        
        pdf_canvas.save()
        buffer.seek(0)
        
        return buffer
    
    def _draw_braille_text(self, pdf_canvas: canvas.Canvas, 
                           braille_text: str, x_start: float, y_start: float) -> None:
        """
        Dibuja el texto Braille como patrones de puntos en el PDF.
        
        Args:
            pdf_canvas: Canvas de ReportLab
            braille_text: Texto en Braille Unicode
            x_start: Posición X inicial
            y_start: Posición Y inicial
        """
        x_pos = x_start
        y_pos = y_start
        
        for char in braille_text:
            if char == ' ':
                x_pos += self.BRAILLE_CELL_WIDTH * mm
                continue
            
            if char in self._BRAILLE_TO_DOTS:
                dots = self._BRAILLE_TO_DOTS[char]
                self._draw_braille_cell(pdf_canvas, dots, x_pos, y_pos)
                x_pos += self.BRAILLE_CELL_WIDTH * mm
            
            # Salto de línea si se alcanza el margen derecho
            if x_pos > (self.page_size[0] - self.MARGIN_LEFT * mm):
                x_pos = x_start
                y_pos -= self.LINE_SPACING * mm
    
    def _draw_braille_cell(self, pdf_canvas: canvas.Canvas, 
                           dots: list, x: float, y: float) -> None:
        """
        Dibuja una celda Braille individual (cuadratín de 6 puntos).
        
        Disposición de puntos:
            1 • • 4
            2 • • 5
            3 • • 6
        
        Args:
            pdf_canvas: Canvas de ReportLab
            dots: Lista de puntos activos (1-6)
            x: Posición X de la celda
            y: Posición Y de la celda
        """
        # Posiciones de los 6 puntos
        dot_positions = {
            1: (x, y),
            2: (x, y - self.BRAILLE_DOT_SPACING_V * mm),
            3: (x, y - 2 * self.BRAILLE_DOT_SPACING_V * mm),
            4: (x + self.BRAILLE_DOT_SPACING_H * mm, y),
            5: (x + self.BRAILLE_DOT_SPACING_H * mm, y - self.BRAILLE_DOT_SPACING_V * mm),
            6: (x + self.BRAILLE_DOT_SPACING_H * mm, y - 2 * self.BRAILLE_DOT_SPACING_V * mm),
        }
        
        # Dibujar todos los puntos (activos en negro, inactivos en gris claro)
        for dot_num in range(1, 7):
            dot_x, dot_y = dot_positions[dot_num]
            
            if dot_num in dots:
                pdf_canvas.setFillColor(black)
                pdf_canvas.circle(dot_x, dot_y, self.BRAILLE_DOT_RADIUS * mm, fill=1)
            else:
                # Puntos inactivos en gris muy claro (opcional, para visualización)
                pdf_canvas.setFillColor(grey)
                pdf_canvas.setStrokeColor(grey)
                pdf_canvas.circle(dot_x, dot_y, self.BRAILLE_DOT_RADIUS * mm * 0.3, 
                                  fill=0, stroke=1)
                pdf_canvas.setStrokeColor(black)
    
    def _draw_legend(self, pdf_canvas: canvas.Canvas) -> None:
        """
        Dibuja una leyenda explicativa del cuadratín Braille.
        
        Args:
            pdf_canvas: Canvas de ReportLab
        """
        legend_x = self.MARGIN_LEFT * mm
        legend_y = 40 * mm
        
        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.setFillColor(black)
        pdf_canvas.drawString(legend_x, legend_y, "Cuadratín Braille (Símbolo Generador):")
        
        # Dibujar ejemplo de cuadratín con números
        legend_y -= 15 * mm
        cell_x = legend_x + 10 * mm
        
        # Dibujar los 6 puntos numerados
        dot_positions = {
            1: (cell_x, legend_y),
            2: (cell_x, legend_y - self.BRAILLE_DOT_SPACING_V * mm),
            3: (cell_x, legend_y - 2 * self.BRAILLE_DOT_SPACING_V * mm),
            4: (cell_x + self.BRAILLE_DOT_SPACING_H * mm, legend_y),
            5: (cell_x + self.BRAILLE_DOT_SPACING_H * mm, 
                legend_y - self.BRAILLE_DOT_SPACING_V * mm),
            6: (cell_x + self.BRAILLE_DOT_SPACING_H * mm, 
                legend_y - 2 * self.BRAILLE_DOT_SPACING_V * mm),
        }
        
        pdf_canvas.setFont("Helvetica", 8)
        for dot_num, (dot_x, dot_y) in dot_positions.items():
            pdf_canvas.circle(dot_x, dot_y, self.BRAILLE_DOT_RADIUS * mm, fill=1)
            pdf_canvas.drawString(dot_x + 3 * mm, dot_y - 1 * mm, str(dot_num))
