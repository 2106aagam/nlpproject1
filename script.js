const input = document.getElementById("textInput");
const counter = document.getElementById("counter");

if (input) {
    input.addEventListener("input", () => {
        counter.textContent = `${input.value.length} / 2000`;
    });
}

function useSample() {
    input.value = "I really enjoyed this project. The website looks amazing and the experience was excellent!";
    input.dispatchEvent(new Event("input"));
}

async function analyzeText() {
    const text = input.value.trim();
    const error = document.getElementById("error");
    const result = document.getElementById("result");
    const btn = document.getElementById("analyzeBtn");

    error.classList.add("hidden");
    result.classList.add("hidden");

    if (!text) {
        error.textContent = "Please enter some text first.";
        error.classList.remove("hidden");
        return;
    }

    btn.disabled = true;
    btn.textContent = "Analyzing...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text})
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Something went wrong.");

        document.getElementById("sentiment").textContent = data.sentiment;
        document.getElementById("confidence").textContent = data.confidence + "%";
        document.getElementById("wordCount").textContent = data.word_count;

        const emoji = document.getElementById("emoji");
        if (data.sentiment === "Positive") emoji.textContent = "😊";
        else if (data.sentiment === "Negative") emoji.textContent = "😞";
        else emoji.textContent = "😐";

        document.getElementById("meterFill").style.width = data.confidence + "%";
        result.classList.remove("hidden");
    } catch (e) {
        error.textContent = e.message;
        error.classList.remove("hidden");
    } finally {
        btn.disabled = false;
        btn.textContent = "Analyze Sentiment";
    }
}
