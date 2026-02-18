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
║   ✦ Clima en tiempo real (wttr.in, gratis)                           ║
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
}

# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN Y CONSTANTES
# ══════════════════════════════════════════════════════════════

APP_NAME = "J.A.R.V.I.S. GOD MODE"
VERSION = "4.2.0"
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
   (chrome, firefox, edge, notepad, calc, explorer, cmd, powershell, code, paint, word, excel, teams, discord, spotify, steam, taskmgr, settings)
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

REGLAS:
- Puedes usar MÚLTIPLES comandos en una respuesta.
- Siempre incluye texto además del comando.
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
            "chrome": "start chrome", "firefox": "start firefox",
            "edge": "start msedge", "brave": "start brave",
            "notepad": "start notepad", "bloc": "start notepad",
            "calc": "start calc", "calculadora": "start calc",
            "explorer": "start explorer", "explorador": "start explorer",
            "cmd": "start cmd", "terminal": "start wt",
            "powershell": "start powershell", "paint": "start mspaint",
            "word": "start winword", "excel": "start excel",
            "powerpoint": "start powerpnt", "outlook": "start outlook",
            "teams": "start msteams:", "code": "start code",
            "vscode": "start code", "spotify": "start spotify:",
            "discord": "start discord:", "steam": "start steam:",
            "taskmgr": "start taskmgr", "settings": "start ms-settings:",
            "configuracion": "start ms-settings:", "control": "start control",
            "snipping": "start snippingtool", "photos": "start ms-photos:",
            "maps": "start bingmaps:", "clock": "start ms-clock:",
            "store": "start ms-windows-store:", "mail": "start outlookmail:",
        }
        key = name.lower().strip()
        cmd = programs.get(key)
        if cmd:
            os.system(cmd)
            return f"Abriendo {name}."
        os.system(f"start {key}")
        return f"Intentando abrir {name}."

    # ─── Web ─────────────────────────────────────────

    def _open_web(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return None

    def _search_google(self, query):
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return None

    def _search_youtube(self, query):
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
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
        return "💻 " + " | ".join(lines)

    def _get_cpu_info(self):
        if not HAS_PSUTIL:
            return f"CPU: {platform.processor()} ({os.cpu_count()} núcleos)"
        cpu_pct = psutil.cpu_percent(interval=1, percpu=True)
        ram = psutil.virtual_memory()
        avg = sum(cpu_pct) / len(cpu_pct)
        return (
            f"🧠 CPU: {self._bar(avg)} {avg:.0f}% (núcleos: {', '.join(f'{p:.0f}%' for p in cpu_pct)})\n"
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
        plug = "🔌 Conectado" if bat.power_plugged else "🔋 Batería"
        return f"{self._bar(bat.percent)} {bat.percent}% ({plug})"

    # ─── CLIMA (wttr.in - GRATIS) ────────────────────

    def _get_weather(self, city):
        """Obtener clima de cualquier ciudad (gratis, sin API key)."""
        try:
            city_encoded = urllib.parse.quote(city.strip())
            url = f"https://wttr.in/{city_encoded}?format=%l:+%c+%t+%h+%w+%p&lang=es"
            req = urllib.request.Request(url, headers={"User-Agent": "Jarvis/4.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                weather = resp.read().decode("utf-8").strip()

            # También obtener pronóstico corto
            url2 = f"https://wttr.in/{city_encoded}?format=%l:+%c+%t+|+Sensación:+%f+|+Humedad:+%h+|+Viento:+%w&lang=es"
            req2 = urllib.request.Request(url2, headers={"User-Agent": "Jarvis/4.0"})
            with urllib.request.urlopen(req2, timeout=10) as resp2:
                detailed = resp2.read().decode("utf-8").strip()

            return f"🌤️ {detailed}"
        except Exception as e:
            return f"🌤️ No pude obtener el clima: {e}"

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
                result = "📰 NOTICIAS:\n"
                for i, h in enumerate(headlines, 1):
                    result += f"  {i}. {h}\n"
                return result
            return "📰 No pude obtener noticias."
        except Exception as e:
            return f"📰 Error: {e}"

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
            return "📅 No hay tareas programadas."
        lines = ["📅 TAREAS PROGRAMADAS:", "═" * 35]
        for i, t in enumerate(self.tasks):
            days_str = ", ".join(dias[d] for d in t.get("days", []))
            status = "✅" if t.get("enabled") else "❌"
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
        return f"🍅 Pomodoro #{self.sessions} iniciado: {work} min de trabajo."

    def stop(self):
        self.running = False
        self.phase = "idle"
        return "🍅 Pomodoro detenido."

    def status(self):
        if not self.running:
            return f"🍅 Pomodoro inactivo. Sesiones completadas hoy: {self.sessions}"
        mins = self.remaining // 60
        secs = self.remaining % 60
        phase_name = "TRABAJO" if self.phase == "work" else "DESCANSO"
        return f"🍅 {phase_name}: {mins:02d}:{secs:02d} restantes (sesión #{self.sessions})"

    def _loop(self):
        while self.running and self.remaining > 0:
            time.sleep(1)
            self.remaining -= 1

        if not self.running:
            return

        if self.phase == "work":
            self.phase = "break"
            self.remaining = self.break_minutes * 60
            self.callback("pomodoro_break", f"🍅 ¡Tiempo! Descanso de {self.break_minutes} min.")
            self._loop()  # Continue with break
        elif self.phase == "break":
            self.phase = "idle"
            self.running = False
            self.callback("pomodoro_done", f"🍅 Pomodoro #{self.sessions} completado. ¡Buen trabajo!")


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
        self.root.geometry("1050x750")
        self.root.minsize(900, 650)

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
        self.root.grid_rowconfigure(0, weight=1)

        # === SIDEBAR ===
        self.sidebar = tk.Frame(self.root, bg=C["bg2"], width=210)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        # Logo
        tk.Label(self.sidebar, text="⚡", font=("Segoe UI", 38),
                 bg=C["bg2"], fg=C["accent"]).pack(pady=(15, 0))
        tk.Label(self.sidebar, text="J.A.R.V.I.S.", font=("Consolas", 14, "bold"),
                 bg=C["bg2"], fg=C["accent"]).pack()
        tk.Label(self.sidebar, text="GOD MODE", font=("Consolas", 7, "bold"),
                 bg=C["bg2"], fg=C["red"]).pack()

        # Reloj
        self.clock_lbl = tk.Label(self.sidebar, font=("Consolas", 22, "bold"),
                                  bg=C["bg2"], fg=C["green"])
        self.clock_lbl.pack(pady=(10, 0))
        self.date_lbl = tk.Label(self.sidebar, font=("Consolas", 9),
                                 bg=C["bg2"], fg=C["text2"])
        self.date_lbl.pack()

        # Monitor CPU/RAM
        self.monitor_lbl = tk.Label(self.sidebar, font=("Consolas", 8),
                                    bg=C["bg2"], fg=C["yellow"], text="")
        self.monitor_lbl.pack(pady=(5, 0))

        # Pomodoro status
        self.pomodoro_lbl = tk.Label(self.sidebar, font=("Consolas", 8),
                                     bg=C["bg2"], fg=C["orange"], text="")
        self.pomodoro_lbl.pack()

        # Estado de voz
        self.voice_status = tk.Label(self.sidebar, text="", font=("Consolas", 9),
                                     bg=C["bg2"], fg=C["accent"])
        self.voice_status.pack(pady=(5, 0))

        # Separador
        tk.Frame(self.sidebar, bg=C["muted"], height=1).pack(fill="x", padx=15, pady=5)

        # Botones
        btns = [
            ("🎤 Modo Voz", self._toggle_continuous_listen),
            ("👂 Wake Word", self._toggle_wake_word),
            ("🔇 Silenciar", self._toggle_voice),
            ("💻 Sistema", lambda: self._quick_cmd("info del sistema")),
            ("🧠 CPU/RAM", lambda: self._quick_cmd("cpu y ram")),
            ("🌤️ Clima", lambda: self._quick_cmd("clima de mi ciudad")),
            ("📰 Noticias", lambda: self._quick_cmd("noticias de hoy")),
            ("🍅 Pomodoro", self._pomodoro_toggle),
            ("📝 Notas", lambda: self._quick_cmd("mis notas")),
            ("✅ Tareas", lambda: self._quick_cmd("mis tareas")),
            ("🔐 Password", lambda: self._quick_cmd("contraseña de 20")),
            ("📅 Schedule", self._show_schedule),
            ("🧹 Limpiar", self._clear_output),
            ("🧠 Reset IA", self._reset_ai),
            ("🎨 Tema", self._cycle_theme),
            ("⚙️ Config", self._show_config),
        ]

        for text, cmd in btns:
            b = tk.Button(self.sidebar, text=text, font=("Segoe UI", 8),
                          bg=C["bg3"], fg=C["text"], bd=0, padx=6, pady=2,
                          anchor="w", cursor="hand2", command=cmd,
                          activebackground=C["accent"], activeforeground="black")
            b.pack(fill="x", padx=8, pady=1)
            b.bind("<Enter>", lambda e, b=b, c=C: b.config(bg=c["border"]))
            b.bind("<Leave>", lambda e, b=b, c=C: b.config(bg=c["bg3"]))

        # Footer
        tk.Label(self.sidebar, text=f"v{VERSION}",
                 font=("Consolas", 7), bg=C["bg2"], fg=C["muted"]).pack(side="bottom", pady=(0, 5))

        # Deps
        deps = []
        deps.append("✅ Edge" if HAS_EDGE_TTS else "❌ Edge")
        deps.append("✅ Voz" if HAS_PYTTSX3 else "❌ Voz")
        deps.append("✅ Mic" if HAS_SPEECH else "❌ Mic")
        deps.append("✅ Sys" if HAS_PSUTIL else "❌ Sys")
        tk.Label(self.sidebar, text=" ".join(deps),
                 font=("Consolas", 6), bg=C["bg2"], fg=C["muted"]).pack(side="bottom")

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

        self.status_lbl = tk.Label(
            input_frame, text="💡 Di 'Jarvis' o escribe tu comando.",
            font=("Segoe UI", 8), bg=C["bg"], fg=C["muted"], anchor="w"
        )
        self.status_lbl.grid(row=1, column=0, columnspan=3, sticky="w", pady=(3, 0))

        # Bindings
        self.entry.bind("<Return>", lambda e: self._send())
        self.entry.bind("<Up>", lambda e: self._hist(-1))
        self.entry.bind("<Down>", lambda e: self._hist(1))
        self.root.bind("<Escape>", lambda e: self.entry.focus_set())
        self.root.bind("<Control-l>", lambda e: self._clear_output())
        self.root.bind("<Control-e>", lambda e: self._export_conversation())

        # Clock & Monitor loop
        self._tick()

    # ─── RELOJ + MONITOR ─────────────────────────────

    def _tick(self):
        C = self.theme
        now = datetime.datetime.now()
        self.clock_lbl.config(text=now.strftime("%H:%M:%S"))
        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        self.date_lbl.config(text=f"{dias[now.weekday()]} {now.day}/{now.month:02d}/{now.year}")

        # Monitor CPU/RAM
        if HAS_PSUTIL:
            self.monitor_lbl.config(
                text=f"CPU: {self.monitor.cpu:.0f}% | RAM: {self.monitor.ram:.0f}%"
            )

        # Pomodoro
        if self.pomodoro.running:
            mins = self.pomodoro.remaining // 60
            secs = self.pomodoro.remaining % 60
            phase = "🔴 TRABAJO" if self.pomodoro.phase == "work" else "🟢 DESCANSO"
            self.pomodoro_lbl.config(text=f"🍅 {phase} {mins:02d}:{secs:02d}")
        else:
            self.pomodoro_lbl.config(text="")

        # Voice status
        if self.voice.is_listening:
            self.voice_status.config(text="🎤 Escuchando...", fg=C["red"])
            self.mic_btn.config(bg=C["red"], fg="white")
        elif self.voice.is_speaking:
            self.voice_status.config(text="🔊 Hablando...", fg=C["green"])
            self.mic_btn.config(bg=C["bg3"], fg=C["accent"])
        elif self.wake_word_mode:
            self.voice_status.config(text="👂 Wake word activo", fg=C["purple"])
            self.mic_btn.config(bg=C["bg3"], fg=C["purple"])
        elif self.continuous_listen:
            self.voice_status.config(text="🎤 Modo voz", fg=C["accent"])
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
                api_key = self.config.get("api_key", "")
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
                lines = ["📝 TUS NOTAS:", "═" * 35]
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
                lines = ["✅ TUS TAREAS:", "═" * 35]
                for i, t in enumerate(todos, 1):
                    status = "✅" if t.get("done") else "⬜"
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

        # ── Enviar al cerebro IA ──

        if not self.brain.ready:
            self._fallback_response(text)
            return

        self.status_lbl.config(text="🧠 Procesando...", fg=C["accent"])
        self.root.update()
        if self.config.get("sound_fx"):
            SoundFX.beep_ready()

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
            clean_text, action_results = self.executor.execute_all(response)

            def show():
                if clean_text.strip():
                    self._print_jarvis(clean_text.strip())
                for r in action_results:
                    if r:
                        self._print_action(r)
                if clean_text.strip():
                    self.voice.speak(clean_text.strip())
                self.status_lbl.config(text="💡 Listo.", fg=self.theme["muted"])
                if self.config.get("sound_fx"):
                    SoundFX.beep_done()
                if self.continuous_listen and not self.voice.is_listening:
                    self.root.after(2000, self._voice_input)

            self.root.after(0, show)

        threading.Thread(target=process, daemon=True).start()

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
            city = comando.replace("clima", "").replace("weather", "").replace("en", "").strip() or "Madrid"
            def get_w():
                r = self.executor._get_weather(city)
                self.root.after(0, lambda: self._print_jarvis(r))
            threading.Thread(target=get_w, daemon=True).start()
            return

        if "chrome" in comando:
            os.system("start chrome")
            self._print_jarvis("Abriendo Chrome.")
            return

        if "notepad" in comando or "bloc" in comando:
            os.system("start notepad")
            self._print_jarvis("Abriendo bloc de notas.")
            return

        provider = self.config.get("provider", "gemini")
        pinfo = PROVIDERS.get(provider, PROVIDERS["gemini"])
        self._print_jarvis(
            f"Cerebro sin conexión. Proveedor: {pinfo['name']}\n\n"
            "🔧 SETUP RÁPIDO (GRATIS):\n\n"
            "  1. Google Gemini:\n"
            "     config proveedor: gemini\n"
            "     config api: TU_KEY → https://aistudio.google.com/apikey\n\n"
            "  2. Groq (ultra rápido):\n"
            "     config proveedor: groq\n"
            "     config api: TU_KEY → https://console.groq.com/keys\n\n"
            "  3. Ollama (local):\n"
            "     config proveedor: ollama → https://ollama.com\n\n"
            "Sin IA: hora, fecha, sistema, cpu, disco, clima"
        )

    # ─── VOZ ─────────────────────────────────────────

    def _voice_input(self):
        if self.voice.is_listening:
            return
        if not HAS_SPEECH:
            self._print_jarvis("Mic no disponible. pip install SpeechRecognition pyaudio")
            return

        self.status_lbl.config(text="🎤 Escuchando...", fg=self.theme["red"])
        self._print("🎤 Escuchando...", "info")
        self.root.update()

        def on_heard(text):
            self.root.after(0, lambda: self._process_input(text))

        def on_error(msg):
            def show():
                self._print(f"  {msg}", "muted")
                self.status_lbl.config(text="💡 Listo.", fg=self.theme["muted"])
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
        DataStore.save(CONFIG_FILE, self.config)

        # Aplicar colores a toda la UI
        self.root.configure(bg=C["bg"])
        self.sidebar.configure(bg=C["bg2"])
        for widget in self.sidebar.winfo_children():
            try:
                if isinstance(widget, tk.Button):
                    widget.configure(bg=C["bg3"], fg=C["text"], activebackground=C["accent"])
                    widget.bind("<Enter>", lambda e, b=widget, c=C: b.config(bg=c["border"]))
                    widget.bind("<Leave>", lambda e, b=widget, c=C: b.config(bg=c["bg3"]))
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=C["bg2"])
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=C["muted"])
            except tk.TclError:
                pass
        self.clock_lbl.config(fg=C["green"], bg=C["bg2"])
        self.date_lbl.config(fg=C["text2"], bg=C["bg2"])
        self.monitor_lbl.config(fg=C["yellow"], bg=C["bg2"])
        self.pomodoro_lbl.config(fg=C["orange"], bg=C["bg2"])
        self.voice_status.config(fg=C["accent"], bg=C["bg2"])
        self.output.config(bg=C["bg"], fg=C["text"], insertbackground=C["accent"],
                           selectbackground=C["accent"])
        self.output.tag_configure("jarvis", foreground=C["accent"])
        self.output.tag_configure("user", foreground=C["green"])
        self.output.tag_configure("error", foreground=C["red"])
        self.output.tag_configure("info", foreground=C["yellow"])
        self.output.tag_configure("muted", foreground=C["muted"])
        self.output.tag_configure("system", foreground=C["purple"])
        self.output.tag_configure("action", foreground=C["orange"])
        self.entry.config(bg=C["bg3"], fg=C["text"], insertbackground=C["accent"])
        self.mic_btn.config(bg=C["bg3"], fg=C["accent"])
        self.status_lbl.config(bg=C["bg"], fg=C["muted"])

        self._print_jarvis(f"Tema aplicado: {THEMES[theme_key]['name']}.")

    # ─── CLIPBOARD HISTORY ───────────────────────────

    def _show_clipboard_history(self):
        history = DataStore.load(CLIPBOARD_FILE, [])
        if not history:
            self._print_jarvis("El historial del portapapeles está vacío.")
            return
        lines = ["📋 HISTORIAL DEL PORTAPAPELES:", "═" * 35]
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
        voice = "Activada" if self.config.get("voice_enabled") else "Desactivada"
        brain = "✅ Conectado" if self.brain.ready else "❌ Sin conexión"
        theme_name = THEMES.get(self.config.get("theme", "jarvis"), {}).get("name", "?")
        tts = "Edge TTS" if HAS_EDGE_TTS else "pyttsx3" if HAS_PYTTSX3 else "Sin voz"
        voice_name = self.config.get("edge_voice", DEFAULT_EDGE_VOICE)

        self._print(f"""
⚙️ CONFIGURACIÓN J.A.R.V.I.S. GOD MODE v{VERSION}
═══════════════════════════════════════
  Proveedor:  {pinfo.get('name', provider)} ({pinfo.get('cost', '?')})
  Estado:     {brain}
  API Key:    {masked}
  Modelo:     {model}
  Motor voz:  {tts}
  Voz:        {voice_name}
  Respuesta:  {voice}
  Tema:       {theme_name}
  Typewriter: {"Sí" if self.config.get("typewriter") else "No"}
  Wake Word:  {"Activo" if self.config.get("wake_word") else "Inactivo"}
  Datos:      {DATA_DIR}

  CONFIGURAR:
  • config proveedor: gemini/groq/ollama/openai
  • config api: TU_API_KEY
  • config modelo: nombre_modelo
  • config nombre: tu_nombre
  • config voz: {", ".join(EDGE_VOICES.keys())}
  • config tema: {", ".join(THEMES.keys())}
  • typewriter    (toggle efecto escritura)
  • proveedores   (ver proveedores)
  • exportar      (guardar chat)
  • clipboard     (historial portapapeles)
  • pomodoro [min] (timer productividad)
  • schedule ver  (tareas programadas)
═══════════════════════════════════════
""", "system")

    def _show_providers(self):
        lines = ["\n🤖 PROVEEDORES DE IA", "═" * 40]
        current = self.config.get("provider", "gemini")
        for key, p in PROVIDERS.items():
            marker = " ◀ ACTIVO" if key == current else ""
            lines.append(f"\n  {p['name']} [{key}] - {p['cost']}{marker}")
            lines.append(f"    Modelos: {', '.join(p['models'])}")
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
        SoundFX.beep_startup()

        # Fase 1: Líneas de arranque del sistema
        boot_lines = [
            "Iniciando núcleos de procesamiento...",
            "Cargando módulos de inteligencia artificial...",
            "Calibrando motores de voz...",
            "Verificando conexión con proveedores de IA...",
            "Escaneando sistemas del equipo...",
            "Activando protocolos de seguridad...",
        ]

        # Mostrar banner
        self._print(f"""
⚡ ═══════════════════════════════════════════════════ ⚡
       J.A.R.V.I.S. GOD MODE  v{VERSION}
       Just A Rather Very Intelligent System
       "{THEMES.get(self.config.get('theme', 'jarvis'), {}).get('name', 'Classic')}" Theme
⚡ ═══════════════════════════════════════════════════ ⚡
""", "jarvis")

        # Boot sequence
        def show_boot_line(idx):
            if idx < len(boot_lines):
                self._print(f"  ▸ {boot_lines[idx]}", "muted")
                self.root.after(200, lambda: show_boot_line(idx + 1))
            else:
                self.root.after(300, self._show_greeting)

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

        self._print("  ▸ Todos los sistemas: ONLINE ✓\n", "info")

        greeting = f"{period}, {name}. Todos los sistemas están operativos."
        self._print_jarvis(greeting)

        # Estado del cerebro
        if self.brain.ready:
            model = self.config.get("model", "") or pinfo.get("default_model", "")
            self._print(f"  🧠 IA: {pinfo.get('name', provider)} → {model}", "muted")
        else:
            if provider == "ollama":
                self._print("  ⚠️ Ollama no conectado. Asegúrate de tenerlo corriendo.", "muted")
            elif not self.config.get("api_key"):
                self._print(f"  ⚠️ Sin API key. Configura: config api: TU_KEY", "muted")
                self._print(f"  ℹ️ Gratis: {pinfo.get('get_key_url', '')}", "muted")

        tts_engine = "Edge TTS (voces realistas)" if HAS_EDGE_TTS else "pyttsx3" if HAS_PYTTSX3 else "Sin voz"
        self._print(f"  🔊 Voz: {tts_engine}", "muted")

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
            self._print(f"  📦 Opcional: pip install {' '.join(missing)}", "muted")

        self._print("", "muted")

        self.voice.speak(greeting)

        # Activar wake word si estaba configurado
        if self.wake_word_mode:
            self.root.after(2000, self._wake_word_listen)

    # ─── HELP ────────────────────────────────────────

    def _show_help(self):
        self._print(f"""
❓ COMANDOS DE J.A.R.V.I.S. GOD MODE v{VERSION}
═══════════════════════════════════════════════
  CHAT IA (escribe cualquier cosa en español):
    "abre chrome"  "busca en google X"  "clima en Madrid"
    "traduce hola al inglés"  "noticias de hoy"
    "guarda una nota: comprar leche"
    "recuérdame X en 5 minutos"
    "dame una contraseña de 20 caracteres"

  COMANDOS LOCALES (no gastan API):
    notas / tareas      — ver guardados
    tarea done 1        — marcar tarea completada
    uptime              — tiempo activo
    pomodoro [min]      — timer productividad
    pomodoro stop       — parar timer
    schedule ver        — tareas programadas
    clipboard           — historial portapapeles
    exportar            — guardar chat a archivo
    proveedores         — ver proveedores de IA
    limpiar / cls       — limpiar pantalla

  CONFIGURACIÓN:
    config proveedor: gemini / groq / ollama / openai
    config api: TU_KEY
    config modelo: nombre
    config nombre: tu_nombre
    config voz: jorge / dalia / elena / alvaro
    config tema: jarvis / ironman / matrix / friday
    typewriter          — toggle efecto escritura

  ATAJOS:
    Enter     — enviar
    ↑/↓       — historial
    Ctrl+L    — limpiar
    Ctrl+E    — exportar chat
    Escape    — focus input

  BOTONES SIDEBAR:
    🎤 Modo Voz  — escucha continua
    👂 Wake Word — di "Jarvis" para activar
═══════════════════════════════════════════════
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
