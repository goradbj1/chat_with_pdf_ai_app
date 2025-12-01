document.getElementById("sendBtn").addEventListener("click", askQuestion);
document.getElementById("userQuery").addEventListener("keypress", function (e) {
    if (e.key === "Enter") askQuestion();
});

async function askQuestion() {
    const input = document.getElementById("userQuery");
    const query = input.value.trim();
    if (!query) return;

    addMessage(query, "user");
    input.value = "";

    // temporary loading bubble
    const loadingId = addMessage("Typing...", "bot", true);

    const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    const data = await response.json();

    // remove loading bubble and add final response
    removeMessage(loadingId);
    addMessage(data.response, "bot");
}

function addMessage(text, sender, isLoading = false) {
    const chatBox = document.getElementById("chatBox");
    const msg = document.createElement("div");

    msg.classList.add("message", sender);

    if (isLoading) {
        msg.innerHTML = `<span class="dots">Typing...</span>`;
    } else {
        msg.innerText = text;
    }

    const id = "msg-" + Math.random().toString(36).substring(2, 9);
    msg.id = id;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;

    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
