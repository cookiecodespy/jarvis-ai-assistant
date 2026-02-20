"""
╔═══════════════════════════════════════════════════════════════════════╗
║                    J.A.R.V.I.S. GOD MODE                             ║
║          Just A Rather Very Intelligent System                       ║
║                                                                       ║
║  La versión más avanzada. Lo más cercano a ser Tony Stark.           ║
║                                                                       ║
║  NUEVAS CARACTERÍSTICAS vs Ultimate:                                  ║
║   ✦ Edge TTS — Voces ultra realistas (casi humanas)                  ║
║   ✦ Wake Word — Di "Jarvis" para activar sin tocar nada             ║
║   ✦ Typewriter — Texto aparece letra por letra                       ║
║   ✦ Clima en tiempo real (Open-Meteo, gratis)                        ║
║   ✦ Traductor integrado (MyMemory API, gratis)                      ║
║   ✦ Noticias en vivo (RSS, gratis)                                   ║
║   ✦ Efectos de sonido (Windows)                                      ║
║   ✦ 4 Temas visuales (Iron Man, Jarvis, Matrix, F.R.I.D.A.Y.)      ║
║   ✦ Pomodoro Timer                                                    ║
║   ✦ Programador de tareas (cron-like)                                ║
║   ✦ Buscador de archivos                                             ║
║   ✦ Administrador de procesos                                        ║
║   ✦ Historial del portapapeles                                       ║
║   ✦ Exportar conversaciones                                          ║
║   ✦ Animación de inicio cinematográfica                              ║
║   ✦ Panel de monitoreo en tiempo real                                ║
║   ✦ Atajos globales de teclado                                       ║
║                                                                       ║
║  Proveedores de IA (elige uno):                                       ║
║   - Google Gemini   → GRATIS (recomendado)                           ║
║   - Groq            → GRATIS (ultra rápido)                          ║
║   - Ollama          → GRATIS (local, sin internet)                   ║
║   - OpenAI          → De pago                                         ║
║                                                                       ║
║  Instalación rápida:                                                  ║
║    pip install edge-tts psutil SpeechRecognition pyaudio              ║
║                                                                       ║
║  Uso: python jarvis_god_mode.py                                      ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import time
import os
import sys
import json
import math
import random
import string
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
import asyncio
import tempfile
import glob
from collections import deque

# ══════════════════════════════════════════════════════════════
# DEPENDENCIAS OPCIONALES
# ══════════════════════════════════════════════════════════════

HAS_PYTTSX3 = False
HAS_SPEECH = False
HAS_PSUTIL = False
HAS_OPENAI = False
HAS_EDGE_TTS = False
HAS_WINSOUND = False

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

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    pass

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    pass

HAS_CV2 = False
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    pass


# ══════════════════════════════════════════════════════════════
# TEMAS VISUALES
# ══════════════════════════════════════════════════════════════

THEMES = {
    "jarvis": {
        "name": "J.A.R.V.I.S. Classic",
        "bg": "#0A0E1A", "bg2": "#111827", "bg3": "#1E293B",
        "accent": "#00D4FF", "accent2": "#38BDF8",
        "green": "#34D399", "red": "#F87171", "yellow": "#FBBF24",
        "purple": "#A78BFA", "orange": "#FB923C",
        "text": "#E2E8F0", "text2": "#94A3B8", "muted": "#475569",
        "border": "#1E293B",
    },
    "ironman": {
        "name": "Iron Man",
        "bg": "#0D0000", "bg2": "#1A0505", "bg3": "#2D0A0A",
        "accent": "#FF3333", "accent2": "#FF6B6B",
        "green": "#FFD700", "red": "#FF0000", "yellow": "#FF8C00",
        "purple": "#FF4500", "orange": "#FF6347",
        "text": "#FFE4E1", "text2": "#CD853F", "muted": "#8B4513",
        "border": "#2D0A0A",
    },
    "matrix": {
        "name": "Matrix",
        "bg": "#000000", "bg2": "#001100", "bg3": "#002200",
        "accent": "#00FF00", "accent2": "#33FF33",
        "green": "#00FF00", "red": "#FF0000", "yellow": "#00FF00",
        "purple": "#00CC00", "orange": "#00FF66",
        "text": "#00FF00", "text2": "#009900", "muted": "#004400",
        "border": "#003300",
    },
    "friday": {
        "name": "F.R.I.D.A.Y.",
        "bg": "#0F0520", "bg2": "#1A0A30", "bg3": "#251540",
        "accent": "#E040FB", "accent2": "#F06EFF",
        "green": "#76FF03", "red": "#FF1744", "yellow": "#FFD740",
        "purple": "#D500F9", "orange": "#FF9100",
        "text": "#F3E5F5", "text2": "#CE93D8", "muted": "#6A1B9A",
        "border": "#251540",
    },
    "edex": {
        "name": "EDEX-UI Cyan",
        "bg": "#000000", "bg2": "#0A0A0A", "bg3": "#111111",
        "accent": "#00FFFF", "accent2": "#00CCCC",
        "green": "#00FF88", "red": "#FF0055", "yellow": "#FFAA00",
        "purple": "#AA00FF", "orange": "#FF6600",
        "text": "#CCFFFF", "text2": "#669999", "muted": "#334444",
        "border": "#00FFFF",
        "glow": "#00FFFF",
    },
    "edex_red": {
        "name": "EDEX-UI Red",
        "bg": "#000000", "bg2": "#0A0000", "bg3": "#110000",
        "accent": "#FF1A1A", "accent2": "#CC0000",
        "green": "#FF4400", "red": "#FF0000", "yellow": "#FF6600",
        "purple": "#FF0066", "orange": "#FF3300",
        "text": "#FFCCCC", "text2": "#994444", "muted": "#442222",
        "border": "#FF1A1A",
        "glow": "#FF1A1A",
    },
}

# ══════════════════════════════════════════════════════════════
# PROVEEDORES DE IA
# ══════════════════════════════════════════════════════════════

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
        "needs_openai_lib": False,
    },
    "openai": {
        "name": "OpenAI",
        "cost": "De pago",
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        "default_model": "gpt-4o-mini",
        "get_key_url": "https://platform.openai.com/api-keys",
        "needs_openai_lib": True,
    },
    "openrouter": {
        "name": "OpenRouter (Free Models)",
        "cost": "GRATIS",
        "models": [
            "google/gemini-2.0-flash-exp:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "qwen/qwen-2.5-72b-instruct:free",
            "deepseek/deepseek-chat-v3-0324:free",
            "mistralai/mistral-small-3.1-24b-instruct:free",
        ],
        "default_model": "google/gemini-2.0-flash-exp:free",
        "get_key_url": "https://openrouter.ai/keys",
        "needs_openai_lib": True,
    },
    "cerebras": {
        "name": "Cerebras (Ultra Fast)",
        "cost": "GRATIS",
        "models": ["llama-3.3-70b", "llama3.1-8b"],
        "default_model": "llama-3.3-70b",
        "get_key_url": "https://cloud.cerebras.ai/",
        "needs_openai_lib": True,
    },
}

# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN Y CONSTANTES
# ══════════════════════════════════════════════════════════════

APP_NAME = "J.A.R.V.I.S. GOD MODE"
VERSION = "6.4.0"
START_TIME = time.time()
DATA_DIR = os.path.join(os.path.expanduser("~"), ".jarvis_god")
NOTES_FILE = os.path.join(DATA_DIR, "notas.json")
TODOS_FILE = os.path.join(DATA_DIR, "tareas.json")
REMINDERS_FILE = os.path.join(DATA_DIR, "recordatorios.json")
HISTORY_FILE = os.path.join(DATA_DIR, "historial.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
CONVERSATION_FILE = os.path.join(DATA_DIR, "conversacion.json")
CLIPBOARD_FILE = os.path.join(DATA_DIR, "clipboard_history.json")
SCHEDULER_FILE = os.path.join(DATA_DIR, "scheduler.json")
HABITS_FILE = os.path.join(DATA_DIR, "habits.json")
FLASHCARDS_FILE = os.path.join(DATA_DIR, "flashcards.json")
AUDIO_CACHE_DIR = os.path.join(DATA_DIR, "audio_cache")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

# Limpiar cache de audio viejo (>24h)
try:
    for f in os.listdir(AUDIO_CACHE_DIR):
        fp = os.path.join(AUDIO_CACHE_DIR, f)
        if os.path.isfile(fp) and time.time() - os.path.getmtime(fp) > 86400:
            os.remove(fp)
except Exception:
    pass

# Edge TTS voices (Spanish)
EDGE_VOICES = {
    "dalia": "es-MX-DaliaNeural",       # Mujer mexicana (clara)
    "jorge": "es-MX-JorgeNeural",       # Hombre mexicano
    "elena": "es-ES-ElviraNeural",      # Mujer española
    "alvaro": "es-ES-AlvaroNeural",     # Hombre español
    "irene": "es-AR-ElenaNeural",       # Mujer argentina
    "tomas": "es-AR-TomasNeural",       # Hombre argentino
}
DEFAULT_EDGE_VOICE = "es-MX-JorgeNeural"  # Voz masculina, estilo Jarvis

# System prompt
JARVIS_SYSTEM_PROMPT = """Eres J.A.R.V.I.S. (Just A Rather Very Intelligent System), el asistente personal de IA más avanzado del mundo. Tu creador es tu usuario.

PERSONALIDAD:
- Profesional, conciso y elegante. Respuestas CORTAS (1-3 oraciones máximo) a menos que te pidan detalles.
- Llama al usuario "señor" o "jefe" ocasionalmente.
- Tono calmado, inteligente, ligeramente sarcástico pero siempre respetuoso.
- Si algo sale mal, mantén la calma. Nunca entres en pánico.
- Hablas en español.

CAPACIDADES (tienes acceso a estas herramientas - ÚSALAS cuando sea apropiado):

1. EJECUTAR COMANDOS EN TERMINAL: [TERMINAL]: comando
2. ABRIR PROGRAMAS: [ABRIR]: nombre_programa
   (chrome, firefox, edge, notepad, calc, explorer, cmd, powershell, code, paint, word, excel, teams, discord, spotify, steam, taskmgr, settings, whatsapp, telegram)
3. ABRIR WEB: [WEB]: url_completa
4. BUSCAR EN GOOGLE: [GOOGLE]: búsqueda
5. BUSCAR EN YOUTUBE: [YOUTUBE]: búsqueda
6. GUARDAR NOTA: [NOTA]: texto
7. CREAR TAREA: [TAREA]: texto
8. RECORDATORIO: [RECORDAR]: texto|minutos
9. SISTEMA: [SISTEMA]: info|cpu|disco|red|bateria
10. CONTRASEÑA: [PASSWORD]: longitud
11. CALCULADORA: [CALC]: expresión
12. BLOQUEAR PC: [BLOQUEAR]
13. CAPTURA DE PANTALLA: [SCREENSHOT]
14. COPIAR AL PORTAPAPELES: [COPIAR]: texto
15. ABRIR CARPETA: [CARPETA]: ruta
16. CLIMA: [CLIMA]: ciudad
17. TRADUCIR: [TRADUCIR]: texto|idioma_origen|idioma_destino
18. NOTICIAS: [NOTICIAS]: categoría
19. BUSCAR ARCHIVOS: [BUSCAR_ARCHIVO]: nombre_o_patron|carpeta
20. MATAR PROCESO: [KILL]: nombre_proceso

REGLAS CRITICAS:
- Cuando el usuario pida buscar algo en YouTube, usa SOLO [YOUTUBE]: con las palabras clave.
  Ejemplo: usuario dice "busca un video de felipe abello" → responde: "Buscando en YouTube, señor. [YOUTUBE]: felipe abello videos"
  NUNCA pongas URLs de YouTube en el texto. NUNCA uses [WEB] para YouTube. SOLO usa [YOUTUBE].
- Cuando uses [YOUTUBE], el contenido debe ser SOLO las palabras clave de búsqueda, NO una URL ni una oración.
  Correcto: [YOUTUBE]: felipe abello videos graciosos
  Incorrecto: [YOUTUBE]: https://youtube.com/search?q=felipe+abello
  Incorrecto: [YOUTUBE]: buscar videos de felipe abello en youtube
- Cuando uses [GOOGLE], el contenido debe ser SOLO las palabras de búsqueda.
  Correcto: [GOOGLE]: clima santiago chile
  Incorrecto: [GOOGLE]: https://google.com/search?q=clima
- NUNCA uses [WEB] y [YOUTUBE] para lo mismo. Elige UNO solo.
- NUNCA uses [WEB] y [GOOGLE] para lo mismo. Elige UNO solo.
- Usa SOLO UN comando de búsqueda/web por petición. No dupliques.
- NUNCA incluyas URLs de búsqueda en tu texto de respuesta.
- Nombres de programa SIN puntuación: [ABRIR]: edge (NO: edge.)
- Puedes usar MÚLTIPLES comandos DIFERENTES en una respuesta.
- Si el usuario pide algo peligroso, ADVIERTE antes.
- NUNCA expliques tus comandos internos. Solo actúa.
"""


# ══════════════════════════════════════════════════════════════
# EFECTOS DE SONIDO
# ══════════════════════════════════════════════════════════════

class SoundFX:
    """Efectos de sonido integrados (Windows)."""

    @staticmethod
    def beep_ready():
        if HAS_WINSOUND:
            threading.Thread(target=lambda: winsound.Beep(800, 150), daemon=True).start()

    @staticmethod
    def beep_listen():
        if HAS_WINSOUND:
            def _b():
                winsound.Beep(600, 100)
                time.sleep(0.05)
                winsound.Beep(900, 100)
            threading.Thread(target=_b, daemon=True).start()

    @staticmethod
    def beep_done():
        if HAS_WINSOUND:
            threading.Thread(target=lambda: winsound.Beep(1000, 80), daemon=True).start()

    @staticmethod
    def beep_error():
        if HAS_WINSOUND:
            threading.Thread(target=lambda: winsound.Beep(300, 200), daemon=True).start()

    @staticmethod
    def beep_alert():
        if HAS_WINSOUND:
            def _b():
                for _ in range(3):
                    winsound.Beep(1200, 100)
                    time.sleep(0.1)
            threading.Thread(target=_b, daemon=True).start()

    @staticmethod
    def beep_startup():
        if HAS_WINSOUND:
            def _b():
                for freq in [400, 500, 600, 800, 1000]:
                    winsound.Beep(freq, 80)
                    time.sleep(0.02)
            threading.Thread(target=_b, daemon=True).start()


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
# MOTOR DE VOZ (Edge TTS + pyttsx3 fallback + Wake Word)
# ══════════════════════════════════════════════════════════════

class VoiceEngine:
    """Motor de voz con Edge TTS (voces ultra realistas) + wake word."""

    def __init__(self):
        self.tts_engine = None
        self.recognizer = None
        self.is_speaking = False
        self.is_listening = False
        self.voice_enabled = True
        self.edge_voice = DEFAULT_EDGE_VOICE
        self._tts_lock = threading.Lock()
        self._init_tts_fallback()
        self._init_stt()

    def _init_tts_fallback(self):
        """Inicializar pyttsx3 como fallback."""
        if not HAS_PYTTSX3:
            return
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            for v in voices:
                if 'spanish' in v.name.lower() or 'español' in v.name.lower():
                    self.tts_engine.setProperty('voice', v.id)
                    break
            self.tts_engine.setProperty('rate', 175)
            self.tts_engine.setProperty('volume', 0.9)
        except Exception:
            self.tts_engine = None

    def _init_stt(self):
        """Inicializar reconocimiento de voz."""
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
        """Hablar texto con Edge TTS (o pyttsx3 fallback)."""
        if not self.voice_enabled:
            return
        clean = re.sub(r'[^\w\s.,;:!?¿¡\-\'\"áéíóúñüÁÉÍÓÚÑÜ]', '', text, flags=re.UNICODE)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if not clean:
            return

        if HAS_EDGE_TTS:
            threading.Thread(target=self._speak_edge, args=(clean,), daemon=True).start()
        elif self.tts_engine:
            threading.Thread(target=self._speak_pyttsx3, args=(clean,), daemon=True).start()

    def _speak_edge(self, text):
        """Edge TTS - voces casi humanas de Microsoft."""
        with self._tts_lock:
            try:
                self.is_speaking = True
                # Generar audio
                tmp = os.path.join(AUDIO_CACHE_DIR, f"tts_{hash(text) & 0xFFFFFFFF}.mp3")

                async def _gen():
                    communicate = edge_tts.Communicate(text, self.edge_voice, rate="+5%")
                    await communicate.save(tmp)

                loop = asyncio.new_event_loop()
                loop.run_until_complete(_gen())
                loop.close()

                # Reproducir en Windows
                if os.name == "nt":
                    # Usar Windows Media Player silenciosamente
                    ps_cmd = (
                        f'Add-Type -AssemblyName presentationCore; '
                        f'$p = New-Object System.Windows.Media.MediaPlayer; '
                        f'$p.Open([Uri]"{tmp}"); '
                        f'Start-Sleep -Milliseconds 300; '
                        f'$p.Play(); '
                        f'while($p.NaturalDuration.HasTimeSpan -eq $false){{Start-Sleep -Milliseconds 100}}; '
                        f'Start-Sleep -Milliseconds ($p.NaturalDuration.TimeSpan.TotalMilliseconds); '
                        f'$p.Close()'
                    )
                    subprocess.run(
                        ["powershell", "-NoProfile", "-Command", ps_cmd],
                        capture_output=True, timeout=30, creationflags=0x08000000
                    )
                else:
                    # Linux/Mac fallback
                    subprocess.run(["mpv", "--no-video", tmp], capture_output=True, timeout=30)

            except Exception:
                # Fallback a pyttsx3
                self._speak_pyttsx3(text)
            finally:
                self.is_speaking = False

    def _speak_pyttsx3(self, text):
        """Fallback con pyttsx3."""
        with self._tts_lock:
            try:
                self.is_speaking = True
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception:
                pass
            finally:
                self.is_speaking = False

    def stop_speaking(self):
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
            except Exception:
                pass

    def listen(self, callback, error_callback=None, timeout=5, phrase_limit=15):
        """Escuchar del micrófono."""
        if not self.recognizer or not HAS_SPEECH:
            if error_callback:
                error_callback("Micrófono no disponible. pip install SpeechRecognition pyaudio")
            return

        def _listen():
            self.is_listening = True
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    SoundFX.beep_listen()
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

                text = self.recognizer.recognize_google(audio, language="es-ES")
                callback(text)

            except sr.WaitTimeoutError:
                if error_callback:
                    error_callback("No detecté audio.")
            except sr.UnknownValueError:
                if error_callback:
                    error_callback("No pude entender. ¿Repites?")
            except sr.RequestError as e:
                if error_callback:
                    error_callback(f"Error de red: {e}")
            except Exception as e:
                if error_callback:
                    error_callback(f"Error de micrófono: {e}")
            finally:
                self.is_listening = False

        threading.Thread(target=_listen, daemon=True).start()

    def listen_for_wake_word(self, on_wake, on_error=None):
        """Escuchar pasivamente por la palabra 'Jarvis'."""
        if not self.recognizer or not HAS_SPEECH:
            return

        def _listen():
            self.is_listening = True
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)

                text = self.recognizer.recognize_google(audio, language="es-ES").lower()

                # Detectar wake word
                wake_words = ["jarvis", "hey jarvis", "oye jarvis", "oiga jarvis"]
                for ww in wake_words:
                    if ww in text:
                        # Extraer comando después del wake word
                        remaining = text.split(ww, 1)[1].strip()
                        SoundFX.beep_ready()
                        on_wake(remaining if remaining else None)
                        return

            except (sr.WaitTimeoutError, sr.UnknownValueError):
                pass  # Silencioso - es escucha pasiva
            except Exception:
                pass
            finally:
                self.is_listening = False

        threading.Thread(target=_listen, daemon=True).start()

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        return self.voice_enabled


# ══════════════════════════════════════════════════════════════
# CEREBRO IA (Multi-proveedor)
# ══════════════════════════════════════════════════════════════

class AIBrain:
    """Cerebro de Jarvis - Soporta Gemini, Groq, Ollama y OpenAI."""

    def __init__(self):
        self.client = None
        self.provider = None
        self.api_key = ""
        self.conversation = []
        self.max_history = 20
        self.ready = False
        saved = DataStore.load(CONVERSATION_FILE, [])
        if saved:
            self.conversation = saved[-self.max_history:]

    def init_provider(self, provider, api_key):
        self.provider = provider.lower().strip()
        self.api_key = api_key
        self.client = None
        self.ready = False

        if self.provider == "gemini":
            if api_key:
                self.ready = True
                return True
            return False
        elif self.provider == "groq":
            if not HAS_OPENAI:
                return False
            try:
                self.client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                self.ready = True
                return True
            except Exception:
                return False
        elif self.provider == "openrouter":
            if not HAS_OPENAI:
                return False
            try:
                self.client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
                self.ready = True
                return True
            except Exception:
                return False
        elif self.provider == "cerebras":
            if not HAS_OPENAI:
                return False
            try:
                self.client = OpenAI(api_key=api_key, base_url="https://api.cerebras.ai/v1")
                self.ready = True
                return True
            except Exception:
                return False
        elif self.provider == "ollama":
            if HAS_OPENAI:
                try:
                    self.client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
                except Exception:
                    pass
            self.ready = True
            return True
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

    def _build_system_prompt(self, context=""):
        now = datetime.datetime.now()
        ctx = (
            f"\n\nCONTEXTO ACTUAL:\n"
            f"- Fecha/hora: {now.strftime('%A %d/%m/%Y %H:%M:%S')}\n"
            f"- Sistema: {platform.system()} {platform.release()}\n"
            f"- Usuario: {os.getlogin()}\n"
            f"- Home: {os.path.expanduser('~')}\n"
        )
        if context:
            ctx += f"- Info adicional: {context}\n"
        return JARVIS_SYSTEM_PROMPT + ctx

    def think(self, user_message, system_context="", model=None):
        if not self.ready:
            return (
                "Mi cerebro no está conectado, señor.\n"
                "Opciones GRATUITAS:\n"
                "  config proveedor: gemini    → config api: TU_KEY (gratis: aistudio.google.com/apikey)\n"
                "  config proveedor: groq      → config api: TU_KEY (gratis: console.groq.com/keys)\n"
                "  config proveedor: ollama    → Sin costo (ollama.com)\n"
            )

        full_system = self._build_system_prompt(system_context)

        if self.provider == "gemini":
            return self._think_gemini(user_message, full_system, model)
        else:
            return self._think_openai_compat(user_message, full_system, model)

    def _think_gemini(self, user_message, system_prompt, model=None):
        if not model:
            model = "gemini-2.0-flash"
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model}:generateContent?key={self.api_key}"
        )
        contents = []
        for msg in self.conversation[-self.max_history:]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        contents.append({"role": "user", "parts": [{"text": user_message}]})

        payload = {
            "contents": contents,
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1500},
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data,
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            self._save_turn(user_message, answer)
            return answer
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                msg = json.loads(body).get("error", {}).get("message", body[:200])
            except Exception:
                msg = body[:200]
            if e.code == 429 or "rate" in str(msg).lower():
                return f"[RATE_LIMIT]Error Gemini ({e.code}): {msg}"
            return f"Error Gemini ({e.code}): {msg}"
        except Exception as e:
            return f"Error Gemini: {e}"

    def _think_openai_compat(self, user_message, system_prompt, model=None):
        if self.provider == "ollama" and not self.client:
            return self._think_ollama_rest(user_message, system_prompt, model)
        if not self.client:
            return "Cliente no inicializado."
        if not model:
            model = PROVIDERS.get(self.provider, {}).get("default_model", "gpt-4o-mini")
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation[-self.max_history:])
        messages.append({"role": "user", "content": user_message})
        try:
            response = self.client.chat.completions.create(
                model=model, messages=messages, max_tokens=1500, temperature=0.7)
            answer = response.choices[0].message.content
            self._save_turn(user_message, answer)
            return answer
        except Exception as e:
            error_str = str(e)
            # Detect rate limit errors (429)
            if "429" in error_str or "rate_limit" in error_str or "Rate limit" in error_str:
                return f"[RATE_LIMIT]{error_str}"
            return f"Error {PROVIDERS.get(self.provider, {}).get('name', self.provider)}: {e}"

    def _think_ollama_rest(self, user_message, system_prompt, model=None):
        if not model:
            model = "llama3.2"
        url = "http://localhost:11434/api/chat"
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation[-self.max_history:])
        messages.append({"role": "user", "content": user_message})
        payload = {"model": model, "messages": messages, "stream": False,
                   "options": {"temperature": 0.7}}
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data,
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            answer = result["message"]["content"]
            self._save_turn(user_message, answer)
            return answer
        except urllib.error.URLError:
            return "No se pudo conectar con Ollama. ¿Está corriendo?"
        except Exception as e:
            return f"Error Ollama: {e}"

    def _save_turn(self, user_message, answer):
        self.conversation.append({"role": "user", "content": user_message})
        self.conversation.append({"role": "assistant", "content": answer})
        if len(self.conversation) > self.max_history * 2:
            self.conversation = self.conversation[-self.max_history:]
        DataStore.save(CONVERSATION_FILE, self.conversation)

    def clear_memory(self):
        self.conversation = []
        DataStore.save(CONVERSATION_FILE, [])

    def think_with_image(self, user_message, image_base64, system_context=""):
        """Send text + image to Gemini Vision API for visual analysis."""
        # Only works with Gemini (has free vision) or can fallback
        api_key = self.api_key
        if self.provider != "gemini":
            # Try using gemini key if available
            config = DataStore.load(CONFIG_FILE, {})
            api_key = config.get("api_key_gemini", "") or config.get("api_key", "")
            if not api_key:
                return "Para usar la cámara necesito una API key de Gemini (gratis).\nConfig: config api_gemini: TU_KEY\nURL: https://aistudio.google.com/apikey"

        model = "gemini-2.0-flash"
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model}:generateContent?key={api_key}"
        )
        system_prompt = self._build_system_prompt(system_context)

        payload = {
            "contents": [{
                "parts": [
                    {"text": f"{system_prompt}\n\nEl usuario te muestra una imagen desde su cámara. {user_message}"},
                    {"inlineData": {"mimeType": "image/jpeg", "data": image_base64}}
                ]
            }],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1500},
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data,
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            return answer
        except Exception as e:
            return f"Error de visión: {e}"


# ══════════════════════════════════════════════════════════════
# EJECUTOR DE ACCIONES (EXPANDIDO)
# ══════════════════════════════════════════════════════════════

class ActionExecutor:
    """Ejecuta acciones — ahora con clima, traductor, noticias, procesos, archivos."""

    def __init__(self, app):
        self.app = app

    def execute_all(self, ai_response):
        results = []
        clean_text = ai_response
        self._opened_urls = set()  # Track to prevent duplicate tab opens

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
            r'\[CLIMA\]:\s*(.+)': self._get_weather,
            r'\[TRADUCIR\]:\s*(.+)': self._translate,
            r'\[NOTICIAS\]:\s*(.*)': self._get_news,
            r'\[BUSCAR_ARCHIVO\]:\s*(.+)': self._search_files,
            r'\[KILL\]:\s*(.+)': self._kill_process,
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
                    results.append(f"Error: {e}")
                clean_text = clean_text.replace(match.group(0), "").strip()

        # Clean any leftover URLs from the response text (prevents accidental display)
        clean_text = re.sub(r'https?://(?:www\.)?(?:youtube\.com|youtu\.be|google\.com)\S*', '', clean_text)
        # Clean up extra whitespace and empty lines
        clean_text = re.sub(r'\n{3,}', '\n\n', clean_text).strip()

        return clean_text, results

    # ─── Terminal ────────────────────────────────────

    def _run_terminal(self, cmd):
        try:
            dangerous = ["format c:", "rm -rf /", "del /f /s /q C:", "diskpart",
                         "shutdown /s", "reg delete", ":(){:|:&};:"]
            for d in dangerous:
                if d.lower() in cmd.lower():
                    return f"⚠️ Comando bloqueado: {cmd}"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=30, encoding="utf-8", errors="replace"
            )
            output = result.stdout.strip()
            error = result.stderr.strip()
            if result.returncode == 0:
                return f"💻 Terminal:\n{output[:2000]}" if output else f"💻 ✓ {cmd}"
            return f"💻 Error ({result.returncode}):\n{error or output}"
        except subprocess.TimeoutExpired:
            return f"⏰ Timeout: {cmd}"
        except Exception as e:
            return f"❌ Terminal: {e}"

    # ─── Programas ───────────────────────────────────

    def _open_program(self, name):
        programs = {
            "chrome": "start chrome", "google chrome": "start chrome",
            "firefox": "start firefox", "mozilla": "start firefox",
            "edge": "start msedge", "msedge": "start msedge",
            "microsoft edge": "start msedge", "brave": "start brave",
            "notepad": "start notepad", "bloc": "start notepad",
            "bloc de notas": "start notepad",
            "calc": "start calc", "calculadora": "start calc",
            "explorer": "start explorer", "explorador": "start explorer",
            "archivos": "start explorer",
            "cmd": "start cmd", "terminal": "start wt",
            "powershell": "start powershell", "paint": "start mspaint",
            "word": "start winword", "excel": "start excel",
            "powerpoint": "start powerpnt", "outlook": "start outlook",
            "teams": "start msteams:", "code": "start code",
            "vscode": "start code", "visual studio code": "start code",
            "spotify": "start spotify:", "discord": "start discord:",
            "steam": "start steam:", "whatsapp": "start whatsapp:",
            "telegram": "start telegram:",
            "taskmgr": "start taskmgr", "administrador de tareas": "start taskmgr",
            "settings": "start ms-settings:",
            "configuracion": "start ms-settings:", "ajustes": "start ms-settings:",
            "control": "start control", "panel de control": "start control",
            "snipping": "start snippingtool", "recortes": "start snippingtool",
            "photos": "start ms-photos:", "fotos": "start ms-photos:",
            "maps": "start bingmaps:", "clock": "start ms-clock:",
            "reloj": "start ms-clock:",
            "store": "start ms-windows-store:", "tienda": "start ms-windows-store:",
            "mail": "start outlookmail:", "correo": "start outlookmail:",
        }
        # Clean the name: strip punctuation, extra spaces
        key = re.sub(r'[^\w\s]', '', name.lower()).strip()
        cmd = programs.get(key)
        if cmd:
            subprocess.Popen(cmd, shell=True, creationflags=0x08000000)
            return f"Abriendo {name}."
        # Try partial match
        for prog_key, prog_cmd in programs.items():
            if prog_key in key or key in prog_key:
                subprocess.Popen(prog_cmd, shell=True, creationflags=0x08000000)
                return f"Abriendo {prog_key}."
        subprocess.Popen(f"start {key}", shell=True, creationflags=0x08000000)
        return f"Intentando abrir {name}."

    # ─── Web ─────────────────────────────────────────

    def _open_in_browser(self, url):
        """Open URL in default browser — uses os.startfile on Windows for Edge compatibility."""
        try:
            os.startfile(url)
        except Exception:
            webbrowser.open_new_tab(url)

    def _open_web(self, url):
        # Avoid opening duplicate YouTube/Google search URLs that the AI sometimes generates
        url_lower = url.lower().strip()
        if 'youtube.com/results' in url_lower or 'youtube.com/search' in url_lower:
            return None  # Already handled by _search_youtube
        if 'google.com/search' in url_lower:
            return None  # Already handled by _search_google
        if not url.startswith("http"):
            url = "https://" + url
        self._open_in_browser(url)
        return None

    def _search_google(self, query):
        # Clean the query: remove URLs, extra text, just keep search terms
        query = query.strip()
        query = re.sub(r'https?://\S+', '', query).strip()
        query = re.sub(r'buscar?\s+(en\s+)?google\s*:?\s*', '', query, flags=re.IGNORECASE).strip()
        if not query:
            return None
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        self._open_in_browser(url)
        return None

    def _search_youtube(self, query):
        # Clean the query: remove URLs, just keep search keywords
        query = query.strip()
        query = re.sub(r'https?://\S+', '', query).strip()
        query = re.sub(r'buscar?\s+(en\s+)?youtube\s*:?\s*', '', query, flags=re.IGNORECASE).strip()
        query = re.sub(r'videos?\s+de\s+', '', query, flags=re.IGNORECASE).strip()
        if not query:
            return None
        # Try to get the first video result and open it directly
        try:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            req = urllib.request.Request(search_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "es-CL,es;q=0.9,en;q=0.8"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            # Find video IDs in the page
            video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            if video_ids:
                # Open the first unique video directly
                video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
                self._open_in_browser(video_url)
                return None
        except Exception:
            pass
        # Fallback: open search results page
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        self._open_in_browser(url)
        return None

    # ─── Notas / Tareas ─────────────────────────────

    def _save_note(self, text):
        notes = DataStore.load(NOTES_FILE, [])
        notes.append({"text": text, "date": datetime.datetime.now().isoformat()})
        DataStore.save(NOTES_FILE, notes)
        return None

    def _save_todo(self, text):
        todos = DataStore.load(TODOS_FILE, [])
        todos.append({"text": text, "done": False, "date": datetime.datetime.now().isoformat()})
        DataStore.save(TODOS_FILE, todos)
        return None

    def _set_reminder(self, text):
        parts = text.split("|")
        if len(parts) == 2:
            self.app.reminder_system.add(parts[0].strip(), int(parts[1].strip()))
        return None

    # ─── Sistema ─────────────────────────────────────

    def _system_info(self, what):
        what = what.lower().strip()
        dispatch = {
            "info": self._get_system_info, "cpu": self._get_cpu_info,
            "disco": self._get_disk_info, "red": self._get_network_info,
            "bateria": self._get_battery_info,
        }
        return dispatch.get(what, self._get_system_info)()

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
            lines.append(f"CPU: {psutil.cpu_percent(interval=0.5)}%")
        return "◈ SYSTEM: " + " | ".join(lines)

    def _get_cpu_info(self):
        if not HAS_PSUTIL:
            return f"CPU: {platform.processor()} ({os.cpu_count()} núcleos)"
        cpu_pct = psutil.cpu_percent(interval=1, percpu=True)
        ram = psutil.virtual_memory()
        avg = sum(cpu_pct) / len(cpu_pct)
        return (
            f"◈ CPU: {self._bar(avg)} {avg:.0f}% (cores: {', '.join(f'{p:.0f}%' for p in cpu_pct)})\n"
            f"🗃️ RAM: {self._bar(ram.percent)} {ram.percent}% ({ram.used/1024**3:.1f}/{ram.total/1024**3:.1f} GB)"
        )

    def _get_disk_info(self):
        lines = []
        if os.name == "nt":
            for letter in "CDEFGH":
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    u = shutil.disk_usage(drive)
                    pct = u.used / u.total * 100
                    lines.append(f"💾 {drive} {self._bar(pct)} {pct:.0f}% ({u.free/1024**3:.1f} GB libres)")
        else:
            u = shutil.disk_usage("/")
            pct = u.used / u.total * 100
            lines.append(f"💾 / {self._bar(pct)} {pct:.0f}% ({u.free/1024**3:.1f} GB libres)")
        return "\n".join(lines)

    def _get_network_info(self):
        lines = []
        try:
            lines.append(f"🏠 Local: {socket.gethostbyname(socket.gethostname())}")
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
            return "Sin batería detectada (PC de escritorio)."
        plug = "AC" if bat.power_plugged else "BAT"
        return f"{self._bar(bat.percent)} {bat.percent}% ({plug})"

    # ─── CLIMA (wttr.in - GRATIS) ────────────────────

    def _get_weather(self, city):
        """Obtener clima usando Open-Meteo (gratis, confiable, sin API key)."""
        try:
            city_clean = city.strip()
            # Step 1: Geocode the city name
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city_clean)}&count=1&language=es"
            req = urllib.request.Request(geo_url, headers={"User-Agent": "Jarvis/6.1"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                geo = json.loads(resp.read().decode("utf-8"))

            if "results" not in geo or not geo["results"]:
                return f"◈ No encontré la ciudad '{city_clean}'. Intenta con otro nombre."

            loc = geo["results"][0]
            lat, lon = loc["latitude"], loc["longitude"]
            name = loc.get("name", city_clean)
            country = loc.get("country", "")

            # Step 2: Get current weather
            wx_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
                f"wind_speed_10m,weather_code,precipitation"
                f"&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset"
                f"&timezone=auto&forecast_days=1"
            )
            req2 = urllib.request.Request(wx_url, headers={"User-Agent": "Jarvis/6.1"})
            with urllib.request.urlopen(req2, timeout=10) as resp2:
                wx = json.loads(resp2.read().decode("utf-8"))

            cur = wx["current"]
            daily = wx.get("daily", {})

            # Weather codes to descriptions and icons
            wx_info = {
                0: ("Despejado", "☀️"), 1: ("Mayormente despejado", "🌤️"),
                2: ("Parcialmente nublado", "⛅"), 3: ("Nublado", "☁️"),
                45: ("Neblina", "🌫️"), 48: ("Escarcha", "🌫️"),
                51: ("Llovizna leve", "🌦️"), 53: ("Llovizna", "🌦️"), 55: ("Llovizna fuerte", "🌧️"),
                61: ("Lluvia leve", "🌧️"), 63: ("Lluvia", "🌧️"), 65: ("Lluvia fuerte", "🌧️"),
                71: ("Nieve leve", "🌨️"), 73: ("Nieve", "❄️"), 75: ("Nieve fuerte", "❄️"),
                80: ("Chubascos", "🌦️"), 81: ("Chubascos fuertes", "🌧️"), 82: ("Tormentas", "⛈️"),
                95: ("Tormenta eléctrica", "⛈️"), 96: ("Tormenta con granizo", "⛈️"),
                99: ("Tormenta fuerte", "⛈️"),
            }
            code = cur.get("weather_code", 0)
            desc, icon = wx_info.get(code, (f"Código {code}", "🌡️"))

            temp = cur.get("temperature_2m", "?")
            feels = cur.get("apparent_temperature", "?")
            humidity = cur.get("relative_humidity_2m", "?")
            wind = cur.get("wind_speed_10m", "?")
            precip = cur.get("precipitation", 0)

            t_max = daily.get("temperature_2m_max", ["?"])[0]
            t_min = daily.get("temperature_2m_min", ["?"])[0]
            sunrise = daily.get("sunrise", [""])[0].split("T")[-1] if daily.get("sunrise") else "?"
            sunset = daily.get("sunset", [""])[0].split("T")[-1] if daily.get("sunset") else "?"

            result = (
                f"◈ CLIMA — {name}, {country}\n"
                f"{'═' * 35}\n"
                f"  {icon} {desc}\n"
                f"  🌡️ Temperatura: {temp}°C (Sensación: {feels}°C)\n"
                f"  💧 Humedad: {humidity}%\n"
                f"  💨 Viento: {wind} km/h\n"
                f"  🌧️ Precipitación: {precip} mm\n"
                f"  📊 Máx: {t_max}°C | Mín: {t_min}°C\n"
                f"  🌅 Amanecer: {sunrise} | 🌇 Atardecer: {sunset}"
            )
            return result
        except Exception as e:
            return f"◈ No pude obtener el clima: {e}"

    # ─── TRADUCTOR (MyMemory API - GRATIS) ───────────

    def _translate(self, args):
        """Traducir texto. Formato: texto|idioma_origen|idioma_destino"""
        parts = args.split("|")
        if len(parts) >= 3:
            text, src, tgt = parts[0].strip(), parts[1].strip(), parts[2].strip()
        elif len(parts) == 2:
            text, tgt = parts[0].strip(), parts[1].strip()
            src = "es"
        else:
            text, src, tgt = args.strip(), "es", "en"

        try:
            encoded_text = urllib.parse.quote(text)
            url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair={src}|{tgt}"
            req = urllib.request.urlopen(url, timeout=10)
            data = json.loads(req.read().decode("utf-8"))
            translation = data["responseData"]["translatedText"]
            return f"🌐 {src}→{tgt}: {translation}"
        except Exception as e:
            return f"🌐 Error traduciendo: {e}"

    # ─── NOTICIAS (RSS - GRATIS) ─────────────────────

    def _get_news(self, category=""):
        """Obtener noticias de RSS feeds gratuitos."""
        feeds = {
            "tecnologia": "https://feeds.feedburner.com/Xataka",
            "mundo": "https://feeds.bbci.co.uk/mundo/rss.xml",
            "default": "https://feeds.bbci.co.uk/mundo/rss.xml",
        }
        category = category.lower().strip() if category else "default"
        feed_url = feeds.get(category, feeds["default"])

        try:
            req = urllib.request.Request(feed_url, headers={"User-Agent": "Jarvis/4.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml = resp.read().decode("utf-8")

            # Parsear RSS simple (sin xml.etree para mantenerlo ligero)
            titles = re.findall(r'<item>.*?<title><!\[CDATA\[(.*?)\]\]></title>|<item>.*?<title>(.*?)</title>', xml, re.DOTALL)
            headlines = []
            for match in titles[:7]:
                title = match[0] or match[1]
                if title:
                    headlines.append(title.strip())

            if not headlines:
                # Fallback: regex más simple
                all_titles = re.findall(r'<title>(.*?)</title>', xml)
                headlines = [t.strip() for t in all_titles[1:8] if t.strip()]  # Skip feed title

            if headlines:
                result = "◈ NOTICIAS:\n"
                for i, h in enumerate(headlines, 1):
                    result += f"  {i}. {h}\n"
                return result
            return "◈ No pude obtener noticias."
        except Exception as e:
            return f"◈ Error noticias: {e}"

    # ─── BUSCAR ARCHIVOS ─────────────────────────────

    def _search_files(self, args):
        """Buscar archivos en el PC. Formato: patrón|carpeta"""
        parts = args.split("|")
        pattern = parts[0].strip()
        folder = parts[1].strip() if len(parts) > 1 else os.path.expanduser("~")

        # Resolver carpetas comunes
        folder_map = {
            "descargas": os.path.join(os.path.expanduser("~"), "Downloads"),
            "documentos": os.path.join(os.path.expanduser("~"), "Documents"),
            "escritorio": os.path.join(os.path.expanduser("~"), "Desktop"),
            "home": os.path.expanduser("~"),
        }
        folder = folder_map.get(folder.lower(), folder)

        try:
            found = []
            search_pattern = os.path.join(folder, "**", f"*{pattern}*")
            for f in glob.glob(search_pattern, recursive=True):
                found.append(f)
                if len(found) >= 15:
                    break

            if found:
                result = f"🔍 {len(found)} archivo(s) encontrado(s):\n"
                for f in found:
                    size = os.path.getsize(f) / 1024
                    unit = "KB"
                    if size > 1024:
                        size /= 1024
                        unit = "MB"
                    result += f"  📄 {os.path.basename(f)} ({size:.1f} {unit})\n     {f}\n"
                return result
            return f"🔍 No se encontraron archivos con '{pattern}' en {folder}"
        except Exception as e:
            return f"🔍 Error buscando: {e}"

    # ─── MATAR PROCESO ───────────────────────────────

    def _kill_process(self, name):
        """Terminar un proceso por nombre."""
        if not HAS_PSUTIL:
            try:
                if os.name == "nt":
                    result = subprocess.run(
                        f"taskkill /IM {name} /F",
                        shell=True, capture_output=True, text=True
                    )
                    return f"💀 {result.stdout.strip() or result.stderr.strip()}"
            except Exception:
                pass
            return "Instala psutil para gestión de procesos."

        killed = 0
        for proc in psutil.process_iter(['name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed:
            return f"💀 {killed} proceso(s) '{name}' terminado(s)."
        return f"💀 No se encontró el proceso '{name}'."

    # ─── Utilidades ──────────────────────────────────

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
            return f"◈ KEY: {pwd}\n(Copiada al portapapeles)"
        except Exception:
            return f"◈ KEY: {pwd}"

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
        path = os.path.join(os.path.expanduser("~"), "Desktop", f"jarvis_cap_{ts}.png")
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            img.save(path)
            return f"📸 Captura: {path}"
        except ImportError:
            if os.name == "nt":
                os.system(f'powershell -command "Add-Type -AssemblyName System.Windows.Forms; '
                          f'[System.Windows.Forms.Screen]::PrimaryScreen | ForEach-Object {{ '
                          f'$bmp = New-Object System.Drawing.Bitmap($_.Bounds.Width,$_.Bounds.Height); '
                          f'$g = [System.Drawing.Graphics]::FromImage($bmp); '
                          f'$g.CopyFromScreen($_.Bounds.Location,[System.Drawing.Point]::Empty,$_.Bounds.Size); '
                          f"$bmp.Save('{path}') }}" + '"')
                return f"📸 Captura: {path}"
        return "No pude capturar pantalla."

    def _copy_clipboard(self, text):
        try:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(text)
            # Guardar en historial de clipboard
            clip_history = DataStore.load(CLIPBOARD_FILE, [])
            clip_history.append({"text": text[:500], "date": datetime.datetime.now().isoformat()})
            if len(clip_history) > 50:
                clip_history = clip_history[-50:]
            DataStore.save(CLIPBOARD_FILE, clip_history)
        except Exception:
            pass
        return None

    def _open_folder(self, path_name):
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
        target = folders.get(path_name.lower().strip(), path_name.strip())
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
                        SoundFX.beep_alert()
            time.sleep(3)

    def stop(self):
        self.running = False


# ══════════════════════════════════════════════════════════════
# PROGRAMADOR DE TAREAS (SCHEDULER)
# ══════════════════════════════════════════════════════════════

class Scheduler:
    """Programar acciones recurrentes: 'todos los lunes a las 8', etc."""

    def __init__(self, callback):
        self.tasks = DataStore.load(SCHEDULER_FILE, [])
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def add(self, description, time_str, days=None, command=""):
        """Agregar tarea programada."""
        task = {
            "description": description,
            "time": time_str,  # HH:MM
            "days": days or [0, 1, 2, 3, 4, 5, 6],  # 0=Lun, 6=Dom
            "command": command,
            "enabled": True,
            "last_run": "",
        }
        self.tasks.append(task)
        DataStore.save(SCHEDULER_FILE, self.tasks)
        return task

    def list_tasks(self):
        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        if not self.tasks:
            return "◈ No hay tareas programadas."
        lines = ["◈ SCHEDULED TASKS:", "═" * 35]
        for i, t in enumerate(self.tasks):
            days_str = ", ".join(dias[d] for d in t.get("days", []))
            status = "[ON]" if t.get("enabled") else "[OFF]"
            lines.append(f"  {i+1}. {status} {t['description']}")
            lines.append(f"     ⏰ {t['time']} | {days_str}")
        return "\n".join(lines)

    def remove(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            DataStore.save(SCHEDULER_FILE, self.tasks)
            return f"Tarea eliminada: {removed['description']}"
        return "Índice inválido."

    def _loop(self):
        while self.running:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.weekday()
            today = now.strftime("%Y-%m-%d")

            for task in self.tasks:
                if not task.get("enabled"):
                    continue
                if task["time"] == current_time and current_day in task.get("days", []):
                    if task.get("last_run") != today:
                        task["last_run"] = today
                        DataStore.save(SCHEDULER_FILE, self.tasks)
                        self.callback(task)
            time.sleep(30)

    def stop(self):
        self.running = False


# ══════════════════════════════════════════════════════════════
# POMODORO TIMER
# ══════════════════════════════════════════════════════════════

class PomodoroTimer:
    """Timer Pomodoro: 25 min trabajo, 5 min descanso."""

    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.thread = None
        self.work_minutes = 25
        self.break_minutes = 5
        self.sessions = 0
        self.remaining = 0
        self.phase = "idle"  # idle, work, break

    def start(self, work=25, brk=5):
        self.work_minutes = work
        self.break_minutes = brk
        self.running = True
        self.phase = "work"
        self.remaining = work * 60
        self.sessions += 1
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        return f"◈ Pomodoro #{self.sessions} iniciado: {work} min de trabajo."

    def stop(self):
        self.running = False
        self.phase = "idle"
        return "◈ Pomodoro detenido."

    def status(self):
        if not self.running:
            return f"◈ Pomodoro inactivo. Sesiones hoy: {self.sessions}"
        mins = self.remaining // 60
        secs = self.remaining % 60
        phase_name = "WORK" if self.phase == "work" else "BREAK"
        return f"◈ {phase_name}: {mins:02d}:{secs:02d} restantes (session #{self.sessions})"

    def _loop(self):
        while self.running and self.remaining > 0:
            time.sleep(1)
            self.remaining -= 1

        if not self.running:
            return

        if self.phase == "work":
            self.phase = "break"
            self.remaining = self.break_minutes * 60
            self.callback("pomodoro_break", f"◈ Break time! {self.break_minutes} min.")
            self._loop()  # Continue with break
        elif self.phase == "break":
            self.phase = "idle"
            self.running = False
            self.callback("pomodoro_done", f"◈ Pomodoro #{self.sessions} completado.")


# ══════════════════════════════════════════════════════════════
# MONITOR DE SISTEMA EN TIEMPO REAL
# ══════════════════════════════════════════════════════════════

class SystemMonitor:
    """Monitor que actualiza CPU/RAM en la sidebar."""

    def __init__(self):
        self.cpu = 0
        self.ram = 0
        self.running = True
        if HAS_PSUTIL:
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def _loop(self):
        while self.running:
            try:
                self.cpu = psutil.cpu_percent(interval=2)
                self.ram = psutil.virtual_memory().percent
            except Exception:
                pass

    def stop(self):
        self.running = False


# ══════════════════════════════════════════════════════════════
# APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════

class JarvisGodMode:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1280x800")
        self.root.minsize(1024, 700)

        # Config
        self.config = DataStore.load(CONFIG_FILE, {})
        if isinstance(self.config, list):
            self.config = {}
        self.config.setdefault("provider", "gemini")
        self.config.setdefault("api_key", "")
        self.config.setdefault("model", "")
        self.config.setdefault("voice_enabled", True)
        self.config.setdefault("user_name", "señor")
        self.config.setdefault("theme", "jarvis")
        self.config.setdefault("edge_voice", DEFAULT_EDGE_VOICE)
        self.config.setdefault("typewriter", True)
        self.config.setdefault("sound_fx", True)
        self.config.setdefault("wake_word", False)

        # Theme
        self.theme = THEMES.get(self.config["theme"], THEMES["jarvis"])
        self.root.configure(bg=self.theme["bg"])

        # Historial
        self.command_history = deque(DataStore.load(HISTORY_FILE, []), maxlen=200)
        self.history_index = -1

        # Subsistemas
        self.voice = VoiceEngine()
        self.voice.voice_enabled = self.config.get("voice_enabled", True)
        self.voice.edge_voice = self.config.get("edge_voice", DEFAULT_EDGE_VOICE)
        self.brain = AIBrain()
        provider = self.config.get("provider", "gemini")
        api_key = self.config.get("api_key", "")
        if api_key or provider == "ollama":
            self.brain.init_provider(provider, api_key)
        self.reminder_system = ReminderSystem(self._on_reminder)
        self.scheduler = Scheduler(self._on_scheduled_task)
        self.pomodoro = PomodoroTimer(self._on_pomodoro)
        self.monitor = SystemMonitor()
        self.executor = ActionExecutor(self)

        # Estado
        self.continuous_listen = False
        self.wake_word_mode = self.config.get("wake_word", False)
        self._typewriter_queue = deque()
        self._typewriter_running = False
        self._start_ts = datetime.datetime.now().timestamp()

        # UI
        self._build_ui()

        # Startup
        self.root.after(300, self._animated_startup)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ─── UI ──────────────────────────────────────────

    def _build_ui(self):
        C = self.theme
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=0)
        self.root.grid_rowconfigure(1, weight=1)

        glow = C.get("glow", C["accent"])

        # ═══ TOP HUD BAR ═══
        self.hud_bar = tk.Frame(self.root, bg=C["bg"], height=38)
        self.hud_bar.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.hud_bar.grid_propagate(False)
        self.hud_bar.grid_columnconfigure(1, weight=1)

        # HUD left
        hud_left = tk.Frame(self.hud_bar, bg=C["bg"])
        hud_left.grid(row=0, column=0, sticky="w", padx=10)
        self.hud_clock = tk.Label(hud_left, font=("Consolas", 14, "bold"),
                                   bg=C["bg"], fg=glow)
        self.hud_clock.pack(side="left")
        self.hud_date = tk.Label(hud_left, font=("Consolas", 9),
                                  bg=C["bg"], fg=C["text2"])
        self.hud_date.pack(side="left", padx=(10, 0))

        # HUD center - title
        hud_center = tk.Frame(self.hud_bar, bg=C["bg"])
        hud_center.grid(row=0, column=1, sticky="")
        self._hud_title_label = tk.Label(hud_center, text="◆ J.A.R.V.I.S. ",
                                          font=("Consolas", 11, "bold"),
                                          bg=C["bg"], fg=glow)
        self._hud_title_label.pack(side="left")
        tk.Label(hud_center, text="GOD MODE ", font=("Consolas", 11, "bold"),
                 bg=C["bg"], fg=C["red"]).pack(side="left")
        tk.Label(hud_center, text=f"v{VERSION} ◆", font=("Consolas", 11, "bold"),
                 bg=C["bg"], fg=glow).pack(side="left")

        # HUD right - system stats
        hud_right = tk.Frame(self.hud_bar, bg=C["bg"])
        hud_right.grid(row=0, column=2, sticky="e", padx=10)
        self.hud_cpu = tk.Label(hud_right, font=("Consolas", 9),
                                 bg=C["bg"], fg=C["green"], text="CPU: --")
        self.hud_cpu.pack(side="left", padx=5)
        self.hud_ram = tk.Label(hud_right, font=("Consolas", 9),
                                 bg=C["bg"], fg=C["yellow"], text="RAM: --")
        self.hud_ram.pack(side="left", padx=5)
        self.hud_provider = tk.Label(hud_right, font=("Consolas", 9),
                                      bg=C["bg"], fg=C["accent"])
        self.hud_provider.pack(side="left", padx=5)

        # HUD horizontal glow line
        self.hud_line = tk.Canvas(self.root, height=2, bg=C["bg"], highlightthickness=0)
        self.hud_line.grid(row=0, column=0, columnspan=3, sticky="sew")
        self.hud_line.create_rectangle(0, 0, 2000, 2, fill=glow, outline="")

        # ═══ LEFT PANEL - GAUGES + CONTROLS ═══
        self.sidebar = tk.Frame(self.root, bg=C["bg2"], width=230)
        self.sidebar.grid(row=1, column=0, sticky="nsw", padx=(4, 0), pady=4)
        self.sidebar.grid_propagate(False)

        # Sidebar border glow (left line)
        self._draw_panel_border(self.sidebar, glow)

        # ── Arc Gauge: CPU ──
        tk.Label(self.sidebar, text="◈ CPU", font=("Consolas", 9, "bold"),
                 bg=C["bg2"], fg=glow).pack(pady=(10, 2))
        self.cpu_canvas = tk.Canvas(self.sidebar, width=180, height=100,
                                     bg=C["bg2"], highlightthickness=0)
        self.cpu_canvas.pack()
        self.cpu_val_lbl = tk.Label(self.sidebar, text="0%", font=("Consolas", 11, "bold"),
                                     bg=C["bg2"], fg=glow)
        self.cpu_val_lbl.pack()

        # ── Arc Gauge: RAM ──
        tk.Label(self.sidebar, text="◈ RAM", font=("Consolas", 9, "bold"),
                 bg=C["bg2"], fg=C["yellow"]).pack(pady=(8, 2))
        self.ram_canvas = tk.Canvas(self.sidebar, width=180, height=100,
                                     bg=C["bg2"], highlightthickness=0)
        self.ram_canvas.pack()
        self.ram_val_lbl = tk.Label(self.sidebar, text="0%", font=("Consolas", 11, "bold"),
                                     bg=C["bg2"], fg=C["yellow"])
        self.ram_val_lbl.pack()

        # ── Voice & Pomodoro status ──
        sep = tk.Canvas(self.sidebar, height=1, bg=C["bg2"], highlightthickness=0)
        sep.pack(fill="x", padx=15, pady=8)
        sep.create_rectangle(0, 0, 300, 1, fill=C["muted"], outline="")

        self.voice_status = tk.Label(self.sidebar, text="", font=("Consolas", 8),
                                     bg=C["bg2"], fg=C["accent"])
        self.voice_status.pack()
        self.pomodoro_lbl = tk.Label(self.sidebar, font=("Consolas", 8),
                                     bg=C["bg2"], fg=C["orange"], text="")
        self.pomodoro_lbl.pack()

        # ── Quick buttons ──
        sep2 = tk.Canvas(self.sidebar, height=1, bg=C["bg2"], highlightthickness=0)
        sep2.pack(fill="x", padx=15, pady=4)
        sep2.create_rectangle(0, 0, 300, 1, fill=C["muted"], outline="")

        btns = [
            ("▸ VOZ", self._toggle_continuous_listen),
            ("▸ WAKE", self._toggle_wake_word),
            ("▸ MUTE", self._toggle_voice),
            ("▸ POMODORO", self._pomodoro_toggle),
            ("▸ SCHEDULE", self._show_schedule),
            ("▸ RESET IA", self._reset_ai),
            ("▸ LIMPIAR", self._clear_output),
            ("▸ TEMA", self._cycle_theme),
            ("▸ CONFIG", self._show_config),
        ]

        for text, cmd in btns:
            b = tk.Button(self.sidebar, text=text, font=("Consolas", 8),
                          bg=C["bg2"], fg=C["text2"], bd=0, padx=8, pady=1,
                          anchor="w", cursor="hand2", command=cmd,
                          activebackground=glow, activeforeground="black")
            b.pack(fill="x", padx=10, pady=0)
            b.bind("<Enter>", lambda e, b=b, g=glow: b.config(fg=g))
            b.bind("<Leave>", lambda e, b=b, c=C: b.config(fg=c["text2"]))

        # Footer
        tk.Label(self.sidebar, text=f"v{VERSION}",
                 font=("Consolas", 7), bg=C["bg2"], fg=C["muted"]).pack(side="bottom", pady=(0, 5))
        deps = []
        deps.append("E" if HAS_EDGE_TTS else "·")
        deps.append("V" if HAS_PYTTSX3 else "·")
        deps.append("M" if HAS_SPEECH else "·")
        deps.append("S" if HAS_PSUTIL else "·")
        tk.Label(self.sidebar, text="[" + "|".join(deps) + "]",
                 font=("Consolas", 7), bg=C["bg2"], fg=C["muted"]).pack(side="bottom")

        # ═══ CENTER - MAIN TERMINAL ═══
        center = tk.Frame(self.root, bg=C["bg"])
        center.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)
        center.grid_rowconfigure(0, weight=0)
        center.grid_rowconfigure(1, weight=1)
        center.grid_columnconfigure(0, weight=1)

        # Terminal header
        term_header = tk.Frame(center, bg=C["bg3"], height=24)
        term_header.grid(row=0, column=0, sticky="ew")
        term_header.grid_propagate(False)
        tk.Label(term_header, text="  ◆ TERMINAL", font=("Consolas", 9, "bold"),
                 bg=C["bg3"], fg=glow, anchor="w").pack(side="left", padx=5)
        self.term_status = tk.Label(term_header, text="ONLINE", font=("Consolas", 8),
                                     bg=C["bg3"], fg=C["green"])
        self.term_status.pack(side="right", padx=10)

        # Output area with monospace font
        self.output = scrolledtext.ScrolledText(
            center, font=("Consolas", 11), bg="#000000", fg=C["text"],
            insertbackground=glow, selectbackground=glow,
            selectforeground="black", bd=0, padx=15, pady=12,
            wrap="word", state="disabled", cursor="xterm",
            relief="flat"
        )
        self.output.grid(row=1, column=0, sticky="nsew")

        # Tags
        self.output.tag_configure("jarvis", foreground=glow)
        self.output.tag_configure("user", foreground=C["green"])
        self.output.tag_configure("error", foreground=C["red"])
        self.output.tag_configure("info", foreground=C["yellow"])
        self.output.tag_configure("muted", foreground=C["muted"])
        self.output.tag_configure("system", foreground=C["purple"])
        self.output.tag_configure("action", foreground=C["orange"])
        self.output.tag_configure("hud", foreground=glow, font=("Consolas", 10, "bold"))

        # Input area
        input_frame = tk.Frame(center, bg=C["bg3"])
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        self.mic_btn = tk.Button(
            input_frame, text="◉", font=("Consolas", 14),
            bg=C["bg3"], fg=glow, bd=0, padx=8,
            cursor="hand2", command=self._voice_input,
            activebackground=glow, activeforeground="black"
        )
        self.mic_btn.grid(row=0, column=0, padx=(5, 0), sticky="ns")

        tk.Label(input_frame, text="❯", font=("Consolas", 14, "bold"),
                 bg=C["bg3"], fg=glow).grid(row=0, column=0, padx=(35, 0), sticky="w")

        self.entry = tk.Entry(
            input_frame, font=("Consolas", 12),
            bg=C["bg3"], fg=C["text"], insertbackground=glow,
            selectbackground=glow, bd=0, relief="flat"
        )
        self.entry.grid(row=0, column=1, sticky="ew", ipady=10, padx=(5, 5))
        self.entry.focus_set()

        send_btn = tk.Button(
            input_frame, text="▶", font=("Consolas", 12, "bold"),
            bg=glow, fg="black", bd=0, padx=12,
            cursor="hand2", command=self._send,
            activebackground=C["green"]
        )
        send_btn.grid(row=0, column=2, padx=(0, 5), sticky="ns", pady=3)

        # ═══ RIGHT PANEL - INFO ═══
        self.right_panel = tk.Frame(self.root, bg=C["bg2"], width=220)
        self.right_panel.grid(row=1, column=2, sticky="nse", padx=(0, 4), pady=4)
        self.right_panel.grid_propagate(False)

        self._draw_panel_border(self.right_panel, glow)

        # System info panel
        tk.Label(self.right_panel, text="◈ SYSTEM", font=("Consolas", 9, "bold"),
                 bg=C["bg2"], fg=glow).pack(pady=(10, 5))

        self.sys_info_lbl = tk.Label(self.right_panel, font=("Consolas", 7),
                                      bg=C["bg2"], fg=C["text2"], justify="left", anchor="w")
        self.sys_info_lbl.pack(padx=10, fill="x")

        sep3 = tk.Canvas(self.right_panel, height=1, bg=C["bg2"], highlightthickness=0)
        sep3.pack(fill="x", padx=15, pady=8)
        sep3.create_rectangle(0, 0, 300, 1, fill=C["muted"], outline="")

        # Network info
        tk.Label(self.right_panel, text="◈ NETWORK", font=("Consolas", 9, "bold"),
                 bg=C["bg2"], fg=C["green"]).pack(pady=(0, 5))
        self.net_info_lbl = tk.Label(self.right_panel, font=("Consolas", 7),
                                      bg=C["bg2"], fg=C["text2"], justify="left", anchor="w")
        self.net_info_lbl.pack(padx=10, fill="x")

        sep4 = tk.Canvas(self.right_panel, height=1, bg=C["bg2"], highlightthickness=0)
        sep4.pack(fill="x", padx=15, pady=8)
        sep4.create_rectangle(0, 0, 300, 1, fill=C["muted"], outline="")

        # Disk info
        tk.Label(self.right_panel, text="◈ STORAGE", font=("Consolas", 9, "bold"),
                 bg=C["bg2"], fg=C["orange"]).pack(pady=(0, 5))
        self.disk_info_lbl = tk.Label(self.right_panel, font=("Consolas", 7),
                                       bg=C["bg2"], fg=C["text2"], justify="left", anchor="w")
        self.disk_info_lbl.pack(padx=10, fill="x")

        sep5 = tk.Canvas(self.right_panel, height=1, bg=C["bg2"], highlightthickness=0)
        sep5.pack(fill="x", padx=15, pady=8)
        sep5.create_rectangle(0, 0, 300, 1, fill=C["muted"], outline="")

        # Quick action buttons (right panel)
        r_btns = [
            ("▸ BRIEFING", lambda: self._quick_cmd("briefing")),
            ("▸ SISTEMA", lambda: self._quick_cmd("info del sistema")),
            ("▸ CLIMA", lambda: self._quick_cmd("clima Santiago Chile")),
            ("▸ NOTICIAS", lambda: self._quick_cmd("noticias de hoy")),
            ("▸ YOUTUBE", lambda: self._quick_cmd("yt musica lofi")),
            ("▸ PROCESOS", lambda: self._quick_cmd("procesos")),
            ("▸ WIKI", lambda: self._quick_cmd("wiki Python")),
            ("▸ DRIVE", lambda: self._quick_cmd("drive")),
            ("▸ GMAIL", lambda: self._quick_cmd("gmail")),
            ("▸ GITHUB", lambda: self._quick_cmd("github")),
            ("▸ TYPING", lambda: self._quick_cmd("typing")),
            ("▸ CALC", lambda: self._quick_cmd("calc 2+2")),
            ("▸ TAREAS", lambda: self._quick_cmd("mis tareas")),
            ("▸ PASSWORD", lambda: self._quick_cmd("contraseña de 20")),
            ("▸ HELP", lambda: self._quick_cmd("help")),
        ]

        for text, cmd in r_btns:
            b = tk.Button(self.right_panel, text=text, font=("Consolas", 8),
                          bg=C["bg2"], fg=C["text2"], bd=0, padx=8, pady=1,
                          anchor="w", cursor="hand2", command=cmd,
                          activebackground=glow, activeforeground="black")
            b.pack(fill="x", padx=10, pady=0)
            b.bind("<Enter>", lambda e, b=b, g=glow: b.config(fg=g))
            b.bind("<Leave>", lambda e, b=b, c=C: b.config(fg=c["text2"]))

        # ═══ BOTTOM STATUS BAR ═══
        self.bottom_bar = tk.Frame(self.root, bg=C["bg3"], height=22)
        self.bottom_bar.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.bottom_bar.grid_propagate(False)

        self.status_lbl = tk.Label(
            self.bottom_bar, text="  ◆ READY", font=("Consolas", 8),
            bg=C["bg3"], fg=glow, anchor="w"
        )
        self.status_lbl.pack(side="left", padx=5)

        self.uptime_lbl = tk.Label(
            self.bottom_bar, text="", font=("Consolas", 8),
            bg=C["bg3"], fg=C["text2"]
        )
        self.uptime_lbl.pack(side="right", padx=10)

        # Bindings
        self.entry.bind("<Return>", lambda e: self._send())
        self.entry.bind("<Up>", lambda e: self._hist(-1))
        self.entry.bind("<Down>", lambda e: self._hist(1))
        self.root.bind("<Escape>", lambda e: self.entry.focus_set())
        self.root.bind("<Control-l>", lambda e: self._clear_output())
        self.root.bind("<Control-e>", lambda e: self._export_conversation())

        # Populate right panel info
        self._update_right_panel()

        # Start visual effects
        self.root.after(1000, self._start_matrix_rain)
        self.root.after(1500, self._start_network_pulse)
        self.root.after(3000, self._start_glitch_effect)

        # Clock & Monitor loop
        self._tick()

    def _draw_panel_border(self, frame, color):
        """Dibujar borde glow en un panel."""
        top = tk.Canvas(frame, height=2, bg=frame["bg"], highlightthickness=0)
        top.pack(fill="x", side="top")
        top.create_rectangle(0, 0, 2000, 2, fill=color, outline="")

    def _draw_arc_gauge(self, canvas, pct, color, bg_color="#1A1A1A"):
        """Dibujar arco circular estilo EDEX-UI."""
        canvas.delete("all")
        w = canvas.winfo_width() or 180
        h = canvas.winfo_height() or 100
        cx, cy = w // 2, h - 5
        r = min(w // 2 - 10, h - 15)

        # Background arc
        canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                          start=0, extent=180, style="arc",
                          outline=bg_color, width=8)

        # Filled arc
        extent = int(180 * pct / 100)
        if extent > 0:
            canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                              start=180, extent=-extent, style="arc",
                              outline=color, width=8)

        # Tick marks
        import math as _m
        for i in range(0, 181, 18):
            angle = _m.radians(i)
            x1 = cx + (r + 5) * _m.cos(angle)
            y1 = cy - (r + 5) * _m.sin(angle)
            x2 = cx + (r + 10) * _m.cos(angle)
            y2 = cy - (r + 10) * _m.sin(angle)
            canvas.create_line(x1, y1, x2, y2, fill=bg_color, width=1)

    def _update_right_panel(self):
        """Populate system info on right panel."""
        try:
            sys_lines = []
            sys_lines.append(f"OS: {platform.system()} {platform.release()}")
            sys_lines.append(f"PC: {platform.node()}")
            sys_lines.append(f"Py: {platform.python_version()}")
            sys_lines.append(f"CPU: {os.cpu_count()} cores")
            if HAS_PSUTIL:
                ram = psutil.virtual_memory()
                sys_lines.append(f"RAM: {ram.total / 1024**3:.1f} GB")
                bat = psutil.sensors_battery()
                if bat:
                    plug = "AC" if bat.power_plugged else "BAT"
                    sys_lines.append(f"BAT: {bat.percent}% [{plug}]")
            self.sys_info_lbl.config(text="\n".join(sys_lines))
        except Exception:
            self.sys_info_lbl.config(text="N/A")

        # Network
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            self.net_info_lbl.config(text=f"Host: {hostname}\nIP: {local_ip}")
        except Exception:
            self.net_info_lbl.config(text="N/A")

        # Disk
        try:
            disk_lines = []
            if os.name == "nt":
                for letter in "CDE":
                    drive = f"{letter}:\\"
                    if os.path.exists(drive):
                        u = shutil.disk_usage(drive)
                        pct = u.used / u.total * 100
                        free_gb = u.free / 1024**3
                        disk_lines.append(f"{drive} {pct:.0f}% ({free_gb:.0f}GB free)")
            else:
                u = shutil.disk_usage("/")
                pct = u.used / u.total * 100
                disk_lines.append(f"/ {pct:.0f}% ({u.free/1024**3:.0f}GB free)")
            self.disk_info_lbl.config(text="\n".join(disk_lines))
        except Exception:
            self.disk_info_lbl.config(text="N/A")

    # ─── MATRIX RAIN EFFECT ─────────────────────────

    def _start_matrix_rain(self):
        """Initialize matrix rain on the sidebar background."""
        self._matrix_drops = []
        self._matrix_canvas = tk.Canvas(self.sidebar, bg=self.theme["bg2"],
                                         highlightthickness=0, width=230, height=60)
        self._matrix_canvas.pack(side="bottom", fill="x")
        import random as _rnd
        for i in range(12):
            x = _rnd.randint(5, 220)
            speed = _rnd.uniform(0.5, 2.0)
            self._matrix_drops.append({"x": x, "y": _rnd.randint(-60, 0),
                                        "speed": speed, "char": ""})
        self._animate_matrix()

    def _animate_matrix(self):
        """Animate matrix rain drops."""
        import random as _rnd
        if not hasattr(self, '_matrix_canvas'):
            return
        try:
            self._matrix_canvas.delete("all")
            glow = self.theme.get("glow", self.theme["accent"])
            chars = "01アイウエオカキクケコサシスセソ"

            for drop in self._matrix_drops:
                drop["y"] += drop["speed"] * 3
                drop["char"] = _rnd.choice(chars)
                if drop["y"] > 60:
                    drop["y"] = _rnd.randint(-20, -5)
                    drop["x"] = _rnd.randint(5, 220)

                # Trail effect (fading)
                for j in range(4):
                    ty = drop["y"] - j * 8
                    if 0 <= ty <= 60:
                        alpha_hex = max(20, 255 - j * 60)
                        # Use progressively darker color for trail
                        c = glow if j == 0 else self.theme.get("muted", "#333333")
                        self._matrix_canvas.create_text(
                            drop["x"], ty, text=drop["char"],
                            fill=c, font=("Consolas", 6))

            self.root.after(80, self._animate_matrix)
        except Exception:
            pass

    # ─── SCANLINE SWEEP EFFECT ──────────────────────

    def _start_scanline(self):
        """Add a horizontal scanline sweep over the terminal output."""
        self._scan_y = 0
        self._scanline_canvas = tk.Canvas(self.output_frame, width=3, height=600,
                                           bg=self.theme["bg"], highlightthickness=0)
        self._scanline_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._scanline_canvas.configure(bg="")
        self._scanline_canvas.lower()  # Behind text
        # Use an overlay approach — transparent-like scanline
        self._scan_overlay = tk.Canvas(self.output_frame, highlightthickness=0)
        self._scan_overlay.place(relx=0, y=0, relwidth=1, height=2)
        self._scan_overlay.configure(bg=self.theme.get("glow", self.theme["accent"]))
        self._scan_overlay.attributes = {}
        self._animate_scanline()

    def _animate_scanline(self):
        """Move scanline down the terminal."""
        try:
            h = self.output_frame.winfo_height()
            if h < 10:
                h = 600
            self._scan_y += 2
            if self._scan_y > h:
                self._scan_y = 0
            self._scan_overlay.place(relx=0, y=self._scan_y, relwidth=1, height=2)
            # Fade effect — change opacity via color
            progress = self._scan_y / h
            alpha = int(40 + 20 * math.sin(progress * math.pi))
            glow = self.theme.get("glow", self.theme["accent"])
            # Dim the scanline color
            r = int(glow[1:3], 16) if len(glow) >= 7 else 0
            g = int(glow[3:5], 16) if len(glow) >= 7 else 255
            b = int(glow[5:7], 16) if len(glow) >= 7 else 0
            dim_r = max(0, min(255, int(r * alpha / 80)))
            dim_g = max(0, min(255, int(g * alpha / 80)))
            dim_b = max(0, min(255, int(b * alpha / 80)))
            dim_color = f"#{dim_r:02x}{dim_g:02x}{dim_b:02x}"
            self._scan_overlay.configure(bg=dim_color)
            self.root.after(50, self._animate_scanline)
        except Exception:
            pass

    # ─── GLITCH EFFECT ON TITLE ──────────────────────

    def _start_glitch_effect(self):
        """Periodically glitch the title text."""
        self._glitch_cycle()

    def _glitch_cycle(self):
        """Randomly glitch the HUD title."""
        try:
            if not hasattr(self, '_hud_title_label'):
                # Find the title labels in hud_center (set during _build_ui)
                self.root.after(random.randint(8000, 20000), self._glitch_cycle)
                return
            original = "◆ J.A.R.V.I.S. "
            glitch_chars = "░▒▓█▀▄▐▌╬╠╣╚╗┤├"
            glitched = ""
            for ch in original:
                if random.random() < 0.3:
                    glitched += random.choice(glitch_chars)
                else:
                    glitched += ch
            self._hud_title_label.config(text=glitched)
            # Restore after brief moment
            self.root.after(120, lambda: self._hud_title_label.config(text=original))
            # Second micro-glitch
            self.root.after(200, lambda: self._hud_title_label.config(
                text="".join(random.choice(glitch_chars) if random.random() < 0.2 else c for c in original)))
            self.root.after(320, lambda: self._hud_title_label.config(text=original))
            # Next glitch in 8-20 seconds
            self.root.after(random.randint(8000, 20000), self._glitch_cycle)
        except Exception:
            pass

    # ─── HEX GRID PATTERN ────────────────────────────

    def _draw_hex_grid(self, canvas, width, height, color):
        """Draw a subtle hexagonal grid pattern (EDEX-UI inspired)."""
        try:
            size = 20
            for row in range(0, height + size, int(size * 1.5)):
                offset = size if (row // int(size * 1.5)) % 2 else 0
                for col in range(-size, width + size, int(size * 1.73)):
                    cx = col + offset
                    cy = row
                    points = []
                    for i in range(6):
                        angle = math.radians(60 * i + 30)
                        px = cx + size * 0.4 * math.cos(angle)
                        py = cy + size * 0.4 * math.sin(angle)
                        points.extend([px, py])
                    if len(points) >= 6:
                        canvas.create_polygon(points, outline=color, fill="", width=1)
        except Exception:
            pass

    # ─── NETWORK ACTIVITY PULSE ──────────────────────

    def _start_network_pulse(self):
        """Show a network activity pulse animation on right panel."""
        self._net_canvas = tk.Canvas(self.right_panel, width=200, height=35,
                                      bg=self.theme["bg2"], highlightthickness=0)
        self._net_canvas.pack(padx=10, fill="x")
        self._net_points = [0.0] * 40
        self._pulse_net()

    def _pulse_net(self):
        """Animate network pulse line."""
        import random as _rnd
        try:
            self._net_canvas.delete("all")
            glow = self.theme.get("glow", self.theme["accent"])

            # Shift left and add new point
            self._net_points.pop(0)
            if HAS_PSUTIL:
                try:
                    net = psutil.net_io_counters()
                    val = (net.bytes_sent + net.bytes_recv) % 100
                    self._net_points.append(val / 100.0 * 25 + _rnd.uniform(-2, 2))
                except Exception:
                    self._net_points.append(_rnd.uniform(5, 20))
            else:
                self._net_points.append(_rnd.uniform(5, 20))

            # Draw the line
            w = 200
            step = w / len(self._net_points)
            coords = []
            for i, val in enumerate(self._net_points):
                x = int(i * step)
                y = 30 - max(2, min(28, val))
                coords.extend([x, y])
            if len(coords) >= 4:
                self._net_canvas.create_line(coords, fill=self.theme["green"],
                                              width=1, smooth=True)
                # Glow line (thicker, slightly transparent)
                self._net_canvas.create_line(coords, fill=self.theme.get("muted", "#333"),
                                              width=2, smooth=True)

            self.root.after(200, self._pulse_net)
        except Exception:
            pass

    # ─── RELOJ + MONITOR ─────────────────────────────

    def _tick(self):
        C = self.theme
        glow = C.get("glow", C["accent"])
        now = datetime.datetime.now()

        # HUD clock
        self.hud_clock.config(text=now.strftime("%H:%M:%S"))
        dias = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
        self.hud_date.config(text=f"{dias[now.weekday()]} {now.day:02d}/{now.month:02d}/{now.year}")

        # HUD provider
        p = self.config.get("provider", "groq").upper()
        m = self.config.get("model", "")
        self.hud_provider.config(text=f"[{p}:{m[:20]}]")

        # Monitor CPU/RAM + gauges
        if HAS_PSUTIL:
            cpu = self.monitor.cpu
            ram = self.monitor.ram
            self.hud_cpu.config(text=f"CPU:{cpu:.0f}%")
            self.hud_ram.config(text=f"RAM:{ram:.0f}%")

            # Update arc gauges
            self._draw_arc_gauge(self.cpu_canvas, cpu, glow)
            self.cpu_val_lbl.config(text=f"{cpu:.0f}%")
            self._draw_arc_gauge(self.ram_canvas, ram, C["yellow"])
            self.ram_val_lbl.config(text=f"{ram:.0f}%")

        # Uptime
        elapsed = int((now - datetime.datetime.fromtimestamp(
            getattr(self, '_start_ts', now.timestamp()))).total_seconds())
        h, m_s = divmod(elapsed, 3600)
        m_v, s_v = divmod(m_s, 60)
        self.uptime_lbl.config(text=f"UPTIME {h:02d}:{m_v:02d}:{s_v:02d}")

        # Pomodoro
        if self.pomodoro.running:
            mins = self.pomodoro.remaining // 60
            secs = self.pomodoro.remaining % 60
            phase = "▶ WORK" if self.pomodoro.phase == "work" else "▷ BREAK"
            self.pomodoro_lbl.config(text=f"◈ {phase} {mins:02d}:{secs:02d}")
        else:
            self.pomodoro_lbl.config(text="")

        # Voice status
        if self.voice.is_listening:
            self.voice_status.config(text="◉ LISTENING", fg=C["red"])
            self.mic_btn.config(bg=C["red"], fg="white")
        elif self.voice.is_speaking:
            self.voice_status.config(text="◉ SPEAKING", fg=C["green"])
            self.mic_btn.config(bg=C["bg3"], fg=glow)
        elif self.wake_word_mode:
            self.voice_status.config(text="◉ WAKE WORD", fg=C["purple"])
            self.mic_btn.config(bg=C["bg3"], fg=C["purple"])
        elif self.continuous_listen:
            self.voice_status.config(text="◉ VOICE MODE", fg=glow)
            self.mic_btn.config(bg=C["bg3"], fg=glow)
        else:
            self.voice_status.config(text="")
            self.mic_btn.config(bg=C["bg3"], fg=glow)

        # Update right panel info every 10 seconds
        if int(now.timestamp()) % 10 == 0:
            self._update_right_panel()

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
        name = self.config.get("user_name", "User").upper()
        self.output.insert("end", f"{name} ❯ {text}\n", "user")
        self.output.config(state="disabled")

    def _print_jarvis(self, text):
        """Imprimir como Jarvis — con efecto typewriter si está activado."""
        ts = datetime.datetime.now().strftime("%H:%M")
        if self.config.get("typewriter", True) and len(text) < 500:
            self._typewriter_print(ts, text)
        else:
            self.output.config(state="normal")
            self.output.insert("end", f"[{ts}] ", "muted")
            self.output.insert("end", f"Jarvis: {text}\n\n", "jarvis")
            self.output.see("end")
            self.output.config(state="disabled")

    def _typewriter_print(self, ts, text):
        """Efecto máquina de escribir — texto aparece caracter por caracter."""
        self.output.config(state="normal")
        self.output.insert("end", f"[{ts}] ", "muted")
        self.output.insert("end", "Jarvis: ", "jarvis")
        self.output.config(state="disabled")

        self._typewriter_queue.append(text)
        if not self._typewriter_running:
            self._typewriter_process()

    def _typewriter_process(self):
        """Procesar cola de typewriter."""
        if not self._typewriter_queue:
            self._typewriter_running = False
            self.output.config(state="normal")
            self.output.insert("end", "\n\n", "jarvis")
            self.output.see("end")
            self.output.config(state="disabled")
            return

        self._typewriter_running = True
        text = self._typewriter_queue[0]

        if not text:
            self._typewriter_queue.popleft()
            self._typewriter_process()
            return

        char = text[0]
        self._typewriter_queue[0] = text[1:]

        self.output.config(state="normal")
        self.output.insert("end", char, "jarvis")
        self.output.see("end")
        self.output.config(state="disabled")

        # Velocidad: más rápido en medio de palabra, pausa en puntuación
        delay = 8
        if char in ".!?":
            delay = 80
        elif char in ",;:":
            delay = 40
        elif char == "\n":
            delay = 30

        if text[1:]:
            self.root.after(delay, self._typewriter_process)
        else:
            self._typewriter_queue.popleft()
            self.root.after(delay, self._typewriter_process)

    def _print_action(self, text):
        self.output.config(state="normal")
        self.output.insert("end", f"  ▸ {text}\n", "action")
        self.output.see("end")
        self.output.config(state="disabled")

    def _animate_thinking(self, step=0):
        """Animate a thinking indicator in the status bar."""
        if not getattr(self, '_thinking', False):
            return
        frames = ["◆ ◇ ◇ ◇", "◇ ◆ ◇ ◇", "◇ ◇ ◆ ◇", "◇ ◇ ◇ ◆",
                   "◇ ◇ ◆ ◇", "◇ ◆ ◇ ◇"]
        glow = self.theme.get("glow", self.theme["accent"])
        frame = frames[step % len(frames)]
        self.status_lbl.config(text=f"  {frame} NEURAL PROCESSING...", fg=glow)
        self.root.after(150, lambda: self._animate_thinking(step + 1))

    def _clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    # ─── UTILIDADES NUEVAS v6.0 ──────────────────────

    def _stopwatch_status(self):
        if getattr(self, '_sw_running', False):
            elapsed = time.time() - self._sw_start
        else:
            elapsed = getattr(self, '_sw_elapsed', 0)
        return f"◈ Cronómetro: {self._format_elapsed(elapsed)}"

    def _format_elapsed(self, seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 100)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}.{ms:02d}"
        return f"{m:02d}:{s:02d}.{ms:02d}"

    def _check_timer(self):
        """Check if timer has expired."""
        if not getattr(self, '_timer_running', False):
            return
        remaining = self._timer_end - time.time()
        if remaining <= 0:
            self._timer_running = False
            self._print("\n◈ TIMER COMPLETADO!", "info")
            self.voice.speak("Señor, el temporizador ha terminado.")
            SoundFX.beep_alert()
            return
        self.root.after(1000, self._check_timer)

    def _safe_calc(self, expression):
        """Safe math calculator."""
        try:
            expr = expression.strip().replace("^", "**").replace(",", ".")
            expr = expr.replace("×", "*").replace("÷", "/")
            safe = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan,
                "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
                "log2": math.log2, "exp": math.exp, "pow": pow,
                "pi": math.pi, "e": math.e, "tau": math.tau,
                "factorial": math.factorial, "ceil": math.ceil,
                "floor": math.floor, "gcd": math.gcd,
                "radians": math.radians, "degrees": math.degrees,
            }
            forbidden = ["import", "exec", "eval", "open", "os.", "sys.", "__", "lambda"]
            for w in forbidden:
                if w in expr.lower():
                    return "◈ Expresión no permitida."
            result = eval(expr, {"__builtins__": {}}, safe)
            if isinstance(result, float):
                if result == int(result) and not math.isinf(result):
                    result = int(result)
                else:
                    result = round(result, 10)
            return f"◈ {expression} = {result}"
        except ZeroDivisionError:
            return "◈ Error: División por cero."
        except Exception as e:
            return f"◈ Error: {e}"

    def _convert_units(self, text):
        """Unit converter."""
        text_lower = text.lower().strip()
        conversions = [
            (r"([\d.]+)\s*(?:km|kilómetros?|kilometros?)\s+(?:a|en|to)\s+(?:mi|millas?)",
             lambda v: (v * 0.621371, "millas")),
            (r"([\d.]+)\s*(?:mi|millas?)\s+(?:a|en|to)\s+(?:km|kilómetros?|kilometros?)",
             lambda v: (v * 1.60934, "km")),
            (r"([\d.]+)\s*(?:kg|kilos?|kilogramos?)\s+(?:a|en|to)\s+(?:lb|libras?)",
             lambda v: (v * 2.20462, "libras")),
            (r"([\d.]+)\s*(?:lb|libras?)\s+(?:a|en|to)\s+(?:kg|kilos?|kilogramos?)",
             lambda v: (v * 0.453592, "kg")),
            (r"([\d.]+)\s*(?:m|metros?)\s+(?:a|en|to)\s+(?:ft|pies?|feet)",
             lambda v: (v * 3.28084, "pies")),
            (r"([\d.]+)\s*(?:ft|pies?|feet)\s+(?:a|en|to)\s+(?:m|metros?)",
             lambda v: (v * 0.3048, "metros")),
            (r"([\d.]+)\s*(?:l|litros?)\s+(?:a|en|to)\s+(?:gal|galones?)",
             lambda v: (v * 0.264172, "galones")),
            (r"([\d.]+)\s*(?:gal|galones?)\s+(?:a|en|to)\s+(?:l|litros?)",
             lambda v: (v * 3.78541, "litros")),
            (r"([\d.]+)\s*(?:cm|centímetros?|centimetros?)\s+(?:a|en|to)\s+(?:in|pulgadas?)",
             lambda v: (v * 0.393701, "pulgadas")),
            (r"([\d.]+)\s*(?:in|pulgadas?)\s+(?:a|en|to)\s+(?:cm|centímetros?|centimetros?)",
             lambda v: (v * 2.54, "cm")),
            (r"([\d.]+)\s*°?(?:c|celsius|centígrados?|centigrados?)\s+(?:a|en|to)\s+°?(?:f|fahrenheit)",
             lambda v: (v * 9/5 + 32, "°F")),
            (r"([\d.]+)\s*°?(?:f|fahrenheit)\s+(?:a|en|to)\s+°?(?:c|celsius|centígrados?|centigrados?)",
             lambda v: ((v - 32) * 5/9, "°C")),
        ]
        for pattern, converter in conversions:
            match = re.search(pattern, text_lower)
            if match:
                value = float(match.group(1))
                result, unit = converter(value)
                return f"◈ {value} → {result:.4f} {unit}"
        return (
            "◈ Formato: '[valor] [unidad] a [unidad]'\n"
            "  Ejemplos: 10 km a millas | 75 kg a libras | 100 celsius a fahrenheit"
        )

    def _date_calc(self, text):
        """Date calculator."""
        text_lower = text.lower().strip()
        today = datetime.date.today()
        match = re.search(r"(?:dias|días)\s+(?:para|hasta)\s+(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?", text_lower)
        if match:
            day, month = int(match.group(1)), int(match.group(2))
            year = int(match.group(3)) if match.group(3) else today.year
            if year < 100:
                year += 2000
            try:
                target = datetime.date(year, month, day)
                diff = (target - today).days
                if diff > 0:
                    return f"◈ Faltan {diff} días para el {target.strftime('%d/%m/%Y')}"
                elif diff < 0:
                    return f"◈ Han pasado {abs(diff)} días desde el {target.strftime('%d/%m/%Y')}"
                else:
                    return "◈ Esa fecha es hoy!"
            except ValueError:
                return "◈ Fecha inválida."
        match = re.search(r"(?:hoy|fecha)\s*([\+\-])\s*(\d+)\s*(?:dias|días)?", text_lower)
        if match:
            op, days = match.group(1), int(match.group(2))
            if op == "+":
                result = today + datetime.timedelta(days=days)
            else:
                result = today - datetime.timedelta(days=days)
            return f"◈ Resultado: {result.strftime('%d/%m/%Y')}"
        return "◈ Uso: 'dias para 25/12' o 'hoy +30 dias'"

    def _show_briefing(self):
        """Daily briefing like jarvis_pro_ultra."""
        now = datetime.datetime.now()
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        dia_nombre = dias[now.weekday()]
        mes_nombre = meses[now.month - 1]
        day_of_year = now.timetuple().tm_yday
        is_leap = (now.year % 4 == 0 and (now.year % 100 != 0 or now.year % 400 == 0))
        total_days = 366 if is_leap else 365
        days_left = total_days - day_of_year
        progress = day_of_year / total_days * 100
        filled = int(20 * progress / 100)
        year_bar = "█" * filled + "░" * (20 - filled)

        todos = DataStore.load(TODOS_FILE, [])
        pending = [t for t in todos if not t.get("done")]

        frases = [
            "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
            "La disciplina es el puente entre las metas y los logros.",
            "Todo parece imposible hasta que se hace. — Nelson Mandela",
            "La creatividad es la inteligencia divirtiéndose. — Einstein",
            "El único modo de hacer un gran trabajo es amar lo que haces.",
        ]

        lines = [
            " ╔══════════════════════════════════════════╗",
            f" ║  ◆ BRIEFING DIARIO — {dia_nombre:<20}║",
            " ╠══════════════════════════════════════════╣",
            f" ║  {dia_nombre}, {now.day} de {mes_nombre} de {now.year}",
            f" ║  {now.strftime('%H:%M:%S')}",
            f" ║  Día {day_of_year} del año | Quedan {days_left} días",
            f" ║  [{year_bar}] {progress:.1f}%",
            " ║",
        ]
        if pending:
            lines.append(f" ║  Tareas pendientes: {len(pending)}")
            for i, t in enumerate(pending[:5], 1):
                lines.append(f" ║    {i}. {t['text']}")
        else:
            lines.append(" ║  Sin tareas pendientes. ¡Buen trabajo!")

        if HAS_PSUTIL:
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory()
            lines.append(" ║")
            lines.append(f" ║  CPU: {cpu:.0f}% | RAM: {ram.percent:.0f}%")

        lines.extend([
            " ║",
            f" ║  \"{random.choice(frases)}\"",
            " ╚══════════════════════════════════════════╝",
        ])
        self._print("\n".join(lines), "system")

    def _show_processes(self):
        """Show top system processes."""
        if not HAS_PSUTIL:
            self._print_jarvis("Instala psutil para ver procesos: pip install psutil")
            return
        try:
            procs = []
            for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                try:
                    info = p.info
                    if info['cpu_percent'] is not None and info['memory_percent'] is not None:
                        procs.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            # Sort by CPU then RAM
            procs.sort(key=lambda x: (x.get('cpu_percent', 0) or 0), reverse=True)
            lines = [" ╔══════════════════════════════════════════╗",
                     " ║  ◆ TOP PROCESSES                         ║",
                     " ╠══════════════════════════════════════════╣",
                     " ║  NAME                    CPU%    RAM%    ║",
                     " ║──────────────────────────────────────────║"]
            for p in procs[:12]:
                name = (p.get('name', '??') or '??')[:22]
                cpu = p.get('cpu_percent', 0) or 0
                mem = p.get('memory_percent', 0) or 0
                if cpu > 0 or mem > 0.1:
                    lines.append(f" ║  {name:<22} {cpu:>5.1f}   {mem:>5.1f}   ║")
            lines.append(" ╚══════════════════════════════════════════╝")
            self._print("\n".join(lines), "system")
        except Exception as e:
            self._print_jarvis(f"Error obteniendo procesos: {e}")

    def _start_typing_test(self):
        """Start a typing speed test."""
        sentences = [
            "El veloz murciélago hindú comía feliz cardillo y kiwi.",
            "La programación es el arte de organizar la complejidad.",
            "Python es un lenguaje de programación muy versátil.",
            "El sistema operativo gestiona todos los recursos del hardware.",
            "Los algoritmos son la base de la informática moderna.",
            "La inteligencia artificial transformará el mundo laboral.",
            "Un buen código se lee como un buen libro.",
            "La ciberseguridad protege nuestros datos digitales.",
        ]
        sentence = random.choice(sentences)
        self._typing_test_sentence = sentence
        self._typing_test_start = time.time()
        self._print(f"\n◈ TYPING TEST — Escribe esta frase exacta:\n", "info")
        self._print(f"  \"{sentence}\"\n", "hud")
        self._print("  Escríbela y presiona Enter...\n", "muted")
        self._typing_test_active = True

    def _check_typing_test(self, user_input):
        """Check typing test results."""
        elapsed = time.time() - self._typing_test_start
        original = self._typing_test_sentence
        self._typing_test_active = False

        # Calculate WPM
        word_count = len(original.split())
        wpm = (word_count / elapsed) * 60

        # Calculate accuracy
        correct = sum(1 for a, b in zip(user_input, original) if a == b)
        total = max(len(original), len(user_input))
        accuracy = (correct / total) * 100 if total > 0 else 0

        # Rating
        if wpm > 80 and accuracy > 95:
            rating = "EXCEPCIONAL"
        elif wpm > 60 and accuracy > 90:
            rating = "MUY BUENO"
        elif wpm > 40 and accuracy > 80:
            rating = "BUENO"
        elif wpm > 25:
            rating = "NORMAL"
        else:
            rating = "SIGUE PRACTICANDO"

        result = (
            f"\n◈ RESULTADOS TYPING TEST\n"
            f"{'═' * 35}\n"
            f"  Velocidad: {wpm:.0f} WPM\n"
            f"  Precisión: {accuracy:.1f}%\n"
            f"  Tiempo: {elapsed:.1f} segundos\n"
            f"  Rating: {rating}\n"
            f"{'═' * 35}"
        )
        self._print(result, "system")

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

    # ─── ENVIAR ──────────────────────────────────────

    def _send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.history_index = -1
        self._process_input(text)

    def _quick_cmd(self, text):
        self._process_input(text)

    # ─── PROCESAMIENTO CENTRAL ───────────────────────

    def _process_input(self, text):
        self.command_history.append(text)
        DataStore.save(HISTORY_FILE, list(self.command_history))
        self._print_user(text)

        # Check if typing test is active
        if getattr(self, '_typing_test_active', False):
            self._check_typing_test(text)
            return

        comando = text.lower().strip()
        C = self.theme

        # ── Comandos locales ──

        if comando in ("salir", "exit", "quit"):
            self._on_close()
            return

        if comando in ("cls", "clear", "limpiar"):
            self._clear_output()
            return

        # Proveedor
        if comando.startswith("config proveedor:") or comando.startswith("config provider:"):
            prov = text.split(":", 1)[1].strip().lower()
            if prov not in PROVIDERS:
                self._print_jarvis(f"Proveedor '{prov}' no reconocido. Opciones: {', '.join(PROVIDERS.keys())}")
                return
            self.config["provider"] = prov
            pinfo = PROVIDERS[prov]
            self.config["model"] = ""
            DataStore.save(CONFIG_FILE, self.config)
            self._print_jarvis(
                f"Proveedor cambiado a {pinfo['name']} ({pinfo['cost']}).\n"
                f"Modelo: {pinfo['default_model']} | Disponibles: {', '.join(pinfo['models'])}"
            )
            if prov == "ollama":
                self._print("  ℹ️ Ollama no necesita API key. Solo asegúrate de tenerlo corriendo.", "muted")
                self.brain.init_provider("ollama", "")
            else:
                api_key = self.config.get(f"api_key_{prov}", "") or self.config.get("api_key", "")
                if api_key:
                    self.brain.init_provider(prov, api_key)
                else:
                    self._print(f"  ⚠️ Configura: config api: TU_KEY → {pinfo['get_key_url']}", "muted")
            self.voice.speak(f"Proveedor cambiado a {pinfo['name']}.")
            return

        # API Key
        if comando.startswith("config api:") or comando.startswith("config key:"):
            key = text.split(":", 1)[1].strip()
            self.config["api_key"] = key
            provider = self.config.get("provider", "gemini")
            DataStore.save(CONFIG_FILE, self.config)
            if self.brain.init_provider(provider, key):
                pname = PROVIDERS.get(provider, {}).get("name", provider)
                self._print_jarvis(f"API Key configurada para {pname}. Cerebro conectado, señor.")
                self.voice.speak("API Key configurada. Estoy listo.")
            else:
                if PROVIDERS.get(provider, {}).get("needs_openai_lib") and not HAS_OPENAI:
                    self._print_jarvis(f"{provider} necesita: pip install openai")
                else:
                    self._print_jarvis("Error conectando. Verifica tu API key.")
            return

        # Provider-specific API keys (config api_openrouter: KEY, config api_cerebras: KEY)
        api_prov_match = re.match(r'config api[_\s](openrouter|cerebras|groq|gemini):', comando)
        if api_prov_match:
            prov = api_prov_match.group(1)
            key = text.split(":", 1)[1].strip()
            self.config[f"api_key_{prov}"] = key
            DataStore.save(CONFIG_FILE, self.config)
            self._print_jarvis(f"API Key guardada para {PROVIDERS.get(prov, {}).get('name', prov)}.")
            return

        # Show all models
        if comando in ("modelos", "models", "model list", "cambiar proveedor", "cambiar modelo", "switch provider", "proveedores"):
            self._show_model_switcher()
            return

        # Quick switch: "cambiar a gemini", "cambiar a openrouter", etc.
        cambiar_match = re.match(r'cambiar a (\w+)', comando)
        if cambiar_match:
            target = cambiar_match.group(1).lower()
            if target in PROVIDERS:
                pinfo = PROVIDERS[target]
                model = pinfo["default_model"]
                api_key = self.config.get(f"api_key_{target}", "") or self.config.get("api_key", "")
                if target == "gemini":
                    api_key = self.config.get("api_key_gemini", "") or self.config.get("api_key", "")
                original = getattr(self, '_last_rate_limit_text', '')
                self._switch_provider_and_retry(target, model, original)
            else:
                self._print(f"Proveedor '{target}' no encontrado. Escribe 'modelos' para ver opciones.", "error")
            return

        # Modelo
        if comando.startswith("config modelo:") or comando.startswith("config model:"):
            model = text.split(":", 1)[1].strip()
            self.config["model"] = model
            DataStore.save(CONFIG_FILE, self.config)
            self._print_jarvis(f"Modelo cambiado a {model}.")
            return

        # Nombre
        if comando.startswith("config nombre:"):
            name = text.split(":", 1)[1].strip()
            self.config["user_name"] = name
            DataStore.save(CONFIG_FILE, self.config)
            self._print_jarvis(f"Entendido. Te llamaré {name}.")
            return

        # Voz Edge TTS
        if comando.startswith("config voz:") or comando.startswith("config voice:"):
            voice_key = text.split(":", 1)[1].strip().lower()
            if voice_key in EDGE_VOICES:
                self.config["edge_voice"] = EDGE_VOICES[voice_key]
                self.voice.edge_voice = EDGE_VOICES[voice_key]
                DataStore.save(CONFIG_FILE, self.config)
                self._print_jarvis(f"Voz cambiada a '{voice_key}'.")
                self.voice.speak("Así suena mi nueva voz, señor.")
            else:
                voices_list = ", ".join(EDGE_VOICES.keys())
                self._print_jarvis(f"Voces disponibles: {voices_list}")
            return

        # Tema
        if comando.startswith("config tema:") or comando.startswith("config theme:"):
            theme_key = text.split(":", 1)[1].strip().lower()
            self._apply_theme(theme_key)
            return

        # Typewriter toggle
        if comando in ("typewriter", "tipo", "efecto"):
            self.config["typewriter"] = not self.config.get("typewriter", True)
            DataStore.save(CONFIG_FILE, self.config)
            status = "activado" if self.config["typewriter"] else "desactivado"
            self._print_jarvis(f"Efecto typewriter {status}.")
            return

        # Proveedores
        if comando in ("proveedores", "providers", "modelos"):
            self._show_providers()
            return

        # Pomodoro
        if comando.startswith("pomodoro"):
            parts = comando.split()
            if len(parts) == 1 or "status" in comando:
                self._print_jarvis(self.pomodoro.status())
            elif "stop" in comando or "parar" in comando:
                self._print_jarvis(self.pomodoro.stop())
            else:
                try:
                    mins = int(parts[1]) if len(parts) > 1 else 25
                except ValueError:
                    mins = 25
                self._print_jarvis(self.pomodoro.start(mins))
            return

        # Scheduler
        if comando.startswith("schedule") or comando.startswith("programar"):
            if "list" in comando or "ver" in comando:
                self._print(self.scheduler.list_tasks(), "system")
            elif "del" in comando or "eliminar" in comando:
                try:
                    idx = int(comando.split()[-1]) - 1
                    self._print_jarvis(self.scheduler.remove(idx))
                except (ValueError, IndexError):
                    self._print_jarvis("Uso: schedule del 1")
            else:
                self._print_jarvis(
                    "Programador de tareas:\n"
                    "  schedule ver     — ver tareas\n"
                    "  schedule del 1   — eliminar tarea #1\n"
                    "  (Dile al cerebro IA que programe algo)"
                )
            return

        # Exportar
        if comando in ("exportar", "export"):
            self._export_conversation()
            return

        # Clipboard history
        if comando in ("clipboard", "portapapeles"):
            self._show_clipboard_history()
            return

        # Help
        if comando in ("help", "ayuda", "comandos", "?"):
            self._show_help()
            return

        # Ver notas localmente (no gasta API)
        if comando in ("ver notas", "mis notas", "notas"):
            notes = DataStore.load(NOTES_FILE, [])
            if not notes:
                self._print_jarvis("No tienes notas guardadas.")
            else:
                lines = ["◈ TUS NOTAS:", "═" * 35]
                for i, n in enumerate(notes[-15:], 1):
                    date = n.get("date", "")[:10]
                    lines.append(f"  {i}. [{date}] {n['text']}")
                self._print("\n".join(lines), "system")
            return

        # Ver tareas localmente
        if comando in ("ver tareas", "mis tareas", "tareas", "todos"):
            todos = DataStore.load(TODOS_FILE, [])
            if not todos:
                self._print_jarvis("No tienes tareas pendientes.")
            else:
                lines = ["◈ TUS TAREAS:", "═" * 35]
                for i, t in enumerate(todos, 1):
                    status = "[x]" if t.get("done") else "[ ]"
                    lines.append(f"  {i}. {status} {t['text']}")
                self._print("\n".join(lines), "system")
            return

        # Marcar tarea como hecha
        if comando.startswith("tarea done ") or comando.startswith("tarea hecha "):
            try:
                idx = int(comando.split()[-1]) - 1
                todos = DataStore.load(TODOS_FILE, [])
                if 0 <= idx < len(todos):
                    todos[idx]["done"] = True
                    DataStore.save(TODOS_FILE, todos)
                    self._print_jarvis(f"Tarea #{idx+1} completada.")
                else:
                    self._print_jarvis("Índice inválido.")
            except (ValueError, IndexError):
                self._print_jarvis("Uso: tarea done 1")
            return

        # Uptime
        if comando in ("uptime", "tiempo"):
            elapsed = time.time() - START_TIME
            h, m, s = int(elapsed // 3600), int((elapsed % 3600) // 60), int(elapsed % 60)
            self._print_jarvis(f"Llevo activo {h}h {m}m {s}s, señor.")
            return

        # ── Cronómetro ──
        if comando in ("cronometro", "cronómetro", "stopwatch"):
            self._print(self._stopwatch_status(), "system")
            return
        if comando in ("iniciar cronometro", "iniciar cronómetro", "start stopwatch"):
            if not hasattr(self, '_sw_start') or not self._sw_running:
                self._sw_running = True
                self._sw_start = time.time() - getattr(self, '_sw_elapsed', 0)
                self._print_jarvis("Cronómetro iniciado.")
            else:
                self._print_jarvis("El cronómetro ya está corriendo.")
            return
        if comando in ("parar cronometro", "parar cronómetro", "stop stopwatch"):
            if getattr(self, '_sw_running', False):
                self._sw_running = False
                self._sw_elapsed = time.time() - self._sw_start
                self._print_jarvis(f"Cronómetro detenido: {self._format_elapsed(self._sw_elapsed)}")
            else:
                self._print_jarvis("El cronómetro no está corriendo.")
            return
        if comando in ("reiniciar cronometro", "reiniciar cronómetro", "reset stopwatch"):
            self._sw_running = False
            self._sw_elapsed = 0
            self._print_jarvis("Cronómetro reiniciado a 00:00.")
            return

        # ── Temporizador ──
        m_timer = re.match(r"^(?:temporizador|timer)\s+(\d+)", comando)
        if m_timer:
            mins = int(m_timer.group(1))
            self._timer_end = time.time() + mins * 60
            self._timer_running = True
            self._print_jarvis(f"Temporizador de {mins} minutos iniciado.")
            self._check_timer()
            return
        if comando in ("temporizador", "timer"):
            if getattr(self, '_timer_running', False) and hasattr(self, '_timer_end'):
                rem = self._timer_end - time.time()
                if rem > 0:
                    m_v, s_v = divmod(int(rem), 60)
                    self._print_jarvis(f"Temporizador: {m_v:02d}:{s_v:02d} restantes.")
                else:
                    self._timer_running = False
                    self._print_jarvis("El temporizador ha terminado.")
            else:
                self._print_jarvis("No hay temporizador activo. Uso: timer 10")
            return

        # ── Calculadora (auto-detect math) ──
        if comando.startswith("calc:") or comando.startswith("calcular:"):
            expr = text.split(":", 1)[1].strip()
            self._print(self._safe_calc(expr), "system")
            return
        if re.match(r'^[\d\s\+\-\*/\(\)\.\^%]+$', comando) and len(comando) > 1:
            self._print(self._safe_calc(text), "system")
            return

        # ── Conversor de unidades ──
        if comando.startswith("convertir:") or comando.startswith("convert:"):
            expr = text.split(":", 1)[1].strip()
            self._print(self._convert_units(expr), "system")
            return
        if re.search(r'\d+.*(?:km|millas?|kg|libras?|metros?|pies|litros?|galones?|celsius|fahrenheit|cm|pulgadas?)\s+(?:a|en|to)\s+', comando):
            self._print(self._convert_units(text), "system")
            return

        # ── Calculadora de fechas ──
        if comando.startswith("dias para") or comando.startswith("días para"):
            self._print(self._date_calc(text), "system")
            return
        if re.match(r'^hoy\s*[\+\-]', comando):
            self._print(self._date_calc(text), "system")
            return

        # ── Contraseña local (sin IA) ──
        if comando.startswith("password") or comando.startswith("contraseña") or comando.startswith("clave"):
            m_pwd = re.search(r'(\d+)', comando)
            length = int(m_pwd.group(1)) if m_pwd else 16
            length = max(8, min(128, length))
            self._print(self.executor._gen_password(str(length)), "system")
            return

        # ── Base64 / Hash ──
        if comando.startswith("base64 encode:") or comando.startswith("b64e:"):
            t = text.split(":", 1)[1].strip()
            import base64 as _b64
            self._print(f"◈ Base64: {_b64.b64encode(t.encode()).decode()}", "system")
            return
        if comando.startswith("base64 decode:") or comando.startswith("b64d:"):
            t = text.split(":", 1)[1].strip()
            import base64 as _b64
            try:
                self._print(f"◈ Decoded: {_b64.b64decode(t.encode()).decode()}", "system")
            except Exception:
                self._print("◈ Texto Base64 inválido.", "error")
            return
        if comando.startswith("hash:"):
            import hashlib as _hl
            t = text.split(":", 1)[1].strip()
            self._print(
                f"◈ HASHES de '{t}':\n"
                f"  MD5:    {_hl.md5(t.encode()).hexdigest()}\n"
                f"  SHA1:   {_hl.sha1(t.encode()).hexdigest()}\n"
                f"  SHA256: {_hl.sha256(t.encode()).hexdigest()}",
                "system"
            )
            return

        # ── Herramientas de texto ──
        if comando.startswith("mayusculas:") or comando.startswith("upper:"):
            self._print(f"◈ {text.split(':', 1)[1].strip().upper()}", "system")
            return
        if comando.startswith("minusculas:") or comando.startswith("lower:"):
            self._print(f"◈ {text.split(':', 1)[1].strip().lower()}", "system")
            return
        if comando.startswith("invertir:") or comando.startswith("reverse:"):
            self._print(f"◈ {text.split(':', 1)[1].strip()[::-1]}", "system")
            return
        if comando.startswith("contar:") or comando.startswith("stats:"):
            t = text.split(":", 1)[1].strip()
            self._print(
                f"◈ TEXT STATS:\n"
                f"  Caracteres: {len(t)} | Sin espacios: {len(t.replace(' ', ''))}\n"
                f"  Palabras: {len(t.split())} | Líneas: {t.count(chr(10)) + 1}",
                "system"
            )
            return

        # ── Chistes / Frases motivacionales ──
        if comando in ("chiste", "joke", "humor"):
            chistes = [
                "¿Por qué los programadores prefieren el frío? Porque no quieren bugs... ¡quieren bytes!",
                "Hay 10 tipos de personas: las que entienden binario y las que no.",
                "Un SQL entra en un bar, se acerca a dos tablas y pregunta: ¿puedo unirme?",
                "¿Por qué Java y JavaScript se parecen? Como car y carpet.",
                "Un programador pone 2 vasos en la mesita: uno con agua por si tiene sed, y otro vacío por si no tiene.",
                "Mi código funciona y no sé por qué. Mi código no funciona y no sé por qué.",
                "// Este código funciona, no lo toques.",
                "¿Cuántos programadores se necesitan para cambiar un foco? Ninguno, es un problema de hardware.",
            ]
            self._print_jarvis(random.choice(chistes))
            return
        if comando in ("frase", "motivacion", "motivación", "quote"):
            frases = [
                "El éxito es la suma de pequeños esfuerzos repetidos día tras día. — Robert Collier",
                "No te detengas cuando estés cansado. Detente cuando hayas terminado.",
                "La disciplina es el puente entre las metas y los logros. — Jim Rohn",
                "El único modo de hacer un gran trabajo es amar lo que haces. — Steve Jobs",
                "Todo parece imposible hasta que se hace. — Nelson Mandela",
                "La creatividad es la inteligencia divirtiéndose. — Albert Einstein",
                "El futuro pertenece a quienes creen en la belleza de sus sueños. — Eleanor Roosevelt",
                "La mejor forma de predecir el futuro es creándolo. — Abraham Lincoln",
            ]
            self._print_jarvis(f"◆ \"{random.choice(frases)}\"")
            return

        # ── Briefing diario ──
        if comando in ("briefing", "buenos dias", "buenos días", "resumen", "inicio"):
            self._show_briefing()
            return

        # ── Dado / Moneda ──
        if comando in ("dado", "dice", "tirar dado", "d6"):
            result = random.randint(1, 6)
            self._print_jarvis(f"Resultado del dado: {result}")
            return
        if comando.startswith("d") and comando[1:].isdigit():
            sides = int(comando[1:])
            if 2 <= sides <= 1000:
                result = random.randint(1, sides)
                self._print_jarvis(f"D{sides}: {result}")
            return
        if comando in ("moneda", "coin", "cara o cruz", "flip"):
            result = random.choice(["CARA", "CRUZ"])
            self._print_jarvis(f"Moneda: {result}")
            return

        # ── Procesos del sistema ──
        if comando in ("procesos", "processes", "top"):
            self._show_processes()
            return

        # ── Buscar archivos local ──
        if comando.startswith("buscar:") or comando.startswith("find:"):
            query = text.split(":", 1)[1].strip()
            self._print("◈ Buscando archivos...", "muted")
            self.root.update()
            def _search():
                r = self.executor._search_files(query)
                self.root.after(0, lambda: self._print(r, "system"))
            threading.Thread(target=_search, daemon=True).start()
            return

        # ── Abrir programas directamente (fallback sin IA) ──
        if comando.startswith("abrir "):
            prog = text[6:].strip()
            r = self.executor._open_program(prog)
            if r:
                self._print_jarvis(r)
            return

        # ── YouTube directo (sin IA) ──
        if comando.startswith("youtube ") or comando.startswith("yt "):
            query = re.sub(r'^(youtube|yt)\s+', '', text, flags=re.IGNORECASE).strip()
            if query:
                self._print_jarvis(f"Abriendo video de YouTube: {query}")
                self.voice.speak(f"Abriendo video, señor.")
                self.root.update()
                def _yt_open():
                    self.executor._search_youtube(query)
                threading.Thread(target=_yt_open, daemon=True).start()
            else:
                self._print_jarvis("Uso: youtube <lo que quieras buscar>")
            return

        # ── Google directo (sin IA) ──
        if comando.startswith("google "):
            query = re.sub(r'^google\s+', '', text, flags=re.IGNORECASE).strip()
            if query:
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                self.executor._open_in_browser(url)
                self._print_jarvis(f"Buscando en Google: {query}")
            else:
                self._print_jarvis("Uso: google <lo que quieras buscar>")
            return

        # ── Pomodoro mejorado para estudio ──
        if comando.startswith("estudiar") or comando.startswith("study"):
            mins = 45
            parts = comando.split()
            for p in parts:
                if p.isdigit():
                    mins = int(p)
                    break
            self.pomodoro.start(work=mins, brk=10)
            self._print_jarvis(f"◈ Modo estudio activado: {mins} min de enfoque, 10 min descanso.\nUsa 'pomodoro stop' para parar.")
            self.voice.speak(f"Modo estudio activado. {mins} minutos de enfoque.")
            return

        # ── Wikipedia rapida ──
        if comando.startswith("wiki ") or comando.startswith("wikipedia "):
            query = re.sub(r'^(wiki|wikipedia)\s+', '', text, flags=re.IGNORECASE).strip()
            self._print("◈ Consultando Wikipedia...", "muted")
            self.root.update()
            def _wiki():
                try:
                    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Jarvis/6.1"})
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    title = data.get("title", query)
                    extract = data.get("extract", "No se encontró información.")
                    desktop_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
                    result = f"◈ WIKIPEDIA: {title}\n{'═' * 40}\n{extract[:800]}"
                    if desktop_url:
                        result += f"\n\n→ {desktop_url}"
                    self.root.after(0, lambda: self._print_jarvis(result))
                except Exception as e:
                    self.root.after(0, lambda: self._print_jarvis(f"No se pudo consultar Wikipedia: {e}"))
            threading.Thread(target=_wiki, daemon=True).start()
            return

        # ── Reloj mundial ──
        if comando.startswith("hora en ") or comando.startswith("time in "):
            city = re.sub(r'^(hora en|time in)\s+', '', comando).strip()
            tz_map = {
                "new york": -5, "nueva york": -5, "los angeles": -8, "london": 0,
                "londres": 0, "paris": 1, "tokyo": 9, "tokio": 9, "sydney": 11,
                "berlin": 1, "moscow": 3, "moscu": 3, "madrid": 1, "roma": 1,
                "beijing": 8, "pekin": 8, "dubai": 4, "mexico": -6, "cdmx": -6,
                "bogota": -5, "buenos aires": -3, "santiago": -3, "lima": -5,
                "sao paulo": -3, "miami": -5, "chicago": -6, "denver": -7,
                "hawaii": -10, "alaska": -9, "seoul": 9, "seul": 9,
            }
            offset = tz_map.get(city.lower())
            if offset is not None:
                import datetime as _dt
                utc = _dt.datetime.utcnow()
                local_time = utc + _dt.timedelta(hours=offset)
                self._print_jarvis(f"◈ Hora en {city.title()}: {local_time.strftime('%H:%M:%S')} (UTC{offset:+d})")
            else:
                self._print_jarvis(f"No tengo la zona horaria de '{city}'. Pregúntame con IA para más precisión.")
            return

        # ── Contador de palabras ──
        if comando.startswith("contar ") or comando.startswith("wc "):
            txt = re.sub(r'^(contar|wc)\s+', '', text, flags=re.IGNORECASE).strip()
            words = len(txt.split())
            chars = len(txt)
            chars_no_space = len(txt.replace(" ", ""))
            lines = txt.count("\n") + 1
            self._print_jarvis(f"◈ Palabras: {words} | Caracteres: {chars} | Sin espacios: {chars_no_space} | Líneas: {lines}")
            return

        # ── IP publica ──
        if comando in ("ip", "mi ip", "ip publica", "myip"):
            self._print("◈ Consultando IP...", "muted")
            def _get_ip():
                try:
                    req = urllib.request.Request("https://api.ipify.org?format=json",
                                                 headers={"User-Agent": "Jarvis/6.1"})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    self.root.after(0, lambda: self._print_jarvis(f"◈ Tu IP pública: {data['ip']}"))
                except Exception:
                    self.root.after(0, lambda: self._print_jarvis("No se pudo obtener la IP pública."))
            threading.Thread(target=_get_ip, daemon=True).start()
            return

        # ── Velocidad de escritura (typing test) ──
        if comando in ("typing", "typing test", "mecanografia", "velocidad"):
            self._start_typing_test()
            return

        # ── Atajos rápidos para la U ──
        if comando in ("google docs", "docs"):
            webbrowser.open_new_tab("https://docs.google.com")
            self._print_jarvis("Abriendo Google Docs.")
            return
        if comando in ("google sheets", "sheets", "hojas de calculo"):
            webbrowser.open_new_tab("https://sheets.google.com")
            self._print_jarvis("Abriendo Google Sheets.")
            return
        if comando in ("google slides", "slides", "presentaciones"):
            webbrowser.open_new_tab("https://slides.google.com")
            self._print_jarvis("Abriendo Google Slides.")
            return
        if comando in ("drive", "google drive"):
            webbrowser.open_new_tab("https://drive.google.com")
            self._print_jarvis("Abriendo Google Drive.")
            return
        if comando in ("classroom", "google classroom"):
            webbrowser.open_new_tab("https://classroom.google.com")
            self._print_jarvis("Abriendo Google Classroom.")
            return
        if comando in ("gmail", "correo", "email"):
            webbrowser.open_new_tab("https://mail.google.com")
            self._print_jarvis("Abriendo Gmail.")
            return
        if comando in ("calendar", "calendario"):
            webbrowser.open_new_tab("https://calendar.google.com")
            self._print_jarvis("Abriendo Google Calendar.")
            return
        if comando in ("github"):
            webbrowser.open_new_tab("https://github.com")
            self._print_jarvis("Abriendo GitHub.")
            return
        if comando in ("chatgpt"):
            webbrowser.open_new_tab("https://chat.openai.com")
            self._print_jarvis("Abriendo ChatGPT.")
            return
        if comando in ("canva"):
            webbrowser.open_new_tab("https://www.canva.com")
            self._print_jarvis("Abriendo Canva.")
            return
        if comando in ("notion"):
            webbrowser.open_new_tab("https://www.notion.so")
            self._print_jarvis("Abriendo Notion.")
            return
        if comando in ("trello"):
            webbrowser.open_new_tab("https://trello.com")
            self._print_jarvis("Abriendo Trello.")
            return

        # ══════════════════════════════════════════════
        # IRON MAN / SYSTEM POWER COMMANDS
        # ══════════════════════════════════════════════

        # ── Battery status ──
        if comando in ("bateria", "battery", "bat"):
            if HAS_PSUTIL:
                bat = psutil.sensors_battery()
                if bat:
                    pct = bat.percent
                    plugged = "🔌 Conectado a corriente" if bat.power_plugged else "🔋 Usando batería"
                    bar = self.executor._bar(pct, 20)
                    time_left = ""
                    if not bat.power_plugged and bat.secsleft > 0:
                        hrs = bat.secsleft // 3600
                        mins = (bat.secsleft % 3600) // 60
                        time_left = f"\n  ⏱️ Tiempo restante: {hrs}h {mins}m"
                    status = "CRITICAL" if pct < 15 else "LOW" if pct < 30 else "OK" if pct < 80 else "FULL"
                    self._print(f"◈ BATERÍA: {pct}% {bar} [{status}]\n  {plugged}{time_left}", "system")
                    if pct < 15:
                        self.voice.speak("Advertencia: batería crítica, conecte el cargador.")
                else:
                    self._print_jarvis("No se detectó batería (probablemente un desktop).")
            else:
                self._print_jarvis("Necesitas psutil: pip install psutil")
            return

        # ── Volume control (Windows) ──
        if comando.startswith("volumen ") or comando.startswith("volume "):
            vol_arg = comando.split()[-1]
            if vol_arg in ("mute", "silencio", "mudo"):
                subprocess.run('powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"',
                               shell=True, creationflags=0x08000000)
                self._print_jarvis("🔇 Volumen silenciado.")
            elif vol_arg.isdigit():
                level = max(0, min(100, int(vol_arg)))
                ps_cmd = f'''powershell -c "
$vol = (New-Object -ComObject WScript.Shell)
# Set volume to {level}%
1..50 | ForEach-Object {{ $vol.SendKeys([char]174) }}
$steps = [math]::Round({level} / 2)
1..$steps | ForEach-Object {{ $vol.SendKeys([char]175) }}
"'''
                subprocess.Popen(ps_cmd, shell=True, creationflags=0x08000000)
                self._print_jarvis(f"🔊 Volumen ajustado a ~{level}%")
            else:
                self._print_jarvis("Uso: volumen 50 | volumen mute")
            return

        # ── Brightness control (Windows) ──
        if comando.startswith("brillo ") or comando.startswith("brightness "):
            try:
                level = int(comando.split()[-1])
                level = max(0, min(100, level))
                subprocess.run(
                    f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"',
                    shell=True, creationflags=0x08000000, timeout=5
                )
                bar = self.executor._bar(level, 20)
                self._print_jarvis(f"💡 Brillo: {level}% {bar}")
            except Exception as e:
                self._print_jarvis(f"No pude cambiar el brillo: {e}")
            return

        # ── Disk cleanup ──
        if comando in ("limpiar disco", "cleanup", "limpiar temp", "clean"):
            self._print("◈ Limpiando archivos temporales...", "muted")
            self.root.update()
            def _cleanup():
                cleaned = 0
                total_size = 0
                temp_dirs = [tempfile.gettempdir(), os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp")]
                for tmp_dir in temp_dirs:
                    if os.path.exists(tmp_dir):
                        for f in os.listdir(tmp_dir):
                            fp = os.path.join(tmp_dir, f)
                            try:
                                if os.path.isfile(fp):
                                    total_size += os.path.getsize(fp)
                                    os.remove(fp)
                                    cleaned += 1
                            except Exception:
                                pass
                size_mb = total_size / (1024 * 1024)
                self.root.after(0, lambda: self._print_jarvis(
                    f"◈ LIMPIEZA COMPLETADA\n  🗑️ {cleaned} archivos eliminados\n  💾 {size_mb:.1f} MB liberados"
                ))
            threading.Thread(target=_cleanup, daemon=True).start()
            return

        # ── Network / WiFi info ──
        if comando in ("red", "network", "wifi", "net"):
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            info = f"◈ RED / NETWORK\n{'═' * 35}\n  🖥️ Host: {hostname}\n  📍 IP Local: {local_ip}"
            try:
                result = subprocess.run('netsh wlan show interfaces', capture_output=True, text=True,
                                        shell=True, creationflags=0x08000000, timeout=5)
                for line in result.stdout.split("\n"):
                    if "SSID" in line and "BSSID" not in line:
                        info += f"\n  📶 {line.strip()}"
                    elif "Signal" in line or "Señal" in line:
                        info += f"\n  📊 {line.strip()}"
                    elif "Radio type" in line or "Tipo de radio" in line:
                        info += f"\n  📻 {line.strip()}"
            except Exception:
                pass
            self._print(info, "system")
            return

        # ── WiFi passwords (Iron Man scan) ──
        if comando in ("wifi pass", "wifi password", "wifi clave", "wifi claves"):
            self._print("◈ Escaneando perfiles WiFi guardados...", "muted")
            self.root.update()
            try:
                result = subprocess.run('netsh wlan show profiles', capture_output=True, text=True,
                                        shell=True, creationflags=0x08000000, timeout=10)
                profiles = re.findall(r":\s*(.+)", result.stdout)
                wifi_list = []
                for prof in profiles[:15]:
                    prof = prof.strip()
                    if not prof:
                        continue
                    try:
                        detail = subprocess.run(f'netsh wlan show profile "{prof}" key=clear',
                                                capture_output=True, text=True, shell=True,
                                                creationflags=0x08000000, timeout=5)
                        key_match = re.search(r"Key Content\s*:\s*(.+)|Contenido de la clave\s*:\s*(.+)", detail.stdout)
                        pwd = (key_match.group(1) or key_match.group(2)).strip() if key_match else "—"
                        wifi_list.append(f"  📶 {prof}: {pwd}")
                    except Exception:
                        wifi_list.append(f"  📶 {prof}: (error)")
                if wifi_list:
                    self._print("◈ WIFI PASSWORDS\n" + "═" * 35 + "\n" + "\n".join(wifi_list), "system")
                else:
                    self._print_jarvis("No se encontraron perfiles WiFi.")
            except Exception as e:
                self._print_jarvis(f"Error: {e}")
            return

        # ── Speed test ──
        if comando in ("speedtest", "velocidad", "speed", "speed test"):
            self._print("◈ Midiendo velocidad de internet...", "muted")
            self.root.update()
            def _speed():
                try:
                    url = "https://speed.cloudflare.com/__down?bytes=10000000"
                    start = time.time()
                    req = urllib.request.Request(url, headers={"User-Agent": "Jarvis/6.2"})
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        data = resp.read()
                    elapsed = time.time() - start
                    mbps = (len(data) * 8 / 1_000_000) / elapsed
                    self.root.after(0, lambda: self._print_jarvis(
                        f"◈ SPEED TEST\n{'═' * 35}\n  ⬇️ Download: {mbps:.1f} Mbps\n  📦 {len(data)/1_000_000:.1f} MB en {elapsed:.1f}s"
                    ))
                except Exception as e:
                    self.root.after(0, lambda: self._print_jarvis(f"Error en speed test: {e}"))
            threading.Thread(target=_speed, daemon=True).start()
            return

        # ══════════════════════════════════════════════
        # FINANCE & DATA
        # ══════════════════════════════════════════════

        # ── Currency converter ──
        if comando.startswith("cambio ") or comando.startswith("moneda ") and "a" in comando:
            m = re.match(r'(?:cambio|moneda)\s+([\d.]+)\s*(\w{3})\s+a\s+(\w{3})', comando)
            if m:
                amount, src, tgt = float(m.group(1)), m.group(2).upper(), m.group(3).upper()
                self._print("◈ Consultando tipo de cambio...", "muted")
                self.root.update()
                def _exchange():
                    try:
                        url = f"https://api.exchangerate-api.com/v4/latest/{src}"
                        req = urllib.request.Request(url, headers={"User-Agent": "Jarvis/6.2"})
                        with urllib.request.urlopen(req, timeout=10) as resp:
                            data = json.loads(resp.read().decode("utf-8"))
                        rate = data["rates"].get(tgt)
                        if rate:
                            result = amount * rate
                            self.root.after(0, lambda: self._print_jarvis(
                                f"◈ CAMBIO DE DIVISA\n  💰 {amount:,.2f} {src} = {result:,.2f} {tgt}\n  📊 1 {src} = {rate:.4f} {tgt}"
                            ))
                        else:
                            self.root.after(0, lambda: self._print_jarvis(f"Moneda '{tgt}' no encontrada."))
                    except Exception as e:
                        self.root.after(0, lambda: self._print_jarvis(f"Error: {e}"))
                threading.Thread(target=_exchange, daemon=True).start()
            else:
                self._print_jarvis("Uso: cambio 100 USD a CLP")
            return

        # ── Crypto prices ──
        if comando in ("crypto", "bitcoin", "btc", "eth", "cripto", "criptomonedas"):
            self._print("◈ Consultando criptomonedas...", "muted")
            self.root.update()
            def _crypto():
                try:
                    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple&vs_currencies=usd,clp&include_24hr_change=true"
                    req = urllib.request.Request(url, headers={"User-Agent": "Jarvis/6.2"})
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    lines = ["◈ CRYPTO PRICES", "═" * 35]
                    symbols = {"bitcoin": "₿ BTC", "ethereum": "Ξ ETH", "solana": "◎ SOL", "ripple": "✕ XRP"}
                    for coin, sym in symbols.items():
                        if coin in data:
                            d = data[coin]
                            usd = d.get("usd", 0)
                            clp = d.get("clp", 0)
                            change = d.get("usd_24h_change", 0)
                            arrow = "📈" if change > 0 else "📉"
                            lines.append(f"  {sym}: ${usd:,.2f} USD | ${clp:,.0f} CLP {arrow} {change:+.1f}%")
                    self.root.after(0, lambda: self._print("\n".join(lines), "system"))
                except Exception as e:
                    self.root.after(0, lambda: self._print_jarvis(f"Error crypto: {e}"))
            threading.Thread(target=_crypto, daemon=True).start()
            return

        # ── Download file ──
        if comando.startswith("descargar ") or comando.startswith("download "):
            url = re.sub(r'^(descargar|download)\s+', '', text, flags=re.IGNORECASE).strip()
            if url:
                self._print(f"◈ Descargando: {url}", "muted")
                self.root.update()
                def _download():
                    try:
                        filename = url.split("/")[-1].split("?")[0] or "download"
                        dest = os.path.join(os.path.expanduser("~"), "Downloads", filename)
                        req = urllib.request.Request(url, headers={"User-Agent": "Jarvis/6.2"})
                        with urllib.request.urlopen(req, timeout=60) as resp:
                            with open(dest, "wb") as f:
                                f.write(resp.read())
                        size = os.path.getsize(dest) / (1024 * 1024)
                        self.root.after(0, lambda: self._print_jarvis(f"◈ Descargado: {filename} ({size:.1f} MB)\n  📁 {dest}"))
                    except Exception as e:
                        self.root.after(0, lambda: self._print_jarvis(f"Error descargando: {e}"))
                threading.Thread(target=_download, daemon=True).start()
            else:
                self._print_jarvis("Uso: descargar https://url.com/archivo.zip")
            return

        # ══════════════════════════════════════════════
        # PRODUCTIVITY
        # ══════════════════════════════════════════════

        # ── Habit tracker ──
        if comando in ("habitos", "habits", "mis habitos"):
            habits = DataStore.load(HABITS_FILE, {})
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if not habits.get("list"):
                self._print_jarvis("No tienes hábitos. Agrega uno: habito add NOMBRE")
            else:
                lines = ["◈ HABIT TRACKER", "═" * 35]
                today_done = habits.get("log", {}).get(today, [])
                for h in habits["list"]:
                    done = "✅" if h in today_done else "⬜"
                    # Count streak
                    streak = 0
                    d = datetime.datetime.now()
                    while True:
                        ds = d.strftime("%Y-%m-%d")
                        if h in habits.get("log", {}).get(ds, []):
                            streak += 1
                            d -= datetime.timedelta(days=1)
                        else:
                            break
                    lines.append(f"  {done} {h} {'🔥' * min(streak, 5)} ({streak}d streak)")
                self._print("\n".join(lines), "system")
            return

        if comando.startswith("habito add ") or comando.startswith("habit add "):
            name = re.sub(r'(?:habito|habit)\s+add\s+', '', text, flags=re.IGNORECASE).strip()
            habits = DataStore.load(HABITS_FILE, {"list": [], "log": {}})
            if name not in habits["list"]:
                habits["list"].append(name)
                DataStore.save(HABITS_FILE, habits)
                self._print_jarvis(f"✅ Hábito '{name}' agregado.")
            else:
                self._print_jarvis(f"Ya tienes el hábito '{name}'.")
            return

        if comando.startswith("habito done ") or comando.startswith("habit done "):
            name = re.sub(r'(?:habito|habit)\s+done\s+', '', text, flags=re.IGNORECASE).strip()
            habits = DataStore.load(HABITS_FILE, {"list": [], "log": {}})
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if today not in habits.get("log", {}):
                habits["log"][today] = []
            if name in habits.get("list", []) and name not in habits["log"][today]:
                habits["log"][today].append(name)
                DataStore.save(HABITS_FILE, habits)
                self._print_jarvis(f"✅ Hábito '{name}' completado hoy.")
            elif name not in habits.get("list", []):
                self._print_jarvis(f"No tienes el hábito '{name}'. Agrégalo: habito add {name}")
            else:
                self._print_jarvis(f"Ya completaste '{name}' hoy.")
            return

        if comando.startswith("habito del ") or comando.startswith("habit del "):
            name = re.sub(r'(?:habito|habit)\s+del\s+', '', text, flags=re.IGNORECASE).strip()
            habits = DataStore.load(HABITS_FILE, {"list": [], "log": {}})
            if name in habits.get("list", []):
                habits["list"].remove(name)
                DataStore.save(HABITS_FILE, habits)
                self._print_jarvis(f"🗑️ Hábito '{name}' eliminado.")
            return

        # ── Flashcards ──
        if comando in ("flashcards", "flash", "tarjetas"):
            cards = DataStore.load(FLASHCARDS_FILE, [])
            if not cards:
                self._print_jarvis("No tienes flashcards. Crea una: flash add PREGUNTA | RESPUESTA")
            else:
                # Random quiz mode
                card = random.choice(cards)
                self._flash_card = card
                self._flash_mode = True
                self._print(f"◈ FLASHCARD ({len(cards)} tarjetas)\n{'═' * 35}\n  ❓ {card['q']}\n\n  (Escribe tu respuesta...)", "system")
            return

        if comando.startswith("flash add ") or comando.startswith("tarjeta add "):
            content = re.sub(r'(?:flash|tarjeta)\s+add\s+', '', text, flags=re.IGNORECASE).strip()
            if "|" in content:
                q, a = content.split("|", 1)
                cards = DataStore.load(FLASHCARDS_FILE, [])
                cards.append({"q": q.strip(), "a": a.strip(), "score": 0})
                DataStore.save(FLASHCARDS_FILE, cards)
                self._print_jarvis(f"📝 Flashcard creada. Total: {len(cards)}")
            else:
                self._print_jarvis("Uso: flash add PREGUNTA | RESPUESTA")
            return

        if comando in ("flash list", "tarjetas ver", "flash ver"):
            cards = DataStore.load(FLASHCARDS_FILE, [])
            if cards:
                lines = ["◈ FLASHCARDS", "═" * 35]
                for i, c in enumerate(cards, 1):
                    lines.append(f"  {i}. Q: {c['q']}")
                    lines.append(f"     A: {c['a']}")
                self._print("\n".join(lines), "system")
            else:
                self._print_jarvis("No tienes flashcards.")
            return

        if comando.startswith("flash del "):
            try:
                idx = int(comando.split()[-1]) - 1
                cards = DataStore.load(FLASHCARDS_FILE, [])
                if 0 <= idx < len(cards):
                    removed = cards.pop(idx)
                    DataStore.save(FLASHCARDS_FILE, cards)
                    self._print_jarvis(f"🗑️ Flashcard eliminada: {removed['q']}")
            except (ValueError, IndexError):
                self._print_jarvis("Uso: flash del 1")
            return

        # Check flashcard answer
        if getattr(self, '_flash_mode', False):
            card = self._flash_card
            self._flash_mode = False
            user_ans = text.strip().lower()
            correct_ans = card["a"].strip().lower()
            # Fuzzy match: check if answer contains key words
            if user_ans == correct_ans or correct_ans in user_ans or user_ans in correct_ans:
                self._print_jarvis(f"✅ ¡Correcto!\n  Respuesta: {card['a']}")
                # Update score
                cards = DataStore.load(FLASHCARDS_FILE, [])
                for c in cards:
                    if c["q"] == card["q"]:
                        c["score"] = c.get("score", 0) + 1
                DataStore.save(FLASHCARDS_FILE, cards)
            else:
                self._print_jarvis(f"❌ Incorrecto.\n  Tu respuesta: {text}\n  ✅ Correcta: {card['a']}")
            return

        # ── Alarm ──
        if comando.startswith("alarma ") or comando.startswith("alarm "):
            m = re.match(r'(?:alarma|alarm)\s+(\d{1,2}):(\d{2})', comando)
            if m:
                h, mn = int(m.group(1)), int(m.group(2))
                alarm_time = f"{h:02d}:{mn:02d}"
                self._print_jarvis(f"⏰ Alarma configurada para las {alarm_time}")
                def _alarm():
                    while True:
                        now = datetime.datetime.now().strftime("%H:%M")
                        if now == alarm_time:
                            for _ in range(5):
                                SoundFX.beep_alert()
                                time.sleep(0.5)
                            self.root.after(0, lambda: self._print_jarvis(f"⏰ ¡¡¡ ALARMA {alarm_time} !!!"))
                            self.root.after(0, lambda: self.voice.speak("Alarma! Es hora, señor."))
                            break
                        time.sleep(10)
                threading.Thread(target=_alarm, daemon=True).start()
            else:
                self._print_jarvis("Uso: alarma 07:30")
            return

        # ══════════════════════════════════════════════
        # DEV & DATA TOOLS
        # ══════════════════════════════════════════════

        # ── JSON formatter ──
        if comando.startswith("json:") or comando.startswith("json "):
            raw = text.split(":", 1)[1].strip() if ":" in text else text[5:].strip()
            try:
                parsed = json.loads(raw)
                formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
                self._print(f"◈ JSON FORMATTED:\n{formatted}", "system")
            except json.JSONDecodeError as e:
                self._print(f"◈ JSON Error: {e}", "error")
            return

        # ── Lorem ipsum ──
        if comando in ("lorem", "ipsum", "lorem ipsum"):
            paragraphs = [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.",
            ]
            text_out = "\n\n".join(paragraphs)
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(text_out)
                self._print(f"◈ LOREM IPSUM (copiado al portapapeles):\n\n{text_out}", "system")
            except Exception:
                self._print(f"◈ LOREM IPSUM:\n\n{text_out}", "system")
            return

        # ── Color converter ──
        if comando.startswith("color #") or comando.startswith("color rgb"):
            color_arg = re.sub(r'^color\s+', '', text, flags=re.IGNORECASE).strip()
            if color_arg.startswith("#"):
                hex_c = color_arg.lstrip("#")
                if len(hex_c) == 6:
                    r, g, b = int(hex_c[:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
                    self._print(f"◈ COLOR: #{hex_c}\n  RGB: ({r}, {g}, {b})\n  HSL: ~use for design", "system")
                else:
                    self._print_jarvis("Formato: color #FF5733")
            elif "rgb" in color_arg.lower():
                nums = re.findall(r'\d+', color_arg)
                if len(nums) >= 3:
                    r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
                    hex_c = f"#{r:02X}{g:02X}{b:02X}"
                    self._print(f"◈ COLOR: RGB({r},{g},{b})\n  HEX: {hex_c}", "system")
            return

        # ── UUID generator ──
        if comando in ("uuid", "guid"):
            import uuid as _uuid
            uid = str(_uuid.uuid4())
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(uid)
            except Exception:
                pass
            self._print(f"◈ UUID: {uid}\n  (copiado al portapapeles)", "system")
            return

        # ── Random generators ──
        if comando.startswith("random "):
            arg = comando.split("random ", 1)[1].strip()
            if arg.startswith("number") or arg.startswith("numero"):
                nums = re.findall(r'\d+', arg)
                lo = int(nums[0]) if len(nums) > 0 else 1
                hi = int(nums[1]) if len(nums) > 1 else 100
                self._print_jarvis(f"🎲 Número random: {random.randint(lo, hi)} (entre {lo} y {hi})")
            elif arg == "color":
                r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                hex_c = f"#{r:02X}{g:02X}{b:02X}"
                self._print_jarvis(f"🎨 Color random: {hex_c} = RGB({r},{g},{b})")
            elif arg == "password" or arg == "pass":
                self._print(self.executor._gen_password("16"), "system")
            else:
                self._print_jarvis("Uso: random number 1 100 | random color | random password")
            return

        # ── Regex tester ──
        if comando.startswith("regex:"):
            parts = text.split(":", 1)[1].strip().split("|", 1)
            if len(parts) == 2:
                pattern, test_str = parts[0].strip(), parts[1].strip()
                try:
                    matches = re.findall(pattern, test_str)
                    self._print(f"◈ REGEX: /{pattern}/\n  Text: {test_str}\n  Matches: {matches}\n  Count: {len(matches)}", "system")
                except re.error as e:
                    self._print(f"◈ Regex error: {e}", "error")
            else:
                self._print_jarvis("Uso: regex: PATRON | TEXTO")
            return

        # ── System uptime (OS level) ──
        if comando in ("uptime os", "uptime sistema", "uptime pc"):
            if HAS_PSUTIL:
                boot = datetime.datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.datetime.now() - boot
                days = uptime.days
                hours = uptime.seconds // 3600
                mins = (uptime.seconds % 3600) // 60
                self._print(f"◈ PC encendido desde: {boot.strftime('%d/%m/%Y %H:%M')}\n  ⏱️ Uptime: {days}d {hours}h {mins}m", "system")
            else:
                self._print_jarvis("Necesitas psutil.")
            return

        # ── Scan open ports (Iron Man network scan) ──
        if comando.startswith("scan ") or comando == "scan":
            target = "127.0.0.1"
            parts = comando.split()
            if len(parts) > 1:
                target = parts[1]
            self._print(f"◈ Escaneando puertos de {target}...", "muted")
            self.root.update()
            def _scan():
                open_ports = []
                common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443]
                for port in common_ports:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.5)
                        if s.connect_ex((target, port)) == 0:
                            open_ports.append(port)
                        s.close()
                    except Exception:
                        pass
                if open_ports:
                    lines = [f"◈ PORT SCAN: {target}", "═" * 35]
                    port_names = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",
                                  135:"RPC",139:"NetBIOS",143:"IMAP",443:"HTTPS",445:"SMB",993:"IMAPS",
                                  995:"POP3S",1433:"MSSQL",3306:"MySQL",3389:"RDP",5432:"PostgreSQL",
                                  5900:"VNC",8080:"HTTP-Alt",8443:"HTTPS-Alt"}
                    for p in open_ports:
                        name = port_names.get(p, "Unknown")
                        lines.append(f"  🟢 Puerto {p}: {name} [OPEN]")
                    self.root.after(0, lambda: self._print("\n".join(lines), "system"))
                else:
                    self.root.after(0, lambda: self._print_jarvis(f"No se encontraron puertos abiertos en {target}"))
            threading.Thread(target=_scan, daemon=True).start()
            return

        # ── Daily summary ──
        if comando in ("mi dia", "my day", "resumen del dia", "daily"):
            hour = datetime.datetime.now().hour
            period = "Buenos días" if hour < 12 else "Buenas tardes" if hour < 19 else "Buenas noches"
            name = self.config.get("user_name", "señor")
            lines = [f"◈ {period.upper()}, {name.upper()}", "═" * 40]
            lines.append(f"  📅 {datetime.datetime.now().strftime('%A %d de %B, %Y')}")
            lines.append(f"  ⏰ {datetime.datetime.now().strftime('%H:%M')}")
            # Tasks
            todos = DataStore.load(TODOS_FILE, [])
            pending = [t for t in todos if not t.get("done")]
            if pending:
                lines.append(f"\n  📋 TAREAS PENDIENTES ({len(pending)}):")
                for t in pending[:5]:
                    lines.append(f"    ⬜ {t['text']}")
            # Habits
            habits = DataStore.load(HABITS_FILE, {})
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today_done = habits.get("log", {}).get(today, [])
            if habits.get("list"):
                lines.append(f"\n  🎯 HÁBITOS ({len(today_done)}/{len(habits['list'])}):")
                for h in habits["list"]:
                    done = "✅" if h in today_done else "⬜"
                    lines.append(f"    {done} {h}")
            # Battery
            if HAS_PSUTIL:
                bat = psutil.sensors_battery()
                if bat:
                    lines.append(f"\n  🔋 Batería: {bat.percent}%{'  🔌' if bat.power_plugged else ''}")
                lines.append(f"  💻 CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%")
            # Notes count
            notes = DataStore.load(NOTES_FILE, [])
            if notes:
                lines.append(f"  📝 {len(notes)} notas guardadas")
            # Pomodoro sessions
            if self.pomodoro.sessions > 0:
                lines.append(f"  🍅 {self.pomodoro.sessions} sesiones pomodoro hoy")
            self._print("\n".join(lines), "system")
            return

        # ══════════════════════════════════════════════
        # CAMERA / VISION (Gemini Vision API)
        # ══════════════════════════════════════════════

        if comando in ("camara", "camera", "cam", "foto", "photo"):
            self._camera_capture("Describe detalladamente lo que ves en esta imagen. Responde en español.")
            return

        if comando.startswith("camara ") or comando.startswith("camera "):
            prompt = re.sub(r'^(camara|camera)\s+', '', text, flags=re.IGNORECASE).strip()
            self._camera_capture(prompt)
            return

        if comando in ("leer", "leer texto", "ocr", "read"):
            self._camera_capture("Lee TODO el texto que aparece en esta imagen. Transcríbelo exactamente como está.")
            return

        if comando in ("resolver", "solve", "math cam", "resolver math"):
            self._camera_capture("Resuelve el problema matemático o ejercicio que aparece en esta imagen. Muestra el procedimiento completo paso a paso.")
            return

        if comando in ("codigo", "code cam", "analizar codigo"):
            self._camera_capture("Analiza el código de programación que aparece en la imagen. Explica qué hace, si tiene errores y cómo mejorarlo.")
            return

        if comando in ("traducir cam", "translate cam"):
            self._camera_capture("Traduce todo el texto que aparece en esta imagen al español. Si ya está en español, tradúcelo al inglés.")
            return

        if comando in ("que es esto", "what is this", "identificar"):
            self._camera_capture("¿Qué es este objeto/cosa que se ve en la imagen? Dame información detallada sobre ello.")
            return

        if not self.brain.ready:
            self._fallback_response(text)
            return

        glow = C.get("glow", C["accent"])
        self.status_lbl.config(text="  ◆ PROCESSING...", fg=glow)
        self.term_status.config(text="THINKING", fg=C["yellow"])
        self.root.update()
        if self.config.get("sound_fx"):
            SoundFX.beep_ready()

        # Show thinking indicator
        self._thinking = True
        self._animate_thinking()

        def process():
            context_parts = []
            notes = DataStore.load(NOTES_FILE, [])
            todos = DataStore.load(TODOS_FILE, [])
            if notes:
                context_parts.append(f"Notas: {json.dumps(notes[-10:], ensure_ascii=False)}")
            if todos:
                context_parts.append(f"Tareas: {json.dumps(todos[-10:], ensure_ascii=False)}")
            context = "\n".join(context_parts)

            model = self.config.get("model", "") or None
            response = self.brain.think(text, system_context=context, model=model)

            # ── Rate limit detection & auto-fallback ──
            if response.startswith("[RATE_LIMIT]"):
                error_msg = response[12:]  # Remove prefix
                self.root.after(0, lambda: self._handle_rate_limit(error_msg, text))
                return

            clean_text, action_results = self.executor.execute_all(response)

            def show():
                self._thinking = False
                if clean_text.strip():
                    self._print_jarvis(clean_text.strip())
                for r in action_results:
                    if r:
                        self._print_action(r)
                if clean_text.strip():
                    self.voice.speak(clean_text.strip())
                glow = self.theme.get("glow", self.theme["accent"])
                self.status_lbl.config(text="  ◆ READY", fg=glow)
                self.term_status.config(text="ONLINE", fg=self.theme["green"])
                if self.config.get("sound_fx"):
                    SoundFX.beep_done()
                if self.continuous_listen and not self.voice.is_listening:
                    self.root.after(2000, self._voice_input)

            self.root.after(0, show)

        threading.Thread(target=process, daemon=True).start()

    # ─── CAMERA CAPTURE ─────────────────────────────

    def _camera_capture(self, prompt):
        """Capture image from camera and send to Gemini Vision for analysis."""
        if not HAS_CV2:
            self._print("◈ ❌ Cámara no disponible. Instala: pip install opencv-python", "error")
            return

        self._print("◈ 📸 Abriendo cámara... (ESPACIO = capturar, ESC = cancelar)", "system")
        self.root.update()

        def capture_thread():
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.root.after(0, lambda: self._print("◈ ❌ No se pudo abrir la cámara.", "error"))
                    return

                captured_frame = None
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Add JARVIS overlay
                    display = frame.copy()
                    h, w = display.shape[:2]
                    cv2.rectangle(display, (0, 0), (w, 40), (0, 0, 0), -1)
                    cv2.putText(display, "J.A.R.V.I.S. VISION", (10, 28),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    cv2.putText(display, "SPACE: Capture | ESC: Cancel", (w - 350, 28),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 200), 1)

                    # Draw scanning lines
                    scan_y = int(time.time() * 100) % h
                    cv2.line(display, (0, scan_y), (w, scan_y), (0, 255, 255), 1)

                    cv2.imshow("JARVIS Vision", display)
                    key = cv2.waitKey(1) & 0xFF

                    if key == 27:  # ESC
                        break
                    elif key == 32:  # SPACE
                        captured_frame = frame
                        break

                cap.release()
                cv2.destroyAllWindows()

                if captured_frame is None:
                    self.root.after(0, lambda: self._print("◈ Captura cancelada.", "muted"))
                    return

                # Encode to base64
                _, buffer = cv2.imencode('.jpg', captured_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                import base64
                img_b64 = base64.b64encode(buffer).decode('utf-8')

                self.root.after(0, lambda: self._print("◈ 🔍 Analizando imagen con IA...", "system"))

                # Send to Gemini Vision
                response = self.brain.think_with_image(prompt, img_b64)

                def show_result():
                    self._print_jarvis(response)
                    self.voice.speak(response)

                self.root.after(0, show_result)

            except Exception as e:
                self.root.after(0, lambda: self._print(f"◈ ❌ Error cámara: {e}", "error"))

        threading.Thread(target=capture_thread, daemon=True).start()

    # ─── RATE LIMIT HANDLER ─────────────────────────

    def _handle_rate_limit(self, error_msg, original_text):
        """Handle rate limit by showing error and model switcher buttons."""
        self._thinking = False
        self._last_rate_limit_text = original_text
        C = self.theme
        glow = C.get("glow", C["accent"])
        self.status_lbl.config(text="  ◆ RATE LIMITED", fg=C["red"])
        self.term_status.config(text="LIMITED", fg=C["red"])
        SoundFX.beep_error()

        self._print(f"◈ ⚠️ TOKENS AGOTADOS\n{'═' * 40}\n  {error_msg[:200]}", "error")
        self._print("\n◈ Puedes cambiar a otro proveedor GRATIS:", "system")

        current_provider = self.config.get("provider", "")
        free_providers = [
            ("🟢 Gemini Flash", "gemini", "gemini-2.0-flash", "Tokens generosos"),
            ("🟢 OpenRouter", "openrouter", "google/gemini-2.0-flash-exp:free", "Modelos gratis ilimitados"),
            ("🟢 Cerebras", "cerebras", "llama-3.3-70b", "Ultra rápido, gratis"),
            ("🟢 Groq", "groq", "llama-3.3-70b-versatile", "100K tokens/día"),
        ]

        # Show each provider as a clickable button on its own line
        for label, provider, model, desc in free_providers:
            if provider == current_provider:
                continue
            try:
                btn = tk.Button(
                    self.output_text, text=f"  ▶ {label} — {desc}  ",
                    font=("Consolas", 11, "bold"),
                    bg=C["bg3"], fg=C["accent"], activebackground=C["accent"], activeforeground=C["bg"],
                    relief="flat", bd=1, padx=15, pady=6, cursor="hand2", anchor="w",
                    command=lambda p=provider, m=model, t=original_text: self._switch_provider_and_retry(p, m, t)
                )
                self.output_text.insert("end", "\n")
                self.output_text.window_create("end", window=btn)
            except Exception:
                pass

        # "All Models" button
        try:
            btn_all = tk.Button(
                self.output_text, text="  📋 Ver Todos los Modelos  ",
                font=("Consolas", 11, "bold"),
                bg=C["bg3"], fg=C["yellow"], activebackground=C["yellow"], activeforeground=C["bg"],
                relief="flat", bd=1, padx=15, pady=6, cursor="hand2",
                command=self._show_model_switcher
            )
            self.output_text.insert("end", "\n")
            self.output_text.window_create("end", window=btn_all)
        except Exception:
            pass

        # Also show text commands as fallback
        self.output_text.insert("end", "\n\n")
        self._print("  O escribe: cambiar a gemini / cambiar a openrouter / cambiar a cerebras", "muted")
        self._print("  Ver todos: modelos\n", "muted")
        self.output_text.see("end")

    def _switch_provider_and_retry(self, provider, model, original_text):
        """Switch to a different provider and retry the original message."""
        C = self.theme
        pinfo = PROVIDERS.get(provider, {})

        # Try provider-specific key first, then main key
        api_key = self.config.get(f"api_key_{provider}", "") or self.config.get("api_key", "")

        # Gemini can use main key if provider was gemini before
        if provider == "gemini":
            api_key = self.config.get("api_key_gemini", "") or self.config.get("api_key", "")

        # Provider needs a key and we don't have one
        if provider not in ("ollama",) and not api_key:
            key_url = pinfo.get("get_key_url", "")
            self._print(f"◈ Para usar {pinfo['name']}, necesitas una API key gratuita:", "system")
            self._print(f"  1. Ve a: {key_url}", "system")
            self._print(f"  2. Crea tu cuenta y copia la API key", "system")
            self._print(f"  3. Escribe: config api_{provider}: TU_KEY", "system")
            return

        self._print(f"◈ Cambiando a {pinfo.get('name', provider)}...", "muted")
        self.root.update()

        if self.brain.init_provider(provider, api_key):
            self.config["provider"] = provider
            self.config["model"] = model
            DataStore.save(CONFIG_FILE, self.config)
            self._print(f"◈ ✅ Ahora usando: {pinfo.get('name', provider)} ({model})", "system")
            self._print(f"◈ Reintentando tu mensaje...\n", "muted")
            # Retry the original message
            self.root.after(500, lambda: self._process_input(original_text))
        else:
            self._print(f"◈ ❌ No se pudo conectar a {provider}.", "error")

    def _show_model_switcher(self):
        """Show all available models from all providers."""
        C = self.theme
        lines = ["◈ MODELOS DISPONIBLES", "═" * 50]
        for prov_key, pinfo in PROVIDERS.items():
            cost_emoji = "🟢" if "GRATIS" in pinfo.get("cost", "") else "🔴"
            lines.append(f"\n  {cost_emoji} {pinfo['name']} ({pinfo['cost']})")
            lines.append(f"     Key URL: {pinfo.get('get_key_url', 'N/A')}")
            for m in pinfo.get("models", []):
                default = " ⭐" if m == pinfo.get("default_model") else ""
                lines.append(f"     • {m}{default}")
        lines.append(f"\n{'═' * 50}")
        lines.append("  Cambiar: config proveedor: NOMBRE")
        lines.append("  API Key: config api: TU_KEY")
        lines.append("  Modelo:  config modelo: NOMBRE")
        lines.append(f"  Key extra: config api_openrouter: KEY")
        self._print("\n".join(lines), "system")

    # ─── FALLBACK (sin IA) ──────────────────────────

    def _fallback_response(self, text):
        comando = text.lower()

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
            self._print_jarvis(self.executor._get_system_info())
            return

        if "cpu" in comando or "ram" in comando:
            self._print_jarvis(self.executor._get_cpu_info())
            return

        if "disco" in comando or "espacio" in comando:
            self._print_jarvis(self.executor._get_disk_info())
            return

        if "clima" in comando or "weather" in comando:
            city = comando.replace("clima", "").replace("weather", "").replace("en", "").replace("de", "").strip() or "Santiago Chile"
            self._print("◈ Consultando clima...", "muted")
            self.root.update()
            def get_w():
                r = self.executor._get_weather(city)
                self.root.after(0, lambda: self._print_jarvis(r))
            threading.Thread(target=get_w, daemon=True).start()
            return

        if "chrome" in comando:
            self.executor._open_program("chrome")
            self._print_jarvis("Abriendo Chrome.")
            return

        if "notepad" in comando or "bloc" in comando:
            self.executor._open_program("notepad")
            self._print_jarvis("Abriendo bloc de notas.")
            return

        if "edge" in comando:
            self.executor._open_program("edge")
            self._print_jarvis("Abriendo Microsoft Edge.")
            return

        # v6.0 offline commands
        if any(w in comando for w in ["calc ", "calcula ", "calculadora"]):
            expr = comando.replace("calc ", "").replace("calcula ", "").replace("calculadora ", "").strip()
            if expr:
                result = self._safe_calc(expr)
                self._print_jarvis(result)
            else:
                self._print_jarvis("Uso: calc EXPRESION (ej: calc 2+2)")
            return

        if "briefing" in comando:
            self._show_briefing()
            return

        if "procesos" in comando:
            self._show_processes()
            return

        if any(w in comando for w in ["chiste", "joke"]):
            chistes = [
                "¿Por qué los programadores prefieren el frío? Porque hay menos bugs.",
                "¿Cuántos programadores se necesitan para cambiar una bombilla? Ninguno, es un problema de hardware.",
                "Un QA entra a un bar. Pide 1 cerveza. Pide 999999 cervezas. Pide -1 cervezas. Pide 0 cervezas.",
            ]
            self._print_jarvis(f"◈ {random.choice(chistes)}")
            return

        if any(w in comando for w in ["frase", "quote", "motivacion"]):
            frases = [
                "El único modo de hacer un gran trabajo es amar lo que haces. — Steve Jobs",
                "La mejor forma de predecir el futuro es inventarlo. — Alan Kay",
                "El código es poesía. — Folklore dev",
            ]
            self._print_jarvis(f"◈ {random.choice(frases)}")
            return

        provider = self.config.get("provider", "gemini")
        pinfo = PROVIDERS.get(provider, PROVIDERS["gemini"])
        self._print_jarvis(
            f"◆ Neural link offline. Provider: {pinfo['name']}\n\n"
            "◈ SETUP RAPIDO (GRATIS):\n\n"
            "  1. Google Gemini:\n"
            "     config proveedor: gemini\n"
            "     config api: TU_KEY → https://aistudio.google.com/apikey\n\n"
            "  2. Groq (ultra rapido):\n"
            "     config proveedor: groq\n"
            "     config api: TU_KEY → https://console.groq.com/keys\n\n"
            "  3. Ollama (local):\n"
            "     config proveedor: ollama → https://ollama.com\n\n"
            "Sin IA disponible: hora, fecha, sistema, cpu, disco,\n"
            "  clima, calc, briefing, procesos, chiste, frase,\n"
            "  cronometro, timer, password, dado, moneda, help"
        )

    # ─── VOZ ─────────────────────────────────────────

    def _voice_input(self):
        if self.voice.is_listening:
            return
        if not HAS_SPEECH:
            self._print_jarvis("Mic no disponible. pip install SpeechRecognition pyaudio")
            return

        glow = self.theme.get("glow", self.theme["accent"])
        self.status_lbl.config(text="  ◆ LISTENING...", fg=self.theme["red"])
        self.term_status.config(text="LISTENING", fg=self.theme["red"])
        self._print("◉ Escuchando...", "info")
        self.root.update()

        def on_heard(text):
            self.root.after(0, lambda: self._process_input(text))

        def on_error(msg):
            def show():
                self._print(f"  {msg}", "muted")
                glow2 = self.theme.get("glow", self.theme["accent"])
                self.status_lbl.config(text="  ◆ READY", fg=glow2)
                self.term_status.config(text="ONLINE", fg=self.theme["green"])
                if self.continuous_listen:
                    self.root.after(1000, self._voice_input)
                elif self.wake_word_mode:
                    self.root.after(500, self._wake_word_listen)
            self.root.after(0, show)

        self.voice.listen(on_heard, on_error, timeout=8, phrase_limit=20)

    def _toggle_continuous_listen(self):
        self.continuous_listen = not self.continuous_listen
        if self.continuous_listen:
            self.wake_word_mode = False
            self._print_jarvis("Modo voz activado. Escuchando todo.")
            self.voice.speak("Modo voz activado.")
            self._voice_input()
        else:
            self._print_jarvis("Modo voz desactivado.")

    def _toggle_wake_word(self):
        """Activar/desactivar wake word 'Jarvis'."""
        self.wake_word_mode = not self.wake_word_mode
        self.config["wake_word"] = self.wake_word_mode
        DataStore.save(CONFIG_FILE, self.config)
        if self.wake_word_mode:
            self.continuous_listen = False
            self._print_jarvis("Wake word activado. Di 'Jarvis' para activarme.")
            self.voice.speak("Wake word activado. Diga Jarvis cuando me necesite.")
            self._wake_word_listen()
        else:
            self._print_jarvis("Wake word desactivado.")

    def _wake_word_listen(self):
        """Escucha pasiva por wake word."""
        if not self.wake_word_mode or self.voice.is_listening:
            return

        def on_wake(remaining_text):
            def _handle():
                SoundFX.beep_listen()
                if remaining_text:
                    # Wake word + comando en la misma frase
                    self._process_input(remaining_text)
                else:
                    # Solo dijo "Jarvis", escuchar el comando
                    self._print_jarvis("Dígame, señor.")
                    self.voice.speak("Dígame.")
                    self.root.after(500, self._voice_input_then_wake)
            self.root.after(0, _handle)

        def on_done():
            # No detectó wake word, seguir escuchando
            if self.wake_word_mode:
                self.root.after(300, self._wake_word_listen)

        self.voice.listen_for_wake_word(on_wake)
        # Re-trigger after listening ends
        self.root.after(12000, lambda: self._wake_word_listen() if self.wake_word_mode and not self.voice.is_listening else None)

    def _voice_input_then_wake(self):
        """Escuchar un comando y luego volver a wake word."""
        if self.voice.is_listening:
            return

        def on_heard(text):
            def _h():
                self._process_input(text)
                # Volver a escuchar wake word después
                self.root.after(3000, self._wake_word_listen)
            self.root.after(0, _h)

        def on_error(msg):
            def _e():
                self._print(f"  {msg}", "muted")
                if self.wake_word_mode:
                    self.root.after(1000, self._wake_word_listen)
            self.root.after(0, _e)

        self.voice.listen(on_heard, on_error, timeout=8, phrase_limit=20)

    def _toggle_voice(self):
        enabled = self.voice.toggle_voice()
        self.config["voice_enabled"] = enabled
        DataStore.save(CONFIG_FILE, self.config)
        self._print_jarvis("Voz activada." if enabled else "Voz silenciada.")
        if enabled:
            self.voice.speak("Voz activada.")

    # ─── POMODORO ────────────────────────────────────

    def _pomodoro_toggle(self):
        if self.pomodoro.running:
            self._print_jarvis(self.pomodoro.stop())
        else:
            self._print_jarvis(self.pomodoro.start())
            self.voice.speak("Pomodoro iniciado. 25 minutos de trabajo.")

    def _on_pomodoro(self, event, message):
        def show():
            self._print(f"\n🍅 {message}\n", "info")
            self.voice.speak(message)
            SoundFX.beep_alert()
        self.root.after(0, show)

    # ─── RECORDATORIOS / SCHEDULER ───────────────────

    def _on_reminder(self, text):
        def show():
            self._print(f"\n🔔 ¡RECORDATORIO! → {text}\n", "info")
            self.voice.speak(f"Señor, le recuerdo: {text}")
            SoundFX.beep_alert()
            try:
                messagebox.showinfo("⏰ Recordatorio", text)
            except Exception:
                pass
        self.root.after(0, show)

    def _on_scheduled_task(self, task):
        def show():
            self._print(f"\n📅 TAREA PROGRAMADA → {task['description']}\n", "info")
            self.voice.speak(f"Señor, tarea programada: {task['description']}")
            SoundFX.beep_alert()
            if task.get("command"):
                self._process_input(task["command"])
        self.root.after(0, show)

    def _show_schedule(self):
        self._print(self.scheduler.list_tasks(), "system")

    # ─── TEMAS ───────────────────────────────────────

    def _cycle_theme(self):
        keys = list(THEMES.keys())
        current = self.config.get("theme", "jarvis")
        idx = keys.index(current) if current in keys else 0
        next_key = keys[(idx + 1) % len(keys)]
        self._apply_theme(next_key)

    def _apply_theme(self, theme_key):
        """Aplicar tema EN VIVO sin reiniciar."""
        if theme_key not in THEMES:
            self._print_jarvis(f"Tema no encontrado. Opciones: {', '.join(THEMES.keys())}")
            return
        self.config["theme"] = theme_key
        self.theme = THEMES[theme_key]
        C = self.theme
        glow = C.get("glow", C["accent"])
        DataStore.save(CONFIG_FILE, self.config)

        # Root
        self.root.configure(bg=C["bg"])

        # HUD bar
        self.hud_bar.configure(bg=C["bg"])
        for w in self.hud_bar.winfo_children():
            try:
                w.configure(bg=C["bg"])
                for child in w.winfo_children():
                    child.configure(bg=C["bg"])
            except tk.TclError:
                pass
        self.hud_clock.config(fg=glow, bg=C["bg"])
        self.hud_date.config(fg=C["text2"], bg=C["bg"])
        self.hud_cpu.config(fg=C["green"], bg=C["bg"])
        self.hud_ram.config(fg=C["yellow"], bg=C["bg"])
        self.hud_provider.config(fg=C["accent"], bg=C["bg"])

        # Sidebar
        self.sidebar.configure(bg=C["bg2"])
        for widget in self.sidebar.winfo_children():
            try:
                if isinstance(widget, tk.Button):
                    widget.configure(bg=C["bg2"], fg=C["text2"],
                                     activebackground=glow, activeforeground="black")
                    widget.bind("<Enter>", lambda e, b=widget, g=glow: b.config(fg=g))
                    widget.bind("<Leave>", lambda e, b=widget, c=C: b.config(fg=c["text2"]))
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=C["bg2"])
                elif isinstance(widget, tk.Canvas):
                    widget.configure(bg=C["bg2"])
            except tk.TclError:
                pass
        self.cpu_val_lbl.config(fg=glow, bg=C["bg2"])
        self.ram_val_lbl.config(fg=C["yellow"], bg=C["bg2"])
        self.pomodoro_lbl.config(fg=C["orange"], bg=C["bg2"])
        self.voice_status.config(fg=C["accent"], bg=C["bg2"])

        # Right panel
        self.right_panel.configure(bg=C["bg2"])
        for widget in self.right_panel.winfo_children():
            try:
                if isinstance(widget, tk.Button):
                    widget.configure(bg=C["bg2"], fg=C["text2"],
                                     activebackground=glow, activeforeground="black")
                    widget.bind("<Enter>", lambda e, b=widget, g=glow: b.config(fg=g))
                    widget.bind("<Leave>", lambda e, b=widget, c=C: b.config(fg=c["text2"]))
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=C["bg2"])
                elif isinstance(widget, tk.Canvas):
                    widget.configure(bg=C["bg2"])
            except tk.TclError:
                pass

        # Output
        self.output.config(bg="#000000", fg=C["text"], insertbackground=glow,
                           selectbackground=glow)
        self.output.tag_configure("jarvis", foreground=glow)
        self.output.tag_configure("user", foreground=C["green"])
        self.output.tag_configure("error", foreground=C["red"])
        self.output.tag_configure("info", foreground=C["yellow"])
        self.output.tag_configure("muted", foreground=C["muted"])
        self.output.tag_configure("system", foreground=C["purple"])
        self.output.tag_configure("action", foreground=C["orange"])
        self.output.tag_configure("hud", foreground=glow)

        # Input
        self.entry.config(bg=C["bg3"], fg=C["text"], insertbackground=glow)
        self.mic_btn.config(bg=C["bg3"], fg=glow)
        self.status_lbl.config(bg=C["bg3"], fg=glow)

        # Bottom bar
        self.bottom_bar.configure(bg=C["bg3"])
        self.uptime_lbl.config(bg=C["bg3"], fg=C["text2"])

        self._print_jarvis(f"◆ Tema aplicado: {THEMES[theme_key]['name']}")

    # ─── CLIPBOARD HISTORY ───────────────────────────

    def _show_clipboard_history(self):
        history = DataStore.load(CLIPBOARD_FILE, [])
        if not history:
            self._print_jarvis("El historial del portapapeles está vacío.")
            return
        lines = ["◈ CLIPBOARD HISTORY:", "═" * 35]
        for i, item in enumerate(history[-10:], 1):
            text = item["text"][:80]
            date = item.get("date", "")[:16]
            lines.append(f"  {i}. [{date}] {text}")
        self._print("\n".join(lines), "system")

    # ─── EXPORTAR ────────────────────────────────────

    def _export_conversation(self):
        """Exportar conversación a archivo de texto."""
        try:
            content = self.output.get("1.0", "end")
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(os.path.expanduser("~"), "Desktop", f"jarvis_chat_{ts}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"=== J.A.R.V.I.S. GOD MODE - Conversación ===\n")
                f.write(f"=== Exportado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')} ===\n\n")
                f.write(content)
            self._print_jarvis(f"Conversación exportada a: {path}")
        except Exception as e:
            self._print_jarvis(f"Error exportando: {e}")

    # ─── CONFIG ──────────────────────────────────────

    def _show_config(self):
        C = self.theme
        provider = self.config.get("provider", "gemini")
        pinfo = PROVIDERS.get(provider, {})
        api = self.config.get("api_key", "")
        masked = f"...{api[-6:]}" if len(api) > 10 else ("(no necesaria)" if provider == "ollama" else "(no configurada)")
        model = self.config.get("model", "") or pinfo.get("default_model", "auto")
        voice = "ON" if self.config.get("voice_enabled") else "OFF"
        brain = "ONLINE" if self.brain.ready else "OFFLINE"
        theme_name = THEMES.get(self.config.get("theme", "jarvis"), {}).get("name", "?")
        tts = "Edge TTS" if HAS_EDGE_TTS else "pyttsx3" if HAS_PYTTSX3 else "None"
        voice_name = self.config.get("edge_voice", DEFAULT_EDGE_VOICE)

        self._print(f"""
 ╔══════════════════════════════════════════════╗
 ║  ◆ J.A.R.V.I.S. CONFIG — v{VERSION}             ║
 ╠══════════════════════════════════════════════╣
 ║  Provider:   {pinfo.get('name', provider):>20} ({pinfo.get('cost', '?')})
 ║  Status:     {brain:>20}
 ║  API Key:    {masked:>20}
 ║  Model:      {model:>20}
 ║  TTS Engine: {tts:>20}
 ║  Voice:      {voice_name:>20}
 ║  Response:   {voice:>20}
 ║  Theme:      {theme_name:>20}
 ║  Typewriter: {"ON" if self.config.get("typewriter") else "OFF":>20}
 ║  Wake Word:  {"ON" if self.config.get("wake_word") else "OFF":>20}
 ║  Data Dir:   ~/.jarvis_god/
 ╠══════════════════════════════════════════════╣
 ║  COMMANDS:                                   ║
 ║  config proveedor: gemini/groq/ollama/openai ║
 ║  config api: TU_API_KEY                      ║
 ║  config modelo: nombre_modelo                ║
 ║  config nombre: tu_nombre                    ║
 ║  config voz: {", ".join(list(EDGE_VOICES.keys())[:4])}
 ║  config tema: {", ".join(list(THEMES.keys())[:6])}
 ╚══════════════════════════════════════════════╝
""", "system")

    def _show_providers(self):
        lines = ["\n◈ AI PROVIDERS", "═" * 40]
        current = self.config.get("provider", "gemini")
        for key, p in PROVIDERS.items():
            marker = " ◀ ACTIVE" if key == current else ""
            lines.append(f"\n  {p['name']} [{key}] - {p['cost']}{marker}")
            lines.append(f"    Models: {', '.join(p['models'])}")
            if key == "ollama":
                lines.append(f"    Setup: {p['get_key_url']}")
            else:
                lines.append(f"    API Key: {p['get_key_url']}")
        lines.append("\n" + "═" * 40)
        self._print("\n".join(lines), "system")

    def _reset_ai(self):
        self.brain.clear_memory()
        self._print_jarvis("Memoria reiniciada. Empezamos de cero.")
        self.voice.speak("Memoria reiniciada.")

    # ─── STARTUP CINEMATOGRÁFICO ─────────────────────

    def _animated_startup(self):
        C = self.theme
        glow = C.get("glow", C["accent"])
        SoundFX.beep_startup()

        # Boot sequence lines
        boot_lines = [
            "[CORE] Initializing quantum neural processing units...",
            "[CORE] Loading AI inference engine v6.4...",
            "[VOICE] Calibrating Edge TTS speech synthesis...",
            "[NET] Establishing secure AI provider link...",
            "[SYS] Scanning hardware: CPU, RAM, GPU, Storage...",
            "[SEC] Activating encryption & security protocols...",
            "[AI] Running neural network self-diagnostics...",
            "[VFX] Enabling EDEX-UI visual effects engine...",
            "[HEX] Loading holographic grid overlay...",
            "[WEB] Connecting YouTube, Google, Wikipedia APIs...",
            "[WX] Initializing Open-Meteo weather service...",
            "[FIN] Loading crypto, currency & finance modules...",
            "[HAB] Initializing habit tracker & flashcard engine...",
            "[NET] Port scanner & speed test ready...",
            "[CAM] Initializing computer vision module...",
            "[AI] Multi-provider fallback system ready...",
            "[RDY] All subsystems nominal. Awaiting commands...",
        ]

        # EDEX-UI style banner
        self._print(f"""
 ╔══════════════════════════════════════════════════════╗
 ║                                                      ║
 ║     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗         ║
 ║     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝         ║
 ║     ██║███████║██████╔╝██║   ██║██║███████╗         ║
 ║██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║         ║
 ║╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║         ║
 ║ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝         ║
 ║              GOD MODE v{VERSION}                        ║
 ║      Just A Rather Very Intelligent System           ║
 ╚══════════════════════════════════════════════════════╝
""", "hud")

        # Animated boot sequence with progress bar
        total = len(boot_lines)

        def show_boot_line(idx):
            if idx < total:
                self._print(f"  ▸ {boot_lines[idx]}", "muted")
                # Progress bar
                filled = int((idx + 1) / total * 30)
                bar = "█" * filled + "░" * (30 - filled)
                pct = int((idx + 1) / total * 100)
                self._print(f"  [{bar}] {pct}%", "action")
                self.root.after(150, lambda: show_boot_line(idx + 1))
            else:
                self._print("  [██████████████████████████████] 100%\n", "info")
                self.root.after(200, self._show_greeting)

        show_boot_line(0)

    def _show_greeting(self):
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

        self._print("  ▸ All systems: ONLINE ◆\n", "info")

        greeting = f"{period}, {name}. Todos los sistemas operativos."
        self._print_jarvis(f"◆ {greeting}")

        # AI Status
        if self.brain.ready:
            model = self.config.get("model", "") or pinfo.get("default_model", "")
            self._print(f"  ◈ AI: {pinfo.get('name', provider)} → {model}", "muted")
        else:
            if provider == "ollama":
                self._print("  ◈ Ollama no conectado. Asegúrate de tenerlo corriendo.", "muted")
            elif not self.config.get("api_key"):
                self._print(f"  ◈ Sin API key. Configura: config api: TU_KEY", "muted")
                self._print(f"  ◈ Gratis: {pinfo.get('get_key_url', '')}", "muted")

        tts_engine = "Edge TTS" if HAS_EDGE_TTS else "pyttsx3" if HAS_PYTTSX3 else "Sin voz"
        self._print(f"  ◈ Voice: {tts_engine}", "muted")

        # Deps
        missing = []
        if not HAS_EDGE_TTS:
            missing.append("edge-tts")
        if not HAS_PYTTSX3:
            missing.append("pyttsx3")
        if not HAS_SPEECH:
            missing.append("SpeechRecognition pyaudio")
        if not HAS_PSUTIL:
            missing.append("psutil")
        if missing:
            self._print(f"  ◈ Install: pip install {' '.join(missing)}", "muted")

        self._print("", "muted")
        self.status_lbl.config(text=f"  ◆ {greeting}")

        self.voice.speak(greeting)

        # Activar wake word si estaba configurado
        if self.wake_word_mode:
            self.root.after(2000, self._wake_word_listen)

    # ─── HELP ────────────────────────────────────────

    def _show_help(self):
        self._print(f"""
 ╔══════════════════════════════════════════════════╗
 ║  ◆ J.A.R.V.I.S. COMMAND REFERENCE v{VERSION}        ║
 ╠══════════════════════════════════════════════════╣
 ║  AI CHAT (natural language):                     ║
 ║    "abre chrome"  "busca X"  "clima de NY"       ║
 ║    "recuerdame X en 5 minutos"                   ║
 ╠══════════════════════════════════════════════════╣
 ║  CAMERA / VISION (Gemini Vision):                ║
 ║    camara             — describe what it sees    ║
 ║    camara [prompt]    — analyze with custom ask  ║
 ║    leer / ocr         — read text from image     ║
 ║    resolver           — solve math from photo    ║
 ║    codigo             — analyze code from photo  ║
 ║    traducir cam       — translate visible text   ║
 ║    que es esto        — identify objects         ║
 ╠══════════════════════════════════════════════════╣
 ║  LOCAL COMMANDS (no API cost):                   ║
 ║    notas / tareas     — view saved items         ║
 ║    tarea done 1       — mark task complete       ║
 ║    uptime             — session time             ║
 ║    pomodoro [min]     — productivity timer       ║
 ║    estudiar [min]     — study mode (45/10)       ║
 ║    schedule ver       — scheduled tasks          ║
 ║    clipboard          — clipboard history        ║
 ║    exportar           — save chat to file        ║
 ║    proveedores        — view AI providers        ║
 ║    modelos            — see all AI models        ║
 ║    limpiar / cls      — clear screen             ║
 ╠══════════════════════════════════════════════════╣
 ║  TOOLS & UTILITIES:                              ║
 ║    cronometro         — start/stop/reset         ║
 ║    timer N            — countdown N minutes      ║
 ║    calc EXPR          — calculator (sin,cos,pi)  ║
 ║    convertir X a Y    — unit converter           ║
 ║    dias hasta DD/MM   — date calculator          ║
 ║    clima CITY         — weather (Open-Meteo)     ║
 ║    briefing           — daily briefing report    ║
 ║    procesos           — top system processes     ║
 ║    password N         — generate strong password ║
 ║    base64 TEXT        — encode/decode base64     ║
 ║    hash TEXT          — MD5/SHA1/SHA256           ║
 ║    mayusculas TEXT    — text tools                ║
 ║    chiste / frase     — jokes & quotes           ║
 ║    dado [N] / moneda  — dice & coin              ║
 ║    typing             — speed typing test        ║
 ║    contar TEXT        — word counter              ║
 ║    ip                 — show public IP            ║
 ╠══════════════════════════════════════════════════╣
 ║  YOUTUBE & WEB (directo, sin IA):                ║
 ║    yt QUERY           — open first YouTube video ║
 ║    youtube QUERY      — same as yt               ║
 ║    google QUERY       — Google search            ║
 ╠══════════════════════════════════════════════════╣
 ║  IRON MAN / SYSTEM POWER:                         ║
 ║    bateria            — battery status & time    ║
 ║    volumen N / mute   — volume control           ║
 ║    brillo N           — screen brightness        ║
 ║    cleanup            — clean temp files         ║
 ║    speedtest          — internet speed test      ║
 ║    red / wifi         — network info             ║
 ║    wifi pass          — show WiFi passwords      ║
 ║    scan [IP]          — port scanner             ║
 ║    uptime os          — system uptime            ║
 ╠══════════════════════════════════════════════════╣
 ║  FINANCE & DATA:                                 ║
 ║    cambio 100 USD a CLP — currency converter     ║
 ║    crypto / bitcoin   — crypto prices live       ║
 ║    descargar URL      — download file            ║
 ╠══════════════════════════════════════════════════╣
 ║  PRODUCTIVITY:                                   ║
 ║    habitos            — view habits & streaks    ║
 ║    habito add NAME    — add a new habit          ║
 ║    habito done NAME   — mark habit done today    ║
 ║    flashcards / flash — study flashcards         ║
 ║    flash add Q | A    — create flashcard         ║
 ║    flash list         — view all flashcards      ║
 ║    alarma HH:MM       — set alarm with sound     ║
 ║    mi dia / daily     — full day summary         ║
 ╠══════════════════════════════════════════════════╣
 ║  DEV TOOLS:                                      ║
 ║    json: {...}        — format/validate JSON     ║
 ║    lorem              — lorem ipsum generator    ║
 ║    color #HEX / rgb   — color converter          ║
 ║    uuid               — generate UUID            ║
 ║    random number 1 100 — random generators       ║
 ║    regex: PAT | TEXT  — regex tester             ║
 ╠══════════════════════════════════════════════════╣
 ║  UNIVERSITY & QUICK ACCESS:                      ║
 ║    wiki TOPIC         — Wikipedia summary        ║
 ║    hora en CITY       — world clock              ║
 ║    docs / sheets      — Google Docs/Sheets       ║
 ║    slides / drive     — Slides/Drive             ║
 ║    classroom          — Google Classroom          ║
 ║    gmail / calendar   — Gmail/Calendar           ║
 ║    github / canva     — GitHub/Canva             ║
 ║    notion / trello    — Notion/Trello            ║
 ║    chatgpt            — Open ChatGPT             ║
 ║    buscar FILE        — search files on disk     ║
 ║    abrir PROGRAM      — open any program         ║
 ╠══════════════════════════════════════════════════╣
 ║  CONFIGURATION:                                  ║
 ║    config proveedor: gemini/groq/openrouter/...  ║
 ║    config api: YOUR_KEY                          ║
 ║    config api_openrouter: KEY                    ║
 ║    config api_cerebras: KEY                      ║
 ║    config modelo: model_name                     ║
 ║    config nombre: your_name                      ║
 ║    config voz: jorge/dalia/elena/alvaro          ║
 ║    config tema: {"/".join(list(THEMES.keys())[:5])}
 ║    typewriter         — toggle typing effect     ║
 ╠══════════════════════════════════════════════════╣
 ║  SHORTCUTS:                                      ║
 ║    Enter   — send     |  Up/Down — history       ║
 ║    Ctrl+L  — clear    |  Ctrl+E  — export        ║
 ║    Escape  — focus    |                          ║
 ╠══════════════════════════════════════════════════╣
 ║  SIDEBAR:                                        ║
 ║    VOZ     — continuous listening mode            ║
 ║    WAKE    — say "Jarvis" to activate            ║
 ║    MUTE    — toggle voice responses              ║
 ╚══════════════════════════════════════════════════╝
""", "system")

    # ─── CERRAR ──────────────────────────────────────

    def _on_close(self):
        self.reminder_system.stop()
        self.scheduler.stop()
        self.monitor.stop()
        self.pomodoro.stop()
        self.voice.stop_speaking()
        DataStore.save(CONFIG_FILE, self.config)
        DataStore.save(HISTORY_FILE, list(self.command_history))
        self.root.destroy()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGodMode(root)
    root.mainloop()
