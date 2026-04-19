
const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

const OPENAI_API_KEY = "PUT_YOUR_API_KEY_HERE";

app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${OPENAI_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content: "You are TOBI, a real estate AI assistant. You help users with buying, selling, renting, pricing, and property advice in a simple and friendly way."
          },
          {
            role: "user",
            content: userMessage
          }
        ]
      })
    });

    const data = await response.json();

    const reply = data.choices?.[0]?.message?.content || "No response from AI.";

    res.json({ reply });

  } catch (error) {
    res.json({ reply: "Server error. Try again later." });
  }
});

app.listen(3000, () => {
  console.log("TOBI server running on http://localhost:3000");
});
