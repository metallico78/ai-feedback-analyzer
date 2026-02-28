document.getElementById("feedbackForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = e.target.text.value;
    const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "x-api-key": "TU_API_KEY_AQUI"
        },
        body: JSON.stringify({ text })
    });
    const data = await response.json();
    document.getElementById("result").innerHTML = `
        <h3>Resultado:</h3>
        <p>Sentimiento: ${data.sentiment}</p>
        <p>Puntuación: ${data.score}</p>
        <p>Sugerencias: ${data.suggestions}</p>
        <p>Resumen: ${data.summary}</p>
    `;
});

async function startPayment(amount) {
    const response = await fetch("/api/payment/create-intent", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({amount: amount, email: "cliente@ejemplo.com"})
    });
    const data = await response.json();
    alert("Inicia tu pago con Stripe, clientSecret: " + data.clientSecret);
}
