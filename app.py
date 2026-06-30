// ---- Update logic ----
function update(dt) {
    // ---- Handle kata sequence ----
    if (state.kataRunning) {
        if (state.kataAction === null) {
            // Start first step
            state.kataAction = state.kataSeq[state.kataIdx];
            state.cmd = state.kataAction[0];
            state.animTimer = 0;
            state.animating = true;
            if (state.cmd === 'walk' || state.cmd === 'run') {
                state.looping = true;
                state.walkCycle = 0;
            } else if (state.cmd === 'bow') {
                state.bowActive = true;
                state.bowProgress = 0;
            } else {
                state.looping = false;
            }
        } else {
            // Wait for current step to finish (animating becomes false)
            if (!state.animating) {
                // Move to next step
                state.kataIdx++;
                if (state.kataIdx >= state.kataSeq.length) {
                    // Kata complete
                    state.kataRunning = false;
                    state.kataComplete = true;
                    state.cmd = 'idle';
                    state.kataAction = null;
                } else {
                    // Start next step
                    state.kataAction = state.kataSeq[state.kataIdx];
                    state.cmd = state.kataAction[0];
                    state.animTimer = 0;
                    state.animating = true;
                    if (state.cmd === 'walk' || state.cmd === 'run') {
                        state.looping = true;
                        state.walkCycle = 0;
                    } else if (state.cmd === 'bow') {
                        state.bowActive = true;
                        state.bowProgress = 0;
                    } else {
                        state.looping = false;
                    }
                }
            }
        }
        updateStepInfo();
        return;
    }

    // ---- Normal command handling (rest unchanged) ----
    // ...
}
