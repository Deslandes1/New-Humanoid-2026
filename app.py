import streamlit as st
import os
import tempfile
import time
import json
import urllib.parse

try:
    from gtts import gTTS
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

def generate_audio(text, lang_code="en"):
    if not VOICE_AVAILABLE or not text.strip():
        return None
    try:
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

# ---- Must be defined first ----
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
    base = [["bow", 2.0], ["walk", 3.0], ["jump", 1.2], ["wave", 2.0], ["backflip", 1.5], ["walk", 3.0], ["bow", 2.0]]
    variations = {
        "Taikyoku Shodan": [["idle", 1.0]] + base,
        "Heian Shodan": base + [["idle", 1.0]],
        "Heian Nidan": [["walk", 2.0], ["run", 2.0]] + base[2:],
        "Heian Sandan": base[:3] + [["run", 2.0]] + base[3:],
        "Heian Yondan": base[:4] + [["idle", 1.0]] + base[4:],
        "Heian Godan": base[:2] + [["jump", 1.2], ["walk", 2.0]] + base[3:],
        "Tekki Shodan": [["bow", 2.0], ["idle", 2.0]] + base[2:],
        "Bassai Dai": base + [["idle", 2.0]],
        "Kanku Dai": [["walk", 4.0], ["jump", 1.2], ["wave", 2.0], ["backflip", 1.5], ["walk", 4.0]],
        "Gojushiho": [["bow", 3.0], ["walk", 3.0], ["run", 3.0], ["jump", 1.2], ["backflip", 1.5], ["wave", 2.0], ["bow", 2.0]]
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
</style>
""", unsafe_allow_html=True)

# ----- Build the 2D Canvas viewer HTML -----
def get_robot_viewer_html(robot_name, command=None, kata_name=None):
    # Get colors for the robot
    color_map = {"Red Titan": "#ff3333", "Blue Sentinel": "#3388ff", "Green Viper": "#33cc66", "Gold Phoenix": "#ffaa00", "Silver Ghost": "#cccccc"}
    main_color = color_map.get(robot_name, "#3388ff")
    # Convert hex to RGB for canvas
    def hex_to_rgb(hex_color):
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    main_rgb = hex_to_rgb(main_color)
    accent_rgb = (min(255, main_rgb[0]+60), min(255, main_rgb[1]+60), min(255, main_rgb[2]+60))

    is_kata = kata_name is not None
    kata_info = KATAS.get(kata_name, None) if is_kata else None
    if is_kata and kata_info:
        kimono_color = kata_info["kimono"]
        belt_color = kata_info["belt"]
        headband_color = kata_info["headband"]
        belt_rank = kata_info["belt_rank"]
    else:
        kimono_color = main_color
        belt_color = main_color
        headband_color = "#ff0000"  # default
        belt_rank = ""

    kimono_rgb = hex_to_rgb(kimono_color)
    belt_rgb = hex_to_rgb(belt_color)
    headband_rgb = hex_to_rgb(headband_color)

    cmd_lower = command.lower() if command else "idle"
    valid_commands = ['walk', 'run', 'jump', 'wave', 'backflip']
    anim_cmd = cmd_lower if cmd_lower in valid_commands else 'idle'

    kata_sequence = get_kata_sequence(kata_name) if is_kata else []
    kata_sequence_json = json.dumps(kata_sequence)

    # Build the HTML with canvas and animation
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { margin: 0; background: #0a0a0f; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
            canvas { display: block; background: #0a0a0f; }
            #info { position: absolute; bottom: 20px; left: 20px; color: #8899bb; font-size: 14px; pointer-events: none; z-index: 10; }
        </style>
    </head>
    <body>
        <canvas id="canvas"></canvas>
        <div id="info">🤖 ROBOT_NAME | Command: COMMAND</div>
        <script>
            (function() {
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');
                let width, height;

                function resize() {
                    width = window.innerWidth;
                    height = window.innerHeight;
                    canvas.width = width;
                    canvas.height = height;
                }
                window.addEventListener('resize', resize);
                resize();

                // Robot parameters
                const mainColor = 'MAIN_COLOR';
                const accentColor = 'ACCENT_COLOR';
                const kimonoColor = 'KIMONO_COLOR';
                const beltColor = 'BELT_COLOR';
                const headbandColor = 'HEADBAND_COLOR';
                const isKata = IS_KATA;
                const animCommand = 'ANIM_CMD';
                const kataSequence = KATA_SEQUENCE;
                // Valid commands list (will be replaced)
                const validCommands = [];

                // Animation state
                let animTime = 0;
                let isAnimating = false;
                let loopAnimation = false;
                let walkCycle = 0;
                let hasStarted = false;
                let bowActive = false;
                let bowProgress = 0;

                // Kata state
                let kataRunning = false;
                let kataActionIndex = 0;
                let kataActionTime = 0;
                let kataAction = null;
                let kataComplete = false;

                // Robot parts positions (relative to center)
                const bodyX = 0, bodyY = 0;
                const headSize = 40;
                const torsoHeight = 80;
                const torsoWidth = 60;
                const armLen = 60;
                const legLen = 70;
                const shoulderY = -20;
                const hipY = 40;

                // Drawing functions
                function drawRobot(angle, swing) {
                    ctx.save();
                    ctx.translate(width/2, height/2 + 30); // shift down a bit

                    // ---- Body (torso) ----
                    ctx.fillStyle = kimonoColor;
                    ctx.shadowColor = 'rgba(0,0,0,0.5)';
                    ctx.shadowBlur = 10;
                    ctx.fillRect(-torsoWidth/2, -torsoHeight/2, torsoWidth, torsoHeight);
                    ctx.shadowBlur = 0;

                    // Belt
                    ctx.fillStyle = beltColor;
                    ctx.fillRect(-torsoWidth/2 + 5, torsoHeight/2 - 8, torsoWidth - 10, 10);

                    // Chest detail
                    ctx.fillStyle = accentColor;
                    ctx.fillRect(-15, -torsoHeight/2 + 10, 30, 15);

                    // ---- Head ----
                    ctx.save();
                    ctx.translate(0, -torsoHeight/2 - headSize/2 + 5);
                    // Head base
                    ctx.fillStyle = '#aaaaaa';
                    ctx.fillRect(-headSize/2, -headSize/2, headSize, headSize);
                    // Visor
                    ctx.fillStyle = '#00ddff';
                    ctx.shadowColor = '#00bbff';
                    ctx.shadowBlur = 15;
                    ctx.fillRect(-headSize/3, -headSize/6, headSize*2/3, headSize/4);
                    ctx.shadowBlur = 0;
                    // Antenna
                    ctx.fillStyle = '#ffaa00';
                    ctx.fillRect(-3, -headSize/2 - 15, 6, 15);
                    ctx.beginPath();
                    ctx.arc(0, -headSize/2 - 15, 6, 0, 2*Math.PI);
                    ctx.fill();
                    // Headband (kata)
                    if (isKata) {
                        ctx.strokeStyle = headbandColor;
                        ctx.lineWidth = 6;
                        ctx.beginPath();
                        ctx.arc(0, 0, headSize/2 + 2, 0, 2*Math.PI);
                        ctx.stroke();
                    }
                    ctx.restore();

                    // ---- Arms ----
                    const shoulderX = torsoWidth/2 + 5;
                    const shoulderYPos = -torsoHeight/2 + 10;

                    // Left arm
                    ctx.save();
                    ctx.translate(-shoulderX, shoulderYPos);
                    const leftSwing = (animCommand === 'walk' || animCommand === 'run') ? -swing : 0;
                    ctx.rotate(leftSwing * 0.5);
                    ctx.fillStyle = kimonoColor;
                    ctx.fillRect(-8, 0, 16, armLen);
                    // Hand
                    ctx.fillStyle = '#cccccc';
                    ctx.fillRect(-6, armLen-5, 12, 12);
                    ctx.restore();

                    // Right arm
                    ctx.save();
                    ctx.translate(shoulderX, shoulderYPos);
                    const rightSwing = (animCommand === 'walk' || animCommand === 'run') ? swing : 0;
                    ctx.rotate(rightSwing * 0.5);
                    ctx.fillStyle = kimonoColor;
                    ctx.fillRect(-8, 0, 16, armLen);
                    ctx.fillStyle = '#cccccc';
                    ctx.fillRect(-6, armLen-5, 12, 12);
                    ctx.restore();

                    // ---- Legs ----
                    const hipYPos = torsoHeight/2 - 5;
                    const legWidth = 12;

                    // Left leg
                    ctx.save();
                    ctx.translate(-torsoWidth/4, hipYPos);
                    const leftLegSwing = (animCommand === 'walk' || animCommand === 'run') ? -swing : 0;
                    ctx.rotate(leftLegSwing * 0.5);
                    ctx.fillStyle = kimonoColor;
                    ctx.fillRect(-legWidth/2, 0, legWidth, legLen);
                    ctx.fillStyle = '#333333';
                    ctx.fillRect(-legWidth/2 - 3, legLen-5, legWidth+6, 8);
                    ctx.restore();

                    // Right leg
                    ctx.save();
                    ctx.translate(torsoWidth/4, hipYPos);
                    const rightLegSwing = (animCommand === 'walk' || animCommand === 'run') ? swing : 0;
                    ctx.rotate(rightLegSwing * 0.5);
                    ctx.fillStyle = kimonoColor;
                    ctx.fillRect(-legWidth/2, 0, legWidth, legLen);
                    ctx.fillStyle = '#333333';
                    ctx.fillRect(-legWidth/2 - 3, legLen-5, legWidth+6, 8);
                    ctx.restore();

                    ctx.restore(); // restore from center translation
                }

                // Animation update
                function update(delta) {
                    if (kataRunning) {
                        // Kata logic
                        if (kataComplete) return;
                        kataActionTime += delta;
                        if (kataAction === null) return;
                        const type = kataAction[0];
                        const duration = kataAction[1];
                        if (type === 'idle') {
                            if (kataActionTime >= duration) {
                                nextKataAction();
                            }
                            return;
                        }
                        if (type === 'walk' || type === 'run') {
                            animCommand = type;
                            loopAnimation = true;
                            isAnimating = true;
                            hasStarted = true;
                            if (kataActionTime >= duration) {
                                isAnimating = false;
                                loopAnimation = false;
                                resetPose();
                                nextKataAction();
                            }
                            return;
                        }
                        if (type === 'jump' || type === 'wave' || type === 'backflip') {
                            animCommand = type;
                            loopAnimation = false;
                            isAnimating = true;
                            hasStarted = true;
                            if (!isAnimating && hasStarted) {
                                hasStarted = false;
                                nextKataAction();
                            }
                            return;
                        }
                        if (type === 'bow') {
                            bowActive = true;
                            bowProgress += delta / duration;
                            if (bowProgress >= 1) {
                                bowProgress = 1;
                                if (kataActionTime >= duration + 0.2) {
                                    bowActive = false;
                                    resetPose();
                                    nextKataAction();
                                }
                            }
                            return;
                        }
                    } else {
                        // Normal command animation
                        if (isAnimating && hasStarted) {
                            animTime += delta;
                            if (loopAnimation) {
                                const speed = animCommand === 'walk' ? 2.0 : 3.0;
                                walkCycle += delta * speed;
                            } else {
                                let duration = 1.2;
                                if (animCommand === 'jump') duration = 1.2;
                                else if (animCommand === 'wave') duration = 2.0;
                                else if (animCommand === 'backflip') duration = 1.5;
                                if (animTime >= duration) {
                                    isAnimating = false;
                                    resetPose();
                                }
                            }
                        }
                    }
                }

                function nextKataAction() {
                    kataActionIndex++;
                    if (kataActionIndex >= kataSequence.length) {
                        kataRunning = false;
                        kataComplete = true;
                        resetPose();
                        return;
                    }
                    kataAction = kataSequence[kataActionIndex];
                    kataActionTime = 0;
                    const type = kataAction[0];
                    if (type === 'idle') {
                        loopAnimation = false;
                        isAnimating = false;
                        hasStarted = false;
                    } else if (type === 'walk' || type === 'run') {
                        loopAnimation = true;
                        isAnimating = true;
                        hasStarted = true;
                        animCommand = type;
                    } else if (type === 'bow') {
                        bowActive = true;
                        bowProgress = 0;
                        isAnimating = false;
                        loopAnimation = false;
                        hasStarted = false;
                    } else {
                        loopAnimation = false;
                        isAnimating = true;
                        hasStarted = true;
                        animCommand = type;
                    }
                }

                function resetPose() {
                    walkCycle = 0;
                    bowActive = false;
                    bowProgress = 0;
                    // not resetting animCommand, but will be overridden
                }

                // Main draw loop
                let prevTime = performance.now();

                function draw(time) {
                    const delta = (time - prevTime) / 1000;
                    prevTime = time;
                    // Cap delta to avoid jumps
                    const dt = Math.min(delta, 0.05);
                    update(dt);

                    // Clear
                    ctx.clearRect(0, 0, width, height);

                    // Background grid
                    ctx.strokeStyle = '#223344';
                    ctx.lineWidth = 1;
                    for (let i = 0; i < width; i += 50) {
                        ctx.beginPath();
                        ctx.moveTo(i, 0);
                        ctx.lineTo(i, height);
                        ctx.stroke();
                    }
                    for (let i = 0; i < height; i += 50) {
                        ctx.beginPath();
                        ctx.moveTo(0, i);
                        ctx.lineTo(width, i);
                        ctx.stroke();
                    }

                    // Determine swing for walk/run
                    let swing = 0;
                    if (animCommand === 'walk' || animCommand === 'run') {
                        swing = Math.sin(walkCycle) * 0.5;
                    }

                    // Apply bow effect
                    let bowAngle = 0;
                    if (bowActive) {
                        const ease = bowProgress < 0.5 ? 2*bowProgress*bowProgress : 1 - Math.pow(-2*bowProgress+2, 2)/2;
                        bowAngle = ease * 0.4;
                    }

                    // Draw robot with swing and bow
                    ctx.save();
                    ctx.translate(0, 0); // base
                    if (bowAngle !== 0) {
                        ctx.rotate(bowAngle);
                    }
                    drawRobot(bowAngle, swing);
                    ctx.restore();

                    // Draw command text
                    ctx.fillStyle = '#8899bb';
                    ctx.font = '18px Arial';
                    ctx.fillText('Command: ' + animCommand, 20, 30);

                    requestAnimationFrame(draw);
                }

                // Initialize kata if needed
                if (kataSequence.length > 0) {
                    kataRunning = true;
                    kataActionIndex = 0;
                    kataActionTime = 0;
                    kataComplete = false;
                    kataAction = kataSequence[0];
                    const type = kataAction[0];
                    if (type === 'idle') {
                        loopAnimation = false;
                        isAnimating = false;
                        hasStarted = false;
                    } else if (type === 'walk' || type === 'run') {
                        loopAnimation = true;
                        isAnimating = true;
                        hasStarted = true;
                        animCommand = type;
                    } else if (type === 'bow') {
                        bowActive = true;
                        bowProgress = 0;
                        isAnimating = false;
                        loopAnimation = false;
                        hasStarted = false;
                    } else {
                        loopAnimation = false;
                        isAnimating = true;
                        hasStarted = true;
                        animCommand = type;
                    }
                } else {
                    // Start with idle
                    resetPose();
                    if (animCommand !== 'idle' && validCommands.includes(animCommand)) {
                        isAnimating = true;
                        hasStarted = true;
                        if (animCommand === 'walk' || animCommand === 'run') {
                            loopAnimation = true;
                        }
                    }
                }

                // Start animation loop
                requestAnimationFrame(draw);
            })();
        </script>
    </body>
    </html>
    """

    # Replace placeholders
    html = html_template.replace('ROBOT_NAME', robot_name)
    html = html.replace('COMMAND', command if command else 'Idle')
    html = html.replace('MAIN_COLOR', main_color)
    html = html.replace('ACCENT_COLOR', f'rgb({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]})')
    html = html.replace('KIMONO_COLOR', kimono_color)
    html = html.replace('BELT_COLOR', belt_color)
    html = html.replace('HEADBAND_COLOR', headband_color)
    html = html.replace('IS_KATA', 'true' if is_kata else 'false')
    html = html.replace('ANIM_CMD', anim_cmd)
    html = html.replace('KATA_SEQUENCE', kata_sequence_json)
    # Replace validCommands placeholder
    html = html.replace('const validCommands = [];', f'const validCommands = {json.dumps(valid_commands)};')

    return html

# ========== SESSION STATE ==========
if 'robot_selected' not in st.session_state: st.session_state.robot_selected = "Red Titan"
if 'command' not in st.session_state: st.session_state.command = ""
if 'speak_text' not in st.session_state: st.session_state.speak_text = ""
if 'last_action' not in st.session_state: st.session_state.last_action = "idle"
if 'history' not in st.session_state: st.session_state.history = []
if 'last_spoken_text' not in st.session_state: st.session_state.last_spoken_text = ""
if 'last_spoken_audio' not in st.session_state: st.session_state.last_spoken_audio = None
if 'last_spoken_timestamp' not in st.session_state: st.session_state.last_spoken_timestamp = 0
if 'kata' not in st.session_state: st.session_state.kata = None

# ========== HEADER ==========
st.markdown("""
<div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #2a3a5a; margin-bottom: 30px;">
    <h1 style="color: #00d4ff; font-size: 2.8rem; margin: 0; text-shadow: 0 0 30px rgba(0,212,255,0.2);">🤖 Robotic Control Center</h1>
    <p style="color: #8899bb; font-size: 1.1rem;">Select a robot, command it, and watch it perform – built by GlobalInternet.py</p>
    <span style="display: inline-block; background: #00ff64; color: #0a0a0f; padding: 4px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; animation: pulse 2s infinite;">● LIVE SIMULATION</span>
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
    
    st.markdown("### 🤖 Robot Selection")
    robot_names = list(ROBOTS.keys())
    selected = st.selectbox("Select Robot", options=robot_names, index=robot_names.index(st.session_state.robot_selected), key="robot_select")
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
    
    st.markdown("### 🥋 Kata Performance")
    kata_names = list(KATAS.keys())
    kata_selected = st.selectbox("Select Kata", options=["None"] + kata_names, 
                                 index=0 if st.session_state.kata is None else kata_names.index(st.session_state.kata) + 1, key="kata_select")
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
            <span style="color: #8899bb; font-size: 0.8rem;">Active Kata</span><br>
            <span style="color: #00d4ff; font-weight: 600;">{st.session_state.kata}</span><br>
            <span style="color: #8899bb; font-size: 0.8rem;">Belt: {kata_info['belt_rank']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎮 Commands")
    st.markdown("*Walk and Run loop continuously. Jump, Wave, Backflip play once.*")
    action_input = st.text_input("Action (e.g., walk, run, jump, wave, backflip)", key="action_input", placeholder="e.g., backflip")
    if st.button("▶️ Execute Action", use_container_width=True):
        if action_input.strip():
            st.session_state.kata = None
            st.session_state.command = action_input.strip()
            st.session_state.last_action = action_input.strip().lower()
            st.rerun()
        else:
            st.warning("Please enter an action.")
    
    st.markdown("---")
    st.markdown("### 🗣️ Speech")
    speak_input = st.text_input("Speak (text)", key="speak_input", placeholder="e.g., Hello, I am your robot.")
    if st.button("🔊 Make Robot Speak", use_container_width=True):
        if speak_input.strip():
            st.session_state.speak_text = speak_input.strip()
            audio_bytes = generate_audio(speak_input.strip(), "en")
            if audio_bytes:
                st.session_state.last_spoken_text = speak_input.strip()
                st.session_state.last_spoken_audio = audio_bytes
                st.session_state.last_spoken_timestamp = time.time()
                st.rerun()
            else:
                st.error("❌ Speech generation failed.")
        else:
            st.warning("Please enter text to speak.")
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("""
    <div style="background: rgba(20,30,50,0.8); border: 1px solid #2a3a5a; border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #8899bb;">
        <strong style="color: #00d4ff;">Email:</strong> deslandes78@gmail.com<br>
        <strong style="color: #00d4ff;">Phone:</strong> (509) 4738-5663<br>
        <strong style="color: #00d4ff;">Website:</strong> <a href="https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/" style="color: #00d4ff;" target="_blank">globalinternet-py.com</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔧 Status")
    st.markdown(f"**Current Robot:** {st.session_state.robot_selected}")
    st.markdown(f"**Last Action:** {st.session_state.last_action}")
    if st.session_state.kata: st.markdown(f"**Kata:** {st.session_state.kata}")

# ========== MAIN CONTENT ==========
col_view, col_info = st.columns([3, 1])

with col_view:
    st.markdown("### 🖥️ Robot View")
    viewer_html = get_robot_viewer_html(
        st.session_state.robot_selected,
        st.session_state.command if st.session_state.kata is None else "",
        st.session_state.kata
    )
    
    # Encode as data URI and use st.iframe
    data_uri = "data:text/html;charset=utf-8," + urllib.parse.quote(viewer_html)
    st.iframe(data_uri, height=650)

with col_info:
    st.markdown(f"""
    <div class="status-panel">
        <div class="label">Current Robot</div>
        <div class="value">{st.session_state.robot_selected}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="status-panel">
        <div class="label">Last Action</div>
        <div class="value">{st.session_state.last_action if st.session_state.last_action != "idle" else "—"}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.kata:
        st.markdown(f"""
        <div class="status-panel" style="border-color: #ffaa00;">
            <div class="label">Kata</div>
            <div class="value" style="color: #ffaa00;">{st.session_state.kata}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.last_spoken_audio and st.session_state.last_spoken_timestamp > 0:
        st.audio(st.session_state.last_spoken_audio, format="audio/mp3", autoplay=True)
        st.caption(f"🔊 Speaking: {st.session_state.last_spoken_text[:50]}...")
        if st.button("🔁 Replay Voice"): st.rerun()
    
    with st.expander("📜 Backstage – Command History", expanded=False):
        if st.session_state.history:
            for cmd, status in reversed(st.session_state.history[-10:]):
                st.markdown(f"""
                <div style="background: rgba(0,212,255,0.05); border-left: 3px solid #00d4ff; padding: 5px 10px; margin: 5px 0; border-radius: 4px;">
                    <span style="color: #00d4ff;">▶️</span> <span style="color: #ffffff;">{cmd}</span><br>
                    <span style="color: #8899bb; font-size: 0.8rem;">{status}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No commands yet. Send a command from the sidebar.")

# ---------- Speak ----------
if st.session_state.last_spoken_text and st.session_state.last_spoken_audio:
    if not any("Speak:" in h[0] and st.session_state.last_spoken_text in h[0] for h in st.session_state.history):
        st.session_state.history.append((f"Speak: {st.session_state.last_spoken_text}", "Speech played"))
        if len(st.session_state.history) > 20:
            st.session_state.history = st.session_state.history[-20:]

# ========== FOOTER ==========
st.markdown("""
<div class="footer">
    <p>© 2026 GlobalInternet.py Online Software Company</p>
    <p>Built by <strong>Gesner Deslandes</strong> | (509) 4738-5663 | deslandes78@gmail.com</p>
    <p style="font-size:0.8rem; color:#445566;">🤖 Simulated robot control – ready for real-world hardware integration.</p>
</div>
""", unsafe_allow_html=True)
