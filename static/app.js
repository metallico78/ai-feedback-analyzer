document.getElementById("feedbackForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = e.target.text.value.trim();

    if (!text) {
        document.getElementById("result").innerHTML = "<p style='color:red'>Por favor escribe un feedback válido.</p>";
        return;
    }

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": "TU_API_KEY_AQUI" // reemplaza con tu API Key real
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            const error = await response.json();
            document.getElementById("result").innerHTML = `<p style='color:red'>Error: ${error.detail}</p>`;
            return;
        }

        const data = await response.json();
        let suggestions = Array.isArray(data.suggestions) ? data.suggestions.join(", ") : data.suggestions;

        document.getElementById("result").innerHTML = `
            <h3>Resultado:</h3>
            <p><strong>Sentimiento:</strong> ${data.sentiment}</p>
            <p><strong>Puntuación:</strong> ${data.score}</p>
            <p><strong>Sugerencias:</strong> ${suggestions}</p>
            <p><strong>Resumen:</strong> ${data.summary}</p>
        `;
    } catch (err) {
        document.getElementById("result").innerHTML = `<p style='color:red'>Error de conexión con el servidor.</p>`;
    }
});

async function startPayment(amount) {
    try {
        const response = await fetch("/api/payment/create-intent", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ amount: amount, email: "cliente@ejemplo.com" })
        });

        if (!response.ok) {
            const error = await response.json();
            alert("Error en el pago: " + error.detail);
            return;
        }

        const data = await response.json();
        alert("Inicia tu pago con Stripe, clientSecret: " + data.clientSecret);
    } catch (err) {
        alert("Error de conexión con el servidor de pagos.");
    }
}
