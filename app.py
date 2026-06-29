import streamlit as st
import os
import tempfile
import time
import json
import urllib.parse
import random

# ---- Check if pyttsx3 is available ----
try:
    import pyttsx3
    PYTTTSX3_AVAILABLE = True
except ImportError:
    PYTTTSX3_AVAILABLE = False

# ---- Language support ----
LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "es": "Español",
    "pt": "Português",
    "zh": "中文 (Chinese)"
}

# ---- Translations (full) ----
TRANSLATIONS = {
    "en": {
        "app_title": "Robotic Control Center",
        "app_subtitle": "Select a robot, command it, and watch it perform – built by GlobalInternet.py",
        "live_sim": "● LIVE SIMULATION",
        "robot_selection": "🤖 Robot Selection",
        "kata_performance": "🥋 Kata Performance",
        "commands": "🎮 Commands",
        "cmd_desc": "Walk and Run loop continuously. Jump, Wave, Frontflip, Backflip, Bow play once.",
        "cmd_hint": "You can also type a kata name (e.g., `Taikyoku Shodan`) to run the full sequence.",
        "action_placeholder": "e.g., backflip or Taikyoku Shodan",
        "execute_action": "▶️ Execute Action",
        "soccer_play": "⚽ Play Soccer (Circle)",
        "speech": "🗣️ Speech",
        "speak_placeholder": "e.g., Hello, I am your robot.",
        "speak_button": "🔊 Make Robot Speak",
        "contact": "📞 Contact",
        "status": "🔧 Status",
        "current_robot": "Current Robot",
        "last_action": "Last Action",
        "kata": "Kata",
        "backstage": "📜 Backstage – Command History",
        "no_commands": "No commands yet. Send a command from the sidebar.",
        "footer_line1": "© 2026 GlobalInternet.py Online Software Company",
        "footer_line2": "Built by <strong>Gesner Deslandes</strong> | (509) 4738-5663 | deslandes78@gmail.com",
        "footer_line3": "🤖 Simulated robot control – ready for real-world hardware integration.",
        "speech_failed": "❌ Speech generation failed. Please ensure pyttsx3 or gTTS is installed.",
        "speech_warning": "Please enter text to speak.",
        "action_warning": "Please enter an action or kata name.",
        "active_kata": "Active Kata",
        "belt": "Belt",
        "robot_view": "🖥️ Robot View",
        "none": "None",
        "select_kata": "Select Kata",
        "select_robot": "Select Robot",
        "language": "🌐 Language",
        "voice_gender": "🎤 Voice Gender",
        "male": "Male",
        "female": "Female",
        "email": "Email",
        "phone": "Phone",
        "website": "Website",
        "contact_info": "Contact Information",
        "status_current_robot": "Current Robot:",
        "status_last_action": "Last Action:",
        "status_kata": "Kata:",
        "speaking": "Speaking:",
        "replay_voice": "🔁 Replay Voice",
        "gender_note": "Gender selection requires pyttsx3. Using gTTS (gender‑neutral) as fallback.",
        "gender_enabled": "✅ Voice gender: {} voice enabled",
        "gender_unavailable": "⚠️ pyttsx3 not available – gender selection ignored. Using gTTS (gender‑neutral).",
    },
    "fr": {
        "app_title": "Centre de Contrôle Robotique",
        "app_subtitle": "Sélectionnez un robot, commandez-le et regardez-le agir – construit par GlobalInternet.py",
        "live_sim": "● SIMULATION EN DIRECT",
        "robot_selection": "🤖 Sélection du robot",
        "kata_performance": "🥋 Performance Kata",
        "commands": "🎮 Commandes",
        "cmd_desc": "Marche et Course en boucle continue. Saut, Salut, Saut périlleux avant, Saut périlleux arrière, Salutation joués une fois.",
        "cmd_hint": "Vous pouvez aussi taper un nom de kata (ex: `Taikyoku Shodan`) pour exécuter la séquence complète.",
        "action_placeholder": "ex: backflip ou Taikyoku Shodan",
        "execute_action": "▶️ Exécuter l'action",
        "soccer_play": "⚽ Jouer au foot (cercle)",
        "speech": "🗣️ Parole",
        "speak_placeholder": "ex: Bonjour, je suis votre robot.",
        "speak_button": "🔊 Faire parler le robot",
        "contact": "📞 Contact",
        "status": "🔧 Statut",
        "current_robot": "Robot actuel",
        "last_action": "Dernière action",
        "kata": "Kata",
        "backstage": "📜 Coulisses – Historique des commandes",
        "no_commands": "Aucune commande pour l'instant. Envoyez une commande depuis la barre latérale.",
        "footer_line1": "© 2026 GlobalInternet.py Online Software Company",
        "footer_line2": "Construit par <strong>Gesner Deslandes</strong> | (509) 4738-5663 | deslandes78@gmail.com",
        "footer_line3": "🤖 Contrôle robotique simulé – prêt pour l'intégration matérielle réelle.",
        "speech_failed": "❌ Échec de la génération vocale. Veuillez vous assurer que pyttsx3 ou gTTS est installé.",
        "speech_warning": "Veuillez entrer du texte à prononcer.",
        "action_warning": "Veuillez entrer une action ou un nom de kata.",
        "active_kata": "Kata actif",
        "belt": "Ceinture",
        "robot_view": "🖥️ Vue du robot",
        "none": "Aucun",
        "select_kata": "Sélectionner un kata",
        "select_robot": "Sélectionner un robot",
        "language": "🌐 Langue",
        "voice_gender": "🎤 Genre de voix",
        "male": "Masculin",
        "female": "Féminin",
        "email": "Email",
        "phone": "Téléphone",
        "website": "Site web",
        "contact_info": "Coordonnées",
        "status_current_robot": "Robot actuel :",
        "status_last_action": "Dernière action :",
        "status_kata": "Kata :",
        "speaking": "Parle :",
        "replay_voice": "🔁 Rejouer la voix",
        "gender_note": "La sélection du genre nécessite pyttsx3. Utilisation de gTTS (genre neutre) comme secours.",
        "gender_enabled": "✅ Voix {} activée",
        "gender_unavailable": "⚠️ pyttsx3 non disponible – la sélection du genre est ignorée. Utilisation de gTTS (genre neutre).",
    },
    "es": {
        "app_title": "Centro de Control Robótico",
        "app_subtitle": "Seleccione un robot, comándelo y observe su rendimiento – construido por GlobalInternet.py",
        "live_sim": "● SIMULACIÓN EN VIVO",
        "robot_selection": "🤖 Selección de robot",
        "kata_performance": "🥋 Rendimiento Kata",
        "commands": "🎮 Comandos",
        "cmd_desc": "Caminar y Correr en bucle continuo. Saltar, Saludar, Mortal hacia adelante, Mortal hacia atrás, Inclinación se ejecutan una vez.",
        "cmd_hint": "También puede escribir un nombre de kata (ej: `Taikyoku Shodan`) para ejecutar la secuencia completa.",
        "action_placeholder": "ej: backflip o Taikyoku Shodan",
        "execute_action": "▶️ Ejecutar acción",
        "soccer_play": "⚽ Jugar al fútbol (círculo)",
        "speech": "🗣️ Voz",
        "speak_placeholder": "ej: Hola, soy su robot.",
        "speak_button": "🔊 Hacer hablar al robot",
        "contact": "📞 Contacto",
        "status": "🔧 Estado",
        "current_robot": "Robot actual",
        "last_action": "Última acción",
        "kata": "Kata",
        "backstage": "📜 Bastidores – Historial de comandos",
        "no_commands": "Aún no hay comandos. Envíe un comando desde la barra lateral.",
        "footer_line1": "© 2026 GlobalInternet.py Online Software Company",
        "footer_line2": "Construido por <strong>Gesner Deslandes</strong> | (509) 4738-5663 | deslandes78@gmail.com",
        "footer_line3": "🤖 Control robótico simulado – listo para la integración con hardware real.",
        "speech_failed": "❌ Error en la generación de voz. Asegúrese de que pyttsx3 o gTTS esté instalado.",
        "speech_warning": "Por favor, ingrese texto para hablar.",
        "action_warning": "Por favor, ingrese una acción o nombre de kata.",
        "active_kata": "Kata activo",
        "belt": "Cinturón",
        "robot_view": "🖥️ Vista del robot",
        "none": "Ninguno",
        "select_kata": "Seleccionar Kata",
        "select_robot": "Seleccionar Robot",
        "language": "🌐 Idioma",
        "voice_gender": "🎤 Género de voz",
        "male": "Masculino",
        "female": "Femenino",
        "email": "Correo electrónico",
        "phone": "Teléfono",
        "website": "Sitio web",
        "contact_info": "Información de contacto",
        "status_current_robot": "Robot actual:",
        "status_last_action": "Última acción:",
        "status_kata": "Kata:",
        "speaking": "Hablando:",
        "replay_voice": "🔁 Repetir voz",
        "gender_note": "La selección de género requiere pyttsx3. Usando gTTS (neutral) como alternativa.",
        "gender_enabled": "✅ Voz {} activada",
        "gender_unavailable": "⚠️ pyttsx3 no disponible – selección de género ignorada. Usando gTTS (neutral).",
    },
    "pt": {
        "app_title": "Centro de Controle Robótico",
        "app_subtitle": "Selecione um robô, comande-o e veja-o atuar – construído por GlobalInternet.py",
        "live_sim": "● SIMULAÇÃO AO VIVO",
        "robot_selection": "🤖 Seleção de Robô",
        "kata_performance": "🥋 Performance Kata",
        "commands": "🎮 Comandos",
        "cmd_desc": "Andar e Correr em loop contínuo. Pular, Acenar, Mortal para frente, Mortal para trás, Reverência executados uma vez.",
        "cmd_hint": "Você também pode digitar um nome de kata (ex: `Taikyoku Shodan`) para executar a sequência completa.",
        "action_placeholder": "ex: backflip ou Taikyoku Shodan",
        "execute_action": "▶️ Executar Ação",
        "soccer_play": "⚽ Jogar futebol (círculo)",
        "speech": "🗣️ Fala",
        "speak_placeholder": "ex: Olá, eu sou o seu robô.",
        "speak_button": "🔊 Fazer o Robô Falar",
        "contact": "📞 Contato",
        "status": "🔧 Status",
        "current_robot": "Robô atual",
        "last_action": "Última ação",
        "kata": "Kata",
        "backstage": "📜 Bastidores – Histórico de Comandos",
        "no_commands": "Nenhum comando ainda. Envie um comando pela barra lateral.",
        "footer_line1": "© 2026 GlobalInternet.py Online Software Company",
        "footer_line2": "Construído por <strong>Gesner Deslandes</strong> | (509) 4738-5663 | deslandes78@gmail.com",
        "footer_line3": "🤖 Controle robótico simulado – pronto para integração com hardware real.",
        "speech_failed": "❌ Falha na geração de fala. Verifique se pyttsx3 ou gTTS está instalado.",
        "speech_warning": "Por favor, insira texto para falar.",
        "action_warning": "Por favor, insira uma ação ou nome de kata.",
        "active_kata": "Kata ativo",
        "belt": "Faixa",
        "robot_view": "🖥️ Visão do Robô",
        "none": "Nenhum",
        "select_kata": "Selecionar Kata",
        "select_robot": "Selecionar Robô",
        "language": "🌐 Idioma",
        "voice_gender": "🎤 Gênero de voz",
        "male": "Masculino",
        "female": "Feminino",
        "email": "E-mail",
        "phone": "Telefone",
        "website": "Site",
        "contact_info": "Informações de Contato",
        "status_current_robot": "Robô atual:",
        "status_last_action": "Última ação:",
        "status_kata": "Kata:",
        "speaking": "Falando:",
        "replay_voice": "🔁 Repetir Voz",
        "gender_note": "A seleção de gênero requer pyttsx3. Usando gTTS (neutro) como fallback.",
        "gender_enabled": "✅ Voz {} ativada",
        "gender_unavailable": "⚠️ pyttsx3 não disponível – seleção de gênero ignorada. Usando gTTS (neutro).",
    },
    "zh": {
        "app_title": "机器人控制中心",
        "app_subtitle": "选择机器人，发出指令，观看表演 – 由 GlobalInternet.py 构建",
        "live_sim": "● 实时模拟",
        "robot_selection": "🤖 机器人选择",
        "kata_performance": "🥋 型 (Kata) 表演",
        "commands": "🎮 指令",
        "cmd_desc": "行走和跑步循环持续。跳跃、挥手、前空翻、后空翻、鞠躬各执行一次。",
        "cmd_hint": "您也可以输入型 (Kata) 名称（例如 `Taikyoku Shodan`）来运行完整序列。",
        "action_placeholder": "例如：backflip 或 Taikyoku Shodan",
        "execute_action": "▶️ 执行指令",
        "soccer_play": "⚽ 踢足球（绕圈）",
        "speech": "🗣️ 语音",
        "speak_placeholder": "例如：你好，我是你的机器人。",
        "speak_button": "🔊 让机器人说话",
        "contact": "📞 联系方式",
        "status": "🔧 状态",
        "current_robot": "当前机器人",
        "last_action": "上次动作",
        "kata": "型 (Kata)",
        "backstage": "📜 后台 – 指令历史",
        "no_commands": "尚无指令。请从侧边栏发送指令。",
        "footer_line1": "© 2026 GlobalInternet.py 在线软件公司",
        "footer_line2": "由 <strong>Gesner Deslandes</strong> 构建 | (509) 4738-5663 | deslandes78@gmail.com",
        "footer_line3": "🤖 模拟机器人控制 – 可集成真实硬件。",
        "speech_failed": "❌ 语音生成失败。请确保已安装 pyttsx3 或 gTTS。",
        "speech_warning": "请输入要说的文本。",
        "action_warning": "请输入动作或型 (Kata) 名称。",
        "active_kata": "当前型 (Kata)",
        "belt": "腰带等级",
        "robot_view": "🖥️ 机器人视图",
        "none": "无",
        "select_kata": "选择型 (Kata)",
        "select_robot": "选择机器人",
        "language": "🌐 语言",
        "voice_gender": "🎤 语音性别",
        "male": "男性",
        "female": "女性",
        "email": "电子邮件",
        "phone": "电话",
        "website": "网站",
        "contact_info": "联系信息",
        "status_current_robot": "当前机器人：",
        "status_last_action": "上次动作：",
        "status_kata": "型 (Kata)：",
        "speaking": "正在说话：",
        "replay_voice": "🔁 重播语音",
        "gender_note": "性别选择需要 pyttsx3。使用 gTTS（中性）作为备选。",
        "gender_enabled": "✅ 已启用 {} 语音",
        "gender_unavailable": "⚠️ pyttsx3 不可用 – 忽略性别选择。使用 gTTS（中性）。",
    }
}

def get_text(key, lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# ---- Speech synthesis ----
def generate_audio(text, lang_code="en", gender="Male"):
    if not text.strip():
        return None

    if PYTTTSX3_AVAILABLE:
        try:
            import pyttsx3
            import tempfile
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            selected_voice = None
            male_patterns = ['david', 'male', 'm', 'paul', 'mike', 'brian', 'scott', 'mark', 'james', 'george']
            female_patterns = ['zira', 'female', 'f', 'susan', 'mary', 'linda', 'patricia', 'jennifer', 'elizabeth']
            for voice in voices:
                name_lower = voice.name.lower()
                gender_lower = voice.gender.lower() if hasattr(voice, 'gender') and voice.gender else ''
                if gender.lower() == 'male':
                    if any(p in name_lower for p in male_patterns) or 'male' in gender_lower:
                        selected_voice = voice.id
                        break
                else:
                    if any(p in name_lower for p in female_patterns) or 'female' in gender_lower:
                        selected_voice = voice.id
                        break
            if not selected_voice:
                for voice in voices:
                    name_lower = voice.name.lower()
                    if gender.lower() == 'male' and 'male' in name_lower:
                        selected_voice = voice.id
                        break
                    elif gender.lower() == 'female' and 'female' in name_lower:
                        selected_voice = voice.id
                        break
            if not selected_voice and voices:
                selected_voice = voices[0].id
            if selected_voice:
                engine.setProperty('voice', selected_voice)
            elif voices:
                engine.setProperty('voice', voices[0].id)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp_path = tmp.name
            engine.save_to_file(text, tmp_path)
            engine.runAndWait()
            with open(tmp_path, "rb") as f:
                audio_bytes = f.read()
            os.unlink(tmp_path)
            return audio_bytes
        except Exception:
            pass

    try:
        from gtts import gTTS
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(tmp_path)
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        os.unlink(tmp_path)
        return audio_bytes
    except Exception:
        return None

st.set_page_config(
    page_title="Robotic Control Center | GlobalInternet.py",
    layout="wide",
    page_icon="🤖"
)

# ---- Data ----
ROBOTS = {
    "Red Titan": {"color": "#ff3333", "accent": "#ff6666", "description": "Heavy combat model with reinforced armor."},
    "Blue Sentinel": {"color": "#3388ff", "accent": "#66aaff", "description": "Scout and reconnaissance unit."},
    "Green Viper": {"color": "#33cc66", "accent": "#66ff99", "description": "Stealth and agility specialist."},
    "Gold Phoenix": {"color": "#ffaa00", "accent": "#ffcc44", "description": "Command and leadership unit."},
    "Silver Ghost": {"color": "#cccccc", "accent": "#eeeeee", "description": "Advanced prototype with unknown capabilities."}
}

KATAS = {
    "Taikyoku Shodan": {"kimono": "#f0f0f0", "belt": "#ffffff", "headband": "#ff0000", "belt_rank": "White"},
    "Heian Shodan": {"kimono": "#f0f0f0", "belt": "#ffff00", "headband": "#0000ff", "belt_rank": "Yellow"},
    "Heian Nidan": {"kimono": "#f0f0f0", "belt": "#ffa500", "headband": "#00ff00", "belt_rank": "Orange"},
    "Heian Sandan": {"kimono": "#f0f0f0", "belt": "#00ff00", "headband": "#ffff00", "belt_rank": "Green"},
    "Heian Yondan": {"kimono": "#f0f0f0", "belt": "#800080", "headband": "#ffa500", "belt_rank": "Purple"},
    "Heian Godan": {"kimono": "#f0f0f0", "belt": "#8b4513", "headband": "#800080", "belt_rank": "Brown"},
    "Tekki Shodan": {"kimono": "#0000ff", "belt": "#8b4513", "headband": "#ff0000", "belt_rank": "Brown"},
    "Bassai Dai": {"kimono": "#0000ff", "belt": "#000000", "headband": "#ffffff", "belt_rank": "Black"},
    "Kanku Dai": {"kimono": "#000000", "belt": "#000000", "headband": "#ffd700", "belt_rank": "Black"},
    "Gojushiho": {"kimono": "#000000", "belt": "#000000", "headband": "#c0c0c0", "belt_rank": "Black"}
}

def get_kata_sequence(kata_name):
    base = [["bow", 2.0], ["walk", 3.0], ["jump", 1.2], ["wave", 2.0], ["frontflip", 1.5], ["walk", 3.0], ["bow", 2.0]]
    variations = {
        "Taikyoku Shodan": [["idle", 1.0]] + base,
        "Heian Shodan": base + [["idle", 1.0]],
        "Heian Nidan": [["walk", 2.0], ["run", 2.0]] + base[2:],
        "Heian Sandan": base[:3] + [["run", 2.0]] + base[3:],
        "Heian Yondan": base[:4] + [["idle", 1.0]] + base[4:],
        "Heian Godan": base[:2] + [["jump", 1.2], ["walk", 2.0]] + base[3:],
        "Tekki Shodan": [["bow", 2.0], ["idle", 2.0]] + base[2:],
        "Bassai Dai": base + [["idle", 2.0]],
        "Kanku Dai": [["walk", 4.0], ["jump", 1.2], ["wave", 2.0], ["frontflip", 1.5], ["walk", 4.0]],
        "Gojushiho": [["bow", 3.0], ["walk", 3.0], ["run", 3.0], ["jump", 1.2], ["frontflip", 1.5], ["wave", 2.0], ["bow", 2.0]]
    }
    return variations.get(kata_name, base)

# ---- Custom CSS ----
st.markdown("""
<style>
    .stApp { background: #0a0a0f; color: #ffffff; }
    [data-testid="stSidebar"] { background: #0d0d12; border-right: 1px solid #2a2a3a; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stCaption { color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6, p, li, .stMarkdown, .stCaption, label { color: #ffffff !important; }
    .robot-card {
        background: rgba(20,30,50,0.7);
        border: 1px solid #2a3a5a;
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        backdrop-filter: blur(5px);
    }
    .robot-card .robot-name { font-size: 1.4rem; font-weight: 600; color: #00d4ff; }
    .robot-card .robot-type { font-size: 0.9rem; color: #8899bb; }
    .footer { text-align: center; padding: 20px 0; border-top: 1px solid #2a3a5a; margin-top: 30px; color: #667799; font-size: 0.9rem; }
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff, #0088ff) !important;
        color: #0a0a0f !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 30px rgba(0,212,255,0.3); }
    .stTextInput>div>div>input {
        background-color: #141018 !important;
        color: #ffffff !important;
        border: 1px solid #2a3a5a !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    .profile-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00d4ff;
        display: block;
        margin: 0 auto 8px auto;
    }
    .profile-name { color: #ffffff; text-align: center; margin-top: 8px; margin-bottom: 0; font-size: 1.2rem; }
    .profile-title { color: #8899bb; text-align: center; font-size: 0.9rem; margin-top: 0; }
    .status-panel {
        background: rgba(20,30,50,0.5);
        border: 1px solid #2a3a5a;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
    }
    .status-panel .label { color: #8899bb; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
    .status-panel .value { color: #00d4ff; font-size: 1.2rem; font-weight: 600; }
    .backstage { margin-top: 20px; }
    .kata-step {
        background: rgba(0,212,255,0.05);
        border: 1px solid #00d4ff;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 8px 0;
        text-align: center;
    }
    .kata-step .step-name { color: #00d4ff; font-weight: 600; font-size: 1.1rem; }
    .kata-step .step-progress { color: #8899bb; font-size: 0.85rem; }
    .note {
        font-size: 0.8rem;
        color: #8899bb;
        font-style: italic;
        margin-top: 4px;
    }
    .stAlert {
        padding: 6px 12px;
        margin-top: 4px;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ---- 3D Viewer HTML generator (robot circles with ball) ----
def get_robot_viewer_html(robot_name, command=None, kata_name=None):
    # Colors, kata info, etc.
    color_map = {r: ROBOTS[r]["color"] for r in ROBOTS}
    main_color = color_map.get(robot_name, "#3388ff")
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    mr = hex_to_rgb(main_color)
    accent_rgb = (min(255, mr[0]+60), min(255, mr[1]+60), min(255, mr[2]+60))
    accent_color = f"rgb({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]})"

    is_kata = kata_name is not None and kata_name in KATAS
    if is_kata:
        ki = KATAS[kata_name]
        kimono_color = ki["kimono"]
        belt_color = ki["belt"]
        headband_color = ki["headband"]
        belt_rank = ki["belt_rank"]
    else:
        kimono_color = main_color
        belt_color = main_color
        headband_color = "#ff0000"
        belt_rank = ""

    valid_commands = ['walk', 'run', 'jump', 'wave', 'frontflip', 'backflip', 'bow', 'soccer']
    cmd_lower = command.lower() if command else "idle"
    anim_cmd = cmd_lower if cmd_lower in valid_commands else 'idle'

    kata_sequence = get_kata_sequence(kata_name) if is_kata else []
    kata_sequence_json = json.dumps(kata_sequence)

    cache_buster = random.randint(100000, 999999)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background: #0a0a0f; }}
            canvas {{ display: block; }}
            #info {{ position: absolute; bottom: 20px; left: 20px; color: #8899bb; font-size: 14px; pointer-events: none; z-index: 10; }}
            #step-info {{
                position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
                color: #00d4ff; font-size: 20px; font-weight: 600;
                text-shadow: 0 0 20px rgba(0,212,255,0.3);
                background: rgba(10,10,15,0.7);
                padding: 8px 24px;
                border-radius: 30px;
                border: 1px solid #00d4ff;
                pointer-events: none;
                z-index: 10;
                text-align: center;
            }}
            #step-progress {{
                position: absolute; bottom: 60px; left: 50%; transform: translateX(-50%);
                width: 60%; max-width: 400px;
                height: 6px;
                background: #1a2a3a;
                border-radius: 3px;
                overflow: hidden;
                pointer-events: none;
                z-index: 10;
            }}
            #step-progress-bar {{
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #00d4ff, #0088ff);
                border-radius: 3px;
                transition: width 0.1s;
            }}
        </style>
    </head>
    <body>
        <!-- cache-buster: {cache_buster} -->
        <div id="info">🤖 {robot_name} | Command: {command if command else 'Idle'}</div>
        <div id="step-info">⏳ Waiting...</div>
        <div id="step-progress"><div id="step-progress-bar" style="width:0%"></div></div>
        <script type="importmap">
        {{
            "imports": {{
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js"
            }}
        }}
        </script>
        <script type="module">
        import * as THREE from 'three';
        import {{ OrbitControls }} from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

        const stepInfoEl = document.getElementById('step-info');
        const progressBar = document.getElementById('step-progress-bar');

        // ---- Scene setup ----
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0f);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
        camera.position.set(4, 3, 6);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.body.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.target.set(0, 1.2, 0);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.update();

        // ---- Lights ----
        const ambient = new THREE.AmbientLight(0x404060);
        scene.add(ambient);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
        dirLight.position.set(5, 10, 7);
        dirLight.castShadow = true;
        scene.add(dirLight);

        const fillLight = new THREE.DirectionalLight(0x88aaff, 0.4);
        fillLight.position.set(-3, 2, 4);
        scene.add(fillLight);

        const rimLight = new THREE.DirectionalLight(0xffaa66, 0.3);
        rimLight.position.set(-2, 1, -5);
        scene.add(rimLight);

        // ---- Ground grid ----
        const gridHelper = new THREE.GridHelper(10, 20, 0x336688, 0x224466);
        gridHelper.position.y = -0.5;
        scene.add(gridHelper);

        // ---- Robot construction (Transformer style with waist, 'G') ----
        const robotGroup = new THREE.Group();
        robotGroup.position.y = 0.5;

        // Materials (same as before)
        const mainMat = new THREE.MeshStandardMaterial({{ color: '{main_color}', roughness: 0.4, metalness: 0.6 }});
        const accentMat = new THREE.MeshStandardMaterial({{ color: '{accent_color}', roughness: 0.3, metalness: 0.5 }});
        const darkMat = new THREE.MeshStandardMaterial({{ color: '#333333', roughness: 0.5, metalness: 0.4 }});
        const jointMat = new THREE.MeshStandardMaterial({{ color: '#888888', roughness: 0.3, metalness: 0.7 }});
        const visorMat = new THREE.MeshStandardMaterial({{ color: '#00ddff', emissive: '#0066aa', emissiveIntensity: 0.5 }});
        const antennaMat = new THREE.MeshStandardMaterial({{ color: '#ffaa00', emissive: '#ff8800', emissiveIntensity: 0.3 }});
        const headbandMat = new THREE.MeshStandardMaterial({{ color: '{headband_color}', roughness: 0.3 }});
        const beltMat = new THREE.MeshStandardMaterial({{ color: '{belt_color}', roughness: 0.5 }});
        const waistMat = new THREE.MeshStandardMaterial({{ color: '#555555', roughness: 0.5, metalness: 0.4 }});

        // ---- Torso ----
        const torsoGroup = new THREE.Group();
        robotGroup.add(torsoGroup);

        const torsoGeo = new THREE.BoxGeometry(0.9, 1.1, 0.6);
        const torso = new THREE.Mesh(torsoGeo, mainMat);
        torso.position.y = 0.55;
        torso.castShadow = true;
        torsoGroup.add(torso);

        const chestGeo = new THREE.BoxGeometry(0.7, 0.4, 0.15);
        const chest = new THREE.Mesh(chestGeo, accentMat);
        chest.position.set(0, 0.3, 0.4);
        torsoGroup.add(chest);

        // "G" emblem
        (function() {{
            const canvas = document.createElement('canvas');
            canvas.width = 128;
            canvas.height = 128;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, 128, 128);
            ctx.shadowColor = 'rgba(255, 215, 0, 0.8)';
            ctx.shadowBlur = 15;
            ctx.font = 'bold 100px "Arial", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#ffd700';
            ctx.fillText('G', 64, 64);
            ctx.shadowBlur = 0;
            ctx.fillStyle = '#ffaa00';
            ctx.fillText('G', 64, 64);
            const texture = new THREE.CanvasTexture(canvas);
            const emblemMat = new THREE.MeshStandardMaterial({{
                map: texture,
                transparent: true,
                emissive: '#ffaa00',
                emissiveIntensity: 0.2,
                side: THREE.DoubleSide
            }});
            const emblemGeo = new THREE.PlaneGeometry(0.35, 0.35);
            const emblem = new THREE.Mesh(emblemGeo, emblemMat);
            emblem.position.set(0, 0.3, 0.48);
            torsoGroup.add(emblem);
        }})();

        const beltGeo = new THREE.BoxGeometry(0.8, 0.12, 0.5);
        const belt = new THREE.Mesh(beltGeo, beltMat);
        belt.position.set(0, 0.0, 0);
        torsoGroup.add(belt);

        // Waist
        const waistGeo = new THREE.BoxGeometry(0.7, 0.2, 0.4);
        const waist = new THREE.Mesh(waistGeo, waistMat);
        waist.position.set(0, -0.2, 0);
        waist.castShadow = true;
        torsoGroup.add(waist);

        const hipGeo = new THREE.BoxGeometry(0.7, 0.2, 0.5);
        const hip = new THREE.Mesh(hipGeo, darkMat);
        hip.position.set(0, -0.4, 0);
        torsoGroup.add(hip);

        // ---- Neck & Head ----
        const neckGeo = new THREE.CylinderGeometry(0.15, 0.15, 0.15);
        const neck = new THREE.Mesh(neckGeo, jointMat);
        neck.position.set(0, 1.1, 0);
        torsoGroup.add(neck);

        const headGroup = new THREE.Group();
        headGroup.position.set(0, 1.2, 0);
        torsoGroup.add(headGroup);

        const headGeo = new THREE.BoxGeometry(0.5, 0.5, 0.5);
        const head = new THREE.Mesh(headGeo, mainMat);
        head.castShadow = true;
        headGroup.add(head);

        const visorGeo = new THREE.BoxGeometry(0.35, 0.12, 0.05);
        const visor = new THREE.Mesh(visorGeo, visorMat);
        visor.position.set(0, 0.0, 0.28);
        head.add(visor);

        const antGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.2);
        const ant = new THREE.Mesh(antGeo, antennaMat);
        ant.position.set(0, 0.35, 0);
        head.add(ant);
        const antBall = new THREE.SphereGeometry(0.06);
        const ball = new THREE.Mesh(antBall, antennaMat);
        ball.position.set(0, 0.45, 0);
        head.add(ball);

        if ({str(is_kata).lower()}) {{
            const bandGeo = new THREE.TorusGeometry(0.3, 0.03, 8, 20);
            const band = new THREE.Mesh(bandGeo, headbandMat);
            band.rotation.x = Math.PI/2;
            band.position.y = 0.0;
            head.add(band);
        }}

        // ---- Shoulder pads ----
        const shoulderPadGeo = new THREE.SphereGeometry(0.22, 8, 8);
        const shoulderPadMat = new THREE.MeshStandardMaterial({{ color: '#555555', roughness: 0.3, metalness: 0.6 }});
        const leftShoulder = new THREE.Mesh(shoulderPadGeo, shoulderPadMat);
        leftShoulder.position.set(-0.6, 0.9, 0);
        torsoGroup.add(leftShoulder);
        const rightShoulder = new THREE.Mesh(shoulderPadGeo, shoulderPadMat);
        rightShoulder.position.set(0.6, 0.9, 0);
        torsoGroup.add(rightShoulder);

        // ---- Arms ----
        const upperArmGeo = new THREE.BoxGeometry(0.2, 0.4, 0.2);
        const elbowGeo = new THREE.SphereGeometry(0.08, 8, 8);
        const forearmGeo = new THREE.BoxGeometry(0.18, 0.3, 0.18);
        const handGeo = new THREE.BoxGeometry(0.15, 0.1, 0.15);

        // Left arm
        const leftArmGroup = new THREE.Group();
        leftArmGroup.position.set(-0.65, 0.8, 0);
        torsoGroup.add(leftArmGroup);
        const leftUpperArm = new THREE.Mesh(upperArmGeo, mainMat);
        leftUpperArm.position.y = -0.2;
        leftUpperArm.castShadow = true;
        leftArmGroup.add(leftUpperArm);
        const leftElbow = new THREE.Mesh(elbowGeo, jointMat);
        leftElbow.position.y = -0.4;
        leftArmGroup.add(leftElbow);
        const leftForearmGroup = new THREE.Group();
        leftForearmGroup.position.y = -0.4;
        leftArmGroup.add(leftForearmGroup);
        const leftForearm = new THREE.Mesh(forearmGeo, darkMat);
        leftForearm.position.y = -0.15;
        leftForearm.castShadow = true;
        leftForearmGroup.add(leftForearm);
        const leftHand = new THREE.Mesh(handGeo, accentMat);
        leftHand.position.y = -0.35;
        leftForearmGroup.add(leftHand);

        // Right arm
        const rightArmGroup = new THREE.Group();
        rightArmGroup.position.set(0.65, 0.8, 0);
        torsoGroup.add(rightArmGroup);
        const rightUpperArm = new THREE.Mesh(upperArmGeo, mainMat);
        rightUpperArm.position.y = -0.2;
        rightUpperArm.castShadow = true;
        rightArmGroup.add(rightUpperArm);
        const rightElbow = new THREE.Mesh(elbowGeo, jointMat);
        rightElbow.position.y = -0.4;
        rightArmGroup.add(rightElbow);
        const rightForearmGroup = new THREE.Group();
        rightForearmGroup.position.y = -0.4;
        rightArmGroup.add(rightForearmGroup);
        const rightForearm = new THREE.Mesh(forearmGeo, darkMat);
        rightForearm.position.y = -0.15;
        rightForearm.castShadow = true;
        rightForearmGroup.add(rightForearm);
        const rightHand = new THREE.Mesh(handGeo, accentMat);
        rightHand.position.y = -0.35;
        rightForearmGroup.add(rightHand);

        // ---- Legs ----
        const upperLegGeo = new THREE.BoxGeometry(0.25, 0.4, 0.25);
        const kneeGeo = new THREE.SphereGeometry(0.1, 8, 8);
        const lowerLegGeo = new THREE.BoxGeometry(0.22, 0.35, 0.22);
        const footGeo = new THREE.BoxGeometry(0.3, 0.08, 0.4);

        // Left leg
        const leftLegGroup = new THREE.Group();
        leftLegGroup.position.set(-0.25, -0.45, 0);
        torsoGroup.add(leftLegGroup);
        const leftUpperLeg = new THREE.Mesh(upperLegGeo, mainMat);
        leftUpperLeg.position.y = -0.2;
        leftUpperLeg.castShadow = true;
        leftLegGroup.add(leftUpperLeg);
        const leftKnee = new THREE.Mesh(kneeGeo, jointMat);
        leftKnee.position.y = -0.4;
        leftLegGroup.add(leftKnee);
        const leftLowerLegGroup = new THREE.Group();
        leftLowerLegGroup.position.y = -0.4;
        leftLegGroup.add(leftLowerLegGroup);
        const leftLowerLeg = new THREE.Mesh(lowerLegGeo, darkMat);
        leftLowerLeg.position.y = -0.175;
        leftLowerLeg.castShadow = true;
        leftLowerLegGroup.add(leftLowerLeg);
        const leftFoot = new THREE.Mesh(footGeo, accentMat);
        leftFoot.position.set(0, -0.4, 0.05);
        leftLowerLegGroup.add(leftFoot);

        // Right leg
        const rightLegGroup = new THREE.Group();
        rightLegGroup.position.set(0.25, -0.45, 0);
        torsoGroup.add(rightLegGroup);
        const rightUpperLeg = new THREE.Mesh(upperLegGeo, mainMat);
        rightUpperLeg.position.y = -0.2;
        rightUpperLeg.castShadow = true;
        rightLegGroup.add(rightUpperLeg);
        const rightKnee = new THREE.Mesh(kneeGeo, jointMat);
        rightKnee.position.y = -0.4;
        rightLegGroup.add(rightKnee);
        const rightLowerLegGroup = new THREE.Group();
        rightLowerLegGroup.position.y = -0.4;
        rightLegGroup.add(rightLowerLegGroup);
        const rightLowerLeg = new THREE.Mesh(lowerLegGeo, darkMat);
        rightLowerLeg.position.y = -0.175;
        rightLowerLeg.castShadow = true;
        rightLowerLegGroup.add(rightLowerLeg);
        const rightFoot = new THREE.Mesh(footGeo, accentMat);
        rightFoot.position.set(0, -0.4, 0.05);
        rightLowerLegGroup.add(rightFoot);

        // ---- Soccer Ball ----
        const ballGeo = new THREE.SphereGeometry(0.2, 16, 16);
        const ballMat = new THREE.MeshStandardMaterial({{
            color: 0xffffff,
            roughness: 0.3,
            metalness: 0.1,
            emissive: 0x222222,
            emissiveIntensity: 0.1
        }});
        const soccerBall = new THREE.Mesh(ballGeo, ballMat);
        soccerBall.castShadow = true;
        (function() {{
            const c = document.createElement('canvas');
            c.width = 256;
            c.height = 256;
            const ctx = c.getContext('2d');
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, 256, 256);
            ctx.fillStyle = '#222222';
            ctx.beginPath();
            ctx.arc(128, 128, 80, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(128, 128, 60, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#222222';
            ctx.font = 'bold 40px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('⚽', 128, 135);
            const tex = new THREE.CanvasTexture(c);
            soccerBall.material.map = tex;
            soccerBall.material.needsUpdate = true;
        }})();
        // Ball positions (relative to robotGroup)
        const ballBasePos = new THREE.Vector3(0, -0.8, 0.5);   // ground
        soccerBall.position.copy(ballBasePos);
        robotGroup.add(soccerBall);

        scene.add(robotGroup);

        // ---- Animation state ----
        const state = {{
            cmd: 'idle',
            looping: false,
            animating: false,
            animTimer: 0,
            walkCycle: 0,
            bowActive: false,
            bowProgress: 0,
            kataRunning: false,
            kataIdx: 0,
            kataTimer: 0,
            kataComplete: false,
            kataAction: null,
            kataSeq: {kata_sequence_json},
            initCmd: '{anim_cmd}',
            validCmds: {json.dumps(valid_commands)},
            // Soccer mode flag for UI label
            soccerMode: false,
            // Circle motion
            circleAngle: 0,
            circleSpeed: 0.6,
            circleRadius: 2.2,
        }};

        // ---- UI update ----
        function updateStepInfo() {{
            if (state.kataRunning && state.kataAction !== null) {{
                const stepName = state.kataAction[0];
                const total = state.kataSeq.length;
                const current = state.kataIdx + 1;
                const progress = (state.kataIdx / total) * 100;
                stepInfoEl.textContent = `🥋 Step ${{current}}/${{total}}: ${{stepName.toUpperCase()}}`;
                progressBar.style.width = progress + '%';
            }} else if (state.kataRunning && state.kataComplete) {{
                stepInfoEl.textContent = '✅ Kata Complete!';
                progressBar.style.width = '100%';
            }} else {{
                if (state.soccerMode && state.cmd === 'run') {{
                    stepInfoEl.textContent = '⚽ Circle Dribble';
                    progressBar.style.width = '100%';
                }} else if (state.cmd !== 'idle') {{
                    stepInfoEl.textContent = `▶️ ${{state.cmd.toUpperCase()}}`;
                    progressBar.style.width = (state.animating ? (state.animTimer / 1.5 * 100) : 0) + '%';
                }} else {{
                    stepInfoEl.textContent = '⏳ Idle';
                    progressBar.style.width = '0%';
                }}
            }}
        }}

        // ---- Update logic ----
        function update(dt) {{
            // Kata logic
            if (state.kataRunning && !state.kataComplete) {{
                if (state.kataAction === null) {{
                    if (state.kataIdx < state.kataSeq.length) {{
                        state.kataAction = state.kataSeq[state.kataIdx];
                        state.kataTimer = 0;
                        const type = state.kataAction[0];
                        if (type === 'walk' || type === 'run') {{
                            state.cmd = type; state.looping = true; state.animating = true; state.bowActive = false;
                        }} else if (type === 'idle') {{
                            state.cmd = 'idle'; state.looping = false; state.animating = false; state.bowActive = false;
                        }} else if (type === 'bow') {{
                            state.cmd = 'bow'; state.looping = false; state.animating = false; state.bowActive = true; state.bowProgress = 0;
                        }} else {{
                            state.cmd = type; state.looping = false; state.animating = true; state.bowActive = false;
                        }}
                        // If kata step is run, we don't want soccer mode
                        state.soccerMode = false;
                        updateStepInfo();
                    }} else {{
                        state.kataComplete = true;
                        state.kataRunning = false;
                        state.cmd = 'idle';
                        state.animating = false;
                        state.looping = false;
                        state.bowActive = false;
                        state.soccerMode = false;
                        updateStepInfo();
                        return;
                    }}
                }}
                state.kataTimer += dt;
                const dur = state.kataAction[1];
                if (state.kataTimer >= dur) {{
                    state.kataIdx++;
                    state.kataAction = null;
                    state.animating = false;
                    state.looping = false;
                    state.bowActive = false;
                }}
                if (state.cmd === 'bow') state.bowProgress = Math.min(state.kataTimer / dur, 1.0);
                return;
            }}

            // ---- Soccer / Circle motion ----
            if (state.soccerMode && state.cmd === 'run') {{
                // Increment angle
                state.circleAngle += dt * state.circleSpeed;
                // Compute position on circle
                const x = state.circleRadius * Math.cos(state.circleAngle);
                const z = state.circleRadius * Math.sin(state.circleAngle);
                robotGroup.position.x = x;
                robotGroup.position.z = z;
                // Compute direction of motion (tangent, normalized)
                const dx = -Math.sin(state.circleAngle);
                const dz = Math.cos(state.circleAngle);
                // Use lookAt to face the direction of motion
                const target = new THREE.Vector3(x + dx, 0, z + dz);
                robotGroup.lookAt(target);
                // Add a slight roll (lean into the turn) – tilt around Z
                // The sign depends on whether we're turning left or right; we want to lean inward.
                // For this circle, the center is at (0,0,0), so inward direction is -position.
                // We'll compute a lean based on the angle.
                const leanAngle = -0.08 * Math.cos(state.circleAngle); // approximate
                robotGroup.rotation.z = leanAngle;

                // Keep ball jiggling (in soccer mode we want ball at feet)
                const swing = Math.sin(state.walkCycle) * 0.05;
                soccerBall.position.set(
                    ballBasePos.x + swing * 0.1,
                    ballBasePos.y + Math.abs(Math.sin(state.walkCycle * 2)) * 0.02,
                    ballBasePos.z + swing * 0.05
                );
                soccerBall.rotation.x += dt * 2;
                soccerBall.rotation.z += dt * 1.5;
                updateStepInfo();
                return;
            }}

            // ---- Ball logic (appears during run) ----
            // Update ball position based on current command (non-soccer)
            if (state.cmd === 'run') {{
                // Normal run: ball on ground jiggles
                const swing = Math.sin(state.walkCycle) * 0.05;
                soccerBall.position.set(
                    ballBasePos.x + swing * 0.1,
                    ballBasePos.y + Math.abs(Math.sin(state.walkCycle * 2)) * 0.02,
                    ballBasePos.z + swing * 0.05
                );
                soccerBall.rotation.x += dt * 2;
                soccerBall.rotation.z += dt * 1.5;
            }} else {{
                // Not running: ball stays on ground
                soccerBall.position.copy(ballBasePos);
            }}

            // ---- Normal commands ----
            if (state.cmd === 'idle') {{
                state.animating = false; state.looping = false; state.bowActive = false;
                // Reset robot position to center when idle
                robotGroup.position.x = 0;
                robotGroup.position.z = 0;
                robotGroup.rotation.y = 0;
                robotGroup.rotation.z = 0;
                return;
            }}
            if (state.looping) {{
                const speed = (state.cmd === 'walk') ? 2.2 : 8.0;
                state.walkCycle += dt * speed;
                return;
            }}
            if (state.animating) {{
                state.animTimer += dt;
                let dur = 1.2;
                if (state.cmd === 'jump') dur = 1.2;
                else if (state.cmd === 'wave') dur = 2.0;
                else if (state.cmd === 'frontflip' || state.cmd === 'backflip') dur = 1.5;
                else if (state.cmd === 'bow') dur = 2.0;
                if (state.cmd === 'bow' && state.bowActive) {{
                    state.bowProgress = Math.min(state.animTimer / dur, 1.0);
                }}
                if (state.animTimer >= dur) {{
                    state.animating = false;
                    state.cmd = 'idle';
                    state.animTimer = 0;
                    state.bowActive = false;
                }}
                updateStepInfo();
            }}
        }}

        // ---- Robot animation ----
        function animateRobot() {{
            const isRun = (state.cmd === 'run');
            const amp = isRun ? 1.2 : 0.5;
            const swing = (state.cmd === 'walk' || isRun) ? Math.sin(state.walkCycle) * amp : 0;

            leftArmGroup.rotation.x = 0;
            rightArmGroup.rotation.x = 0;
            leftForearmGroup.rotation.x = 0;
            rightForearmGroup.rotation.x = 0;
            leftLegGroup.rotation.x = 0;
            rightLegGroup.rotation.x = 0;
            leftLowerLegGroup.rotation.x = 0;
            rightLowerLegGroup.rotation.x = 0;
            // Do NOT reset robotGroup position or rotation here, they are set in update
            torsoGroup.rotation.x = 0;

            if (state.cmd === 'walk' || isRun) {{
                const armSwing = swing * 0.8;
                const legSwing = swing * 0.6;
                const elbowSwing = swing * 0.3;
                const kneeSwing = swing * 0.3;
                leftArmGroup.rotation.x = -armSwing;
                rightArmGroup.rotation.x = armSwing;
                leftForearmGroup.rotation.x = -elbowSwing;
                rightForearmGroup.rotation.x = elbowSwing;
                leftLegGroup.rotation.x = legSwing;
                rightLegGroup.rotation.x = -legSwing;
                leftLowerLegGroup.rotation.x = -kneeSwing;
                rightLowerLegGroup.rotation.x = kneeSwing;
            }}

            if (state.cmd === 'jump' && state.animating) {{
                const t = Math.min(state.animTimer / 1.2, 1);
                const y = 1.5 * 4 * t * (1 - t);
                robotGroup.position.y = 0.5 + y;
            }} else {{
                // Ensure y is reset if not jumping
                if (!state.soccerMode) robotGroup.position.y = 0.5;
            }}

            if (state.cmd === 'frontflip' && state.animating) {{
                const t = Math.min(state.animTimer / 1.5, 1);
                const y = 2.0 * 4 * t * (1 - t);
                robotGroup.position.y = 0.5 + y;
                robotGroup.rotation.x = t * 2 * Math.PI;
                robotGroup.position.z = -0.3 * Math.sin(t * Math.PI);
            }}

            if (state.cmd === 'backflip' && state.animating) {{
                const t = Math.min(state.animTimer / 1.5, 1);
                const y = 2.0 * 4 * t * (1 - t);
                robotGroup.position.y = 0.5 + y;
                robotGroup.rotation.x = -t * 2 * Math.PI;
                robotGroup.position.z = 0.3 * Math.sin(t * Math.PI);
            }}

            if (state.cmd === 'wave' && state.animating) {{
                rightArmGroup.rotation.x = -0.8 + Math.sin(state.animTimer * 6) * 0.3;
                rightForearmGroup.rotation.x = 0.2 + Math.sin(state.animTimer * 6 + 1) * 0.2;
            }}

            if (state.cmd === 'bow' && (state.bowActive || state.animating)) {{
                const prog = state.bowActive ? state.bowProgress : Math.min(state.animTimer / 2.0, 1);
                const ease = prog < 0.5 ? 2 * prog * prog : 1 - Math.pow(-2 * prog + 2, 2) / 2;
                torsoGroup.rotation.x = ease * 0.6;
            }} else {{
                torsoGroup.rotation.x = 0;
            }}
        }}

        // ---- Animation loop ----
        let prevTime = performance.now();
        function animate(time) {{
            const dt = Math.min((time - prevTime) / 1000, 0.05);
            prevTime = time;
            update(dt);
            animateRobot();
            // Update step info if not kata and not soccerMode (but soccer mode updates separately)
            if (!state.kataRunning) {{
                updateStepInfo();
            }}
            controls.update();
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }}

        // ---- Resize ----
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        // ---- Init ----
        state.cmd = state.initCmd;
        if (state.cmd === 'soccer') {{
            state.soccerMode = true;
            state.cmd = 'run';
            state.looping = true;
            state.animating = true;
            // Initialize circle angle
            state.circleAngle = 0;
            updateStepInfo();
        }} else if (state.kataSeq.length > 0) {{
            state.kataRunning = true;
            state.kataIdx = 0;
            state.kataTimer = 0;
            state.kataComplete = false;
            state.kataAction = null;
            state.soccerMode = false;
        }} else {{
            if (state.validCmds.includes(state.cmd)) {{
                if (state.cmd === 'walk' || state.cmd === 'run') {{
                    state.looping = true;
                    state.animating = true;
                    state.walkCycle = 0;
                }} else if (state.cmd === 'bow') {{
                    state.looping = false;
                    state.animating = true;
                    state.bowActive = true;
                    state.bowProgress = 0;
                    state.animTimer = 0;
                }} else {{
                    state.looping = false;
                    state.animating = true;
                    state.animTimer = 0;
                }}
            }} else {{
                state.cmd = 'idle';
                state.looping = false;
                state.animating = false;
            }}
        }}
        updateStepInfo();
        animate(performance.now());
        </script>
    </body>
    </html>
    """
    return html

# ---- Session state ----
if 'robot_selected' not in st.session_state:
    st.session_state.robot_selected = "Red Titan"
if 'command' not in st.session_state:
    st.session_state.command = ""
if 'speak_text' not in st.session_state:
    st.session_state.speak_text = ""
if 'last_action' not in st.session_state:
    st.session_state.last_action = "idle"
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_spoken_text' not in st.session_state:
    st.session_state.last_spoken_text = ""
if 'last_spoken_audio' not in st.session_state:
    st.session_state.last_spoken_audio = None
if 'last_spoken_timestamp' not in st.session_state:
    st.session_state.last_spoken_timestamp = 0
if 'kata' not in st.session_state:
    st.session_state.kata = None
if 'language' not in st.session_state:
    st.session_state.language = "en"
if 'voice_gender' not in st.session_state:
    st.session_state.voice_gender = "Male"

# ========== HEADER ==========
lang = st.session_state.language
t = lambda key: get_text(key, lang)

st.markdown(f"""
<div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #2a3a5a; margin-bottom: 30px;">
    <h1 style="color: #00d4ff; font-size: 2.8rem; margin: 0; text-shadow: 0 0 30px rgba(0,212,255,0.2);">🤖 {t('app_title')}</h1>
    <p style="color: #8899bb; font-size: 1.1rem;">{t('app_subtitle')}</p>
    <span style="display: inline-block; background: #00ff64; color: #0a0a0f; padding: 4px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; animation: pulse 2s infinite;">{t('live_sim')}</span>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/Deslandes1/-Robotic-Control-Center-June-2026/main/Gesner%20Deslandes.png" 
             class="profile-img">
        <h3 class="profile-name">Gesner Deslandes</h3>
        <p class="profile-title">Engineer-in-Chief, GlobalInternet.py</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    lang_choice = st.selectbox(
        t('language'),
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(st.session_state.language),
        key="lang_select"
    )
    if lang_choice != st.session_state.language:
        st.session_state.language = lang_choice
        st.rerun()

    voice_gender_choice = st.selectbox(
        t('voice_gender'),
        options=[t('male'), t('female')],
        index=0 if st.session_state.voice_gender == "Male" else 1,
        key="voice_gender_select"
    )
    new_gender = "Male" if voice_gender_choice == t('male') else "Female"
    if new_gender != st.session_state.voice_gender:
        st.session_state.voice_gender = new_gender
        st.rerun()

    if PYTTTSX3_AVAILABLE:
        st.success(t('gender_enabled').format(st.session_state.voice_gender))
    else:
        st.warning(t('gender_unavailable'))

    st.markdown("---")

    st.markdown(f"### {t('robot_selection')}")
    robot_names = list(ROBOTS.keys())
    selected = st.selectbox(t('select_robot'), options=robot_names,
                            index=robot_names.index(st.session_state.robot_selected),
                            key="robot_select")
    if selected != st.session_state.robot_selected:
        st.session_state.robot_selected = selected
        st.session_state.last_action = "idle"
        st.session_state.kata = None
        st.rerun()

    robot_info = ROBOTS[st.session_state.robot_selected]
    st.markdown(f"""
    <div class="robot-card">
        <div class="robot-name" style="color: {robot_info['color']};">{st.session_state.robot_selected}</div>
        <div class="robot-type">{robot_info['description']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"### {t('kata_performance')}")
    kata_names = list(KATAS.keys())
    kata_selected = st.selectbox(t('select_kata'), options=["None"] + kata_names,
                                 index=0 if st.session_state.kata is None else kata_names.index(st.session_state.kata) + 1,
                                 key="kata_select")
    if kata_selected == "None":
        if st.session_state.kata is not None:
            st.session_state.kata = None
            st.session_state.command = ""
            st.rerun()
    else:
        if st.session_state.kata != kata_selected:
            st.session_state.kata = kata_selected
            st.session_state.command = ""
            st.rerun()

    if st.session_state.kata:
        kata_info = KATAS[st.session_state.kata]
        st.markdown(f"""
        <div style="background: rgba(0,212,255,0.05); border: 1px solid #00d4ff; border-radius: 8px; padding: 8px 12px; margin-top: 5px;">
            <span style="color: #8899bb; font-size: 0.8rem;">{t('active_kata')}</span><br>
            <span style="color: #00d4ff; font-weight: 600;">{st.session_state.kata}</span><br>
            <span style="color: #8899bb; font-size: 0.8rem;">{t('belt')}: {kata_info['belt_rank']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"### {t('commands')}")
    st.markdown(f"*{t('cmd_desc')}*")
    st.markdown(f"*{t('cmd_hint')}*")
    action_input = st.text_input("", key="action_input",
                                 placeholder=t('action_placeholder'))
    if st.button(t('execute_action'), use_container_width=True):
        if action_input.strip():
            kata_name_match = None
            for k in KATAS.keys():
                if k.lower() == action_input.strip().lower():
                    kata_name_match = k
                    break
            if kata_name_match:
                st.session_state.kata = kata_name_match
                st.session_state.command = ""
                st.session_state.last_action = f"Kata: {kata_name_match}"
                st.rerun()
            else:
                st.session_state.kata = None
                st.session_state.command = action_input.strip()
                st.session_state.last_action = action_input.strip().lower()
                st.rerun()
        else:
            st.warning(t('action_warning'))

    if st.button(t('soccer_play'), use_container_width=True):
        st.session_state.kata = None
        st.session_state.command = "soccer"
        st.session_state.last_action = "soccer"
        st.rerun()

    st.markdown("---")
    st.markdown(f"### {t('speech')}")
    speak_input = st.text_input("", key="speak_input", placeholder=t('speak_placeholder'))
    if st.button(t('speak_button'), use_container_width=True):
        if speak_input.strip():
            st.session_state.speak_text = speak_input.strip()
            audio_bytes = generate_audio(speak_input.strip(), lang, st.session_state.voice_gender)
            if audio_bytes:
                st.session_state.last_spoken_text = speak_input.strip()
                st.session_state.last_spoken_audio = audio_bytes
                st.session_state.last_spoken_timestamp = time.time()
                st.rerun()
            else:
                st.error(t('speech_failed'))
        else:
            st.warning(t('speech_warning'))

    st.markdown("---")
    st.markdown(f"### {t('contact')}")
    st.markdown(f"""
    <div style="background: rgba(20,30,50,0.8); border: 1px solid #2a3a5a; border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #8899bb;">
        <strong style="color: #00d4ff;">{t('email')}:</strong> deslandes78@gmail.com<br>
        <strong style="color: #00d4ff;">{t('phone')}:</strong> (509) 4738-5663<br>
        <strong style="color: #00d4ff;">{t('website')}:</strong> <a href="https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/" style="color: #00d4ff;" target="_blank">globalinternet-py.com</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### {t('status')}")
    st.markdown(f"**{t('status_current_robot')}** {st.session_state.robot_selected}")
    st.markdown(f"**{t('status_last_action')}** {st.session_state.last_action}")
    if st.session_state.kata:
        st.markdown(f"**{t('status_kata')}** {st.session_state.kata}")

# ========== MAIN CONTENT ==========
col_view, col_info = st.columns([3, 1])

with col_view:
    st.markdown(f"### {t('robot_view')}")
    viewer_html = get_robot_viewer_html(
        st.session_state.robot_selected,
        st.session_state.command if st.session_state.kata is None else "",
        st.session_state.kata
    )
    st.components.v1.html(viewer_html, height=650, width=700, scrolling=False)

with col_info:
    st.markdown(f"""
    <div class="status-panel">
        <div class="label">{t('current_robot')}</div>
        <div class="value">{st.session_state.robot_selected}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-panel">
        <div class="label">{t('last_action')}</div>
        <div class="value">{st.session_state.last_action if st.session_state.last_action != "idle" else "—"}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.kata:
        st.markdown(f"""
        <div class="status-panel" style="border-color: #ffaa00;">
            <div class="label">{t('kata')}</div>
            <div class="value" style="color: #ffaa00;">{st.session_state.kata}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.last_spoken_audio and st.session_state.last_spoken_timestamp > 0:
        st.audio(st.session_state.last_spoken_audio, format="audio/mp3", autoplay=True)
        st.caption(f"🔊 {t('speaking')} {st.session_state.last_spoken_text[:50]}...")
        if st.button(t('replay_voice')):
            st.rerun()

    with st.expander(t('backstage'), expanded=False):
        if st.session_state.history:
            for cmd, status in reversed(st.session_state.history[-10:]):
                st.markdown(f"""
                <div style="background: rgba(0,212,255,0.05); border-left: 3px solid #00d4ff; padding: 5px 10px; margin: 5px 0; border-radius: 4px;">
                    <span style="color: #00d4ff;">▶️</span> <span style="color: #ffffff;">{cmd}</span><br>
                    <span style="color: #8899bb; font-size: 0.8rem;">{status}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t('no_commands'))

# ---------- Speak history ----------
if st.session_state.last_spoken_text and st.session_state.last_spoken_audio:
    if not any("Speak:" in h[0] and st.session_state.last_spoken_text in h[0] for h in st.session_state.history):
        st.session_state.history.append((f"Speak: {st.session_state.last_spoken_text}", "Speech played"))
        if len(st.session_state.history) > 20:
            st.session_state.history = st.session_state.history[-20:]

# ========== FOOTER ==========
st.markdown(f"""
<div class="footer">
    <p>{t('footer_line1')}</p>
    <p>{t('footer_line2')}</p>
    <p style="font-size:0.8rem; color:#445566;">{t('footer_line3')}</p>
</div>
""", unsafe_allow_html=True)
