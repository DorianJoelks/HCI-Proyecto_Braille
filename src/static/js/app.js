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

// Elementos del simulador Perkins
const perkinsElements = {
    modeWriteBtn: null,
    modeReadBtn: null,
    speechStatus: null,
    keys: [],
    dots: [],
    spaceBtn: null,
    nextBtn: null
};

// Estado del simulador Perkins
const perkinsState = {
    mode: 'write',
    activeDots: new Set(),
    bufferWord: '',
    sequenceIndex: 0,
    speechAvailable: false
};

/**
 * Inicializa la aplicación cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    attachEventListeners();
    initializeTheme();
    addAnimations();
    initializePerkins();
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

    perkinsElements.modeWriteBtn = document.getElementById('perkinsModeWrite');
    perkinsElements.modeReadBtn = document.getElementById('perkinsModeRead');
    perkinsElements.speechStatus = document.getElementById('perkinsSpeechStatus');
    perkinsElements.keys = Array.from(document.querySelectorAll('.perkins-key'));
    perkinsElements.dots = Array.from(document.querySelectorAll('.perkins-dot'));
    perkinsElements.spaceBtn = document.getElementById('perkinsSpace');
    perkinsElements.nextBtn = document.getElementById('perkinsNext');
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

    if (perkinsElements.modeWriteBtn && perkinsElements.modeReadBtn) {
        perkinsElements.modeWriteBtn.addEventListener('click', () => setPerkinsMode('write'));
        perkinsElements.modeReadBtn.addEventListener('click', () => setPerkinsMode('read'));
    }

    if (perkinsElements.spaceBtn) {
        perkinsElements.spaceBtn.addEventListener('click', handlePerkinsSpace);
    }

    if (perkinsElements.nextBtn) {
        perkinsElements.nextBtn.addEventListener('click', handlePerkinsNext);
    }

    if (perkinsElements.keys.length) {
        perkinsElements.keys.forEach((key) => {
            key.addEventListener('click', handlePerkinsKey);
        });
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

// === Simulador Perkins ===
const perkinsLetterSequence = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', 'ñ'
];

const perkinsDotPatterns = {
    a: [1],
    b: [1, 2],
    c: [1, 4],
    d: [1, 4, 5],
    e: [1, 5],
    f: [1, 2, 4],
    g: [1, 2, 4, 5],
    h: [1, 2, 5],
    i: [2, 4],
    j: [2, 4, 5],
    k: [1, 3],
    l: [1, 2, 3],
    m: [1, 3, 4],
    n: [1, 3, 4, 5],
    o: [1, 3, 5],
    p: [1, 2, 3, 4],
    q: [1, 2, 3, 4, 5],
    r: [1, 2, 3, 5],
    s: [2, 3, 4],
    t: [2, 3, 4, 5],
    u: [1, 3, 6],
    v: [1, 2, 3, 6],
    w: [2, 4, 5, 6],
    x: [1, 3, 4, 6],
    y: [1, 3, 4, 5, 6],
    z: [1, 3, 5, 6],
    ñ: [1, 2, 4, 5, 6]
};

const perkinsPatternToLetter = Object.entries(perkinsDotPatterns).reduce((acc, [letter, dots]) => {
    acc[patternKey(dots)] = letter;
    return acc;
}, {});

function initializePerkins() {
    perkinsState.speechAvailable = 'speechSynthesis' in window;
    if (perkinsElements.speechStatus) {
        perkinsElements.speechStatus.textContent = perkinsState.speechAvailable
            ? ''
            : 'Sintesis de voz no disponible en este navegador.';
    }
    setPerkinsMode('write');
}

function setPerkinsMode(mode) {
    perkinsState.mode = mode;
    perkinsState.activeDots.clear();
    perkinsState.bufferWord = '';
    perkinsState.sequenceIndex = 0;

    if (perkinsElements.modeWriteBtn && perkinsElements.modeReadBtn) {
        perkinsElements.modeWriteBtn.classList.toggle('is-active', mode === 'write');
        perkinsElements.modeReadBtn.classList.toggle('is-active', mode === 'read');
    }

    perkinsElements.keys.forEach((key) => {
        key.disabled = mode === 'read';
        key.classList.remove('is-active');
    });

    if (mode === 'read') {
        applyDotsForLetter(perkinsLetterSequence[0]);
        if (perkinsElements.nextBtn) {
            perkinsElements.nextBtn.classList.remove('is-hidden');
        }
    } else {
        updatePerkinsDots();
        if (perkinsElements.nextBtn) {
            perkinsElements.nextBtn.classList.add('is-hidden');
        }
    }
}

function handlePerkinsKey(event) {
    if (perkinsState.mode !== 'write') {
        return;
    }

    const dot = Number(event.currentTarget.dataset.dot);
    if (perkinsState.activeDots.has(dot)) {
        perkinsState.activeDots.delete(dot);
    } else {
        perkinsState.activeDots.add(dot);
    }

    updatePerkinsDots();
    updatePerkinsKeys();
}

function handlePerkinsSpace() {
    if (perkinsState.mode === 'read') {
        const currentLetter = perkinsLetterSequence[perkinsState.sequenceIndex];
        speakPerkinsText(`Letra ${currentLetter.toUpperCase()}`);
        return;
    }

    if (perkinsState.activeDots.size === 0) {
        if (perkinsState.bufferWord) {
            speakPerkinsText(perkinsState.bufferWord);
            perkinsState.bufferWord = '';
        }
        return;
    }

    const letter = getLetterFromActiveDots();
    if (!letter) {
        speakPerkinsText('Combinacion no valida');
        perkinsState.activeDots.clear();
        updatePerkinsDots();
        updatePerkinsKeys();
        return;
    }

    perkinsState.bufferWord += letter;
    speakPerkinsText(`Letra ${letter.toUpperCase()}`);
    perkinsState.activeDots.clear();
    updatePerkinsDots();
    updatePerkinsKeys();
}

function handlePerkinsNext() {
    if (perkinsState.mode !== 'read') {
        return;
    }
    advancePerkinsSequence();
}

function advancePerkinsSequence() {
    perkinsState.sequenceIndex = (perkinsState.sequenceIndex + 1) % perkinsLetterSequence.length;
    applyDotsForLetter(perkinsLetterSequence[perkinsState.sequenceIndex]);
}

function applyDotsForLetter(letter) {
    perkinsState.activeDots.clear();
    const dots = perkinsDotPatterns[letter] || [];
    dots.forEach((dot) => perkinsState.activeDots.add(dot));
    updatePerkinsDots();
    updatePerkinsKeys();
}

function updatePerkinsDots() {
    perkinsElements.dots.forEach((dotEl) => {
        const dot = Number(dotEl.dataset.dot);
        dotEl.classList.toggle('is-active', perkinsState.activeDots.has(dot));
    });
}

function updatePerkinsKeys() {
    perkinsElements.keys.forEach((key) => {
        const dot = Number(key.dataset.dot);
        key.classList.toggle('is-active', perkinsState.activeDots.has(dot));
    });
}

function getLetterFromActiveDots() {
    const pattern = patternKey(Array.from(perkinsState.activeDots));
    return perkinsPatternToLetter[pattern] || null;
}

function patternKey(dots) {
    return dots.slice().sort((a, b) => a - b).join('-');
}

function speakPerkinsText(text) {
    if (!perkinsState.speechAvailable) {
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
}
