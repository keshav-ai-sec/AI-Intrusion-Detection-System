document.addEventListener('DOMContentLoaded', () => {

    const trafficTableBody = document.getElementById('traffic-table-body');
    const toggleStreamBtn = document.getElementById('toggle-stream');
    
    // Stat elements
    const totalAnalyzedEl = document.getElementById('total-analyzed');
    const threatsBlockedEl = document.getElementById('threats-blocked');
    const systemStatusEl = document.getElementById('system-status');

    let streamActive = true;
    let streamInterval;
    let localTotalAnalyzed = 0;
    let localThreatsBlocked = 0;

    // Fetch initial stats
    async function fetchStats() {
        try {
            const res = await fetch('/api/stats');
            const data = await res.json();
            localTotalAnalyzed = data.total_analyzed;
            localThreatsBlocked = data.threats_blocked;
            updateStatUI();
        } catch (e) {
            console.error("Error fetching stats", e);
        }
    }

    function updateStatUI() {
        totalAnalyzedEl.innerText = localTotalAnalyzed.toLocaleString();
        threatsBlockedEl.innerText = localThreatsBlocked.toLocaleString();

        if (localThreatsBlocked > 2000) {
            systemStatusEl.innerText = "Under Attack";
            systemStatusEl.className = "danger-text";
            document.querySelector('.dot').className = "dot pulse-danger";
        }
    }

    // Fetch a simulated packet
    async function fetchPacket() {
        if (!streamActive) return;

        try {
            const res = await fetch('/api/stream');
            const data = await res.json();
            renderPacket(data);
        } catch (e) {
            console.error("Error fetching stream data", e);
        }
    }

    function renderPacket(data) {
        const row = document.createElement('tr');
        row.className = 'new-row-animation';

        const timeString = new Date().toLocaleTimeString('en-US', { hour12: false, hour: "numeric", minute: "numeric", second: "numeric" });
        
        const isThreat = data.analysis.prediction === 1;
        const labelClass = isThreat ? 'danger' : 'safe';
        const labelText = isThreat ? 'ATTACK' : 'BENIGN';
        
        // Update stats
        localTotalAnalyzed++;
        if (isThreat) {
            localThreatsBlocked++;
            row.style.background = "rgba(239, 68, 68, 0.05)";
        }
        updateStatUI();

        row.innerHTML = `
            <td>${timeString}</td>
            <td style="font-family: monospace;">${data.packet.source_ip}</td>
            <td style="font-family: monospace;">${data.packet.dest_ip}</td>
            <td>${data.packet.protocol} / ${data.packet.port}</td>
            <td>${(data.analysis.confidence * 100).toFixed(2)}%</td>
            <td><span class="badge ${labelClass}">${labelText}</span></td>
        `;

        trafficTableBody.prepend(row);

        // Keep only last 20 rows
        if (trafficTableBody.children.length > 20) {
            trafficTableBody.lastChild.remove();
        }
    }

    // Controls
    toggleStreamBtn.addEventListener('click', () => {
        streamActive = !streamActive;
        toggleStreamBtn.innerText = streamActive ? 
            "Pause Stream" : "Resume Stream";
            
        toggleStreamBtn.classList.toggle('paused');
    });

    // Initialize
    fetchStats();
    
    // Poll the stream endpoint continuously, but dynamically based on async completion
    async function loopStream() {
        await fetchPacket();
        if (streamActive) {
            setTimeout(loopStream, 600); // Wait 600ms before requesting next packet
        } else {
            setTimeout(loopStream, 2000); // Check loop slower if paused
        }
    }
    
    // Start loop
    loopStream();
});
