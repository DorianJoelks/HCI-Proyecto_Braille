/**
 * Aplicación Frontend - Transcriptor Braille
 * 
 * Maneja la interacción del usuario con la aplicación web,
 * siguiendo principios de código limpio y separación de responsabilidades.
 */

// Configuración de la API
const API_CONFIG = {
    BASE_URL: '/api',
    ENDPOINTS: {
        TRANSCRIBE: '/transcribe',
        VALIDATE: '/validate',
        GENERATE_SIGNAGE: '/generate-signage'
    }
};

// Estado de la aplicación (patrón State Management simple)
const appState = {
    originalText: '',
    brailleText: '',
    isTranscribing: false
};

// Elementos del DOM (cacheados para mejor rendimiento)
const elements = {
    inputText: null,
    transcribeBtn: null,
    clearBtn: null,
    generatePdfBtn: null,
    copyBrailleBtn: null,
    charCount: null,
    errorMessage: null,
    successMessage: null,
    resultsSection: null,
    originalTextDisplay: null,
    brailleTextDisplay: null
};

/**
 * Inicializa la aplicación cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    attachEventListeners();
    initializeTheme();
    addAnimations();
});

/**
 * Inicializa las referencias a elementos del DOM
 */
function initializeElements() {
    elements.inputText = document.getElementById('inputText');
    elements.transcribeBtn = document.getElementById('transcribeBtn');
    elements.clearBtn = document.getElementById('clearBtn');
    elements.generatePdfBtn = document.getElementById('generatePdfBtn');
    elements.copyBrailleBtn = document.getElementById('copyBrailleBtn');
    elements.charCount = document.getElementById('charCount');
    elements.errorMessage = document.getElementById('errorMessage');
    elements.successMessage = document.getElementById('successMessage');
    elements.resultsSection = document.getElementById('resultsSection');
    elements.originalTextDisplay = document.getElementById('originalText');
    elements.brailleTextDisplay = document.getElementById('brailleText');
}

/**
 * Adjunta event listeners a los elementos interactivos
 */
function attachEventListeners() {
    elements.inputText.addEventListener('input', handleTextInput);
    elements.transcribeBtn.addEventListener('click', handleTranscribe);
    elements.clearBtn.addEventListener('click', handleClear);
    elements.generatePdfBtn.addEventListener('click', handleGeneratePdf);
    elements.copyBrailleBtn.addEventListener('click', handleCopyBraille);
    
    // Event listener para cambio de tema
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

/**
 * Maneja la entrada de texto y actualiza el contador de caracteres
 * @param {Event} event - Evento de input
 */
function handleTextInput(event) {
    const text = event.target.value;
    elements.charCount.textContent = text.length;
    
    // Limpiar mensajes previos
    hideMessages();
}

/**
 * Maneja la solicitud de transcripción
 */
async function handleTranscribe() {
    const text = elements.inputText.value.trim();
    
    // Validación básica
    if (!text) {
        showError('Por favor, ingrese un texto para transcribir.');
        return;
    }
    
    // Deshabilitar botón durante la petición
    setTranscribing(true);
    hideMessages();
    
    try {
        const result = await transcribeText(text);
        
        if (result.success) {
            appState.originalText = result.original_text;
            appState.brailleText = result.braille_text;
            displayResults();
            showSuccess('¡Transcripción completada exitosamente!');
        } else {
            showError(result.error || 'Error al transcribir el texto.');
        }
    } catch (error) {
        showError('Error de conexión. Por favor, intente nuevamente.');
        console.error('Error en transcripción:', error);
    } finally {
        setTranscribing(false);
    }
}

/**
 * Realiza la petición de transcripción a la API
 * @param {string} text - Texto a transcribir
 * @returns {Promise<Object>} Resultado de la transcripción
 */
async function transcribeText(text) {
    const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.TRANSCRIBE}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });
    
    return await response.json();
}

/**
 * Muestra los resultados de la transcripción
 */
function displayResults() {
    elements.originalTextDisplay.textContent = appState.originalText;
    elements.brailleTextDisplay.textContent = appState.brailleText;
    elements.resultsSection.style.display = 'block';
    
    // Scroll suave a los resultados
    elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Limpia el formulario y oculta los resultados
 */
function handleClear() {
    elements.inputText.value = '';
    elements.charCount.textContent = '0';
    elements.resultsSection.style.display = 'none';
    appState.originalText = '';
    appState.brailleText = '';
    hideMessages();
    elements.inputText.focus();
}

/**
 * Genera y descarga el PDF de señalética
 */
async function handleGeneratePdf() {
    if (!appState.brailleText) {
        showError('Primero debe realizar una transcripción.');
        return;
    }
    
    setButtonLoading(elements.generatePdfBtn, true);
    hideMessages();
    
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.GENERATE_SIGNAGE}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                original_text: appState.originalText,
                braille_text: appState.brailleText
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            downloadFile(blob, 'senaletica_braille.pdf', 'application/pdf');
            showSuccess('¡PDF generado y descargado exitosamente!');
        } else {
            const error = await response.json();
            showError(error.error || 'Error al generar el PDF.');
        }
    } catch (error) {
        showError('Error al generar el PDF. Por favor, intente nuevamente.');
        console.error('Error en generación de PDF:', error);
    } finally {
        setButtonLoading(elements.generatePdfBtn, false);
    }
}

/**
 * Descarga un archivo blob
 * @param {Blob} blob - Blob a descargar
 * @param {string} filename - Nombre del archivo
 * @param {string} mimeType - Tipo MIME
 */
function downloadFile(blob, filename, mimeType) {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

/**
 * Copia el texto Braille al portapapeles
 */
async function handleCopyBraille() {
    if (!appState.brailleText) {
        showError('No hay texto Braille para copiar.');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(appState.brailleText);
        showSuccess('¡Texto Braille copiado al portapapeles!');
    } catch (error) {
        // Fallback para navegadores más antiguos
        fallbackCopyToClipboard(appState.brailleText);
    }
}

/**
 * Método alternativo para copiar al portapapeles (fallback)
 * @param {string} text - Texto a copiar
 */
function fallbackCopyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        document.execCommand('copy');
        showSuccess('¡Texto Braille copiado!');
    } catch (error) {
        showError('No se pudo copiar el texto.');
    } finally {
        document.body.removeChild(textarea);
    }
}

/**
 * Muestra un mensaje de error
 * @param {string} message - Mensaje a mostrar
 */
function showError(message) {
    hideMessages();
    elements.errorMessage.textContent = message;
    elements.errorMessage.style.display = 'block';
    elements.errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Muestra un mensaje de éxito
 * @param {string} message - Mensaje a mostrar
 */
function showSuccess(message) {
    hideMessages();
    elements.successMessage.textContent = message;
    elements.successMessage.style.display = 'block';
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        elements.successMessage.style.display = 'none';
    }, 5000);
}

/**
 * Oculta todos los mensajes
 */
function hideMessages() {
    elements.errorMessage.style.display = 'none';
    elements.successMessage.style.display = 'none';
}

/**
 * Establece el estado de "transcribiendo"
 * @param {boolean} isTranscribing - Estado de transcripción
 */
function setTranscribing(isTranscribing) {
    appState.isTranscribing = isTranscribing;
    elements.transcribeBtn.disabled = isTranscribing;
    elements.inputText.disabled = isTranscribing;
    
    if (isTranscribing) {
        elements.transcribeBtn.textContent = 'Transcribiendo...';
        elements.transcribeBtn.classList.add('loading');
    } else {
        elements.transcribeBtn.textContent = 'Transcribir a Braille';
        elements.transcribeBtn.classList.remove('loading');
    }
}

/**
 * Establece el estado de carga de un botón
 * @param {HTMLElement} button - Botón a modificar
 * @param {boolean} isLoading - Estado de carga
 */
function setButtonLoading(button, isLoading) {
    button.disabled = isLoading;
    
    if (isLoading) {
        button.dataset.originalText = button.textContent;
        button.textContent = 'Generando...';
        button.classList.add('loading');
    } else {
        button.textContent = button.dataset.originalText || button.textContent;
        button.classList.remove('loading');
    }
}

/**
 * Inicializa el tema de la aplicación
 */
function initializeTheme() {
    // Verificar si hay tema guardado en localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeToggleButton(savedTheme);
}

/**
 * Alterna entre tema claro y oscuro
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeToggleButton(newTheme);
}

/**
 * Actualiza el texto del botón de cambio de tema
 * @param {string} theme - Tema actual ('light' o 'dark')
 */
function updateThemeToggleButton(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Oscuro';
    }
}

/**
 * Agrega animaciones a los elementos de la página
 */
function addAnimations() {
    // Agregar animación fade-in a las cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
}
