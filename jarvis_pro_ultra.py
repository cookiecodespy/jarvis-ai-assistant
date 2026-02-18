"""
╔══════════════════════════════════════════════════════════════╗
║              JARVIS PRO ULTRA - Asistente Personal          ║
║         Basado en jarvis_ai_jeanCarlo.py (original)         ║
║                                                              ║
║  Funcionalidades:                                            ║
║   - Chat con IA (OpenAI GPT)                                ║
║   - Monitor del sistema (CPU, RAM, Disco, Batería)          ║
║   - Notas y Lista de Tareas persistentes                    ║
║   - Sistema de recordatorios con notificaciones             ║
║   - Cronómetro y Temporizador                               ║
║   - Calculadora de expresiones matemáticas                  ║
║   - Generador de contraseñas seguras                        ║
║   - Buscador de archivos                                    ║
║   - Búsquedas web (Google, YouTube, Wikipedia)              ║
║   - Info de red (IP pública/privada)                        ║
║   - Conversor de unidades                                   ║
║   - Herramientas de texto                                   ║
║   - Codificador Base64 / Generador de hashes                ║
║   - Calculadora de fechas                                   ║
║   - Control del sistema (bloquear, apagar, reiniciar)       ║
║   - Abrir 15+ aplicaciones                                  ║
║   - Historial de comandos                                   ║
║   - Chistes, frases, dados, moneda al aire                  ║
║   - Briefing diario                                         ║
║   - Y mucho más...                                          ║
║                                                              ║
║  Escribe 'ayuda' para ver todos los comandos disponibles.   ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, colorchooser
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
import pathlib
import datetime
import urllib.request
import urllib.parse
import textwrap
from collections import deque

# ══════════════════════════════════════════════════════════════
# CONSTANTES Y CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════

APP_NAME = "JARVIS PRO ULTRA"
VERSION = "2.0.0"
DATA_DIR = os.path.join(os.path.expanduser("~"), ".jarvis_pro_ultra")
NOTES_FILE = os.path.join(DATA_DIR, "notas.json")
TODOS_FILE = os.path.join(DATA_DIR, "tareas.json")
REMINDERS_FILE = os.path.join(DATA_DIR, "recordatorios.json")
HISTORY_FILE = os.path.join(DATA_DIR, "historial.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
CLIPS_FILE = os.path.join(DATA_DIR, "clipboard.json")

# Crear directorio de datos si no existe
os.makedirs(DATA_DIR, exist_ok=True)

# Colores del tema oscuro
COLORS = {
    "bg_dark": "#0F172A",
    "bg_sidebar": "#1E293B",
    "bg_main": "#111827",
    "bg_input": "#1F2937",
    "bg_card": "#1E293B",
    "accent": "#38BDF8",
    "accent_hover": "#7DD3FC",
    "accent_green": "#34D399",
    "accent_red": "#F87171",
    "accent_yellow": "#FBBF24",
    "accent_purple": "#A78BFA",
    "accent_orange": "#FB923C",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "border": "#334155",
}

# Frases motivacionales
FRASES_MOTIVACIONALES = [
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día. — Robert Collier",
    "No te detengas cuando estés cansado. Detente cuando hayas terminado.",
    "La disciplina es el puente entre las metas y los logros. — Jim Rohn",
    "Cada día es una nueva oportunidad para cambiar tu vida.",
    "El único modo de hacer un gran trabajo es amar lo que haces. — Steve Jobs",
    "Cree en ti mismo y todo será posible.",
    "La persistencia puede transformar el fracaso en un logro extraordinario.",
    "No cuentes los días, haz que los días cuenten. — Muhammad Ali",
    "El futuro pertenece a quienes creen en la belleza de sus sueños. — Eleanor Roosevelt",
    "La mejor forma de predecir el futuro es creándolo. — Abraham Lincoln",
    "Actúa como si lo que haces marcara la diferencia. Lo hace. — William James",
    "El conocimiento es poder. — Francis Bacon",
    "Sé el cambio que deseas ver en el mundo. — Mahatma Gandhi",
    "La creatividad es la inteligencia divirtiéndose. — Albert Einstein",
    "Todo parece imposible hasta que se hace. — Nelson Mandela",
]

# Chistes
CHISTES = [
    "¿Por qué los programadores prefieren el frío? Porque no quieren bugs... ¡quieren bytes!",
    "— ¿Qué le dijo un bit al otro?\n— Nos vemos en el bus.",
    "Hay 10 tipos de personas: las que entienden binario y las que no.",
    "Un SQL entra en un bar, se acerca a dos tablas y pregunta: ¿puedo unirme?",
    "— ¿Cuál es el animal más antiguo?\n— La cebra, porque está en blanco y negro.",
    "— ¿Cómo se llama el campeón de buceo japonés?\n— Tokofondo.",
    "¿Por qué Java y JavaScript se parecen? Como car y carpet.",
    "— Doctor, me siento invisible.\n— ¡Siguiente!",
    "Un programador pone 2 vasos en la mesita de noche: uno con agua por si tiene sed, y otro vacío por si no tiene.",
    "¿Cuántos programadores se necesitan para cambiar un foco? Ninguno, es un problema de hardware.",
    "Mi código funciona y no sé por qué. Mi código no funciona y no sé por qué.",
    "// Este código funciona, no lo toques.",
    "En teoría, no hay diferencia entre teoría y práctica. En la práctica, sí la hay.",
]

# Datos de conversión de unidades
CONVERSIONES = {
    "km_a_millas": 0.621371,
    "millas_a_km": 1.60934,
    "kg_a_libras": 2.20462,
    "libras_a_kg": 0.453592,
    "metros_a_pies": 3.28084,
    "pies_a_metros": 0.3048,
    "litros_a_galones": 0.264172,
    "galones_a_litros": 3.78541,
    "cm_a_pulgadas": 0.393701,
    "pulgadas_a_cm": 2.54,
}

# ══════════════════════════════════════════════════════════════
# CLASE: PERSISTENCIA DE DATOS
# ══════════════════════════════════════════════════════════════

class DataStore:
    """Maneja la persistencia de datos en archivos JSON."""

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
# CLASE: MONITOR DEL SISTEMA
# ══════════════════════════════════════════════════════════════

class SystemMonitor:
    """Recopila información del sistema operativo."""

    @staticmethod
    def get_system_info():
        info = []
        info.append(f"💻 Sistema: {platform.system()} {platform.release()}")
        info.append(f"🏷️ Nombre: {platform.node()}")
        info.append(f"🔧 Arquitectura: {platform.machine()}")
        info.append(f"🐍 Python: {platform.python_version()}")
        info.append(f"👤 Usuario: {os.getlogin()}")
        return "\n".join(info)

    @staticmethod
    def get_disk_usage():
        info = []
        try:
            for part in shutil.disk_usage("/") if os.name != "nt" else []:
                pass
            # En Windows, revisar las unidades comunes
            if os.name == "nt":
                for letter in "CDEFGH":
                    drive = f"{letter}:\\"
                    if os.path.exists(drive):
                        usage = shutil.disk_usage(drive)
                        total_gb = usage.total / (1024**3)
                        used_gb = usage.used / (1024**3)
                        free_gb = usage.free / (1024**3)
                        pct = (usage.used / usage.total) * 100
                        bar = SystemMonitor._progress_bar(pct)
                        info.append(
                            f"💾 {drive}  {bar} {pct:.0f}%\n"
                            f"   Total: {total_gb:.1f} GB | "
                            f"Usado: {used_gb:.1f} GB | "
                            f"Libre: {free_gb:.1f} GB"
                        )
            else:
                usage = shutil.disk_usage("/")
                total_gb = usage.total / (1024**3)
                used_gb = usage.used / (1024**3)
                free_gb = usage.free / (1024**3)
                pct = (usage.used / usage.total) * 100
                bar = SystemMonitor._progress_bar(pct)
                info.append(
                    f"💾 /  {bar} {pct:.0f}%\n"
                    f"   Total: {total_gb:.1f} GB | "
                    f"Usado: {used_gb:.1f} GB | "
                    f"Libre: {free_gb:.1f} GB"
                )
        except Exception as e:
            info.append(f"⚠️ Error al leer disco: {e}")
        return "\n".join(info) if info else "No se pudo obtener info del disco."

    @staticmethod
    def get_cpu_info():
        """Intenta obtener info de CPU usando psutil si está disponible."""
        try:
            import psutil
            cpu_pct = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            ram = psutil.virtual_memory()
            ram_bar = SystemMonitor._progress_bar(ram.percent)
            cpu_bar = SystemMonitor._progress_bar(cpu_pct)

            info = [
                f"🧠 CPU: {cpu_bar} {cpu_pct}%",
                f"   Núcleos: {cpu_count}",
            ]
            if cpu_freq:
                info.append(f"   Frecuencia: {cpu_freq.current:.0f} MHz")
            info.append(
                f"🗃️ RAM: {ram_bar} {ram.percent}%\n"
                f"   Total: {ram.total / (1024**3):.1f} GB | "
                f"Usada: {ram.used / (1024**3):.1f} GB | "
                f"Libre: {ram.available / (1024**3):.1f} GB"
            )

            # Batería
            bat = psutil.sensors_battery()
            if bat:
                bat_bar = SystemMonitor._progress_bar(bat.percent)
                plug = "🔌 Conectado" if bat.power_plugged else "🔋 Batería"
                info.append(f"🔋 Batería: {bat_bar} {bat.percent}% ({plug})")

            return "\n".join(info)
        except ImportError:
            return (
                "⚠️ Instala 'psutil' para monitoreo avanzado:\n"
                "   pip install psutil\n\n"
                + SystemMonitor.get_basic_cpu_info()
            )

    @staticmethod
    def get_basic_cpu_info():
        info = [
            f"🧠 Procesador: {platform.processor() or 'No disponible'}",
            f"   Núcleos lógicos: {os.cpu_count() or 'N/A'}",
        ]
        return "\n".join(info)

    @staticmethod
    def _progress_bar(percent, length=15):
        filled = int(length * percent / 100)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"

    @staticmethod
    def get_network_info():
        info = []
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            info.append(f"🏠 Hostname: {hostname}")
            info.append(f"🔗 IP Local: {local_ip}")
        except Exception:
            info.append("⚠️ No se pudo obtener IP local")

        # IP pública
        try:
            req = urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5)
            data = json.loads(req.read().decode())
            info.append(f"🌍 IP Pública: {data.get('ip', 'N/A')}")
        except Exception:
            info.append("🌍 IP Pública: No disponible (sin conexión)")

        return "\n".join(info)


# ══════════════════════════════════════════════════════════════
# CLASE: HERRAMIENTAS DE UTILIDAD
# ══════════════════════════════════════════════════════════════

class Tools:
    """Colección de herramientas útiles."""

    @staticmethod
    def generate_password(length=16, use_special=True):
        chars = string.ascii_letters + string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = "".join(random.SystemRandom().choice(chars) for _ in range(length))
        # Evaluar fortaleza
        score = 0
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in string.punctuation for c in password): score += 1
        if length >= 12: score += 1
        if length >= 16: score += 1

        strength = ["Muy débil", "Débil", "Regular", "Buena", "Fuerte", "Muy fuerte", "Excelente"]
        strength_text = strength[min(score, len(strength)-1)]
        bar = SystemMonitor._progress_bar(score / 6 * 100)

        return (
            f"🔐 Contraseña generada ({length} caracteres):\n\n"
            f"   {password}\n\n"
            f"   Fortaleza: {bar} {strength_text}"
        )

    @staticmethod
    def calculate(expression):
        """Calculadora segura de expresiones matemáticas."""
        try:
            # Limpiar la expresión
            expr = expression.strip()
            expr = expr.replace("^", "**")
            expr = expr.replace("×", "*").replace("÷", "/")
            expr = expr.replace(",", ".")

            # Funciones matemáticas permitidas
            safe_dict = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan,
                "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
                "log2": math.log2, "exp": math.exp, "pow": pow,
                "pi": math.pi, "e": math.e, "tau": math.tau,
                "factorial": math.factorial, "ceil": math.ceil,
                "floor": math.floor, "gcd": math.gcd,
                "radians": math.radians, "degrees": math.degrees,
                "inf": float("inf"),
            }

            # Validar que no haya código malicioso
            forbidden = ["import", "exec", "eval", "open", "os.", "sys.", "__", "lambda"]
            for word in forbidden:
                if word in expr.lower():
                    return "⚠️ Expresión no permitida por seguridad."

            result = eval(expr, {"__builtins__": {}}, safe_dict)

            if isinstance(result, float):
                if result == int(result) and not math.isinf(result):
                    result = int(result)
                else:
                    result = round(result, 10)

            return f"🧮 {expression} = {result}"

        except ZeroDivisionError:
            return "⚠️ Error: División por cero."
        except Exception as e:
            return f"⚠️ Error en el cálculo: {e}"

    @staticmethod
    def convert_units(text):
        """Conversor de unidades."""
        text = text.lower().strip()

        patterns = [
            (r"([\d.]+)\s*(?:km|kilómetros?|kilometros?)\s+(?:a|en|to)\s+(?:mi|millas?)",
             lambda v: (v * CONVERSIONES["km_a_millas"], "millas")),
            (r"([\d.]+)\s*(?:mi|millas?)\s+(?:a|en|to)\s+(?:km|kilómetros?|kilometros?)",
             lambda v: (v * CONVERSIONES["millas_a_km"], "km")),
            (r"([\d.]+)\s*(?:kg|kilos?|kilogramos?)\s+(?:a|en|to)\s+(?:lb|libras?)",
             lambda v: (v * CONVERSIONES["kg_a_libras"], "libras")),
            (r"([\d.]+)\s*(?:lb|libras?)\s+(?:a|en|to)\s+(?:kg|kilos?|kilogramos?)",
             lambda v: (v * CONVERSIONES["libras_a_kg"], "kg")),
            (r"([\d.]+)\s*(?:m|metros?)\s+(?:a|en|to)\s+(?:ft|pies?|feet)",
             lambda v: (v * CONVERSIONES["metros_a_pies"], "pies")),
            (r"([\d.]+)\s*(?:ft|pies?|feet)\s+(?:a|en|to)\s+(?:m|metros?)",
             lambda v: (v * CONVERSIONES["pies_a_metros"], "metros")),
            (r"([\d.]+)\s*(?:l|litros?)\s+(?:a|en|to)\s+(?:gal|galones?)",
             lambda v: (v * CONVERSIONES["litros_a_galones"], "galones")),
            (r"([\d.]+)\s*(?:gal|galones?)\s+(?:a|en|to)\s+(?:l|litros?)",
             lambda v: (v * CONVERSIONES["galones_a_litros"], "litros")),
            (r"([\d.]+)\s*(?:cm|centímetros?|centimetros?)\s+(?:a|en|to)\s+(?:in|pulgadas?)",
             lambda v: (v * CONVERSIONES["cm_a_pulgadas"], "pulgadas")),
            (r"([\d.]+)\s*(?:in|pulgadas?)\s+(?:a|en|to)\s+(?:cm|centímetros?|centimetros?)",
             lambda v: (v * CONVERSIONES["pulgadas_a_cm"], "cm")),
            # Temperatura
            (r"([\d.]+)\s*°?(?:c|celsius|centígrados?|centigrados?)\s+(?:a|en|to)\s+°?(?:f|fahrenheit)",
             lambda v: (v * 9/5 + 32, "°F")),
            (r"([\d.]+)\s*°?(?:f|fahrenheit)\s+(?:a|en|to)\s+°?(?:c|celsius|centígrados?|centigrados?)",
             lambda v: ((v - 32) * 5/9, "°C")),
        ]

        for pattern, converter in patterns:
            match = re.search(pattern, text)
            if match:
                value = float(match.group(1))
                result, unit = converter(value)
                return f"📐 {value} → {result:.4f} {unit}"

        return (
            "📐 Formato: '[valor] [unidad] a [unidad]'\n"
            "   Ejemplos:\n"
            "   • 10 km a millas\n"
            "   • 75 kg a libras\n"
            "   • 100 celsius a fahrenheit\n"
            "   • 5.5 litros a galones\n"
            "   • 180 cm a pulgadas"
        )

    @staticmethod
    def encode_base64(text):
        encoded = base64.b64encode(text.encode()).decode()
        return f"🔒 Base64 encode:\n   {encoded}"

    @staticmethod
    def decode_base64(text):
        try:
            decoded = base64.b64decode(text.encode()).decode()
            return f"🔓 Base64 decode:\n   {decoded}"
        except Exception:
            return "⚠️ Texto Base64 inválido."

    @staticmethod
    def generate_hash(text):
        md5 = hashlib.md5(text.encode()).hexdigest()
        sha1 = hashlib.sha1(text.encode()).hexdigest()
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        return (
            f"🔑 Hashes de: '{text}'\n\n"
            f"   MD5:    {md5}\n"
            f"   SHA1:   {sha1}\n"
            f"   SHA256: {sha256}"
        )

    @staticmethod
    def text_stats(text):
        chars = len(text)
        chars_no_space = len(text.replace(" ", ""))
        words = len(text.split())
        lines = text.count("\n") + 1
        sentences = len(re.findall(r'[.!?]+', text))
        vowels = len(re.findall(r'[aeiouáéíóúü]', text, re.IGNORECASE))
        return (
            f"📊 Estadísticas del texto:\n"
            f"   Caracteres: {chars}\n"
            f"   Sin espacios: {chars_no_space}\n"
            f"   Palabras: {words}\n"
            f"   Líneas: {lines}\n"
            f"   Oraciones: {sentences}\n"
            f"   Vocales: {vowels}"
        )

    @staticmethod
    def date_calculator(text):
        """Calculadora de fechas."""
        text = text.lower().strip()
        today = datetime.date.today()

        # Cuántos días faltan para una fecha
        match = re.search(r"(?:dias|días)\s+(?:para|hasta)\s+(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?", text)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3)) if match.group(3) else today.year
            if year < 100:
                year += 2000
            try:
                target = datetime.date(year, month, day)
                diff = (target - today).days
                if diff > 0:
                    return f"📅 Faltan {diff} días para el {target.strftime('%d/%m/%Y')}"
                elif diff < 0:
                    return f"📅 Han pasado {abs(diff)} días desde el {target.strftime('%d/%m/%Y')}"
                else:
                    return "📅 ¡Esa fecha es hoy!"
            except ValueError:
                return "⚠️ Fecha inválida."

        # Sumar/restar días
        match = re.search(r"(?:hoy|fecha)\s*([\+\-])\s*(\d+)\s*(?:dias|días)?", text)
        if match:
            op = match.group(1)
            days = int(match.group(2))
            if op == "+":
                result = today + datetime.timedelta(days=days)
                return f"📅 Hoy + {days} días = {result.strftime('%A %d/%m/%Y')}"
            else:
                result = today - datetime.timedelta(days=days)
                return f"📅 Hoy - {days} días = {result.strftime('%A %d/%m/%Y')}"

        # Días entre dos fechas
        match = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\s+(?:a|hasta|y)\s+(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", text)
        if match:
            try:
                d1 = datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
                d2 = datetime.date(int(match.group(6)), int(match.group(5)), int(match.group(4)))
                diff = abs((d2 - d1).days)
                weeks = diff // 7
                return (
                    f"📅 Entre {d1.strftime('%d/%m/%Y')} y {d2.strftime('%d/%m/%Y')}:\n"
                    f"   {diff} días ({weeks} semanas y {diff % 7} días)"
                )
            except ValueError:
                return "⚠️ Fecha inválida."

        return (
            "📅 Uso del calculador de fechas:\n"
            "   • dias para 25/12         → Días hasta Navidad\n"
            "   • hoy +30 dias            → Fecha en 30 días\n"
            "   • hoy -15 dias            → Fecha hace 15 días\n"
            "   • 01/01/2025 a 31/12/2025 → Días entre fechas"
        )

    @staticmethod
    def search_files(query, path=None, max_results=20):
        """Buscar archivos en el sistema."""
        if not path:
            path = os.path.expanduser("~")

        results = []

        def search_recursive(dir_path, depth=0):
            if depth > 4 or len(results) >= max_results:
                return
            try:
                for entry in os.scandir(dir_path):
                    if len(results) >= max_results:
                        return
                    try:
                        if query.lower() in entry.name.lower():
                            size = ""
                            if entry.is_file():
                                s = entry.stat().st_size
                                if s < 1024:
                                    size = f" ({s} B)"
                                elif s < 1024**2:
                                    size = f" ({s/1024:.1f} KB)"
                                elif s < 1024**3:
                                    size = f" ({s/1024**2:.1f} MB)"
                                else:
                                    size = f" ({s/1024**3:.1f} GB)"
                            icon = "📁" if entry.is_dir() else "📄"
                            results.append(f"  {icon} {entry.path}{size}")
                        if entry.is_dir() and not entry.name.startswith("."):
                            search_recursive(entry.path, depth + 1)
                    except (PermissionError, OSError):
                        continue
            except (PermissionError, OSError):
                pass

        search_recursive(path)

        if results:
            return (
                f"🔍 Resultados para '{query}' "
                f"(máx. {max_results}):\n\n" + "\n".join(results)
            )
        return f"🔍 No se encontraron archivos con '{query}'"

    @staticmethod
    def get_daily_briefing():
        """Briefing diario completo."""
        now = datetime.datetime.now()

        # Día en español
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        dia_nombre = dias[now.weekday()]
        mes_nombre = meses[now.month - 1]

        # Día del año
        day_of_year = now.timetuple().tm_yday
        days_left = 365 + (1 if now.year % 4 == 0 else 0) - day_of_year
        progress = day_of_year / (365 + (1 if now.year % 4 == 0 else 0)) * 100

        # Tareas pendientes
        todos = DataStore.load(TODOS_FILE, [])
        pending = [t for t in todos if not t.get("done")]

        # Frase del día
        frase = random.choice(FRASES_MOTIVACIONALES)

        year_bar = SystemMonitor._progress_bar(progress)

        briefing = [
            "═" * 45,
            f"  ☀️ BRIEFING DIARIO — {dia_nombre}",
            "═" * 45,
            "",
            f"📅 {dia_nombre}, {now.day} de {mes_nombre} de {now.year}",
            f"🕐 {now.strftime('%H:%M:%S')}",
            f"📆 Día {day_of_year} del año | Quedan {days_left} días",
            f"   Progreso del año: {year_bar} {progress:.1f}%",
            "",
        ]

        if pending:
            briefing.append(f"📋 Tareas pendientes: {len(pending)}")
            for i, t in enumerate(pending[:5], 1):
                briefing.append(f"   {i}. {t['text']}")
            if len(pending) > 5:
                briefing.append(f"   ... y {len(pending) - 5} más")
        else:
            briefing.append("📋 No hay tareas pendientes. ¡Buen trabajo!")

        briefing.extend([
            "",
            "💬 Frase del día:",
            f"   \"{frase}\"",
            "",
            "═" * 45,
        ])

        return "\n".join(briefing)


# ══════════════════════════════════════════════════════════════
# CLASE: SISTEMA DE RECORDATORIOS
# ══════════════════════════════════════════════════════════════

class ReminderSystem:
    """Sistema de recordatorios con verificación periódica."""

    def __init__(self, callback):
        self.reminders = DataStore.load(REMINDERS_FILE, [])
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()

    def add(self, text, minutes):
        reminder = {
            "id": int(time.time() * 1000),
            "text": text,
            "time": (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).isoformat(),
            "triggered": False,
        }
        self.reminders.append(reminder)
        DataStore.save(REMINDERS_FILE, self.reminders)
        target_time = datetime.datetime.fromisoformat(reminder["time"])
        return (
            f"⏰ Recordatorio creado:\n"
            f"   '{text}'\n"
            f"   Te avisaré a las {target_time.strftime('%H:%M:%S')} "
            f"(en {minutes} min)"
        )

    def list_active(self):
        active = [r for r in self.reminders if not r.get("triggered")]
        if not active:
            return "⏰ No hay recordatorios activos."
        lines = ["⏰ Recordatorios activos:\n"]
        for i, r in enumerate(active, 1):
            t = datetime.datetime.fromisoformat(r["time"])
            remaining = (t - datetime.datetime.now()).total_seconds()
            if remaining > 0:
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                lines.append(f"   {i}. {r['text']} — en {mins}m {secs}s")
            else:
                lines.append(f"   {i}. {r['text']} — ¡ya pasó!")
        return "\n".join(lines)

    def clear(self):
        self.reminders = []
        DataStore.save(REMINDERS_FILE, self.reminders)
        return "⏰ Todos los recordatorios han sido eliminados."

    def _check_loop(self):
        while self.running:
            now = datetime.datetime.now()
            for r in self.reminders:
                if not r.get("triggered"):
                    target = datetime.datetime.fromisoformat(r["time"])
                    if now >= target:
                        r["triggered"] = True
                        DataStore.save(REMINDERS_FILE, self.reminders)
                        self.callback(r["text"])
            time.sleep(5)

    def stop(self):
        self.running = False


# ══════════════════════════════════════════════════════════════
# CLASE: CRONÓMETRO Y TEMPORIZADOR
# ══════════════════════════════════════════════════════════════

class TimerSystem:
    """Cronómetro y temporizador."""

    def __init__(self):
        self.stopwatch_start = None
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.timer_end = None
        self.timer_running = False

    def start_stopwatch(self):
        if self.stopwatch_running:
            return "⏱️ El cronómetro ya está corriendo."
        self.stopwatch_running = True
        self.stopwatch_start = time.time() - self.stopwatch_elapsed
        return "⏱️ Cronómetro iniciado."

    def stop_stopwatch(self):
        if not self.stopwatch_running:
            return "⏱️ El cronómetro no está corriendo."
        self.stopwatch_running = False
        self.stopwatch_elapsed = time.time() - self.stopwatch_start
        return f"⏱️ Cronómetro detenido: {self._format_time(self.stopwatch_elapsed)}"

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.stopwatch_start = None
        return "⏱️ Cronómetro reiniciado."

    def get_stopwatch(self):
        if self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start
        else:
            elapsed = self.stopwatch_elapsed
        return f"⏱️ Cronómetro: {self._format_time(elapsed)}"

    def start_timer(self, minutes):
        self.timer_end = time.time() + (minutes * 60)
        self.timer_running = True
        return f"⏳ Temporizador de {minutes} minutos iniciado."

    def get_timer(self):
        if not self.timer_running or not self.timer_end:
            return "⏳ No hay temporizador activo."
        remaining = self.timer_end - time.time()
        if remaining <= 0:
            self.timer_running = False
            return "⏳ ¡El temporizador ha terminado! 🔔"
        return f"⏳ Tiempo restante: {self._format_time(remaining)}"

    def _format_time(self, seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 100)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}.{ms:02d}"
        return f"{m:02d}:{s:02d}.{ms:02d}"


# ══════════════════════════════════════════════════════════════
# CLASE PRINCIPAL: JARVIS PRO ULTRA
# ══════════════════════════════════════════════════════════════

class JarvisApp:
    """Aplicación principal de Jarvis PRO ULTRA."""

    def __init__(self, root):
        self.root = root
        self.root.title(f"🤖 {APP_NAME} v{VERSION}")
        self.root.geometry("920x680")
        self.root.minsize(800, 600)
        self.root.configure(bg=COLORS["bg_dark"])

        # Intentar poner icono (no falla si no existe)
        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        # Datos persistentes
        self.notes = DataStore.load(NOTES_FILE, [])
        self.todos = DataStore.load(TODOS_FILE, [])
        self.command_history = deque(DataStore.load(HISTORY_FILE, []), maxlen=100)
        self.history_index = -1
        self.clips = deque(DataStore.load(CLIPS_FILE, []), maxlen=20)

        # Subsistemas
        self.reminder_system = ReminderSystem(self._on_reminder)
        self.timer_system = TimerSystem()
        self.openai_client = None  # Lazy init

        # Configuración
        self.config = DataStore.load(CONFIG_FILE, {
            "api_key": "",
            "ai_model": "gpt-4o-mini",
            "user_name": "Usuario",
        })
        if isinstance(self.config, list):
            self.config = {"api_key": "", "ai_model": "gpt-4o-mini", "user_name": "Usuario"}

        # Construir UI
        self._build_ui()

        # Mostrar briefing al iniciar
        self.root.after(300, lambda: self._display_output(Tools.get_daily_briefing()))

        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ─────────────────────────────────────────────────
    # INTERFAZ DE USUARIO
    # ─────────────────────────────────────────────────

    def _build_ui(self):
        """Construye toda la interfaz."""

        # Frame principal con grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # ── SIDEBAR ──
        sidebar = tk.Frame(self.root, bg=COLORS["bg_sidebar"], width=200)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        sidebar.configure(width=180)

        # Logo
        tk.Label(
            sidebar, text="🤖", font=("Segoe UI", 36),
            bg=COLORS["bg_sidebar"], fg=COLORS["accent"]
        ).pack(pady=(15, 0))

        tk.Label(
            sidebar, text="JARVIS", font=("Consolas", 16, "bold"),
            bg=COLORS["bg_sidebar"], fg=COLORS["accent"]
        ).pack()

        tk.Label(
            sidebar, text="PRO ULTRA", font=("Consolas", 9),
            bg=COLORS["bg_sidebar"], fg=COLORS["text_muted"]
        ).pack()

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=10, pady=10)

        # Reloj en sidebar
        self.clock_label = tk.Label(
            sidebar, font=("Consolas", 20, "bold"),
            bg=COLORS["bg_sidebar"], fg=COLORS["accent_green"]
        )
        self.clock_label.pack(pady=5)

        self.date_label = tk.Label(
            sidebar, font=("Consolas", 9),
            bg=COLORS["bg_sidebar"], fg=COLORS["text_secondary"]
        )
        self.date_label.pack()

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=10, pady=10)

        # Botones rápidos
        quick_buttons = [
            ("📋 Briefing", lambda: self._display_output(Tools.get_daily_briefing())),
            ("💻 Sistema", lambda: self._display_output(SystemMonitor.get_cpu_info())),
            ("💾 Disco", lambda: self._display_output(SystemMonitor.get_disk_usage())),
            ("🌐 Red", lambda: self._run_async(SystemMonitor.get_network_info)),
            ("📝 Notas", self._show_notes),
            ("✅ Tareas", self._show_todos),
            ("⏰ Recordar", self._show_reminders),
            ("🔐 Password", lambda: self._display_output(Tools.generate_password())),
            ("❓ Ayuda", self._show_help),
        ]

        for text, cmd in quick_buttons:
            btn = tk.Button(
                sidebar, text=text, font=("Segoe UI", 10),
                bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                activebackground=COLORS["accent"],
                activeforeground="black",
                bd=0, padx=10, pady=4,
                anchor="w", cursor="hand2",
                command=cmd
            )
            btn.pack(fill="x", padx=8, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COLORS["border"]))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COLORS["bg_card"]))

        # Versión al fondo
        tk.Label(
            sidebar, text=f"v{VERSION}", font=("Consolas", 8),
            bg=COLORS["bg_sidebar"], fg=COLORS["text_muted"]
        ).pack(side="bottom", pady=5)

        # ── ÁREA PRINCIPAL ──
        main_frame = tk.Frame(self.root, bg=COLORS["bg_main"])
        main_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Área de salida (scrollable)
        output_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        output_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            font=("Consolas", 11),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["accent"],
            selectforeground="black",
            bd=0, padx=15, pady=15,
            wrap="word",
            state="disabled",
            cursor="arrow",
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")

        # Tags de colores para el output
        self.output_text.tag_configure("system", foreground=COLORS["accent"])
        self.output_text.tag_configure("user", foreground=COLORS["accent_green"])
        self.output_text.tag_configure("error", foreground=COLORS["accent_red"])
        self.output_text.tag_configure("info", foreground=COLORS["accent_yellow"])
        self.output_text.tag_configure("muted", foreground=COLORS["text_muted"])

        # ── ÁREA DE ENTRADA ──
        input_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        input_frame.grid_columnconfigure(0, weight=1)

        # Status bar
        self.status_bar = tk.Label(
            input_frame, text="💡 Escribe 'ayuda' para ver todos los comandos",
            font=("Segoe UI", 9),
            bg=COLORS["bg_main"], fg=COLORS["text_muted"],
            anchor="w"
        )
        self.status_bar.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 3))

        self.entry = tk.Entry(
            input_frame,
            font=("Consolas", 13),
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["accent"],
            bd=0, relief="flat",
        )
        self.entry.grid(row=1, column=0, sticky="ew", ipady=8, padx=(0, 5))
        self.entry.focus_set()

        send_btn = tk.Button(
            input_frame, text="Enviar ▶",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["accent"], fg="black",
            activebackground=COLORS["accent_hover"],
            bd=0, padx=20, cursor="hand2",
            command=self._process_command
        )
        send_btn.grid(row=1, column=1, sticky="ew", ipady=6)

        # Bindings
        self.entry.bind("<Return>", lambda e: self._process_command())
        self.entry.bind("<Up>", lambda e: self._history_navigate(-1))
        self.entry.bind("<Down>", lambda e: self._history_navigate(1))
        self.root.bind("<Escape>", lambda e: self.entry.focus_set())

        # Actualizar reloj
        self._update_clock()

    # ─────────────────────────────────────────────────
    # RELOJ
    # ─────────────────────────────────────────────────

    def _update_clock(self):
        now = datetime.datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M:%S"))

        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                 "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        self.date_label.config(
            text=f"{dias[now.weekday()]} {now.day} {meses[now.month-1]} {now.year}"
        )
        self.root.after(1000, self._update_clock)

    # ─────────────────────────────────────────────────
    # SALIDA / DISPLAY
    # ─────────────────────────────────────────────────

    def _display_output(self, text, tag="system"):
        self.output_text.config(state="normal")
        self.output_text.insert("end", text + "\n\n", tag)
        self.output_text.see("end")
        self.output_text.config(state="disabled")

    def _display_user_command(self, text):
        self.output_text.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.output_text.insert("end", f"[{timestamp}] ", "muted")
        self.output_text.insert("end", f"❯ {text}\n", "user")
        self.output_text.config(state="disabled")

    def _clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")

    # ─────────────────────────────────────────────────
    # HISTORIAL DE COMANDOS
    # ─────────────────────────────────────────────────

    def _history_navigate(self, direction):
        if not self.command_history:
            return
        history = list(self.command_history)
        self.history_index += direction
        self.history_index = max(-1, min(self.history_index, len(history) - 1))

        self.entry.delete(0, "end")
        if self.history_index >= 0:
            self.entry.insert(0, history[-(self.history_index + 1)])

    # ─────────────────────────────────────────────────
    # PROCESAMIENTO DE COMANDOS
    # ─────────────────────────────────────────────────

    def _process_command(self):
        raw = self.entry.get().strip()
        if not raw:
            return

        comando = raw.lower()
        self.entry.delete(0, "end")
        self.history_index = -1

        # Guardar en historial
        self.command_history.append(raw)
        DataStore.save(HISTORY_FILE, list(self.command_history))

        # Mostrar comando del usuario
        self._display_user_command(raw)

        # ── SALIR ──
        if comando in ("salir", "exit", "quit", "cerrar"):
            self._on_close()
            return

        # ── LIMPIAR ──
        if comando in ("cls", "clear", "limpiar"):
            self._clear_output()
            return

        # ── AYUDA ──
        if comando in ("ayuda", "help", "?", "comandos"):
            self._show_help()
            return

        # ── BRIEFING ──
        if comando in ("briefing", "buenos dias", "buenos días", "resumen", "inicio"):
            self._display_output(Tools.get_daily_briefing())
            return

        # ── HORA / FECHA ──
        if comando in ("hora", "time"):
            self._display_output(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}")
            return
        if comando in ("fecha", "date", "hoy"):
            now = datetime.datetime.now()
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                     "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            self._display_output(
                f"📅 {dias[now.weekday()]}, {now.day} de {meses[now.month-1]} de {now.year}"
            )
            return

        # ── SISTEMA ──
        if comando in ("sistema", "system", "info sistema", "sysinfo"):
            self._display_output(SystemMonitor.get_system_info())
            return
        if comando in ("cpu", "ram", "monitor", "recursos"):
            self._display_output(SystemMonitor.get_cpu_info())
            return
        if comando in ("disco", "disk", "espacio", "almacenamiento"):
            self._display_output(SystemMonitor.get_disk_usage())
            return
        if comando in ("red", "network", "ip", "internet"):
            self._run_async(SystemMonitor.get_network_info)
            return

        # ── NOTAS ──
        if comando in ("notas", "mis notas", "notes"):
            self._show_notes()
            return
        if comando.startswith("nota:") or comando.startswith("anotar:"):
            text = raw.split(":", 1)[1].strip()
            if text:
                self._add_note(text)
            return
        if comando.startswith("borrar nota"):
            self._delete_note(comando)
            return

        # ── TAREAS ──
        if comando in ("tareas", "todos", "todo", "pendientes"):
            self._show_todos()
            return
        if comando.startswith("tarea:") or comando.startswith("todo:"):
            text = raw.split(":", 1)[1].strip()
            if text:
                self._add_todo(text)
            return
        if re.match(r"^(?:completar|done|hecho)\s+(\d+)", comando):
            match = re.match(r"^(?:completar|done|hecho)\s+(\d+)", comando)
            self._complete_todo(int(match.group(1)))
            return
        if comando.startswith("borrar tarea"):
            self._delete_todo(comando)
            return

        # ── RECORDATORIOS ──
        if comando in ("recordatorios", "reminders", "alarmas"):
            self._show_reminders()
            return
        match = re.match(r"^(?:recordar|reminder|alarma)[:\s]+(.+)\s+en\s+(\d+)\s*(?:min|minutos?)?$", comando)
        if match:
            text = match.group(1).strip()
            minutes = int(match.group(2))
            self._display_output(self.reminder_system.add(text, minutes))
            return
        if comando in ("borrar recordatorios", "limpiar recordatorios"):
            self._display_output(self.reminder_system.clear())
            return

        # ── CRONÓMETRO ──
        if comando in ("cronómetro", "cronometro", "stopwatch"):
            self._display_output(self.timer_system.get_stopwatch())
            return
        if comando in ("iniciar cronómetro", "iniciar cronometro", "start stopwatch"):
            self._display_output(self.timer_system.start_stopwatch())
            return
        if comando in ("parar cronómetro", "parar cronometro", "stop stopwatch", "detener cronómetro"):
            self._display_output(self.timer_system.stop_stopwatch())
            return
        if comando in ("reiniciar cronómetro", "reiniciar cronometro", "reset stopwatch"):
            self._display_output(self.timer_system.reset_stopwatch())
            return

        # ── TEMPORIZADOR ──
        match = re.match(r"^(?:temporizador|timer)\s+(\d+)", comando)
        if match:
            minutes = int(match.group(1))
            self._display_output(self.timer_system.start_timer(minutes))
            return
        if comando in ("temporizador", "timer"):
            self._display_output(self.timer_system.get_timer())
            return

        # ── CALCULADORA ──
        if comando.startswith("calc:") or comando.startswith("calcular:"):
            expr = raw.split(":", 1)[1].strip()
            self._display_output(Tools.calculate(expr))
            return
        # Detección automática de expresiones matemáticas
        if re.match(r"^[\d\s\+\-\*/\(\)\.\^%]+$", comando) and len(comando) > 1:
            self._display_output(Tools.calculate(raw))
            return

        # ── CONTRASEÑA ──
        if comando.startswith("password") or comando.startswith("contraseña"):
            match = re.search(r"(\d+)", comando)
            length = int(match.group(1)) if match else 16
            length = max(4, min(128, length))
            self._display_output(Tools.generate_password(length))
            return

        # ── CONVERSOR DE UNIDADES ──
        if comando.startswith("convertir:") or comando.startswith("convert:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(Tools.convert_units(text))
            return
        # Auto-detectar conversiones
        if re.search(r"\d+.*(?:km|millas?|kg|libras?|metros?|pies|litros?|galones?|celsius|fahrenheit|cm|pulgadas?)\s+(?:a|en|to)\s+", comando):
            self._display_output(Tools.convert_units(raw))
            return

        # ── FECHAS ──
        if comando.startswith("fecha:") or comando.startswith("dias") or comando.startswith("días"):
            text = raw.split(":", 1)[1].strip() if ":" in raw else raw
            self._display_output(Tools.date_calculator(text))
            return
        if re.match(r"^hoy\s*[\+\-]", comando):
            self._display_output(Tools.date_calculator(raw))
            return

        # ── BUSCAR ARCHIVOS ──
        if comando.startswith("buscar:") or comando.startswith("buscar archivos:"):
            query = raw.split(":", 1)[1].strip()
            self._display_output("🔍 Buscando...", "info")
            self.root.update()
            self._run_async(lambda: Tools.search_files(query))
            return

        # ── BASE64 ──
        if comando.startswith("base64 encode:") or comando.startswith("b64e:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(Tools.encode_base64(text))
            return
        if comando.startswith("base64 decode:") or comando.startswith("b64d:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(Tools.decode_base64(text))
            return

        # ── HASH ──
        if comando.startswith("hash:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(Tools.generate_hash(text))
            return

        # ── HERRAMIENTAS DE TEXTO ──
        if comando.startswith("mayúsculas:") or comando.startswith("mayusculas:") or comando.startswith("upper:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(f"🔤 {text.upper()}")
            return
        if comando.startswith("minúsculas:") or comando.startswith("minusculas:") or comando.startswith("lower:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(f"🔤 {text.lower()}")
            return
        if comando.startswith("invertir:") or comando.startswith("reverse:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(f"🔄 {text[::-1]}")
            return
        if comando.startswith("contar:") or comando.startswith("stats:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(Tools.text_stats(text))
            return
        if comando.startswith("titulo:") or comando.startswith("title:"):
            text = raw.split(":", 1)[1].strip()
            self._display_output(f"🔤 {text.title()}")
            return

        # ── BÚSQUEDAS WEB ──
        if comando.startswith("google:") or comando.startswith("buscar en google:"):
            query = raw.split(":", 1)[1].strip()
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(url)
            self._display_output(f"🔍 Buscando en Google: '{query}'")
            return
        if comando.startswith("youtube:") or comando.startswith("yt:"):
            query = raw.split(":", 1)[1].strip()
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            webbrowser.open(url)
            self._display_output(f"🎬 Buscando en YouTube: '{query}'")
            return
        if comando.startswith("wiki:") or comando.startswith("wikipedia:"):
            query = raw.split(":", 1)[1].strip()
            url = f"https://es.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}"
            webbrowser.open(url)
            self._display_output(f"📚 Buscando en Wikipedia: '{query}'")
            return
        if comando.startswith("github:"):
            query = raw.split(":", 1)[1].strip()
            url = f"https://github.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(url)
            self._display_output(f"🐙 Buscando en GitHub: '{query}'")
            return
        if comando.startswith("maps:") or comando.startswith("mapa:"):
            query = raw.split(":", 1)[1].strip()
            url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"
            webbrowser.open(url)
            self._display_output(f"🗺️ Abriendo en Google Maps: '{query}'")
            return
        if comando.startswith("traducir:") or comando.startswith("translate:"):
            query = raw.split(":", 1)[1].strip()
            url = f"https://translate.google.com/?sl=auto&tl=en&text={urllib.parse.quote(query)}"
            webbrowser.open(url)
            self._display_output(f"🌐 Abriendo Google Translate: '{query}'")
            return

        # ── ABRIR SITIOS WEB ──
        web_sites = {
            "abrir gmail": "https://mail.google.com",
            "abrir correo": "https://mail.google.com",
            "abrir drive": "https://drive.google.com",
            "abrir calendar": "https://calendar.google.com",
            "abrir calendario": "https://calendar.google.com",
            "abrir twitter": "https://twitter.com",
            "abrir x": "https://x.com",
            "abrir facebook": "https://facebook.com",
            "abrir instagram": "https://instagram.com",
            "abrir linkedin": "https://linkedin.com",
            "abrir reddit": "https://reddit.com",
            "abrir whatsapp": "https://web.whatsapp.com",
            "abrir spotify": "https://open.spotify.com",
            "abrir netflix": "https://netflix.com",
            "abrir chatgpt": "https://chat.openai.com",
            "abrir github": "https://github.com",
            "abrir stackoverflow": "https://stackoverflow.com",
        }
        for key, url in web_sites.items():
            if comando == key or comando == key.replace("abrir ", ""):
                webbrowser.open(url)
                self._display_output(f"🌐 Abriendo {key.replace('abrir ', '').title()}...")
                return

        # ── ABRIR PROGRAMAS ──
        program_opened = self._open_program(comando)
        if program_opened:
            self._display_output(program_opened)
            return

        # ── CONTROL DEL SISTEMA ──
        if comando in ("bloquear", "lock", "bloquear pc"):
            if os.name == "nt":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                self._display_output("🔒 Bloqueando equipo...")
            return
        if comando in ("apagar", "shutdown"):
            if messagebox.askyesno("Confirmar", "¿Seguro que quieres apagar el equipo?"):
                os.system("shutdown /s /t 60")
                self._display_output("⚠️ El equipo se apagará en 60 segundos.\nEscribe 'cancelar apagado' para cancelar.")
            return
        if comando in ("reiniciar", "restart", "reboot"):
            if messagebox.askyesno("Confirmar", "¿Seguro que quieres reiniciar?"):
                os.system("shutdown /r /t 60")
                self._display_output("⚠️ El equipo se reiniciará en 60 segundos.\nEscribe 'cancelar apagado' para cancelar.")
            return
        if comando in ("cancelar apagado", "cancel shutdown"):
            os.system("shutdown /a")
            self._display_output("✅ Apagado/reinicio cancelado.")
            return
        if comando in ("suspender", "sleep", "dormir"):
            if os.name == "nt":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return

        # ── DIVERSIÓN ──
        if comando in ("chiste", "joke", "hazme reír", "hazme reir", "un chiste"):
            self._display_output(f"😂 {random.choice(CHISTES)}")
            return
        if comando in ("frase", "motivación", "motivacion", "frase motivacional", "quote"):
            self._display_output(f"💬 {random.choice(FRASES_MOTIVACIONALES)}")
            return
        if comando in ("dado", "dice", "tirar dado", "lanzar dado"):
            result = random.randint(1, 6)
            dice_faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
            self._display_output(f"🎲 {dice_faces[result]}  ¡Sacaste un {result}!")
            return
        match = re.match(r"^(?:dado|dice|d)(\d+)$", comando)
        if match:
            sides = int(match.group(1))
            result = random.randint(1, max(sides, 1))
            self._display_output(f"🎲 D{sides} → ¡Sacaste un {result}!")
            return
        if comando in ("moneda", "coin", "cara o cruz", "flip"):
            result = random.choice(["🪙 ¡Cara!", "🪙 ¡Cruz!"])
            self._display_output(result)
            return
        if comando.startswith("random") or comando.startswith("aleatorio"):
            match = re.search(r"(\d+)\s*(?:a|-|y|to)\s*(\d+)", comando)
            if match:
                a, b = int(match.group(1)), int(match.group(2))
                result = random.randint(min(a, b), max(a, b))
                self._display_output(f"🎯 Número aleatorio entre {min(a,b)} y {max(a,b)}: {result}")
            else:
                self._display_output(f"🎯 Número aleatorio (1-100): {random.randint(1, 100)}")
            return
        if comando in ("8ball", "bola 8", "bola magica", "bola mágica"):
            responses = [
                "🎱 Sí, definitivamente.",
                "🎱 Sin duda alguna.",
                "🎱 Probablemente sí.",
                "🎱 Las señales apuntan a que sí.",
                "🎱 Pregunta de nuevo más tarde.",
                "🎱 No puedo predecirlo ahora.",
                "🎱 Concéntrate y pregunta de nuevo.",
                "🎱 No cuentes con ello.",
                "🎱 Mi respuesta es no.",
                "🎱 Mis fuentes dicen que no.",
                "🎱 Las perspectivas no son buenas.",
                "🎱 Muy dudoso.",
            ]
            self._display_output(random.choice(responses))
            return

        # ── SALUDOS ──
        if any(s in comando for s in ["hola", "hey", "buenas", "hi", "hello", "qué tal", "que tal"]):
            hour = datetime.datetime.now().hour
            if hour < 12:
                greeting = "Buenos días"
            elif hour < 19:
                greeting = "Buenas tardes"
            else:
                greeting = "Buenas noches"

            name = self.config.get("user_name", "")
            self._display_output(
                f"👋 ¡{greeting}{', ' + name if name and name != 'Usuario' else ''}! "
                f"Soy Jarvis, tu asistente personal.\n"
                f"   Escribe 'ayuda' para ver lo que puedo hacer."
            )
            return

        # ── ABRIR URL DIRECTA ──
        if re.match(r"^(?:https?://|www\.)\S+", comando):
            url = raw if raw.startswith("http") else f"https://{raw}"
            webbrowser.open(url)
            self._display_output(f"🌐 Abriendo: {url}")
            return

        # ── CONFIGURACIÓN ──
        if comando.startswith("config api:") or comando.startswith("api key:"):
            key = raw.split(":", 1)[1].strip()
            self.config["api_key"] = key
            DataStore.save(CONFIG_FILE, self.config)
            self.openai_client = None  # Reset client
            self._display_output("✅ API Key de OpenAI guardada correctamente.")
            return
        if comando.startswith("config nombre:") or comando.startswith("mi nombre es"):
            name = raw.split(":", 1)[1].strip() if ":" in raw else raw.replace("mi nombre es", "").strip()
            self.config["user_name"] = name
            DataStore.save(CONFIG_FILE, self.config)
            self._display_output(f"✅ ¡Hola {name}! Tu nombre ha sido guardado.")
            return
        if comando.startswith("config modelo:"):
            model = raw.split(":", 1)[1].strip()
            self.config["ai_model"] = model
            DataStore.save(CONFIG_FILE, self.config)
            self._display_output(f"✅ Modelo de IA cambiado a: {model}")
            return

        # ── HISTORIAL ──
        if comando in ("historial", "history"):
            if self.command_history:
                history = list(self.command_history)[-20:]
                lines = ["📜 Últimos comandos:\n"]
                for i, cmd in enumerate(history, 1):
                    lines.append(f"   {i}. {cmd}")
                self._display_output("\n".join(lines))
            else:
                self._display_output("📜 No hay historial de comandos.")
            return
        if comando in ("limpiar historial", "clear history"):
            self.command_history.clear()
            DataStore.save(HISTORY_FILE, [])
            self._display_output("✅ Historial limpiado.")
            return

        # ── SCREENSHOT ──
        if comando in ("screenshot", "captura", "captura de pantalla", "pantallazo"):
            self._take_screenshot()
            return

        # ── PORTAPAPELES ──
        if comando in ("clipboard", "portapapeles", "pegado"):
            try:
                content = self.root.clipboard_get()
                self._display_output(f"📋 Contenido del portapapeles:\n\n{content}")
            except Exception:
                self._display_output("📋 El portapapeles está vacío.")
            return
        if comando.startswith("copiar:") or comando.startswith("copy:"):
            text = raw.split(":", 1)[1].strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self._display_output(f"📋 Copiado al portapapeles: '{text}'")
            return

        # ── ABRIR CARPETAS ──
        if comando in ("abrir descargas", "descargas", "downloads"):
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            os.startfile(path) if os.name == "nt" else subprocess.Popen(["xdg-open", path])
            self._display_output("📂 Abriendo carpeta de Descargas...")
            return
        if comando in ("abrir documentos", "documentos", "documents"):
            path = os.path.join(os.path.expanduser("~"), "Documents")
            os.startfile(path) if os.name == "nt" else subprocess.Popen(["xdg-open", path])
            self._display_output("📂 Abriendo carpeta de Documentos...")
            return
        if comando in ("abrir escritorio", "escritorio", "desktop"):
            path = os.path.join(os.path.expanduser("~"), "Desktop")
            os.startfile(path) if os.name == "nt" else subprocess.Popen(["xdg-open", path])
            self._display_output("📂 Abriendo Escritorio...")
            return
        if comando in ("abrir home", "home", "inicio carpeta"):
            path = os.path.expanduser("~")
            os.startfile(path) if os.name == "nt" else subprocess.Popen(["xdg-open", path])
            self._display_output("📂 Abriendo carpeta Home...")
            return

        # ── COLOR PICKER ──
        if comando in ("color", "color picker", "selector de color"):
            color = colorchooser.askcolor(title="Selecciona un color")
            if color and color[1]:
                rgb = color[0]
                hex_color = color[1]
                self._display_output(
                    f"🎨 Color seleccionado:\n"
                    f"   HEX: {hex_color}\n"
                    f"   RGB: ({int(rgb[0])}, {int(rgb[1])}, {int(rgb[2])})"
                )
            return

        # ── LOREM IPSUM ──
        if comando in ("lorem", "lorem ipsum"):
            lorem = (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
                "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
                "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
                "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
                "culpa qui officia deserunt mollit anim id est laborum."
            )
            self._display_output(f"📝 {lorem}")
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(lorem)
                self._display_output("   (Copiado al portapapeles)", "muted")
            except Exception:
                pass
            return

        # ── IA (ChatGPT) ──
        if comando.startswith("ia:") or comando.startswith("ai:") or comando.startswith("gpt:"):
            question = raw.split(":", 1)[1].strip()
            if question:
                self._ask_ai(question)
            else:
                self._display_output("⚠️ Escribe tu pregunta después de 'ia:'", "error")
            return

        # ── COMANDO NO RECONOCIDO ──
        self._display_output(
            f"❓ Comando no reconocido: '{raw}'\n"
            f"   Escribe 'ayuda' para ver los comandos disponibles.\n"
            f"   Usa 'ia: tu pregunta' para preguntar a la IA.",
            "info"
        )

    # ─────────────────────────────────────────────────
    # ABRIR PROGRAMAS
    # ─────────────────────────────────────────────────

    def _open_program(self, comando):
        """Abrir aplicaciones del sistema."""
        programs = {
            "chrome": ("start chrome", "🌐 Abriendo Google Chrome..."),
            "firefox": ("start firefox", "🦊 Abriendo Firefox..."),
            "edge": ("start msedge", "🌐 Abriendo Microsoft Edge..."),
            "brave": ("start brave", "🦁 Abriendo Brave..."),
            "notepad": ("start notepad", "📝 Abriendo Bloc de notas..."),
            "bloc": ("start notepad", "📝 Abriendo Bloc de notas..."),
            "calculadora": ("start calc", "🧮 Abriendo Calculadora..."),
            "calc": ("start calc", "🧮 Abriendo Calculadora..."),
            "explorador": ("start explorer", "📂 Abriendo Explorador de archivos..."),
            "explorer": ("start explorer", "📂 Abriendo Explorador de archivos..."),
            "cmd": ("start cmd", "💻 Abriendo CMD..."),
            "terminal": ("start wt", "💻 Abriendo Terminal..."),
            "powershell": ("start powershell", "💻 Abriendo PowerShell..."),
            "paint": ("start mspaint", "🎨 Abriendo Paint..."),
            "word": ("start winword", "📄 Abriendo Word..."),
            "excel": ("start excel", "📊 Abriendo Excel..."),
            "powerpoint": ("start powerpnt", "📽️ Abriendo PowerPoint..."),
            "outlook": ("start outlook", "📧 Abriendo Outlook..."),
            "teams": ("start msteams:", "💬 Abriendo Teams..."),
            "vscode": ("start code", "💻 Abriendo VS Code..."),
            "code": ("start code", "💻 Abriendo VS Code..."),
            "spotify": ("start spotify:", "🎵 Abriendo Spotify..."),
            "discord": ("start discord:", "🎮 Abriendo Discord..."),
            "steam": ("start steam:", "🎮 Abriendo Steam..."),
            "task manager": ("start taskmgr", "📊 Abriendo Administrador de tareas..."),
            "administrador de tareas": ("start taskmgr", "📊 Abriendo Administrador de tareas..."),
            "configuración": ("start ms-settings:", "⚙️ Abriendo Configuración..."),
            "config windows": ("start ms-settings:", "⚙️ Abriendo Configuración..."),
            "panel de control": ("start control", "⚙️ Abriendo Panel de Control..."),
            "snipping": ("start snippingtool", "✂️ Abriendo Recortes..."),
        }

        # Buscar en el comando
        for key, (cmd, msg) in programs.items():
            if key in comando and ("abrir" in comando or "abre" in comando or "open" in comando or key == comando):
                try:
                    if os.name == "nt":
                        os.system(cmd)
                    else:
                        subprocess.Popen(cmd.replace("start ", ""), shell=True)
                    return msg
                except Exception as e:
                    return f"⚠️ Error al abrir: {e}"

        return None

    # ─────────────────────────────────────────────────
    # NOTAS
    # ─────────────────────────────────────────────────

    def _add_note(self, text):
        note = {
            "id": int(time.time() * 1000),
            "text": text,
            "date": datetime.datetime.now().isoformat(),
        }
        self.notes.append(note)
        DataStore.save(NOTES_FILE, self.notes)
        self._display_output(f"📝 Nota guardada: '{text}'")

    def _show_notes(self):
        if not self.notes:
            self._display_output("📝 No tienes notas guardadas.\n   Usa 'nota: tu texto' para crear una.")
            return
        lines = [f"📝 Tus notas ({len(self.notes)}):\n"]
        for i, note in enumerate(self.notes, 1):
            date = datetime.datetime.fromisoformat(note["date"]).strftime("%d/%m %H:%M")
            lines.append(f"   {i}. [{date}] {note['text']}")
        lines.append(f"\n   Usa 'borrar nota [número]' para eliminar.")
        self._display_output("\n".join(lines))

    def _delete_note(self, comando):
        match = re.search(r"(\d+)", comando)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(self.notes):
                removed = self.notes.pop(idx)
                DataStore.save(NOTES_FILE, self.notes)
                self._display_output(f"🗑️ Nota eliminada: '{removed['text']}'")
            else:
                self._display_output("⚠️ Número de nota inválido.", "error")
        else:
            self._display_output("⚠️ Especifica el número: 'borrar nota 1'", "error")

    # ─────────────────────────────────────────────────
    # TAREAS
    # ─────────────────────────────────────────────────

    def _add_todo(self, text):
        todo = {
            "id": int(time.time() * 1000),
            "text": text,
            "done": False,
            "date": datetime.datetime.now().isoformat(),
        }
        self.todos.append(todo)
        DataStore.save(TODOS_FILE, self.todos)
        pending = len([t for t in self.todos if not t["done"]])
        self._display_output(f"✅ Tarea añadida: '{text}'\n   Tareas pendientes: {pending}")

    def _show_todos(self):
        if not self.todos:
            self._display_output("✅ No tienes tareas.\n   Usa 'tarea: tu tarea' para crear una.")
            return
        pending = [t for t in self.todos if not t["done"]]
        completed = [t for t in self.todos if t["done"]]

        lines = [f"✅ Tareas ({len(pending)} pendientes, {len(completed)} completadas):\n"]

        if pending:
            lines.append("   PENDIENTES:")
            for i, t in enumerate(self.todos):
                if not t["done"]:
                    lines.append(f"   {i+1}. ⬜ {t['text']}")

        if completed:
            lines.append("\n   COMPLETADAS:")
            for i, t in enumerate(self.todos):
                if t["done"]:
                    lines.append(f"   {i+1}. ✅ {t['text']}")

        lines.append(f"\n   Usa 'completar [número]' o 'borrar tarea [número]'")
        self._display_output("\n".join(lines))

    def _complete_todo(self, index):
        idx = index - 1
        if 0 <= idx < len(self.todos):
            self.todos[idx]["done"] = True
            DataStore.save(TODOS_FILE, self.todos)
            self._display_output(f"🎉 ¡Tarea completada: '{self.todos[idx]['text']}'!")
        else:
            self._display_output("⚠️ Número de tarea inválido.", "error")

    def _delete_todo(self, comando):
        match = re.search(r"(\d+)", comando)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(self.todos):
                removed = self.todos.pop(idx)
                DataStore.save(TODOS_FILE, self.todos)
                self._display_output(f"🗑️ Tarea eliminada: '{removed['text']}'")
            else:
                self._display_output("⚠️ Número de tarea inválido.", "error")
        else:
            self._display_output("⚠️ Especifica el número: 'borrar tarea 1'", "error")

    # ─────────────────────────────────────────────────
    # RECORDATORIOS
    # ─────────────────────────────────────────────────

    def _show_reminders(self):
        self._display_output(self.reminder_system.list_active())

    def _on_reminder(self, text):
        """Callback cuando un recordatorio se activa."""
        def show():
            self._display_output(
                f"🔔 ¡RECORDATORIO!\n"
                f"═══════════════════════════\n"
                f"   {text}\n"
                f"═══════════════════════════",
                "info"
            )
            try:
                messagebox.showinfo("⏰ Recordatorio", text)
            except Exception:
                pass
        self.root.after(0, show)

    # ─────────────────────────────────────────────────
    # IA / CHATGPT
    # ─────────────────────────────────────────────────

    def _ask_ai(self, question):
        """Envía pregunta a OpenAI."""
        api_key = self.config.get("api_key", "")
        if not api_key or api_key == "PEGA_AQUI_TU_API_KEY":
            self._display_output(
                "⚠️ API Key no configurada.\n"
                "   Usa: config api: TU_API_KEY\n"
                "   Obtén una en: https://platform.openai.com/api-keys",
                "error"
            )
            return

        self._display_output("🤖 Pensando...", "info")
        self.root.update()

        def query():
            try:
                if not self.openai_client:
                    from openai import OpenAI
                    self.openai_client = OpenAI(api_key=api_key)

                model = self.config.get("ai_model", "gpt-4o-mini")
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Eres Jarvis, un asistente inteligente, profesional y amigable. "
                                "Responde de forma clara y concisa en español. "
                                "Usa emojis cuando sea apropiado."
                            )
                        },
                        {"role": "user", "content": question}
                    ],
                    max_tokens=1000,
                )
                answer = response.choices[0].message.content
                self.root.after(0, lambda: self._display_output(f"🧠 {answer}"))
            except Exception as e:
                self.root.after(0, lambda: self._display_output(
                    f"⚠️ Error con IA: {e}", "error"
                ))

        threading.Thread(target=query, daemon=True).start()

    # ─────────────────────────────────────────────────
    # SCREENSHOT
    # ─────────────────────────────────────────────────

    def _take_screenshot(self):
        """Toma una captura de pantalla."""
        try:
            from PIL import ImageGrab
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
            img = ImageGrab.grab()
            img.save(path)
            self._display_output(f"📸 Captura guardada en:\n   {path}")
        except ImportError:
            # Fallback usando PowerShell en Windows
            if os.name == "nt":
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
                ps_cmd = (
                    f'Add-Type -AssemblyName System.Windows.Forms; '
                    f'[System.Windows.Forms.Screen]::PrimaryScreen | ForEach-Object {{ '
                    f'$bmp = New-Object System.Drawing.Bitmap($_.Bounds.Width, $_.Bounds.Height); '
                    f'$g = [System.Drawing.Graphics]::FromImage($bmp); '
                    f'$g.CopyFromScreen($_.Bounds.Location, [System.Drawing.Point]::Empty, $_.Bounds.Size); '
                    f'$bmp.Save("{path}") }}'
                )
                os.system(f'powershell -command "{ps_cmd}"')
                self._display_output(f"📸 Captura guardada en:\n   {path}")
            else:
                self._display_output(
                    "⚠️ Instala Pillow para capturas:\n   pip install Pillow", "error"
                )

    # ─────────────────────────────────────────────────
    # UTILIDADES ASYNC
    # ─────────────────────────────────────────────────

    def _run_async(self, func):
        """Ejecuta una función en un hilo separado."""
        self._display_output("⏳ Procesando...", "info")
        self.root.update()

        def run():
            result = func()
            self.root.after(0, lambda: self._display_output(result))

        threading.Thread(target=run, daemon=True).start()

    # ─────────────────────────────────────────────────
    # AYUDA
    # ─────────────────────────────────────────────────

    def _show_help(self):
        help_text = """
═══════════════════════════════════════════════════════
  📖 JARVIS PRO ULTRA — GUÍA DE COMANDOS
═══════════════════════════════════════════════════════

  🤖 INTELIGENCIA ARTIFICIAL
  ─────────────────────────
  ia: [pregunta]          Preguntar a ChatGPT
  config api: [key]       Configurar API Key de OpenAI
  config modelo: [modelo] Cambiar modelo (gpt-4o-mini, gpt-4o)

  📋 PRODUCTIVIDAD
  ─────────────────────────
  briefing                Resumen diario
  nota: [texto]           Guardar una nota
  notas                   Ver todas las notas
  borrar nota [n]         Eliminar nota
  tarea: [texto]          Crear tarea
  tareas                  Ver tareas
  completar [n]           Marcar tarea como hecha
  borrar tarea [n]        Eliminar tarea

  ⏰ TIEMPO
  ─────────────────────────
  hora / fecha            Ver hora o fecha actual
  recordar: [texto] en [min]  Crear recordatorio
  recordatorios           Ver recordatorios activos
  iniciar cronómetro      Iniciar cronómetro
  parar cronómetro        Detener cronómetro
  reiniciar cronómetro    Reiniciar cronómetro
  temporizador [min]      Iniciar temporizador

  🧮 CÁLCULOS
  ─────────────────────────
  calc: [expresión]       Calculadora (ej: calc: 2^10)
  [expresión numérica]    Auto-detecta (ej: 5+3*2)
  convertir: 10 km a mi   Convertir unidades
  dias para 25/12         Calcular días hasta fecha
  hoy +30 dias            Fecha en N días

  💻 SISTEMA
  ─────────────────────────
  sistema / cpu / disco   Info del sistema
  red / ip                Info de red + IP pública
  buscar: [archivo]       Buscar archivos
  screenshot              Captura de pantalla
  clipboard               Ver portapapeles
  copiar: [texto]         Copiar al portapapeles
  bloquear                Bloquear PC
  apagar / reiniciar      Apagar/reiniciar PC

  🌐 WEB Y BÚSQUEDAS
  ─────────────────────────
  google: [texto]         Buscar en Google
  youtube: [texto]        Buscar en YouTube
  wiki: [texto]           Buscar en Wikipedia
  github: [texto]         Buscar en GitHub
  maps: [lugar]           Abrir en Google Maps
  traducir: [texto]       Google Translate
  gmail / drive / etc.    Abrir sitios web

  📂 PROGRAMAS Y CARPETAS
  ─────────────────────────
  abrir chrome/firefox/edge/vscode/calc/paint...
  descargas / documentos / escritorio
  (15+ programas soportados)

  🔐 SEGURIDAD
  ─────────────────────────
  password [largo]        Generar contraseña
  hash: [texto]           Generar MD5/SHA1/SHA256
  base64 encode: [texto]  Codificar en Base64
  base64 decode: [texto]  Decodificar Base64

  🔤 TEXTO
  ─────────────────────────
  mayusculas: [texto]     Convertir a MAYÚSCULAS
  minusculas: [texto]     Convertir a minúsculas
  titulo: [texto]         Convertir a Título
  invertir: [texto]       Invertir texto
  contar: [texto]         Estadísticas del texto
  lorem                   Generar Lorem Ipsum

  🎮 DIVERSIÓN
  ─────────────────────────
  chiste                  Contar un chiste
  frase                   Frase motivacional
  dado / d20              Lanzar dado (6 o N caras)
  moneda                  Cara o cruz
  random 1 a 100          Número aleatorio
  8ball                   Bola mágica

  🎨 OTROS
  ─────────────────────────
  color                   Selector de color (HEX/RGB)
  config nombre: [nombre] Guardar tu nombre
  historial               Ver historial de comandos
  cls / clear             Limpiar pantalla
  salir                   Cerrar Jarvis

  ⌨️ ATAJOS DE TECLADO
  ─────────────────────────
  Enter                   Enviar comando
  ↑ / ↓                   Navegar historial
  Esc                     Enfocar entrada

═══════════════════════════════════════════════════════
"""
        self._display_output(help_text)

    # ─────────────────────────────────────────────────
    # CIERRE
    # ─────────────────────────────────────────────────

    def _on_close(self):
        """Guardar datos y cerrar."""
        self.reminder_system.stop()
        DataStore.save(NOTES_FILE, self.notes)
        DataStore.save(TODOS_FILE, self.todos)
        DataStore.save(HISTORY_FILE, list(self.command_history))
        DataStore.save(CONFIG_FILE, self.config)
        self.root.destroy()


# ══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisApp(root)
    root.mainloop()
