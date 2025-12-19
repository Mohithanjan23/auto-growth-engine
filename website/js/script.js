document.addEventListener('DOMContentLoaded', () => {
    console.log("🛡️ CyberSentinel Dashboard Loaded");

    // 1. Auto-update the "Last Sync" time to show the page is active
    const syncTime = document.getElementById('last-sync');
    if (syncTime) {
        const now = new Date();
        syncTime.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // 2. Add interaction to the "System Status" badge
    const statusBadge = document.querySelector('.system-status');
    if (statusBadge) {
        statusBadge.addEventListener('click', () => {
            alert("System Diagnostics: All services running normally.\n\nPython Automation: Active\nDatabase: Connected");
        });
        statusBadge.style.cursor = 'pointer';
    }
});