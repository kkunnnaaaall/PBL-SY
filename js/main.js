// Wait for the page to load before running script
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

        // --- FAKE DEMO (Start Here) ---
        // This is a placeholder. It just pretends to work.
        console.log("Analyzing:", transactionHash);
        // showFakeResult(transactionHash);
        // --- END FAKE DEMO ---


        // --- REAL CODE (Uncomment later) ---
        // When your Python backend is running, delete the "FAKE DEMO" 
        // block above and uncomment this block.

        resultBox.innerHTML = "Analyzing... Please wait.";
        resultBox.className = ""; // Clear old styles
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

                // --- THIS IS THE FINAL, MOST ROBUST LOGIC ---
                if (data.status === "PHISHING") {
                    resultBox.innerHTML = `<strong>Status: PHISHING</strong><br>Reason: ${data.reason}`;
                    resultBox.className = "phishing";
                } else if (data.status === "SAFE") {
                    resultBox.innerHTML = `<strong>Status: SAFE</strong><br>Reason: ${data.reason}`;
                    resultBox.className = "safe";
                } else {
                    // This block now catches all other errors
                    // It checks for a 'reason' key OR an 'error' key
                    const reason = data.reason || data.error || "Unknown error";
                    resultBox.innerHTML = `<strong>Status: ERROR</strong><br>Reason: ${reason}`;
                    resultBox.className = "error";
                }
                // --- END OF FINAL LOGIC ---
            })
            .catch(error => {
                console.error("Error:", error);
                resultBox.innerHTML = "Error connecting to analysis engine. Is the backend running?";
                resultBox.className = "phishing";
            });

        // --- END REAL CODE ---
    });
});