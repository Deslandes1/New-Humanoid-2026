from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>🥋 Kata Performance</title>
    <style>
        /* ─── Reset & base ─── */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #0b0e14;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .card {
            background: #1a1f2b;
            border-radius: 28px;
            padding: 32px 36px 40px;
            max-width: 640px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: 0.2s;
        }

        /* ─── Header ─── */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 28px;
        }
        .header h1 {
            font-size: 26px;
            font-weight: 700;
            color: #f0eae3;
            letter-spacing: -0.3px;
        }
        .header h1 span {
            background: linear-gradient(135deg, #f7c948, #f0a030);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .belt-badge {
            background: #f7c948;
            color: #1a1f2b;
            font-weight: 700;
            font-size: 14px;
            padding: 6px 16px;
            border-radius: 40px;
            letter-spacing: 0.3px;
            box-shadow: 0 0 20px rgba(247, 201, 72, 0.25);
        }

        /* ─── Select Kata ─── */
        .select-section {
            margin-bottom: 24px;
        }
        .select-section label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #7a8499;
            margin-bottom: 8px;
        }
        .kata-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .kata-btn {
            background: #252c3b;
            border: none;
            border-radius: 40px;
            padding: 8px 22px;
            font-size: 15px;
            font-weight: 600;
            color: #bcc3d4;
            cursor: pointer;
            transition: 0.2s;
            border: 1px solid transparent;
        }
        .kata-btn:hover {
            background: #2f3749;
            color: #e8eef5;
        }
        .kata-btn.active {
            background: #f7c948;
            color: #141a24;
            border-color: #f7c948;
            box-shadow: 0 0 24px rgba(247, 201, 72, 0.25);
        }

        /* ─── Active Kata card ─── */
        .active-card {
            background: #222a39;
            border-radius: 18px;
            padding: 20px 24px;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-left: 4px solid #f7c948;
        }
        .active-card .name {
            font-size: 20px;
            font-weight: 700;
            color: #f0eae3;
        }
        .active-card .belt {
            font-size: 14px;
            font-weight: 600;
            color: #f7c948;
            background: rgba(247, 201, 72, 0.12);
            padding: 4px 14px;
            border-radius: 40px;
        }

        /* ─── Commands info ─── */
        .commands-box {
            background: #131924;
            border-radius: 16px;
            padding: 16px 20px;
            margin-bottom: 28px;
            border: 1px solid #2a3345;
        }
        .commands-box .label {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: #5e6a80;
            margin-bottom: 6px;
        }
        .commands-box .desc {
            font-size: 15px;
            color: #bcc8de;
            line-height: 1.5;
        }
        .commands-box .desc code {
            background: #1e2738;
            padding: 2px 10px;
            border-radius: 6px;
            font-size: 13px;
            color: #f0eae3;
        }

        /* ─── Action ─── */
        .action-section {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #131924;
            border-radius: 16px;
            padding: 12px 20px 12px 24px;
            border: 1px solid #2a3345;
            transition: 0.25s;
        }
        .action-section .label {
            font-size: 14px;
            font-weight: 600;
            color: #7a8499;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .action-btn {
            background: linear-gradient(135deg, #f7c948, #e8a830);
            border: none;
            border-radius: 40px;
            padding: 10px 32px;
            font-size: 16px;
            font-weight: 700;
            color: #141a24;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 4px 16px rgba(247, 201, 72, 0.25);
            letter-spacing: 0.2px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .action-btn:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 28px rgba(247, 201, 72, 0.4);
        }
        .action-btn:active {
            transform: scale(0.96);
        }
        .action-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .action-btn .spinner {
            display: none;
            width: 18px;
            height: 18px;
            border: 2.5px solid rgba(20, 26, 36, 0.2);
            border-top-color: #141a24;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
        }
        .action-btn.running .spinner {
            display: inline-block;
        }
        .action-btn.running .btn-text {
            display: none;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        /* ─── Status / step info ─── */
        .step-info {
            margin-top: 18px;
            padding: 10px 16px;
            background: #1a212f;
            border-radius: 12px;
            font-size: 14px;
            color: #9aa9c2;
            text-align: center;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            border: 1px solid #283040;
            transition: 0.2s;
        }
        .step-info .highlight {
            color: #f7c948;
            font-weight: 700;
        }
        .step-info .done {
            color: #5fcb7a;
        }

        /* ─── Responsive ─── */
        @media (max-width: 540px) {
            .card {
                padding: 20px;
            }
            .active-card {
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
            .action-section {
                flex-wrap: wrap;
                gap: 12px;
                justify-content: center;
                padding: 16px;
            }
            .action-btn {
                width: 100%;
                justify-content: center;
            }
            .kata-list {
                gap: 6px;
            }
            .kata-btn {
                font-size: 13px;
                padding: 6px 14px;
            }
        }
    </style>
</head>
<body>

    <div class="card" id="app">
        <!-- Header -->
        <div class="header">
            <h1>🥋 <span>Kata Performance</span></h1>
            <div class="belt-badge">⚡ Live</div>
        </div>

        <!-- Select Kata -->
        <div class="select-section">
            <label>📋 Select Kata</label>
            <div class="kata-list" id="kataList">
                <button class="kata-btn" data-kata="Heian Shodan">Heian Shodan</button>
                <button class="kata-btn" data-kata="Heian Nidan">Heian Nidan</button>
                <button class="kata-btn" data-kata="Taikyoku Shodan">Taikyoku Shodan</button>
                <button class="kata-btn" data-kata="Bassai Dai">Bassai Dai</button>
            </div>
        </div>

        <!-- Active Kata -->
        <div class="active-card">
            <span class="name" id="activeName">Heian Shodan</span>
            <span class="belt" id="activeBelt">🥋 Yellow</span>
        </div>

        <!-- Commands -->
        <div class="commands-box">
            <div class="label">🎮 Commands</div>
            <div class="desc" id="commandsDesc">
                <code>Walk</code> and <code>Run</code> loop continuously.
                <code>Jump</code>, <code>Wave</code>, <code>Frontflip</code>, <code>Backflip</code>, <code>Bow</code> play once.
                <br />
                You can also type a kata name (e.g., <code>Taikyoku Shodan</code>) to run the full sequence.
            </div>
        </div>

        <!-- Action -->
        <div class="action-section">
            <span class="label">⚡ Action</span>
            <button class="action-btn" id="executeBtn">
                <span class="btn-text" id="executeLabel">▶ Heian Shodan</span>
                <span class="spinner"></span>
            </button>
        </div>

        <!-- Step info -->
        <div class="step-info" id="stepInfo">
            <span>⏸ Idle — select a kata and press <span class="highlight">Action</span></span>
        </div>
    </div>

    <script>
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  STATE
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        const state = {
            // Current kata
            selectedKata: 'Heian Shodan',

            // Kata sequences (command arrays)
            kataLibrary: {
                'Heian Shodan': [
                    ['walk', 1.2],
                    ['bow', 0.8],
                    ['walk', 0.6],
                    ['frontflip', 0.5],
                    ['run', 1.0],
                    ['backflip', 0.5],
                    ['walk', 0.8],
                    ['jump', 0.4],
                    ['bow', 0.6],
                ],
                'Heian Nidan': [
                    ['walk', 0.8],
                    ['jump', 0.4],
                    ['run', 1.2],
                    ['wave', 0.5],
                    ['walk', 0.6],
                    ['frontflip', 0.5],
                    ['bow', 0.8],
                ],
                'Taikyoku Shodan': [
                    ['walk', 0.6],
                    ['run', 0.8],
                    ['jump', 0.4],
                    ['walk', 0.6],
                    ['bow', 0.8],
                    ['backflip', 0.5],
                ],
                'Bassai Dai': [
                    ['run', 1.0],
                    ['frontflip', 0.5],
                    ['walk', 0.8],
                    ['backflip', 0.5],
                    ['jump', 0.4],
                    ['walk', 0.6],
                    ['bow', 0.8],
                    ['wave', 0.5],
                ],
            },

            // Runtime
            kataRunning: false,
            kataComplete: false,
            kataSeq: [],
            kataIdx: 0,
            kataAction: null, // current [cmd, duration]
            cmd: 'idle',
            animTimer: 0,
            animating: false,
            looping: false,
            walkCycle: 0,
            bowActive: false,
            bowProgress: 0,
            stepLabel: '',
        };

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  DOM refs
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        const activeName = document.getElementById('activeName');
        const activeBelt = document.getElementById('activeBelt');
        const executeBtn = document.getElementById('executeBtn');
        const executeLabel = document.getElementById('executeLabel');
        const stepInfo = document.getElementById('stepInfo');
        const kataBtns = document.querySelectorAll('.kata-btn');

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  HELPERS
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function getBeltForKata(name) {
            const map = {
                'Heian Shodan': 'Yellow',
                'Heian Nidan': 'Orange',
                'Taikyoku Shodan': 'White',
                'Bassai Dai': 'Green',
            };
            return map[name] || 'Yellow';
        }

        function updateStepInfo() {
            if (state.kataRunning && state.kataAction) {
                const [cmd, dur] = state.kataAction;
                const total = state.kataSeq.length;
                const current = state.kataIdx + 1;
                const progress = Math.round((state.kataIdx / total) * 100);
                state.stepLabel =
                    `🥋 <span class="highlight">${cmd}</span>  (${current}/${total})  ${progress}%`;
                stepInfo.innerHTML = state.stepLabel;
            } else if (state.kataComplete) {
                stepInfo.innerHTML = '✅ <span class="done">Kata complete!</span>  🎉';
            } else {
                stepInfo.innerHTML =
                    `⏸ Idle — select a kata and press <span class="highlight">Action</span>`;
            }
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  KATA EXECUTION — START
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function startKata(kataName) {
            // Guard: if already running, reset first
            if (state.kataRunning) {
                resetKataState();
            }

            const seq = state.kataLibrary[kataName];
            if (!seq || seq.length === 0) {
                stepInfo.innerHTML = '⚠️ Unknown kata sequence.';
                return;
            }

            // Copy sequence
            state.kataSeq = seq.map(item => [...item]);
            state.kataIdx = 0;
            state.kataRunning = true;
            state.kataComplete = false;
            state.kataAction = null; // will be picked up in update
            state.cmd = 'idle';
            state.animTimer = 0;
            state.animating = false;
            state.looping = false;
            state.walkCycle = 0;
            state.bowActive = false;
            state.bowProgress = 0;

            // UI
            executeBtn.classList.add('running');
            executeBtn.disabled = true;
            executeLabel.textContent = '▶ ' + kataName;

            // Update active display
            activeName.textContent = kataName;
            activeBelt.textContent = '🥋 ' + getBeltForKata(kataName);

            // Highlight selected kata in list
            kataBtns.forEach(btn => {
                btn.classList.toggle('active', btn.dataset.kata === kataName);
            });

            stepInfo.innerHTML = '⏳ Starting <span class="highlight">' + kataName + '</span> …';
            state.stepLabel = '';

            // The update loop will pick up the first step on next tick
            // We force one update to start immediately
            processKataStep();
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  KATA STEP PROCESSOR (called from update)
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function processKataStep() {
            if (!state.kataRunning) return;

            // If no current action, start the next one
            if (state.kataAction === null) {
                if (state.kataIdx >= state.kataSeq.length) {
                    // Finished
                    state.kataRunning = false;
                    state.kataComplete = true;
                    state.cmd = 'idle';
                    state.kataAction = null;
                    executeBtn.classList.remove('running');
                    executeBtn.disabled = false;
                    executeLabel.textContent = '▶ ' + state.selectedKata;
                    updateStepInfo();
                    return;
                }

                // Load next step
                state.kataAction = state.kataSeq[state.kataIdx];
                const [cmd, duration] = state.kataAction;
                state.cmd = cmd;
                state.animTimer = 0;
                state.animating = true;

                if (cmd === 'walk' || cmd === 'run') {
                    state.looping = true;
                    state.walkCycle = 0;
                } else if (cmd === 'bow') {
                    state.bowActive = true;
                    state.bowProgress = 0;
                    state.looping = false;
                } else {
                    state.looping = false;
                }

                updateStepInfo();
                return;
            }

            // If we have an action, check if it's done (animating flag will be set false by update)
            // This is handled in the main update loop via the animating flag.
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  RESET
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function resetKataState() {
            state.kataRunning = false;
            state.kataComplete = false;
            state.kataSeq = [];
            state.kataIdx = 0;
            state.kataAction = null;
            state.cmd = 'idle';
            state.animTimer = 0;
            state.animating = false;
            state.looping = false;
            state.walkCycle = 0;
            state.bowActive = false;
            state.bowProgress = 0;
            executeBtn.classList.remove('running');
            executeBtn.disabled = false;
            executeLabel.textContent = '▶ ' + state.selectedKata;
            updateStepInfo();
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  UPDATE LOOP  (dt in seconds)
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function update(dt) {
            // ── Handle kata sequence ──
            if (state.kataRunning) {
                if (state.kataAction === null) {
                    // Start first step (or next)
                    processKataStep();
                    // If kata just finished, processKataStep may set kataRunning = false
                    if (!state.kataRunning) {
                        updateStepInfo();
                        return;
                    }
                    // If we just loaded an action, continue
                    if (state.kataAction === null) return;
                }

                // We have an action — advance its timer
                const [cmd, duration] = state.kataAction;
                state.animTimer += dt;

                // For looping commands (walk/run), we keep going until duration is met
                if (state.looping) {
                    state.walkCycle += dt * 3.2;
                    if (state.animTimer >= duration) {
                        // Step complete
                        state.animating = false;
                        state.looping = false;
                        state.kataAction = null;
                        state.kataIdx++;
                        // Immediately process next step
                        processKataStep();
                        if (!state.kataRunning) {
                            updateStepInfo();
                        }
                        return;
                    }
                    // Still animating — update step info with progress
                    const progress = Math.min(100, Math.round((state.animTimer / duration) * 100));
                    const total = state.kataSeq.length;
                    const current = state.kataIdx + 1;
                    state.stepLabel =
                        `🥋 <span class="highlight">${cmd}</span>  (${current}/${total})  ${progress}%`;
                    stepInfo.innerHTML = state.stepLabel;
                    return;
                }

                // ── Non-looping commands (jump, wave, frontflip, backflip, bow) ──
                if (cmd === 'bow') {
                    state.bowProgress = Math.min(1, state.animTimer / duration);
                    if (state.animTimer >= duration) {
                        state.bowActive = false;
                        state.bowProgress = 0;
                        state.animating = false;
                        state.kataAction = null;
                        state.kataIdx++;
                        processKataStep();
                        if (!state.kataRunning) {
                            updateStepInfo();
                        }
                        return;
                    }
                    // Update progress
                    const progress = Math.min(100, Math.round((state.animTimer / duration) * 100));
                    const total = state.kataSeq.length;
                    const current = state.kataIdx + 1;
                    state.stepLabel =
                        `🥋 <span class="highlight">${cmd}</span>  (${current}/${total})  ${progress}%`;
                    stepInfo.innerHTML = state.stepLabel;
                    return;
                }

                // Other one-shot commands: jump, wave, frontflip, backflip
                if (state.animTimer >= duration) {
                    state.animating = false;
                    state.kataAction = null;
                    state.kataIdx++;
                    processKataStep();
                    if (!state.kataRunning) {
                        updateStepInfo();
                    }
                    return;
                }

                // Still animating a one-shot
                const progress = Math.min(100, Math.round((state.animTimer / duration) * 100));
                const total = state.kataSeq.length;
                const current = state.kataIdx + 1;
                state.stepLabel =
                    `🥋 <span class="highlight">${cmd}</span>  (${current}/${total})  ${progress}%`;
                stepInfo.innerHTML = state.stepLabel;
                return;
            }

            // ── Normal idle state (no kata running) ──
            // We just update the step info if needed
            if (!state.kataRunning && !state.kataComplete) {
                // Keep step info fresh
            }
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  ANIMATION LOOP
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        let lastTime = 0;

        function loop(time) {
            const dt = Math.min(0.05, (time - lastTime) / 1000);
            lastTime = time;

            update(dt);

            requestAnimationFrame(loop);
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  CLICK HANDLER — EXECUTE ACTION
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function handleExecute() {
            const kataName = state.selectedKata;

            // If a kata is already running, do nothing (button is disabled anyway)
            if (state.kataRunning) return;

            // If complete, reset state first
            if (state.kataComplete) {
                resetKataState();
                // Small delay so the reset renders, then start
                setTimeout(() => {
                    startKata(kataName);
                }, 50);
                return;
            }

            startKata(kataName);
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  KATA SELECTION
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function selectKata(name) {
            if (state.kataRunning) return; // can't change while running

            state.selectedKata = name;
            activeName.textContent = name;
            activeBelt.textContent = '🥋 ' + getBeltForKata(name);
            executeLabel.textContent = '▶ ' + name;

            // Highlight
            kataBtns.forEach(btn => {
                btn.classList.toggle('active', btn.dataset.kata === name);
            });

            // Reset complete state if needed
            if (state.kataComplete) {
                state.kataComplete = false;
                updateStepInfo();
            }

            stepInfo.innerHTML =
                `📌 <span class="highlight">${name}</span> selected — press Action to execute`;
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        //  INIT
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function init() {
            // Set default active
            selectKata('Heian Shodan');

            // Event: execute button
            executeBtn.addEventListener('click', handleExecute);

            // Event: kata selection buttons
            kataBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    const name = btn.dataset.kata;
                    selectKata(name);
                });
            });

            // Start animation loop
            requestAnimationFrame(loop);

            console.log('🥋 Kata Performance ready — click "Action" to execute!');
        }

        // Go
        init();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
