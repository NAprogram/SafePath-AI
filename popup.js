document.getElementById('scanBtn').addEventListener('click', async () => {
    const text = document.getElementById('emailText').value;
    const btn = document.getElementById('scanBtn');
    const label = document.getElementById('btnLabel');
    const loader = document.getElementById('loading');
    const resultArea = document.getElementById('result-area');

    if (!text.trim()) return;

    // UI state: Scanning
    btn.disabled = true;
    label.style.display = 'none';
    loader.style.display = 'block';
    resultArea.style.display = 'none';

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        resultArea.style.display = 'block';

        if (data.is_phishing) {
            resultArea.style.background = 'rgba(255, 255, 255, 1)';
            resultArea.style.border = '1px solid var(--danger)';
            resultArea.style.color = '#eb1111ff';
            resultArea.innerHTML = `<b>THREAT DETECTED</b><br>Phishing Probability: ${data.confidence}%`;
        } else {
            resultArea.style.background = 'rgba(255, 255, 255, 1)';
            resultArea.style.border = '1px solid var(--success)';
            resultArea.style.color = '#255c3cff';
            resultArea.innerHTML = `<b>SCAN CLEAN</b><br>This path appears safe.`;
        }
    } catch (err) {
        resultArea.style.display = 'block';
        resultArea.style.border = '1px solid #fab005';
        resultArea.innerText = "Error: Python Server Offline.";
    } finally {
        btn.disabled = false;
        label.style.display = 'inline';
        loader.style.display = 'none';
    }
});