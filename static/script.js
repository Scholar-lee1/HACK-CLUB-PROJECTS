document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const actionInput = document.getElementById('actionInput');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    const samples = [
        "Quitting my job to sell hand-made clay spoons on Etsy",
        "Moving to a remote island with no internet for a year",
        "Investing my entire life savings into a taco-themed cryptocurrency"
    ];

    const runSimulation = async (action) => {
        if (!action) return;

        loading.classList.remove('hidden');
        results.classList.add('hidden');
        submitBtn.disabled = true;

        try {
            const response = await fetch('/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action })
            });

            const data = await response.json();

            if (data.status === "success") {
                document.getElementById('bestText').innerText = data.outcomes.best_case;
                document.getElementById('worstText').innerText = data.outcomes.worst_case;
                document.getElementById('unexpectedText').innerText = data.outcomes.unexpected;
                results.classList.remove('hidden');
            }
        } catch (err) {
            console.error("Fetch Error:", err);
        } finally {
            loading.classList.add('hidden');
            submitBtn.disabled = false;
        }
    };

    submitBtn.addEventListener('click', () => runSimulation(actionInput.value));

    sampleBtn.addEventListener('click', () => {
        const randomAction = samples[Math.floor(Math.random() * samples.length)];
        actionInput.value = randomAction;
        runSimulation(randomAction);
    });
});