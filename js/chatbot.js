const chatBox = document.createElement("div");
chatBox.id = "chatbot";
document.body.appendChild(chatBox);

chatBox.innerHTML = `
  <div id="chatbot-header">TOBI • AI Real Estate Assistant</div>
  <div id="chatbot-messages"></div>
  <div id="chatbot-input">
    <input type="text" id="chatInput" placeholder="Ask about real estate..." />
    <button id="chatSend">Send</button>
  </div>
`;

const messagesDiv = document.getElementById("chatbot-messages");
const input = document.getElementById("chatInput");
const button = document.getElementById("chatSend");

button.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

function addMessage(text, type) {
  const msg = document.createElement("div");
  msg.textContent = text;
  msg.style.margin = "5px 0";
  msg.style.textAlign = type === "user" ? "right" : "left";
  messagesDiv.appendChild(msg);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  addMessage("Typing...", "bot");

  try {
    const res = await fetch("http://localhost:3000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();

    messagesDiv.lastChild.remove();
    addMessage(data.reply, "bot");

  } catch (err) {
    messagesDiv.lastChild.remove();
    addMessage("Server error", "bot");
  }
}
