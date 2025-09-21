const chatBox = document.getElementById("chat-box");

function addMessage(text, sender = "bot") {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerHTML = text.replace(/\*/g, "•");
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}


async function uploadFile() {
  const fileInput = document.getElementById("pdfFile");
  if (!fileInput.files.length) {
    addMessage("⚠️ Please select a PDF first.", "bot");
    return;
  }
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  addMessage("📂 File uploaded: " + fileInput.files[0].name, "user");

  const res = await fetch("/upload", { method: "POST", body: formData });
  const data = await res.json();
  addMessage("✅ " + data.message, "bot");
}


async function simplifyDoc() {
  await handleFileAction("/simplify", "✨ Simplifying document...", "Simplified Document:");
}


async function analyzeRisk() {
  await handleFileAction("/risk", "⚖️ Analyzing risks...", "Risk Analysis:");
}


async function complianceCheck() {
  await handleFileAction("/compliance", "📑 Checking compliance...", "Compliance Check:");
}


async function handleFileAction(endpoint, actionMsg, resultTitle) {
  const fileInput = document.getElementById("pdfFile");
  if (!fileInput.files.length) {
    addMessage("⚠️ Upload a file first.", "bot");
    return;
  }
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  addMessage(actionMsg, "user");

  const res = await fetch(endpoint, { method: "POST", body: formData });
  const data = await res.json();

  if (data.error) {
    addMessage("❌ Error: " + data.error, "bot");
  } else {
    const key = Object.keys(data)[0];
    addMessage("<b>" + resultTitle + "</b><br>" + data[key], "bot");
  }
}

// Ask
async function askQuestion() {
  const questionInput = document.getElementById("question");
  const question = questionInput.value.trim();
  if (!question) {
    addMessage("⚠️ Enter a question.", "bot");
    return;
  }

  addMessage("🧑 You: " + question, "user");

  const formData = new FormData();
  formData.append("question", question);

  const res = await fetch("/ask", { method: "POST", body: formData });
  const data = await res.json();

  if (data.answer) {
    addMessage("<b>Answer:</b><br>" + data.answer, "bot");
  } else {
    addMessage("❌ Error: " + data.error, "bot");
  }

  questionInput.value = "";
}


function clearChat() {
  chatBox.innerHTML = "";
  addMessage("🧹 Chat cleared.", "bot");
}

