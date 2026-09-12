const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const greetingBubble = document.getElementById("greetingBubble");
const pincodeInput = document.getElementById("pincodeInput");

let sessionId = localStorage.getItem("aarogya_session");
if (!sessionId) {
  sessionId = "s-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 10);
  localStorage.setItem("aarogya_session", sessionId);
}

function scrollBottom() {
  chatArea.scrollTop = chatArea.scrollHeight;
}

function addMessage(text, who, extra) {
  const wrap = document.createElement("div");
  wrap.className = "msg " + who;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  if (extra && extra.verdict) {
    const badge = document.createElement("span");
    badge.className = "verdict-badge verdict-" + extra.verdict;
    badge.textContent = extra.verdict + (extra.fearMongering ? " (context)" : "");
    bubble.appendChild(badge);
    bubble.appendChild(document.createElement("br"));
  }
  bubble.appendChild(document.createTextNode(text));
  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = who === "user" ? "You" : (extra && extra.generator === "llm" ? "AarogyaSathi (AI answer)" : "AarogyaSathi");
  wrap.appendChild(bubble);
  wrap.appendChild(meta);
  chatArea.appendChild(wrap);
  scrollBottom();
}

function addTyping() {
  const wrap = document.createElement("div");
  wrap.className = "msg bot typing";
  wrap.id = "typingIndicator";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = " ";
  wrap.appendChild(bubble);
  chatArea.appendChild(wrap);
  scrollBottom();
  return wrap;
}

async function sendMessage(text) {
  if (!text.trim()) return;
  const msg = text.trim();
  addMessage(msg, "user");
  userInput.value = "";
  sendBtn.disabled = true;
  const typing = addTyping();
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, session_id: sessionId, pincode: pincodeInput.value.trim() || null }),
    });
    const data = await res.json();
    typing.remove();
    addMessage(data.reply || "Sorry, something went wrong.", "bot", {
      verdict: data.factcheck ? data.factcheck.verdict : null,
      fearMongering: data.factcheck ? data.factcheck.fear_mongering : false,
      generator: data.generator,
    });
  } catch (err) {
    typing.remove();
    addMessage("Network error. Please try again.", "bot");
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

document.getElementById("quickChips").addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (chip) sendMessage(chip.dataset.msg);
});

sendBtn.addEventListener("click", () => sendMessage(userInput.value));
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage(userInput.value);
});

(async function boot() {
  try {
    const res = await fetch("/api/health");
    if (res.ok) {
      greetingBubble.textContent = "";
    }
  } catch (e) {}
  sendMessage("hi");
})();
