
async function sendMessage() {
    const textInput = document.getElementById("textInput");
    const imageInput = document.getElementById("imageInput");
    const chatBox = document.getElementById("chatBox");

    const message = textInput.value.trim();
    const image = imageInput.files[0];

    if (!message && !image) {
        alert("Please type a question or upload a plant photo.");
        return;
    }

    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message || "Please examine this plant photo.";

    if (image) {
        const preview = document.createElement("img");
        preview.src = URL.createObjectURL(image);
        preview.alt = "Uploaded plant";
        preview.style.maxWidth = "180px";
        preview.style.display = "block";
        preview.style.marginTop = "8px";
        userMessage.appendChild(preview);
    }

    chatBox.appendChild(userMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    textInput.value = "";

    const formData = new FormData();
    formData.append("message", message);

    if (image) {
        formData.append("image", image);
    }

    imageInput.value = "";

    const typing = document.createElement("div");
    typing.className = "bot-message";
    typing.textContent = "🌱 Plant Bot is examining your question/photo...";
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        typing.textContent = data.reply || "Sorry, I couldn't generate a response.";

    } catch (error) {
        typing.textContent =
            "I couldn't connect to the AI. Please check that the Plant Bot server and Ollama are running.";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("textInput").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
