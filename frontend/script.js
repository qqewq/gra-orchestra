const API_BASE = "http://localhost:8000";

async function fetchState() {
    const res = await fetch(`${API_BASE}/state`);
    return await res.json();
}

async function stepGRA(steps = 1) {
    await fetch(`${API_BASE}/step`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ steps })
    });
    updateUI();
}

async function connectAgent(agentId) {
    await fetch(`${API_BASE}/connect`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agent_id: agentId, local_pena_threshold: 1.2 })
    });
    updateUI();
}

async function disconnectAgent(agentId) {
    await fetch(`${API_BASE}/disconnect/${agentId}`, { method: "POST" });
    updateUI();
}

async function updateUI() {
    const state = await fetchState();
    document.getElementById("global_pena").innerText = state.global_pena.toFixed(4);
    document.getElementById("delta_global").innerText = state.delta_global.toFixed(4);
    document.getElementById("delta2_global").innerText = state.delta2_global.toFixed(4);
    const stabilitySpan = document.getElementById("stability");
    if (state.is_stable) {
        stabilitySpan.innerHTML = "✅ Стабилен (Φ→0, ΔΦ→0, Δ²Φ>0)";
        stabilitySpan.style.color = "#6fcf97";
    } else {
        stabilitySpan.innerHTML = "⚠️ Нестабилен — требуется GRA-шаг";
        stabilitySpan.style.color = "#f0a3a3";
    }

    const agentsDiv = document.getElementById("agentsList");
    agentsDiv.innerHTML = "";
    for (const agent of state.agents) {
        const card = document.createElement("div");
        card.className = `agent-card ${agent.is_connected ? "connected" : "disconnected"}`;
        card.innerHTML = `
            <div class="agent-name">
                ${agent.id}
                <span>${agent.is_connected ? "🎧" : "🔌"}</span>
            </div>
            <div class="local-pena">🔥 локальная пена = ${agent.local_pena.toFixed(3)}</div>
            <div class="align-error">⚖️ align error = ${agent.align_error.toFixed(3)}</div>
            <div class="agent-actions">
                ${!agent.is_connected ? `<button class="small" onclick="connectAgent('${agent.id}')">Подключить</button>` : 
                                          `<button class="small" onclick="disconnectAgent('${agent.id}')">Отключить</button>`}
            </div>
        `;
        agentsDiv.appendChild(card);
    }
}

document.getElementById("stepBtn").addEventListener("click", () => stepGRA(1));

setInterval(updateUI, 1000);
updateUI();
