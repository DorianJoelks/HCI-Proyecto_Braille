# Sistema de Transcripción Braille 🔤

> **Desarrollado por GR1 - HCI**

Sistema web moderno desarrollado en Python/Flask para transcribir textos en español a Braille y generar señalética imprimible de alta calidad.

## ✨ Características Destacadas

- **Transcripción completa**: Soporta el alfabeto español completo (a-z, ñ, w), vocales acentuadas (á, é, í, ó, ú, ü), números (0-9) y signos de puntuación básicos
- **Generación de PDF**: Crea documentos vectoriales listos para imprimir con representación visual del Braille
- **Interfaz moderna**: Diseño web responsive con gradientes dinámicos y animaciones suaves
- **🌙 Modo Oscuro**: Cambia entre temas claro y oscuro con persistencia local
- **Arquitectura limpia**: Implementa el patrón de arquitectura de 3 capas
- **Dockerizado**: Completamente portable mediante contenedores Docker
- **Accesible**: Diseño inclusivo siguiendo estándares WCAG

## 🏗️ Arquitectura

El proyecto sigue una **Arquitectura de Tres Capas**:

```
┌─────────────────────────────────────┐
│   Capa de Presentación (Frontend)  │
│   HTML/CSS/JavaScript               │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   Capa de Lógica de Negocio        │
│   Flask + Motor de Transcripción    │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   Capa de Datos                     │
│   Mapeos Braille (JSON/Python)      │
└─────────────────────────────────────┘
```

## 📖 Uso de la Aplicación

1. **Ingresar texto**: Escribir el texto en español en el área de texto principal
2. **Transcribir**: Hacer clic en "Transcribir a Braille"
3. **Ver resultado**: El sistema mostrará el texto original y su transcripción en Braille
4. **Generar PDF**: Hacer clic en "Generar Señalética PDF" para descargar el archivo imprimible
5. **Copiar Braille**: Usar el botón "Copiar Braille" para copiar el texto al portapapeles

## 🧪 Casos de Uso Soportados

- ✅ Transcripción de alfabeto completo (a-z, ñ, w)
- ✅ Vocales acentuadas (á, é, í, ó, ú, ü)
- ✅ Números (0-9) con signo de número
- ✅ Signos de puntuación (. , ; : ¿ ? ¡ ! ( ) -)
- ✅ Generación de PDF con representación visual del Braille
- ✅ Validación de caracteres no soportados

## 🔧 Tecnologías Utilizadas

- **Backend**: Python 3.11, Flask 3.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **PDF Generation**: ReportLab 4.0
- **Containerización**: Docker
- **Control de Versiones**: Git

## 📚 Documentación del Proyecto

Este repositorio utiliza una **estrategia de ramificación separada para documentación**:

### 🌿 Estructura de Ramas

#### `main` - Código Estable de Producción
- Contiene únicamente el código fuente de la aplicación
- Solo acepta merges probados y validados
- Versión lista para desplegar en producción

#### `documentacion` - Documentación Completa del Proyecto
- **Documentación independiente del código**
- Estructura completa con 6 secciones obligatorias:
  1. 📐 **Diseño Arquitectónico** - Diagramas y decisiones de arquitectura
  2. 🛠️ **Ambiente de Desarrollo** - Herramientas, estrategia de ramificación, flujo de trabajo
  3. 📖 **Documentación Técnica** - API endpoints, módulos, código fuente
  4. 🧪 **Casos de Prueba** - Plan de pruebas, casos de prueba detallados con resultados
  5. 📦 **Manual de Instalación** - Instalación local, Docker, troubleshooting
  6. 👤 **Manual de Usuario** - Guía completa de uso con ejemplos prácticos

#### `feature/*` - Ramas de Funcionalidades
- Ramas temporales para desarrollo de nuevas características
- Se crean desde `develop` y se fusionan de vuelta a `develop`

### 📋 Flujo de Trabajo Git (Feature Branch Workflow)

```
main (producción) ←──────────── merge estable ←──────── develop (integración)
                                                              ↑
                                                              │ merge
                                                              │
                                                         feature/nueva-funcionalidad
```

**Proceso de desarrollo**:
1. Crear feature desde `develop`: 
   ```bash
   git checkout develop
   git checkout -b feature/nombre-funcionalidad
   ```
2. Desarrollar y hacer commits:
   ```bash
   git add .
   git commit -m "feat: descripción de la funcionalidad"
   ```
3. Fusionar a `develop`:
   ```bash
   git checkout develop
   git merge feature/nombre-funcionalidad
   ```
4. Cuando `develop` esté estable, fusionar a `main`:
   ```bash
   git checkout main
   git merge develop
   ```

### 📝 Convenciones de Commits

Seguimos **Conventional Commits**:
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `refactor:` - Refactorización de código
- `test:` - Añadir o modificar tests
- `style:` - Cambios de formato (no afectan funcionalidad)

## 📝 Licencia

Proyecto académico desarrollado para el curso de HCI.

## 👥 Contribuciones

Este es un proyecto académico. Para contribuir, seguir el flujo de ramificación establecido.

---

**Desarrollado con ❤️ para mejorar la accesibilidad**
