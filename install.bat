@echo off
chcp 65001 >nul 2>&1
title ╔══ JARVIS AI ASSISTANT - INSTALLER ══╗
color 0B

echo.
echo   ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
echo   ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
echo   ██║███████║██████╔╝██║   ██║██║███████╗
echo   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
echo   ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
echo   ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
echo.
echo   ════════════════════════════════════════
echo     INSTALADOR AUTOMATICO - J.A.R.V.I.S.
echo   ════════════════════════════════════════
echo.

:: Check Python
echo   [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo   ╔══════════════════════════════════════════════╗
    echo   ║  ERROR: Python no encontrado                 ║
    echo   ║                                              ║
    echo   ║  Descargalo aqui:                            ║
    echo   ║  https://www.python.org/downloads/           ║
    echo   ║                                              ║
    echo   ║  IMPORTANTE: Marca "Add Python to PATH"      ║
    echo   ║  durante la instalacion                      ║
    echo   ╚══════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo   OK: %%i

:: Install dependencies
echo.
echo   [2/5] Instalando dependencias...
echo         (esto puede tomar 1-2 minutos)
echo.
pip install openai pyaudio edge-tts pyttsx3 SpeechRecognition psutil opencv-python >nul 2>&1
if %errorlevel% neq 0 (
    echo   Intentando instalar una por una...
    pip install openai >nul 2>&1
    echo     - openai OK
    pip install edge-tts >nul 2>&1
    echo     - edge-tts OK
    pip install pyttsx3 >nul 2>&1
    echo     - pyttsx3 OK
    pip install SpeechRecognition >nul 2>&1
    echo     - SpeechRecognition OK
    pip install psutil >nul 2>&1
    echo     - psutil OK
    pip install opencv-python >nul 2>&1
    echo     - opencv-python OK
    pip install pyaudio >nul 2>&1 || echo     - pyaudio (opcional, para microfono)
)
echo   OK: Dependencias instaladas

:: Download Jarvis
echo.
echo   [3/5] Descargando Jarvis...
set JARVIS_DIR=%USERPROFILE%\Downloads\jarvis-ai-assistant
if not exist "%JARVIS_DIR%" mkdir "%JARVIS_DIR%"

:: Try git clone first, fallback to curl
git --version >nul 2>&1
if %errorlevel% equ 0 (
    if not exist "%JARVIS_DIR%\.git" (
        git clone https://github.com/cookiecodespy/jarvis-ai-assistant.git "%JARVIS_DIR%" >nul 2>&1
    ) else (
        cd /d "%JARVIS_DIR%"
        git pull >nul 2>&1
    )
) else (
    curl -L -o "%JARVIS_DIR%\jarvis_god_mode.py" "https://raw.githubusercontent.com/cookiecodespy/jarvis-ai-assistant/master/jarvis_god_mode.py" 2>nul
)
echo   OK: Jarvis descargado en %JARVIS_DIR%

:: API Key setup
echo.
echo   [4/5] Configuracion de IA (GRATIS)
echo.
echo   ════════════════════════════════════════
echo   Necesitas una API key GRATUITA.
echo   Elige tu proveedor favorito:
echo.
echo   OPCION 1 - GROQ (recomendado, rapido):
echo     1. Ve a: https://console.groq.com/keys
echo     2. Crea cuenta con Google
echo     3. Click "Create API Key"
echo     4. Copia la key
echo.
echo   OPCION 2 - GEMINI (Google, muy generoso):
echo     1. Ve a: https://aistudio.google.com/apikey
echo     2. "Create API Key"
echo     3. Copia la key
echo.
echo   OPCION 3 - OPENROUTER (modelos ilimitados):
echo     1. Ve a: https://openrouter.ai/keys
echo     2. Crea cuenta
echo     3. Copia la key
echo   ════════════════════════════════════════
echo.

set /p PROVIDER="  Que proveedor? (groq/gemini/openrouter) [groq]: "
if "%PROVIDER%"=="" set PROVIDER=groq

set /p API_KEY="  Pega tu API key aqui: "

if "%API_KEY%"=="" (
    echo.
    echo   Sin API key. Puedes configurarla despues en Jarvis:
    echo     config proveedor: groq
    echo     config api: TU_KEY
) else (
    :: Save config
    set CONFIG_DIR=%USERPROFILE%\.jarvis_god
    if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"
    echo {"provider": "%PROVIDER%", "api_key": "%API_KEY%", "user_name": "señor", "theme": "edex", "voice_enabled": true, "edge_voice": "es-CL-CatalinaNeural", "typewriter": true, "sound_fx": true} > "%CONFIG_DIR%\config.json"
    echo   OK: Configuracion guardada
)

:: Create desktop shortcut
echo.
echo   [5/5] Creando acceso directo en Escritorio...
echo @echo off > "%USERPROFILE%\Desktop\Jarvis.bat"
echo title JARVIS AI Assistant >> "%USERPROFILE%\Desktop\Jarvis.bat"
echo cd /d "%JARVIS_DIR%" >> "%USERPROFILE%\Desktop\Jarvis.bat"
echo python jarvis_god_mode.py >> "%USERPROFILE%\Desktop\Jarvis.bat"
echo pause >> "%USERPROFILE%\Desktop\Jarvis.bat"
echo   OK: Acceso directo creado en el Escritorio

:: Done!
echo.
echo   ════════════════════════════════════════════
echo.
echo   ╔══════════════════════════════════════════╗
echo   ║  INSTALACION COMPLETADA                  ║
echo   ║                                          ║
echo   ║  Para abrir Jarvis:                      ║
echo   ║    - Doble click en "Jarvis" en tu       ║
echo   ║      escritorio                          ║
echo   ║    - O abre terminal y escribe:          ║
echo   ║      python jarvis_god_mode.py           ║
echo   ║                                          ║
echo   ║  Comandos utiles:                        ║
echo   ║    help     - ver todos los comandos     ║
echo   ║    modelos  - ver modelos de IA          ║
echo   ║    mi dia   - resumen del dia            ║
echo   ╚══════════════════════════════════════════╝
echo.

set /p LAUNCH="  Quieres abrir Jarvis ahora? (s/n) [s]: "
if "%LAUNCH%"=="" set LAUNCH=s
if /i "%LAUNCH%"=="s" (
    cd /d "%JARVIS_DIR%"
    python jarvis_god_mode.py
)

pause
