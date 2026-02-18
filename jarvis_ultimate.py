"""
╔═══════════════════════════════════════════════════════════════════╗
║                    J.A.R.V.I.S. ULTIMATE                         ║
║          Just A Rather Very Intelligent System                    ║
║                                                                   ║
║  Asistente personal con IA como cerebro central.                 ║
║  - Comandos de voz + respuestas habladas                         ║
║  - GPT como cerebro (decide qué hacer con cada pedido)           ║
║  - Acceso completo a terminal (ejecuta comandos reales)          ║
║  - Control del sistema, archivos, apps, web                      ║
║  - Notas, tareas, recordatorios persistentes                     ║
║  - Monitor del sistema en tiempo real                            ║
║  - Personalidad Jarvis: profesional, corto, con estilo           ║
║                                                                   ║
║  Proveedores de IA (elige uno, todos funcionan):                  ║
║   - Google Gemini   → GRATIS (recomendado para empezar)          ║
║   - Groq            → GRATIS (ultra rápido)                      ║
║   - Ollama          → GRATIS (local, sin internet)               ║
║   - OpenAI          → De pago (API key separada de Plus)         ║
║                                                                   ║
║  Requisitos mínimos:                                              ║
║    pip install pyttsx3 SpeechRecognition pyaudio psutil           ║
║    (openai solo si usas OpenAI/Groq/Ollama como proveedor)       ║
║                                                                   ║
║  Uso:                                                             ║
║    python jarvis_ultimate.py                                      ║
║    Di "Jarvis" o escribe tu comando.                             ║
╚═══════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import scrolledtext, messagebox, colorchooser
import time
import os
import sys
import json
import math
import random
import string
import hashlib
import base64
import re
import socket
import platform
import subprocess
import threading
import webbrowser
import shutil
import datetime
import urllib.request
import urllib.parse
from collections import deque

# ══════════════════════════════════════════════════════════════
# VERIFICAR E IMPORTAR DEPENDENCIAS OPCIONALES
# ══════════════════════════════════════════════════════════════

HAS_PYTTSX3 = False
HAS_SPEECH = False
HAS_PSUTIL = False
HAS_OPENAI = False

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    pass

try:
    import speech_recognition as sr
    HAS_SPEECH = True
except ImportError:
    pass

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    pass

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    pass

# Proveedores de IA soportados
PROVIDERS = {
    "gemini": {
        "name": "Google Gemini",
        "cost": "GRATIS",
        "models": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "default_model": "gemini-2.0-flash",
        "get_key_url": "https://aistudio.google.com/apikey",
        "needs_openai_lib": False,
    },
    "groq": {
        "name": "Groq",
        "cost": "GRATIS",
        "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        "default_model": "llama-3.3-70b-versatile",
        "get_key_url": "https://console.groq.com/keys",
        "needs_openai_lib": True,
    },
    "ollama": {
        "name": "Ollama (Local)",
        "cost": "GRATIS (local)",
        "models": ["llama3.2", "mistral", "phi3", "gemma2"],
        "default_model": "llama3.2",
        "get_key_url": "https://ollama.com/download",
        "needs_openai_lib": True,
    },
    "openai": {
        "name": "OpenAI",
        "cost": "De pago",
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        "default_model": "gpt-4o-mini",
        "get_key_url": "https://platform.openai.com/api-keys",
        "needs_openai_lib": True,
    },
}

# ══════════════════════════════════════════════════════════════
# CONFIGURACION Y CONSTANTES
# ══════════════════════════════════════════════════════════════

APP_NAME = "J.A.R.V.I.S. ULTIMATE"
VERSION = "3.5.0"
DATA_DIR = os.path.join(os.path.expanduser("~"), ".jarvis_ultimate")
NOTES_FILE = os.path.join(DATA_DIR, "notas.json")
TODOS_FILE = os.path.join(DATA_DIR, "tareas.json")
REMINDERS_FILE = os.path.join(DATA_DIR, "recordatorios.json")
HISTORY_FILE = os.path.join(DATA_DIR, "historial.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
CONVERSATION_FILE = os.path.join(DATA_DIR, "conversacion.json")

os.makedirs(DATA_DIR, exist_ok=True)

# Colores
C = {
    "bg": "#0A0E1A",
    "bg2": "#111827",
    "bg3": "#1E293B",
    "accent": "#00D4FF",
    "accent2": "#38BDF8",
    "green": "#34D399",
    "red": "#F87171",
    "yellow": "#FBBF24",
    "purple": "#A78BFA",
    "orange": "#FB923C",
    "text": "#E2E8F0",
    "text2": "#94A3B8",
    "muted": "#475569",
    "border": "#1E293B",
}

# System prompt - La personalidad de Jarvis
JARVIS_SYSTEM_PROMPT = """Eres J.A.R.V.I.S. (Just A Rather Very Intelligent System), el asistente personal de IA más avanzado del mundo. Tu creador es tu usuario.

PERSONALIDAD:
- Profesional, conciso y elegante. Respuestas CORTAS (1-3 oraciones máximo) a menos que te pidan detalles.
- Llama al usuario "señor" o "jefe" ocasionalmente.
- Tono calmado, inteligente, ligeramente sarcástico pero siempre respetuoso.
- Si algo sale mal, mantén la calma. Nunca entres en pánico.
- Hablas en español.

CAPACIDADES (tienes acceso a estas herramientas - ÚSALAS cuando sea apropiado):

1. EJECUTAR COMANDOS EN TERMINAL: Cuando el usuario pida algo que requiera terminal/cmd/powershell, responde con:
   [TERMINAL]: comando_aqui
   Ejemplos: instalar paquetes, listar archivos, git, npm, pip, crear archivos, etc.

2. ABRIR PROGRAMAS: Cuando pida abrir una app, responde con:
   [ABRIR]: nombre_programa
   Programas: chrome, firefox, edge, notepad, calc, explorer, cmd, powershell, code, paint, word, excel, teams, discord, spotify, steam, taskmgr, settings

3. ABRIR WEB: Cuando pida abrir un sitio o buscar algo:
   [WEB]: url_completa
   
4. BUSCAR EN GOOGLE:
   [GOOGLE]: texto_a_buscar

5. BUSCAR EN YOUTUBE:
   [YOUTUBE]: texto_a_buscar

6. GUARDAR NOTA:
   [NOTA]: texto_de_la_nota

7. CREAR TAREA:
   [TAREA]: texto_de_la_tarea

8. RECORDATORIO:
   [RECORDAR]: texto|minutos
   Ejemplo: [RECORDAR]: Llamar al doctor|30

9. SISTEMA - Info del sistema:
   [SISTEMA]: info|cpu|disco|red|bateria

10. GENERAR CONTRASEÑA:
    [PASSWORD]: longitud (número)

11. CALCULADORA:
    [CALC]: expresion_matematica

12. BLOQUEAR PC:
    [BLOQUEAR]

13. CAPTURA DE PANTALLA:
    [SCREENSHOT]

14. COPIAR AL PORTAPAPELES:
    [COPIAR]: texto

15. ABRIR CARPETA:
    [CARPETA]: ruta (o: descargas, documentos, escritorio)

REGLAS IMPORTANTES:
- Puedes usar MÚLTIPLES comandos en una respuesta. Ejemplo: abrir Chrome y buscar algo.
- Siempre incluye una respuesta de texto ADEMÁS del comando. No solo el comando suelto.
- Si el usuario pide algo peligroso (borrar sistema, formatear), ADVIERTE antes.
- Si no necesitas ninguna herramienta, simplemente responde como Jarvis.
- Recuerda el contexto de la conversación.
- NUNCA expliques tus comandos internos. Solo actúa.
"""

# Frases de Jarvis
JARVIS_GREETINGS = [
    "A sus órdenes, señor.",
    "Sistema operativo. ¿En qué puedo ayudarle?",
    "Todos los sistemas en línea. ¿Qué necesita?",
    "Buenos días, jefe. Estoy listo.",
    "Jarvis en línea. Dígame.",
]

JARVIS_CONFIRMATIONS = [
    "Hecho, señor.",
    "Enseguida.",
    "Procesando.",
    "En eso estoy.",
    "Entendido.",
    "Considérelo hecho.",
]

JARVIS_ERRORS = [
    "Eso no salió como esperaba, señor.",
    "Tenemos un pequeño inconveniente.",
    "Hmm, algo no fue según el plan.",
]


# ══════════════════════════════════════════════════════════════
# PERSISTENCIA
# ══════════════════════════════════════════════════════════════

class DataStore:
    @staticmethod
    def load(filepath, default=None):
        if default is None:
            default = []
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return default

    @staticmethod
    def save(filepath, data):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False


# ══════════════════════════════════════════════════════════════
# MOTOR DE VOZ (Text-to-Speech)
# ══════════════════════════════════════════════════════════════

class VoiceEngine:
    """Motor de voz de Jarvis - habla y escucha."""

    def __init__(self):
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None
        self.is_speaking = False
        self.is_listening = False
        self.voice_enabled = True
        self._init_tts()
        self._init_stt()

    def _init_tts(self):
        """Inicializar text-to-speech."""
        if not HAS_PYTTSX3:
            return
        try:
            self.tts_engine = pyttsx3.init()
            # Buscar voz en español o usar la más natural disponible
            voices = self.tts_engine.getProperty('voices')
            spanish_voice = None
            for v in voices:
                if 'spanish' in v.name.lower() or 'español' in v.name.lower() or 'es' in v.languages:
                    spanish_voice = v
                    break
            if spanish_voice:
                self.tts_engine.setProperty('voice', spanish_voice.id)
            # Velocidad y volumen
            self.tts_engine.setProperty('rate', 175)  # Velocidad natural
            self.tts_engine.setProperty('volume', 0.9)
        except Exception:
            self.tts_engine = None

    def _init_stt(self):
        """Inicializar speech-to-text."""
        if not HAS_SPEECH:
            return
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
        except Exception:
            self.recognizer = None

    def speak(self, text):
        """Hablar texto en voz alta (en hilo separado)."""
        if not self.tts_engine or not self.voice_enabled:
            return
        # Limpiar texto de emojis y caracteres especiales para TTS
        clean = re.sub(r'[^\w\s.,;:!?¿¡\-\'\"áéíóúñü]', '', text, flags=re.UNICODE)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if not clean:
            return

        def _speak():
            try:
                self.is_speaking = True
                self.tts_engine.say(clean)
                self.tts_engine.runAndWait()
            except Exception:
                pass
            finally:
                self.is_speaking = False

        threading.Thread(target=_speak, daemon=True).start()

    def stop_speaking(self):
        """Detener el habla."""
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
            except Exception:
                pass

    def listen(self, callback, error_callback=None, timeout=5, phrase_limit=15):
        """Escuchar del micrófono (en hilo separado)."""
        if not self.recognizer or not HAS_SPEECH:
            if error_callback:
                error_callback("Reconocimiento de voz no disponible. Instala: pip install SpeechRecognition pyaudio")
            return

        def _listen():
            self.is_listening = True
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

                # Usar Google Speech Recognition (gratis)
                text = self.recognizer.recognize_google(audio, language="es-ES")
                callback(text)

            except sr.WaitTimeoutError:
                if error_callback:
                    error_callback("No detecté audio. Intenta de nuevo.")
            except sr.UnknownValueError:
                if error_callback:
                    error_callback("No pude entender eso. ¿Puedes repetir?")
            except sr.RequestError as e:
                if error_callback:
                    error_callback(f"Error de red en reconocimiento: {e}")
            except Exception as e:
                if error_callback:
                    error_callback(f"Error de micrófono: {e}")
            finally:
                self.is_listening = False

        threading.Thread(target=_listen, daemon=True).start()

    def toggle_voice(self):
        """Activar/desactivar voz."""
        self.voice_enabled = not self.voice_enabled
        return self.voice_enabled


# ══════════════════════════════════════════════════════════════
# CEREBRO IA (Multi-proveedor: Gemini, Groq, Ollama, OpenAI)
# ══════════════════════════════════════════════════════════════

class AIBrain:
    """Cerebro de Jarvis - Soporta múltiples proveedores de IA."""

    def __init__(self):
        self.client = None
        self.provider = None  # gemini, groq, ollama, openai
        self.api_key = ""
        self.conversation = []
        self.max_history = 20
        self.ready = False

        # Cargar conversación previa
        saved = DataStore.load(CONVERSATION_FILE, [])
        if saved:
            self.conversation = saved[-self.max_history:]

    def init_provider(self, provider, api_key):
        """Inicializar proveedor de IA."""
        self.provider = provider.lower().strip()
        self.api_key = api_key
        self.client = None
        self.ready = False

        if self.provider == "gemini":
            # Gemini usa REST API directamente (no necesita openai lib)
            if api_key:
                self.ready = True
                return True
            return False

        elif self.provider == "groq":
            if not HAS_OPENAI:
                return False
            try:
                self.client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                self.ready = True
                return True
            except Exception:
                return False

        elif self.provider == "ollama":
            if not HAS_OPENAI:
                # Intentar con REST API directa
                self.ready = True
                return True
            try:
                self.client = OpenAI(
                    api_key="ollama",
                    base_url="http://localhost:11434/v1"
                )
                self.ready = True
                return True
            except Exception:
                return False

        elif self.provider == "openai":
            if not HAS_OPENAI:
                return False
            try:
                self.client = OpenAI(api_key=api_key)
                self.ready = True
                return True
            except Exception:
                return False

        return False

    def _build_system_prompt(self, system_context=""):
        """Construir el system prompt con contexto actual."""
        now = datetime.datetime.now()
        context = (
            f"\n\nCONTEXTO ACTUAL:\n"
            f"- Fecha/hora: {now.strftime('%A %d/%m/%Y %H:%M:%S')}\n"
            f"- Sistema: {platform.system()} {platform.release()}\n"
            f"- Usuario: {os.getlogin()}\n"
            f"- Directorio home: {os.path.expanduser('~')}\n"
        )
        if system_context:
            context += f"- Info adicional: {system_context}\n"
        return JARVIS_SYSTEM_PROMPT + context

    def think(self, user_message, system_context="", model=None):
        """Enviar mensaje al proveedor de IA seleccionado."""
        if not self.ready:
            return (
                "Mi cerebro no está conectado, señor. Configure un proveedor de IA.\n"
                "Opciones GRATUITAS:\n"
                "  config proveedor: gemini    → Luego: config api: TU_KEY (gratis en aistudio.google.com/apikey)\n"
                "  config proveedor: groq      → Luego: config api: TU_KEY (gratis en console.groq.com/keys)\n"
                "  config proveedor: ollama    → Instala Ollama (ollama.com) y corre un modelo local\n"
                "Si ya tienes API de OpenAI:\n"
                "  config proveedor: openai    → Luego: config api: TU_KEY"
            )

        full_system = self._build_system_prompt(system_context)

        # Seleccionar método según proveedor
        if self.provider == "gemini":
            return self._think_gemini(user_message, full_system, model)
        else:
            return self._think_openai_compat(user_message, full_system, model)

    def _think_gemini(self, user_message, system_prompt, model=None):
        """Enviar a Google Gemini via REST API (sin dependencias extra)."""
        if not model:
            model = "gemini-2.0-flash"

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model}:generateContent?key={self.api_key}"
        )

        # Convertir historial al formato de Gemini
        contents = []
        for msg in self.conversation[-self.max_history:]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        # Agregar mensaje actual
        contents.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1500,
            }
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            answer = result["candidates"][0]["content"]["parts"][0]["text"]

            # Guardar en historial
            self._save_turn(user_message, answer)
            return answer

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                err = json.loads(body)
                msg = err.get("error", {}).get("message", body[:200])
            except Exception:
                msg = body[:200]
            return f"Error Gemini ({e.code}): {msg}"
        except Exception as e:
            return f"Error de comunicación con Gemini: {e}"

    def _think_openai_compat(self, user_message, system_prompt, model=None):
        """Enviar via API compatible con OpenAI (OpenAI, Groq, Ollama)."""
        if self.provider == "ollama" and not self.client:
            # Fallback: REST API directa para Ollama sin librería openai
            return self._think_ollama_rest(user_message, system_prompt, model)

        if not self.client:
            return "Cliente no inicializado. Verifica la configuración."

        if not model:
            provider_info = PROVIDERS.get(self.provider, {})
            model = provider_info.get("default_model", "gpt-4o-mini")

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation[-self.max_history:])
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1500,
                temperature=0.7,
            )
            answer = response.choices[0].message.content
            self._save_turn(user_message, answer)
            return answer

        except Exception as e:
            return f"Error con {PROVIDERS.get(self.provider, {}).get('name', self.provider)}: {e}"

    def _think_ollama_rest(self, user_message, system_prompt, model=None):
        """Fallback: Ollama via REST API directa (sin librería openai)."""
        if not model:
            model = "llama3.2"

        url = "http://localhost:11434/api/chat"

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation[-self.max_history:])
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.7}
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            answer = result["message"]["content"]
            self._save_turn(user_message, answer)
            return answer

        except urllib.error.URLError:
            return (
                "No se pudo conectar con Ollama. Asegúrate de que esté corriendo:\n"
                "  1. Descarga Ollama: https://ollama.com/download\n"
                "  2. Instala un modelo: ollama pull llama3.2\n"
                "  3. Ollama debe estar ejecutándose en segundo plano"
            )
        except Exception as e:
            return f"Error con Ollama: {e}"

    def _save_turn(self, user_message, answer):
        """Guardar turno de conversación."""
        self.conversation.append({"role": "user", "content": user_message})
        self.conversation.append({"role": "assistant", "content": answer})
        if len(self.conversation) > self.max_history * 2:
            self.conversation = self.conversation[-self.max_history:]
        DataStore.save(CONVERSATION_FILE, self.conversation)

    def clear_memory(self):
        """Limpiar memoria de conversación."""
        self.conversation = []
        DataStore.save(CONVERSATION_FILE, [])


# ══════════════════════════════════════════════════════════════
# EJECUTOR DE ACCIONES
# ══════════════════════════════════════════════════════════════

class ActionExecutor:
    """Ejecuta las acciones que el cerebro IA decide."""

    def __init__(self, app):
        self.app = app

    def execute_all(self, ai_response):
        """Parsear respuesta de IA y ejecutar todos los comandos encontrados."""
        results = []
        clean_text = ai_response

        # Extraer y ejecutar cada comando
        patterns = {
            r'\[TERMINAL\]:\s*(.+)': self._run_terminal,
            r'\[ABRIR\]:\s*(.+)': self._open_program,
            r'\[WEB\]:\s*(.+)': self._open_web,
            r'\[GOOGLE\]:\s*(.+)': self._search_google,
            r'\[YOUTUBE\]:\s*(.+)': self._search_youtube,
            r'\[NOTA\]:\s*(.+)': self._save_note,
            r'\[TAREA\]:\s*(.+)': self._save_todo,
            r'\[RECORDAR\]:\s*(.+)': self._set_reminder,
            r'\[SISTEMA\]:\s*(.+)': self._system_info,
            r'\[PASSWORD\]:\s*(.+)': self._gen_password,
            r'\[CALC\]:\s*(.+)': self._calculate,
            r'\[BLOQUEAR\]': self._lock_pc,
            r'\[SCREENSHOT\]': self._screenshot,
            r'\[COPIAR\]:\s*(.+)': self._copy_clipboard,
            r'\[CARPETA\]:\s*(.+)': self._open_folder,
        }

        for pattern, handler in patterns.items():
            matches = re.finditer(pattern, ai_response, re.IGNORECASE)
            for match in matches:
                try:
                    arg = match.group(1).strip() if match.lastindex else ""
                    result = handler(arg)
                    if result:
                        results.append(result)
                except Exception as e:
                    results.append(f"Error ejecutando acción: {e}")

                # Limpiar el comando del texto visible
                clean_text = clean_text.replace(match.group(0), "").strip()

        return clean_text, results

    def _run_terminal(self, cmd):
        """Ejecutar comando en terminal/PowerShell."""
        try:
            # Seguridad: avisar sobre comandos peligrosos
            dangerous = ["format", "rm -rf /", "del /f /s /q C:", "diskpart"]
            for d in dangerous:
                if d.lower() in cmd.lower():
                    return f"⚠️ Comando bloqueado por seguridad: {cmd}"

            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=30, encoding="utf-8", errors="replace"
            )
            output = result.stdout.strip()
            error = result.stderr.strip()

            if result.returncode == 0:
                if output:
                    return f"💻 Terminal:\n{output[:1500]}"
                return f"💻 Comando ejecutado exitosamente: {cmd}"
            else:
                return f"💻 Terminal (código {result.returncode}):\n{error or output}"

        except subprocess.TimeoutExpired:
            return f"⏰ Comando excedió el tiempo límite: {cmd}"
        except Exception as e:
            return f"❌ Error en terminal: {e}"

    def _open_program(self, name):
        """Abrir un programa."""
        programs = {
            "chrome": "start chrome",
            "firefox": "start firefox",
            "edge": "start msedge",
            "brave": "start brave",
            "notepad": "start notepad",
            "bloc": "start notepad",
            "calc": "start calc",
            "calculadora": "start calc",
            "explorer": "start explorer",
            "explorador": "start explorer",
            "cmd": "start cmd",
            "terminal": "start wt",
            "powershell": "start powershell",
            "paint": "start mspaint",
            "word": "start winword",
            "excel": "start excel",
            "powerpoint": "start powerpnt",
            "outlook": "start outlook",
            "teams": "start msteams:",
            "code": "start code",
            "vscode": "start code",
            "spotify": "start spotify:",
            "discord": "start discord:",
            "steam": "start steam:",
            "taskmgr": "start taskmgr",
            "settings": "start ms-settings:",
            "configuracion": "start ms-settings:",
            "control": "start control",
            "snipping": "start snippingtool",
        }

        key = name.lower().strip()
        cmd = programs.get(key)
        if cmd:
            os.system(cmd)
            return f"Abriendo {name}."
        else:
            # Intentar abrir directamente
            os.system(f"start {key}")
            return f"Intentando abrir {name}."

    def _open_web(self, url):
        """Abrir URL en navegador."""
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return None  # Silencioso

    def _search_google(self, query):
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return None

    def _search_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return None

    def _save_note(self, text):
        notes = DataStore.load(NOTES_FILE, [])
        notes.append({
            "text": text,
            "date": datetime.datetime.now().isoformat()
        })
        DataStore.save(NOTES_FILE, notes)
        return None  # IA ya confirma

    def _save_todo(self, text):
        todos = DataStore.load(TODOS_FILE, [])
        todos.append({
            "text": text,
            "done": False,
            "date": datetime.datetime.now().isoformat()
        })
        DataStore.save(TODOS_FILE, todos)
        return None

    def _set_reminder(self, text):
        parts = text.split("|")
        if len(parts) == 2:
            reminder_text = parts[0].strip()
            minutes = int(parts[1].strip())
            self.app.reminder_system.add(reminder_text, minutes)
        return None

    def _system_info(self, what):
        what = what.lower().strip()
        if what == "info":
            return self._get_system_info()
        elif what == "cpu":
            return self._get_cpu_info()
        elif what == "disco":
            return self._get_disk_info()
        elif what == "red":
            return self._get_network_info()
        elif what == "bateria":
            return self._get_battery_info()
        return self._get_system_info()

    def _get_system_info(self):
        lines = [
            f"Sistema: {platform.system()} {platform.release()}",
            f"Equipo: {platform.node()}",
            f"CPU: {platform.processor() or 'N/A'} ({os.cpu_count()} núcleos)",
            f"Python: {platform.python_version()}",
        ]
        if HAS_PSUTIL:
            ram = psutil.virtual_memory()
            lines.append(f"RAM: {ram.used/1024**3:.1f}/{ram.total/1024**3:.1f} GB ({ram.percent}%)")
            cpu_pct = psutil.cpu_percent(interval=0.5)
            lines.append(f"CPU: {cpu_pct}%")
        return "💻 " + " | ".join(lines)

    def _get_cpu_info(self):
        if not HAS_PSUTIL:
            return f"CPU: {platform.processor()} ({os.cpu_count()} núcleos). Instala psutil para más detalles."
        cpu_pct = psutil.cpu_percent(interval=1, percpu=True)
        ram = psutil.virtual_memory()
        avg = sum(cpu_pct) / len(cpu_pct)
        bar = self._bar(avg)
        ram_bar = self._bar(ram.percent)
        return (
            f"🧠 CPU: {bar} {avg:.0f}% (núcleos: {', '.join(f'{p:.0f}%' for p in cpu_pct)})\n"
            f"🗃️ RAM: {ram_bar} {ram.percent}% ({ram.used/1024**3:.1f}/{ram.total/1024**3:.1f} GB)"
        )

    def _get_disk_info(self):
        lines = []
        if os.name == "nt":
            for letter in "CDEFGH":
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    u = shutil.disk_usage(drive)
                    pct = u.used / u.total * 100
                    bar = self._bar(pct)
                    lines.append(f"💾 {drive} {bar} {pct:.0f}% ({u.free/1024**3:.1f} GB libres)")
        else:
            u = shutil.disk_usage("/")
            pct = u.used / u.total * 100
            lines.append(f"💾 / {self._bar(pct)} {pct:.0f}% ({u.free/1024**3:.1f} GB libres)")
        return "\n".join(lines)

    def _get_network_info(self):
        lines = []
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            lines.append(f"🏠 Local: {local_ip}")
        except Exception:
            pass
        try:
            req = urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5)
            data = json.loads(req.read().decode())
            lines.append(f"🌍 Pública: {data.get('ip', 'N/A')}")
        except Exception:
            lines.append("🌍 Pública: Sin conexión")
        return " | ".join(lines)

    def _get_battery_info(self):
        if not HAS_PSUTIL:
            return "Instala psutil para ver batería."
        bat = psutil.sensors_battery()
        if not bat:
            return "No se detectó batería (probablemente PC de escritorio)."
        plug = "🔌 Conectado" if bat.power_plugged else "🔋 Batería"
        return f"{self._bar(bat.percent)} {bat.percent}% ({plug})"

    def _gen_password(self, length_str):
        try:
            length = int(length_str.strip())
        except (ValueError, AttributeError):
            length = 16
        length = max(8, min(128, length))
        chars = string.ascii_letters + string.digits + "!@#$%^&*_+-="
        pwd = "".join(random.SystemRandom().choice(chars) for _ in range(length))
        try:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(pwd)
            return f"🔐 {pwd}\n(Copiada al portapapeles)"
        except Exception:
            return f"🔐 {pwd}"

    def _calculate(self, expr):
        try:
            expr = expr.replace("^", "**").replace(",", ".")
            safe = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
                "pi": math.pi, "e": math.e, "pow": pow,
            }
            result = eval(expr, {"__builtins__": {}}, safe)
            return f"🧮 = {result}"
        except Exception as e:
            return f"🧮 Error: {e}"

    def _lock_pc(self, _=None):
        if os.name == "nt":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        return None

    def _screenshot(self, _=None):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(os.path.expanduser("~"), "Desktop", f"jarvis_capture_{ts}.png")
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            img.save(path)
            return f"📸 Captura guardada: {path}"
        except ImportError:
            if os.name == "nt":
                os.system(f'powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen | ForEach-Object {{ $bmp = New-Object System.Drawing.Bitmap($_.Bounds.Width,$_.Bounds.Height); $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($_.Bounds.Location,[System.Drawing.Point]::Empty,$_.Bounds.Size); $bmp.Save(\'{path}\') }}"')
                return f"📸 Captura guardada: {path}"
        return "No pude tomar la captura."

    def _copy_clipboard(self, text):
        try:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(text)
        except Exception:
            pass
        return None

    def _open_folder(self, path_name):
        path_name = path_name.lower().strip()
        home = os.path.expanduser("~")
        folders = {
            "descargas": os.path.join(home, "Downloads"),
            "downloads": os.path.join(home, "Downloads"),
            "documentos": os.path.join(home, "Documents"),
            "documents": os.path.join(home, "Documents"),
            "escritorio": os.path.join(home, "Desktop"),
            "desktop": os.path.join(home, "Desktop"),
            "home": home,
        }
        target = folders.get(path_name, path_name)
        if os.path.exists(target):
            if os.name == "nt":
                os.startfile(target)
            else:
                subprocess.Popen(["xdg-open", target])
        return None

    def _bar(self, pct, length=12):
        filled = int(length * pct / 100)
        return "[" + "█" * filled + "░" * (length - filled) + "]"


# ══════════════════════════════════════════════════════════════
# SISTEMA DE RECORDATORIOS
# ══════════════════════════════════════════════════════════════

class ReminderSystem:
    def __init__(self, callback):
        self.reminders = DataStore.load(REMINDERS_FILE, [])
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def add(self, text, minutes):
        r = {
            "text": text,
            "time": (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).isoformat(),
            "triggered": False,
        }
        self.reminders.append(r)
        DataStore.save(REMINDERS_FILE, self.reminders)
        return r

    def _loop(self):
        while self.running:
            now = datetime.datetime.now()
            for r in self.reminders:
                if not r.get("triggered"):
                    if now >= datetime.datetime.fromisoformat(r["time"]):
                        r["triggered"] = True
                        DataStore.save(REMINDERS_FILE, self.reminders)
                        self.callback(r["text"])
            time.sleep(3)

    def stop(self):
        self.running = False


# ══════════════════════════════════════════════════════════════
# APLICACION PRINCIPAL
# ══════════════════════════════════════════════════════════════

class JarvisUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S. ULTIMATE")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)
        self.root.configure(bg=C["bg"])

        # Config
        self.config = DataStore.load(CONFIG_FILE, {})
        if isinstance(self.config, list):
            self.config = {}
        self.config.setdefault("provider", "gemini")  # Proveedor por defecto (GRATIS)
        self.config.setdefault("api_key", "")
        self.config.setdefault("model", "")  # Vacío = usa default del proveedor
        self.config.setdefault("voice_enabled", True)
        self.config.setdefault("user_name", "señor")

        # Historial
        self.command_history = deque(DataStore.load(HISTORY_FILE, []), maxlen=200)
        self.history_index = -1

        # Subsistemas
        self.voice = VoiceEngine()
        self.voice.voice_enabled = self.config.get("voice_enabled", True)
        self.brain = AIBrain()
        provider = self.config.get("provider", "gemini")
        api_key = self.config.get("api_key", "")
        if api_key or provider == "ollama":
            self.brain.init_provider(provider, api_key)
        self.reminder_system = ReminderSystem(self._on_reminder)
        self.executor = ActionExecutor(self)

        # Estado
        self.listening_mode = False
        self.continuous_listen = False

        # UI
        self._build_ui()

        # Saludo inicial
        self.root.after(500, self._startup_greeting)

        # Cerrar
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ─── UI ──────────────────────────────────────────

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # === SIDEBAR ===
        sidebar = tk.Frame(self.root, bg=C["bg2"], width=200)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        # Logo
        tk.Label(sidebar, text="⚡", font=("Segoe UI", 40),
                 bg=C["bg2"], fg=C["accent"]).pack(pady=(20, 0))
        tk.Label(sidebar, text="J.A.R.V.I.S.", font=("Consolas", 14, "bold"),
                 bg=C["bg2"], fg=C["accent"]).pack()
        tk.Label(sidebar, text="ULTIMATE", font=("Consolas", 8),
                 bg=C["bg2"], fg=C["muted"]).pack()

        # Reloj
        self.clock_lbl = tk.Label(sidebar, font=("Consolas", 22, "bold"),
                                  bg=C["bg2"], fg=C["green"])
        self.clock_lbl.pack(pady=(15, 0))
        self.date_lbl = tk.Label(sidebar, font=("Consolas", 9),
                                 bg=C["bg2"], fg=C["text2"])
        self.date_lbl.pack()

        # Estado de voz
        self.voice_status = tk.Label(sidebar, text="", font=("Consolas", 9),
                                     bg=C["bg2"], fg=C["accent"])
        self.voice_status.pack(pady=(10, 0))

        # Separador
        tk.Frame(sidebar, bg=C["muted"], height=1).pack(fill="x", padx=15, pady=10)

        # Botones
        btns = [
            ("🎤 Modo Voz", self._toggle_continuous_listen),
            ("🔇 Silenciar", self._toggle_voice),
            ("💻 Info Sistema", lambda: self._quick_cmd("dame info del sistema")),
            ("🧠 CPU/RAM", lambda: self._quick_cmd("como esta el cpu y la ram")),
            ("💾 Disco", lambda: self._quick_cmd("cuanto espacio tengo en disco")),
            ("🌐 Mi IP", lambda: self._quick_cmd("cual es mi ip")),
            ("📝 Mis Notas", lambda: self._quick_cmd("muestrame mis notas")),
            ("✅ Tareas", lambda: self._quick_cmd("muestrame mis tareas pendientes")),
            ("🔐 Password", lambda: self._quick_cmd("generame una contraseña de 20 caracteres")),
            ("🧹 Limpiar", self._clear_output),
            ("🧠 Reset IA", self._reset_ai),
            ("⚙️ Config", self._show_config),
        ]

        for text, cmd in btns:
            b = tk.Button(sidebar, text=text, font=("Segoe UI", 9),
                          bg=C["bg3"], fg=C["text"], bd=0, padx=8, pady=3,
                          anchor="w", cursor="hand2", command=cmd,
                          activebackground=C["accent"], activeforeground="black")
            b.pack(fill="x", padx=10, pady=1)
            b.bind("<Enter>", lambda e, b=b: b.config(bg=C["border"]))
            b.bind("<Leave>", lambda e, b=b: b.config(bg=C["bg3"]))

        # Deps status
        deps = []
        if HAS_OPENAI: deps.append("✅ OpenAI")
        else: deps.append("❌ OpenAI")
        if HAS_PYTTSX3: deps.append("✅ Voz")
        else: deps.append("❌ Voz")
        if HAS_SPEECH: deps.append("✅ Mic")
        else: deps.append("❌ Mic")
        if HAS_PSUTIL: deps.append("✅ Psutil")
        else: deps.append("❌ Psutil")

        tk.Label(sidebar, text=" | ".join(deps[:2]),
                 font=("Consolas", 7), bg=C["bg2"], fg=C["muted"]).pack(side="bottom", pady=(0, 2))
        tk.Label(sidebar, text=" | ".join(deps[2:]),
                 font=("Consolas", 7), bg=C["bg2"], fg=C["muted"]).pack(side="bottom")
        tk.Label(sidebar, text=f"v{VERSION}",
                 font=("Consolas", 7), bg=C["bg2"], fg=C["muted"]).pack(side="bottom")

        # === MAIN ===
        main = tk.Frame(self.root, bg=C["bg"])
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Output
        self.output = scrolledtext.ScrolledText(
            main, font=("Consolas", 11), bg=C["bg"], fg=C["text"],
            insertbackground=C["accent"], selectbackground=C["accent"],
            selectforeground="black", bd=0, padx=15, pady=15,
            wrap="word", state="disabled", cursor="arrow"
        )
        self.output.grid(row=0, column=0, sticky="nsew", padx=(5, 10), pady=(10, 5))

        # Tags
        self.output.tag_configure("jarvis", foreground=C["accent"])
        self.output.tag_configure("user", foreground=C["green"])
        self.output.tag_configure("error", foreground=C["red"])
        self.output.tag_configure("info", foreground=C["yellow"])
        self.output.tag_configure("muted", foreground=C["muted"])
        self.output.tag_configure("system", foreground=C["purple"])
        self.output.tag_configure("action", foreground=C["orange"])

        # Input area
        input_frame = tk.Frame(main, bg=C["bg"])
        input_frame.grid(row=1, column=0, sticky="ew", padx=(5, 10), pady=(0, 10))
        input_frame.grid_columnconfigure(1, weight=1)

        # Mic button
        self.mic_btn = tk.Button(
            input_frame, text="🎤", font=("Segoe UI", 16),
            bg=C["bg3"], fg=C["accent"], bd=0, padx=8,
            cursor="hand2", command=self._voice_input,
            activebackground=C["accent"], activeforeground="black"
        )
        self.mic_btn.grid(row=0, column=0, padx=(0, 5), sticky="ns")

        self.entry = tk.Entry(
            input_frame, font=("Consolas", 13),
            bg=C["bg3"], fg=C["text"], insertbackground=C["accent"],
            selectbackground=C["accent"], bd=0, relief="flat"
        )
        self.entry.grid(row=0, column=1, sticky="ew", ipady=10)
        self.entry.focus_set()

        send_btn = tk.Button(
            input_frame, text="▶", font=("Segoe UI", 14, "bold"),
            bg=C["accent"], fg="black", bd=0, padx=15,
            cursor="hand2", command=self._send,
            activebackground=C["green"]
        )
        send_btn.grid(row=0, column=2, padx=(5, 0), sticky="ns")

        # Status
        self.status_lbl = tk.Label(
            input_frame, text="💡 Habla o escribe. Todo pasa por el cerebro IA.",
            font=("Segoe UI", 8), bg=C["bg"], fg=C["muted"], anchor="w"
        )
        self.status_lbl.grid(row=1, column=0, columnspan=3, sticky="w", pady=(3, 0))

        # Bindings
        self.entry.bind("<Return>", lambda e: self._send())
        self.entry.bind("<Up>", lambda e: self._hist(-1))
        self.entry.bind("<Down>", lambda e: self._hist(1))
        self.root.bind("<Escape>", lambda e: self.entry.focus_set())
        self.root.bind("<Control-l>", lambda e: self._clear_output())

        # Clock
        self._tick()

    # ─── RELOJ ───────────────────────────────────────

    def _tick(self):
        now = datetime.datetime.now()
        self.clock_lbl.config(text=now.strftime("%H:%M:%S"))
        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        self.date_lbl.config(text=f"{dias[now.weekday()]} {now.day}/{now.month:02d}/{now.year}")

        # Actualizar estado de voz
        if self.voice.is_listening:
            self.voice_status.config(text="🎤 Escuchando...", fg=C["red"])
            self.mic_btn.config(bg=C["red"], fg="white")
        elif self.voice.is_speaking:
            self.voice_status.config(text="🔊 Hablando...", fg=C["green"])
            self.mic_btn.config(bg=C["bg3"], fg=C["accent"])
        elif self.continuous_listen:
            self.voice_status.config(text="🎤 Modo voz activo", fg=C["accent"])
            self.mic_btn.config(bg=C["bg3"], fg=C["accent"])
        else:
            self.voice_status.config(text="")
            self.mic_btn.config(bg=C["bg3"], fg=C["accent"])

        self.root.after(500, self._tick)

    # ─── OUTPUT ──────────────────────────────────────

    def _print(self, text, tag="jarvis"):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n", tag)
        self.output.see("end")
        self.output.config(state="disabled")

    def _print_user(self, text):
        ts = datetime.datetime.now().strftime("%H:%M")
        self.output.config(state="normal")
        self.output.insert("end", f"\n[{ts}] ", "muted")
        self.output.insert("end", f"Tú: {text}\n", "user")
        self.output.config(state="disabled")

    def _print_jarvis(self, text):
        ts = datetime.datetime.now().strftime("%H:%M")
        self.output.config(state="normal")
        self.output.insert("end", f"[{ts}] ", "muted")
        self.output.insert("end", f"Jarvis: {text}\n\n", "jarvis")
        self.output.see("end")
        self.output.config(state="disabled")

    def _print_action(self, text):
        self.output.config(state="normal")
        self.output.insert("end", f"  → {text}\n", "action")
        self.output.see("end")
        self.output.config(state="disabled")

    def _clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    # ─── HISTORIAL ───────────────────────────────────

    def _hist(self, direction):
        if not self.command_history:
            return
        h = list(self.command_history)
        self.history_index += direction
        self.history_index = max(-1, min(self.history_index, len(h) - 1))
        self.entry.delete(0, "end")
        if self.history_index >= 0:
            self.entry.insert(0, h[-(self.history_index + 1)])

    # ─── ENVIAR MENSAJE ─────────────────────────────

    def _send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.history_index = -1
        self._process_input(text)

    def _quick_cmd(self, text):
        """Enviar comando rápido desde botón."""
        self._process_input(text)

    def _process_input(self, text):
        """Procesar cualquier input (texto o voz)."""
        # Guardar historial
        self.command_history.append(text)
        DataStore.save(HISTORY_FILE, list(self.command_history))

        # Mostrar en pantalla
        self._print_user(text)

        comando = text.lower().strip()

        # ── Comandos locales (no necesitan IA) ──

        if comando in ("salir", "exit", "quit"):
            self._on_close()
            return

        if comando in ("cls", "clear", "limpiar"):
            self._clear_output()
            return

        if comando.startswith("config proveedor:") or comando.startswith("config provider:"):
            prov = text.split(":", 1)[1].strip().lower()
            if prov not in PROVIDERS:
                self._print_jarvis(
                    f"Proveedor '{prov}' no reconocido. Opciones: {', '.join(PROVIDERS.keys())}"
                )
                return
            self.config["provider"] = prov
            pinfo = PROVIDERS[prov]
            self.config["model"] = ""  # Reset model al default del proveedor
            DataStore.save(CONFIG_FILE, self.config)
            self._print_jarvis(
                f"Proveedor cambiado a {pinfo['name']} ({pinfo['cost']}).\n"
                f"Modelo por defecto: {pinfo['default_model']}\n"
                f"Modelos disponibles: {', '.join(pinfo['models'])}"
            )
            if prov == "ollama":
                self._print("  ℹ️ Ollama no necesita API key. Asegúrate de tener Ollama corriendo.", "muted")
                self._print("  ℹ️ Instala un modelo: ollama pull llama3.2", "muted")
                # Intentar conectar directamente
                self.brain.init_provider("ollama", "")
            else:
                api_key = self.config.get("api_key", "")
                if api_key:
                    self.brain.init_provider(prov, api_key)
                    self._print_jarvis("Cerebro reconectado con el nuevo proveedor.")
                else:
                    self._print(f"  ⚠️ Configura tu API key: config api: TU_KEY", "muted")
                    self._print(f"  ℹ️ Obtén una gratis en: {pinfo['get_key_url']}", "muted")
            self.voice.speak(f"Proveedor cambiado a {pinfo['name']}.")
            return

        if comando.startswith("config api:") or comando.startswith("config key:"):
            key = text.split(":", 1)[1].strip()
            self.config["api_key"] = key
            provider = self.config.get("provider", "gemini")
            DataStore.save(CONFIG_FILE, self.config)
            if self.brain.init_provider(provider, key):
                pname = PROVIDERS.get(provider, {}).get("name", provider)
                self._print_jarvis(f"API Key configurada para {pname}. Mi cerebro está conectado, señor.")
                self.voice.speak("API Key configurada. Estoy listo.")
            else:
                if PROVIDERS.get(provider, {}).get("needs_openai_lib") and not HAS_OPENAI:
                    self._print_jarvis(
                        f"El proveedor {provider} necesita la librería openai.\n"
                        "Instálala con: pip install openai"
                    )
                else:
                    self._print_jarvis("Hubo un problema conectando. Verifica tu API key.")
            return

        if comando.startswith("config modelo:") or comando.startswith("config model:"):
            model = text.split(":", 1)[1].strip()
            provider = self.config.get("provider", "gemini")
            available = PROVIDERS.get(provider, {}).get("models", [])
            self.config["model"] = model
            DataStore.save(CONFIG_FILE, self.config)
            self._print_jarvis(f"Modelo cambiado a {model}.")
            if available and model not in available:
                self._print(f"  ⚠️ Modelos conocidos para {provider}: {', '.join(available)}", "muted")
            return

        if comando.startswith("config nombre:"):
            name = text.split(":", 1)[1].strip()
            self.config["user_name"] = name
            DataStore.save(CONFIG_FILE, self.config)
            self._print_jarvis(f"Entendido. Te llamaré {name} de ahora en adelante.")
            return

        if comando in ("proveedores", "providers", "modelos"):
            self._show_providers()
            return

        # ── Todo lo demás: enviar al cerebro IA ──

        if not self.brain.ready:
            # Sin IA: Intentar respuesta local básica
            self._fallback_response(text)
            return

        # Status
        self.status_lbl.config(text="🧠 Procesando...", fg=C["accent"])
        self.root.update()

        def process():
            # Contexto adicional
            context_parts = []

            # Notas y tareas para que IA las conozca
            notes = DataStore.load(NOTES_FILE, [])
            todos = DataStore.load(TODOS_FILE, [])
            if notes:
                context_parts.append(f"Notas guardadas: {json.dumps(notes[-10:], ensure_ascii=False)}")
            if todos:
                context_parts.append(f"Tareas: {json.dumps(todos[-10:], ensure_ascii=False)}")

            context = "\n".join(context_parts)

            # Pensar
            model = self.config.get("model", "") or None  # None = usa default del proveedor
            response = self.brain.think(
                text,
                system_context=context,
                model=model
            )

            # Ejecutar acciones
            clean_text, action_results = self.executor.execute_all(response)

            # Mostrar en UI (desde hilo principal)
            def show():
                if clean_text.strip():
                    self._print_jarvis(clean_text.strip())
                for r in action_results:
                    if r:
                        self._print_action(r)

                # Hablar respuesta
                if clean_text.strip():
                    self.voice.speak(clean_text.strip())

                self.status_lbl.config(text="💡 Listo.", fg=C["muted"])

                # Si estamos en modo escucha continua, volver a escuchar
                if self.continuous_listen and not self.voice.is_listening:
                    self.root.after(1500, self._voice_input)

            self.root.after(0, show)

        threading.Thread(target=process, daemon=True).start()

    def _fallback_response(self, text):
        """Respuesta sin IA - modo offline básico."""
        comando = text.lower()

        # Comandos básicos sin IA
        if any(w in comando for w in ["hora", "time", "qué hora"]):
            r = f"Son las {datetime.datetime.now().strftime('%H:%M:%S')}."
            self._print_jarvis(r)
            self.voice.speak(r)
            return

        if any(w in comando for w in ["fecha", "día", "dia", "date"]):
            r = f"Hoy es {datetime.datetime.now().strftime('%d/%m/%Y')}."
            self._print_jarvis(r)
            self.voice.speak(r)
            return

        if "sistema" in comando or "info" in comando:
            info = self.executor._get_system_info()
            self._print_jarvis(info)
            return

        if "cpu" in comando or "ram" in comando:
            info = self.executor._get_cpu_info()
            self._print_jarvis(info)
            return

        if "disco" in comando or "espacio" in comando:
            info = self.executor._get_disk_info()
            self._print_jarvis(info)
            return

        if "ip" in comando or "red" in comando:
            self._print_jarvis("Consultando red...")
            def get_net():
                info = self.executor._get_network_info()
                self.root.after(0, lambda: self._print_jarvis(info))
            threading.Thread(target=get_net, daemon=True).start()
            return

        if "chrome" in comando:
            os.system("start chrome")
            self._print_jarvis("Abriendo Chrome.")
            return

        if "notepad" in comando or "bloc" in comando:
            os.system("start notepad")
            self._print_jarvis("Abriendo bloc de notas.")
            return

        if "calc" in comando:
            os.system("start calc")
            self._print_jarvis("Abriendo calculadora.")
            return

        provider = self.config.get("provider", "gemini")
        pinfo = PROVIDERS.get(provider, PROVIDERS["gemini"])
        self._print_jarvis(
            f"Mi cerebro no está conectado, señor. Proveedor actual: {pinfo['name']}\n\n"
            "🔧 CONFIGURACIÓN RÁPIDA (elige una opción GRATIS):\n\n"
            "  Opción 1 - Google Gemini (recomendado):\n"
            "    config proveedor: gemini\n"
            "    config api: TU_KEY  → Obtén gratis: https://aistudio.google.com/apikey\n\n"
            "  Opción 2 - Groq (ultra rápido):\n"
            "    config proveedor: groq\n"
            "    config api: TU_KEY  → Obtén gratis: https://console.groq.com/keys\n\n"
            "  Opción 3 - Ollama (local, sin internet):\n"
            "    config proveedor: ollama  → Solo necesitas instalar: https://ollama.com\n\n"
            "  Opción 4 - OpenAI (de pago):\n"
            "    config proveedor: openai\n"
            "    config api: TU_KEY  → https://platform.openai.com/api-keys\n\n"
            "Sin IA, solo tengo comandos básicos."
        )
        self._print("  Comandos offline: hora, fecha, sistema, cpu, disco, ip, abrir chrome/notepad/calc", "muted")

    # ─── VOZ ─────────────────────────────────────────

    def _voice_input(self):
        """Activar escucha por micrófono."""
        if self.voice.is_listening:
            return

        if not HAS_SPEECH:
            self._print_jarvis("Micrófono no disponible. Instala: pip install SpeechRecognition pyaudio")
            return

        self.status_lbl.config(text="🎤 Escuchando...", fg=C["red"])
        self._print("🎤 Escuchando...", "info")
        self.root.update()

        def on_heard(text):
            self.root.after(0, lambda: self._process_input(text))

        def on_error(msg):
            def show():
                self._print(f"  {msg}", "muted")
                self.status_lbl.config(text="💡 Listo.", fg=C["muted"])
                # Reintentar si modo continuo
                if self.continuous_listen:
                    self.root.after(1000, self._voice_input)
            self.root.after(0, show)

        self.voice.listen(on_heard, on_error, timeout=8, phrase_limit=20)

    def _toggle_continuous_listen(self):
        """Activar/desactivar modo escucha continua."""
        self.continuous_listen = not self.continuous_listen
        if self.continuous_listen:
            self._print_jarvis("Modo voz activado. Estoy escuchando, señor.")
            self.voice.speak("Modo voz activado. Estoy escuchando.")
            self._voice_input()
        else:
            self._print_jarvis("Modo voz desactivado.")
            self.voice.speak("Modo voz desactivado.")

    def _toggle_voice(self):
        """Silenciar/activar respuestas de voz."""
        enabled = self.voice.toggle_voice()
        self.config["voice_enabled"] = enabled
        DataStore.save(CONFIG_FILE, self.config)
        if enabled:
            self._print_jarvis("Voz activada.")
            self.voice.speak("Voz activada.")
        else:
            self._print_jarvis("Voz desactivada. Solo responderé por texto.")

    # ─── RECORDATORIOS ───────────────────────────────

    def _on_reminder(self, text):
        def show():
            self._print(f"\n🔔 ¡RECORDATORIO! → {text}\n", "info")
            self.voice.speak(f"Señor, le recuerdo: {text}")
            try:
                messagebox.showinfo("⏰ Recordatorio - Jarvis", text)
            except Exception:
                pass
        self.root.after(0, show)

    # ─── CONFIG / RESET ──────────────────────────────

    def _show_config(self):
        provider = self.config.get("provider", "gemini")
        pinfo = PROVIDERS.get(provider, {})
        pname = pinfo.get("name", provider)
        pcost = pinfo.get("cost", "?")
        api = self.config.get("api_key", "")
        if len(api) > 10:
            masked = f"...{api[-6:]}"
        elif provider == "ollama":
            masked = "(no necesaria)"
        else:
            masked = "(no configurada)"
        model = self.config.get("model", "") or pinfo.get("default_model", "auto")
        voice = "Activada" if self.config.get("voice_enabled") else "Desactivada"
        brain = "✅ Conectado" if self.brain.ready else "❌ Sin conexión"

        self._print(f"""
⚙️ CONFIGURACIÓN ACTUAL
═══════════════════════════════
  Proveedor: {pname} ({pcost})
  Estado:    {brain}
  API Key:   {masked}
  Modelo:    {model}
  Voz:       {voice}
  Datos:     {DATA_DIR}

  Cambiar:
  • config proveedor: gemini/groq/ollama/openai
  • config api: TU_API_KEY
  • config modelo: nombre_del_modelo
  • config nombre: tu_nombre
  • proveedores   (ver todos los proveedores)
═══════════════════════════════
""", "system")

    def _show_providers(self):
        """Mostrar todos los proveedores disponibles."""
        lines = ["\n🤖 PROVEEDORES DE IA DISPONIBLES", "═" * 40]
        current = self.config.get("provider", "gemini")
        for key, p in PROVIDERS.items():
            marker = " ◀ ACTIVO" if key == current else ""
            lines.append(f"\n  {p['name']} [{key}] - {p['cost']}{marker}")
            lines.append(f"    Modelos: {', '.join(p['models'])}")
            lines.append(f"    Default: {p['default_model']}")
            if key == "ollama":
                lines.append(f"    Setup: Instala desde {p['get_key_url']}")
            else:
                lines.append(f"    API Key: {p['get_key_url']}")
            if p.get("needs_openai_lib"):
                lib_status = "✅" if HAS_OPENAI else "❌ (pip install openai)"
                lines.append(f"    Librería openai: {lib_status}")
        lines.append("\n" + "═" * 40)
        self._print("\n".join(lines), "system")

    def _reset_ai(self):
        self.brain.clear_memory()
        self._print_jarvis("Memoria reiniciada. Empezamos de cero, señor.")
        self.voice.speak("Memoria reiniciada.")

    # ─── STARTUP ─────────────────────────────────────

    def _startup_greeting(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            period = "Buenos días"
        elif hour < 19:
            period = "Buenas tardes"
        else:
            period = "Buenas noches"

        name = self.config.get("user_name", "señor")
        provider = self.config.get("provider", "gemini")
        pinfo = PROVIDERS.get(provider, {})

        self._print(f"""
⚡ ═══════════════════════════════════════════════ ⚡
       J.A.R.V.I.S. ULTIMATE v{VERSION}
       Just A Rather Very Intelligent System
       IA: {pinfo.get('name', provider)} ({pinfo.get('cost', '?')})
⚡ ═══════════════════════════════════════════════ ⚡
""", "jarvis")

        greeting = f"{period}, {name}. Todos los sistemas están operativos."
        self._print_jarvis(greeting)

        # Estado del cerebro
        if self.brain.ready:
            model = self.config.get("model", "") or pinfo.get("default_model", "")
            self._print(f"  🧠 Cerebro: {pinfo.get('name', provider)} → {model}", "muted")
        else:
            if provider == "ollama":
                self._print("  ⚠️ Ollama no está conectado. Asegúrate de tener Ollama corriendo.", "muted")
                self._print("  ℹ️ Descarga: https://ollama.com/download", "muted")
            elif not self.config.get("api_key"):
                self._print(f"  ⚠️ Sin API key. Configura: config api: TU_KEY", "muted")
                self._print(f"  ℹ️ Obtén gratis: {pinfo.get('get_key_url', '')}", "muted")
                self._print("  ℹ️ O cambia proveedor: config proveedor: gemini/groq/ollama", "muted")

        # Verificar dependencias
        missing = []
        if not HAS_PYTTSX3: missing.append("pyttsx3")
        if not HAS_SPEECH: missing.append("SpeechRecognition pyaudio")
        if not HAS_PSUTIL: missing.append("psutil")
        # Solo avisar de openai si el proveedor lo necesita
        if pinfo.get("needs_openai_lib") and not HAS_OPENAI:
            missing.append("openai")

        if missing:
            self._print(f"  ⚠️ Para funcionalidad completa instala: pip install {' '.join(missing)}", "muted")

        self.voice.speak(greeting)

    # ─── CERRAR ──────────────────────────────────────

    def _on_close(self):
        self.reminder_system.stop()
        self.voice.stop_speaking()
        DataStore.save(CONFIG_FILE, self.config)
        DataStore.save(HISTORY_FILE, list(self.command_history))
        self.root.destroy()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisUltimate(root)
    root.mainloop()
