import tkinter as tk
from tkinter import messagebox
import time
import os
from openai import OpenAI

# ----------------------------
# CONFIG CHATGPT (Nivel 4)
# ----------------------------

API_KEY = "PEGA_AQUI_TU_API_KEY"

client = OpenAI(api_key=API_KEY)

# ----------------------------
# FUNCIONES PRINCIPALES
# ----------------------------

def actualizar_reloj():
    hora = time.strftime("%H:%M:%S")
    reloj.config(text=hora)
    ventana.after(1000, actualizar_reloj)


def abrir_programa(comando):
    """Nivel 3: Abrir aplicaciones reales"""

    if "chrome" in comando:
        os.system("start chrome")
        return "🌐 Abriendo Google Chrome..."

    elif "bloc" in comando or "notepad" in comando:
        os.system("start notepad")
        return "📝 Abriendo Bloc de notas..."

    elif "calculadora" in comando:
        os.system("start calc")
        return "🧮 Abriendo Calculadora..."

    else:
        return None


def preguntar_ia(texto):
    """Nivel 4: Respuesta con ChatGPT real"""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres Jarvis, un asistente inteligente y profesional."},
                {"role": "user", "content": texto}
            ]
        )

        return respuesta.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error con IA: {e}"


def responder():
    comando = entrada.get().lower()

    if comando == "":
        return

    # SALIR
    if "salir" in comando:
        ventana.destroy()
        return

    # NIVEL 3: Abrir programas
    respuesta_programa = abrir_programa(comando)
    if respuesta_programa:
        salida.config(text=respuesta_programa)
        entrada.delete(0, tk.END)
        return

    # NIVEL 4: IA
    if comando.startswith("ia:"):
        pregunta = comando.replace("ia:", "").strip()
        salida.config(text="🤖 Pensando...")
        ventana.update()

        respuesta_ia = preguntar_ia(pregunta)
        salida.config(text="🧠 " + respuesta_ia)

        entrada.delete(0, tk.END)
        return

    # RESPUESTA NORMAL
    if "hola" in comando:
        salida.config(text="👋 Hola Jean, listo para ayudarte.")
    elif "hora" in comando:
        salida.config(text=f"🕒 Son las {time.strftime('%H:%M:%S')}")
    else:
        salida.config(text="❓ Comando no reconocido. Usa 'ia:' para preguntas.")

    entrada.delete(0, tk.END)


def info():
    messagebox.showinfo(
        "Jarvis AI PRO",
        "Nivel 3: Abre programas\n"
        "Nivel 4: IA con ChatGPT\n\n"
        "Ejemplo:\n"
        "abre chrome\n"
        "ia: que es una IP?"
    )

# ----------------------------
# INTERFAZ
# ----------------------------

ventana = tk.Tk()
ventana.title("Jarvis AI PRO")
ventana.geometry("600x450")
ventana.configure(bg="#111827")

titulo = tk.Label(
    ventana,
    text="🤖 JARVIS AI PRO",
    font=("Consolas", 24, "bold"),
    fg="#38BDF8",
    bg="#111827"
)
titulo.pack(pady=15)

reloj = tk.Label(
    ventana,
    font=("Consolas", 18),
    fg="white",
    bg="#111827"
)
reloj.pack()

salida = tk.Label(
    ventana,
    text="Escribe un comando...",
    font=("Arial", 14),
    fg="#E5E7EB",
    bg="#111827",
    wraplength=520
)
salida.pack(pady=25)

entrada = tk.Entry(
    ventana,
    font=("Arial", 14),
    justify="center",
    width=35
)
entrada.pack(pady=10)

boton = tk.Button(
    ventana,
    text="Enviar 🚀",
    font=("Arial", 12, "bold"),
    bg="#38BDF8",
    fg="black",
    command=responder
)
boton.pack(pady=10)

boton_info = tk.Button(
    ventana,
    text="ℹ️ Info",
    font=("Arial", 10),
    command=info
)
boton_info.pack()

actualizar_reloj()
ventana.mainloop()