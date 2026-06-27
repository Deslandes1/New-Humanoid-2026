import streamlit as st
import os
import tempfile
import time
import json
import urllib.parse
import random

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
    # Use "frontflip" as the flip in kata sequences
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
</style>
""", unsafe_allow_html=True)

# ---- 3D Viewer HTML generator (Transformer-style robot) ----
def get_robot_viewer_html(robot_name, command=None, kata_name=None):
    # Colors
    color_map = {r: ROBOTS[r]["color"] for r in ROBOTS}
    main_color = color_map.get(robot_name, "#3388ff")
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    mr = hex_to_rgb(main_color)
    accent_rgb = (min(255, mr[0]+60), min(255, mr[1]+60), min(255, mr[2]+60))
    accent_color = f"rgb({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]})"

    # Kata info
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

    # Command – include both frontflip and backflip
    valid_commands = ['walk', 'run', 'jump', 'wave', 'frontflip', 'backflip', 'bow']
    cmd_lower = command.lower() if command else "idle"
    anim_cmd = cmd_lower if cmd_lower in valid_commands else 'idle'

    # Kata sequence
    kata_sequence = get_kata_sequence(kata_name) if is_kata else []
    kata_sequence_json = json.dumps(kata_sequence)

    # Build HTML with Three.js embedded – all JS braces are doubled!
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

        // DOM elements for step info
        const stepInfoEl = document.getElementById('step-info');
        const progressBar = document.getElementById('step-progress-bar');

        // ---- Setup scene ----
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

        // ---- Controls ----
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

        // ---- Robot construction (Transformer style) ----
        const robotGroup = new THREE.Group();
        robotGroup.position.y = 0.5;

        // Materials
        const mainMat = new THREE.MeshStandardMaterial({{ color: '{main_color}', roughness: 0.4, metalness: 0.6 }});
        const accentMat = new THREE.MeshStandardMaterial({{ color: '{accent_color}', roughness: 0.3, metalness: 0.5 }});
        const darkMat = new THREE.MeshStandardMaterial({{ color: '#333333', roughness: 0.5, metalness: 0.4 }});
        const jointMat = new THREE.MeshStandardMaterial({{ color: '#888888', roughness: 0.3, metalness: 0.7 }});
        const visorMat = new THREE.MeshStandardMaterial({{ color: '#00ddff', emissive: '#0066aa', emissiveIntensity: 0.5 }});
        const antennaMat = new THREE.MeshStandardMaterial({{ color: '#ffaa00', emissive: '#ff8800', emissiveIntensity: 0.3 }});
        const headbandMat = new THREE.MeshStandardMaterial({{ color: '{headband_color}', roughness: 0.3 }});
        const beltMat = new THREE.MeshStandardMaterial({{ color: '{belt_color}', roughness: 0.5 }});

        // ---- Torso ----
        const torsoGroup = new THREE.Group();
        robotGroup.add(torsoGroup);

        // Main torso box
        const torsoGeo = new THREE.BoxGeometry(0.9, 1.1, 0.6);
        const torso = new THREE.Mesh(torsoGeo, mainMat);
        torso.position.y = 0.55;
        torso.castShadow = true;
        torsoGroup.add(torso);

        // Chest plate
        const chestGeo = new THREE.BoxGeometry(0.7, 0.4, 0.15);
        const chest = new THREE.Mesh(chestGeo, accentMat);
        chest.position.set(0, 0.3, 0.4);
        torsoGroup.add(chest);

        // Abs / belt
        const beltGeo = new THREE.BoxGeometry(0.8, 0.12, 0.5);
        const belt = new THREE.Mesh(beltGeo, beltMat);
        belt.position.set(0, 0.0, 0);
        torsoGroup.add(belt);

        // Pelvis / hip
        const hipGeo = new THREE.BoxGeometry(0.7, 0.2, 0.5);
        const hip = new THREE.Mesh(hipGeo, darkMat);
        hip.position.set(0, -0.4, 0);
        torsoGroup.add(hip);

        // ---- Neck ----
        const neckGeo = new THREE.CylinderGeometry(0.15, 0.15, 0.15);
        const neck = new THREE.Mesh(neckGeo, jointMat);
        neck.position.set(0, 1.1, 0);
        torsoGroup.add(neck);

        // ---- Head ----
        const headGroup = new THREE.Group();
        headGroup.position.set(0, 1.2, 0);
        torsoGroup.add(headGroup);

        const headGeo = new THREE.BoxGeometry(0.5, 0.5, 0.5);
        const head = new THREE.Mesh(headGeo, mainMat);
        head.castShadow = true;
        headGroup.add(head);

        // Visor
        const visorGeo = new THREE.BoxGeometry(0.35, 0.12, 0.05);
        const visor = new THREE.Mesh(visorGeo, visorMat);
        visor.position.set(0, 0.0, 0.28);
        head.add(visor);

        // Antenna
        const antGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.2);
        const ant = new THREE.Mesh(antGeo, antennaMat);
        ant.position.set(0, 0.35, 0);
        head.add(ant);
        const antBall = new THREE.SphereGeometry(0.06);
        const ball = new THREE.Mesh(antBall, antennaMat);
        ball.position.set(0, 0.45, 0);
        head.add(ball);

        // Headband (kata)
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

        // Left shoulder
        const leftShoulder = new THREE.Mesh(shoulderPadGeo, shoulderPadMat);
        leftShoulder.position.set(-0.6, 0.9, 0);
        torsoGroup.add(leftShoulder);

        // Right shoulder
        const rightShoulder = new THREE.Mesh(shoulderPadGeo, shoulderPadMat);
        rightShoulder.position.set(0.6, 0.9, 0);
        torsoGroup.add(rightShoulder);

        // ---- Arms ----
        // Left arm
        const leftArmGroup = new THREE.Group();
        leftArmGroup.position.set(-0.65, 0.8, 0);
        torsoGroup.add(leftArmGroup);

        // Upper arm
        const upperArmGeo = new THREE.BoxGeometry(0.2, 0.4, 0.2);
        const leftUpperArm = new THREE.Mesh(upperArmGeo, mainMat);
        leftUpperArm.position.y = -0.2;
        leftUpperArm.castShadow = true;
        leftArmGroup.add(leftUpperArm);

        // Elbow joint
        const elbowGeo = new THREE.SphereGeometry(0.08, 8, 8);
        const leftElbow = new THREE.Mesh(elbowGeo, jointMat);
        leftElbow.position.y = -0.4;
        leftArmGroup.add(leftElbow);

        // Forearm group (for elbow rotation)
        const leftForearmGroup = new THREE.Group();
        leftForearmGroup.position.y = -0.4;
        leftArmGroup.add(leftForearmGroup);

        const forearmGeo = new THREE.BoxGeometry(0.18, 0.3, 0.18);
        const leftForearm = new THREE.Mesh(forearmGeo, darkMat);
        leftForearm.position.y = -0.15;
        leftForearm.castShadow = true;
        leftForearmGroup.add(leftForearm);

        // Hand
        const handGeo = new THREE.BoxGeometry(0.15, 0.1, 0.15);
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
        // Left leg
        const leftLegGroup = new THREE.Group();
        leftLegGroup.position.set(-0.25, -0.45, 0);
        torsoGroup.add(leftLegGroup);

        // Upper leg
        const upperLegGeo = new THREE.BoxGeometry(0.25, 0.4, 0.25);
        const leftUpperLeg = new THREE.Mesh(upperLegGeo, mainMat);
        leftUpperLeg.position.y = -0.2;
        leftUpperLeg.castShadow = true;
        leftLegGroup.add(leftUpperLeg);

        // Knee joint
        const kneeGeo = new THREE.SphereGeometry(0.1, 8, 8);
        const leftKnee = new THREE.Mesh(kneeGeo, jointMat);
        leftKnee.position.y = -0.4;
        leftLegGroup.add(leftKnee);

        // Lower leg group
        const leftLowerLegGroup = new THREE.Group();
        leftLowerLegGroup.position.y = -0.4;
        leftLegGroup.add(leftLowerLegGroup);

        const lowerLegGeo = new THREE.BoxGeometry(0.22, 0.35, 0.22);
        const leftLowerLeg = new THREE.Mesh(lowerLegGeo, darkMat);
        leftLowerLeg.position.y = -0.175;
        leftLowerLeg.castShadow = true;
        leftLowerLegGroup.add(leftLowerLeg);

        // Foot
        const footGeo = new THREE.BoxGeometry(0.3, 0.08, 0.4);
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
        }};

        // Helper to update step info
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
                // Single command
                if (state.cmd !== 'idle') {{
                    stepInfoEl.textContent = `▶️ ${{state.cmd.toUpperCase()}}`;
                    progressBar.style.width = (state.animating ? (state.animTimer / 1.5 * 100) : 0) + '%';
                }} else {{
                    stepInfoEl.textContent = '⏳ Idle';
                    progressBar.style.width = '0%';
                }}
            }}
        }}

        // ---- Update function ----
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
                        updateStepInfo();
                    }} else {{
                        state.kataComplete = true;
                        state.kataRunning = false;
                        state.cmd = 'idle';
                        state.animating = false;
                        state.looping = false;
                        state.bowActive = false;
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
                    // updateStepInfo will be called when next action starts
                }}
                if (state.cmd === 'bow') state.bowProgress = Math.min(state.kataTimer / dur, 1.0);
                return;
            }}

            // Normal command
            if (state.cmd === 'idle') {{
                state.animating = false; state.looping = false; state.bowActive = false;
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
                updateStepInfo(); // update progress bar for single commands
            }}
        }}

        // ---- Apply animations to robot ----
        function animateRobot() {{
            const isRun = (state.cmd === 'run');
            const amp = isRun ? 1.2 : 0.5;
            const swing = (state.cmd === 'walk' || isRun) ? Math.sin(state.walkCycle) * amp : 0;

            // Reset
            leftArmGroup.rotation.x = 0;
            rightArmGroup.rotation.x = 0;
            leftForearmGroup.rotation.x = 0;
            rightForearmGroup.rotation.x = 0;
            leftLegGroup.rotation.x = 0;
            rightLegGroup.rotation.x = 0;
            leftLowerLegGroup.rotation.x = 0;
            rightLowerLegGroup.rotation.x = 0;
            robotGroup.rotation.x = 0;
            robotGroup.position.y = 0.5;
            robotGroup.position.z = 0;
            torsoGroup.rotation.x = 0;

            // Walk/Run
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

            // Jump
            if (state.cmd === 'jump' && state.animating) {{
                const t = Math.min(state.animTimer / 1.2, 1);
                const y = 1.5 * 4 * t * (1 - t);
                robotGroup.position.y = 0.5 + y;
            }}

            // Frontflip
            if (state.cmd === 'frontflip' && state.animating) {{
                const t = Math.min(state.animTimer / 1.5, 1);
                const y = 2.0 * 4 * t * (1 - t);
                robotGroup.position.y = 0.5 + y;
                robotGroup.rotation.x = t * 2 * Math.PI;
                robotGroup.position.z = -0.3 * Math.sin(t * Math.PI);
            }}

            // Backflip
            if (state.cmd === 'backflip' && state.animating) {{
                const t = Math.min(state.animTimer / 1.5, 1);
                const y = 2.0 * 4 * t * (1 - t);
                robotGroup.position.y = 0.5 + y;
                robotGroup.rotation.x = -t * 2 * Math.PI;
                robotGroup.position.z = 0.3 * Math.sin(t * Math.PI);
            }}

            // Wave
            if (state.cmd === 'wave' && state.animating) {{
                rightArmGroup.rotation.x = -0.8 + Math.sin(state.animTimer * 6) * 0.3;
                rightForearmGroup.rotation.x = 0.2 + Math.sin(state.animTimer * 6 + 1) * 0.2;
            }}

            // Bow
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
            updateStepInfo();  // keep UI updated

            controls.update();
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }}

        // ---- Resize handler ----
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        // ---- Init ----
        state.cmd = state.initCmd;
        if (state.kataSeq.length > 0) {{
            state.kataRunning = true;
            state.kataIdx = 0;
            state.kataTimer = 0;
            state.kataComplete = false;
            state.kataAction = null;
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
    selected = st.selectbox("Select Robot", options=robot_names,
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

    st.markdown("### 🥋 Kata Performance")
    kata_names = list(KATAS.keys())
    kata_selected = st.selectbox("Select Kata", options=["None"] + kata_names,
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
            <span style="color: #8899bb; font-size: 0.8rem;">Active Kata</span><br>
            <span style="color: #00d4ff; font-weight: 600;">{st.session_state.kata}</span><br>
            <span style="color: #8899bb; font-size: 0.8rem;">Belt: {kata_info['belt_rank']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🎮 Commands")
    st.markdown("*Walk and Run loop continuously. Jump, Wave, Frontflip, Backflip, Bow play once.*")
    st.markdown("*You can also type a kata name (e.g., `Taikyoku Shodan`) to run the full sequence.*")
    action_input = st.text_input("Action or Kata", key="action_input",
                                 placeholder="e.g., backflip or Taikyoku Shodan")
    if st.button("▶️ Execute Action", use_container_width=True):
        if action_input.strip():
            # Check if input matches a kata name (case-insensitive)
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
                # Treat as single command
                st.session_state.kata = None
                st.session_state.command = action_input.strip()
                st.session_state.last_action = action_input.strip().lower()
                st.rerun()
        else:
            st.warning("Please enter an action or kata name.")

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
                st.error("❌ Speech generation failed. Please ensure gTTS is installed.")
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
    if st.session_state.kata:
        st.markdown(f"**Kata:** {st.session_state.kata}")

# ========== MAIN CONTENT ==========
col_view, col_info = st.columns([3, 1])

with col_view:
    st.markdown("### 🖥️ Robot View")
    viewer_html = get_robot_viewer_html(
        st.session_state.robot_selected,
        st.session_state.command if st.session_state.kata is None else "",
        st.session_state.kata
    )
    data_uri = "data:text/html;charset=utf-8," + urllib.parse.quote(viewer_html)
    data_uri += f"#{random.randint(1, 999999)}"
    st.iframe(data_uri, height=650, width=700)

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
        if st.button("🔁 Replay Voice"):
            st.rerun()

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

# ---------- Speak history ----------
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
