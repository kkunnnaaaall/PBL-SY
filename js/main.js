document.addEventListener("DOMContentLoaded", () => {

    const analyzeBtn = document.getElementById("analyze-btn");
    const txnHashInput = document.getElementById("txn-hash");
    const resultBox = document.getElementById("result-box");

    analyzeBtn.addEventListener("click", () => {
        const transactionHash = txnHashInput.value;

        if (!transactionHash) {
            alert("Please enter a transaction hash.");
            return;
        }

        resultBox.innerHTML = "Analyzing... Please wait.";
        fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "transaction_hash": transactionHash }),
        })
            .then(response => response.json())
            .then(data => {
                console.log("Got response from backend:", data);

                if (data.status === "PHISHING") {
                    resultBox.innerHTML = `<strong>Status: PHISHING</strong><br>Reason: ${data.reason}`;
                    resultBox.className = "phishing";
                } else if (data.status === "SAFE") {
                    resultBox.innerHTML = `<strong>Status: SAFE</strong><br>Reason: ${data.reason}`;
                    resultBox.className = "safe";
                } else {
                    const reason = data.reason || data.error || "Unknown error";
                    resultBox.innerHTML = `<strong>Status: ERROR</strong><br>Reason: ${reason}`;
                    resultBox.className = "error";
                }
            })
            .catch(error => {
                console.error("Error:", error);
                resultBox.innerHTML = "Error connecting to analysis engine. Is the backend running?";
                resultBox.className = "phishing";
            });

    });
});