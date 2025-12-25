// ===============================
// ELEMENTS
// ===============================
const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const voiceBtn = document.getElementById("voiceBtn");
const cameraBtn = document.getElementById("cameraBtn");
const cameraOverlay = document.getElementById("cameraOverlay");
const videoPreview = document.getElementById("videoPreview");
const captureBtn = document.getElementById("captureBtn");
const recordBtn = document.getElementById("recordBtn");
const closeCameraBtn = document.getElementById("closeCameraBtn");
const switchCameraBtn = document.getElementById("switchCameraBtn");
const recordingStatus = document.getElementById("recordingStatus");

// ===============================
// BACKEND URL
// ===============================
const API_URL = "https://chatbot-ai-agent-production-8ade.up.railway.app/chat";

// ===============================
// USER ID
// ===============================
let userId = localStorage.getItem("matrix_user_id");
if (!userId) {
  userId = "user_" + Math.random().toString(36).substr(2, 9);
  localStorage.setItem("matrix_user_id", userId);
}

// ===============================
// TEXTAREA AUTO EXPAND
// ===============================
userInput.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
});

// ===============================
// VOICE RECOGNITION
// ===============================
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition;
if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = "id-ID";
  recognition.interimResults = false;

  recognition.onstart = () => {
    voiceBtn.classList.add("active");
    userInput.placeholder = "Mendengarkan...";
  };

  recognition.onresult = (event) => {
    userInput.value = event.results[0][0].transcript;
    sendMessage();
  };

  recognition.onend = () => {
    voiceBtn.classList.remove("active");
    userInput.placeholder = "Ketik pesan...";
  };

  voiceBtn.addEventListener("click", () => {
    try {
      recognition.start();
    } catch {
      recognition.stop();
    }
  });
}

// ===============================
// CAMERA & VIDEO
// ===============================
let stream;
let currentFacingMode = "user";
let mediaRecorder;
let recordedChunks = [];

async function startCamera(facingMode) {
  if (stream) stream.getTracks().forEach((t) => t.stop());

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode },
      audio: true,
    });
    videoPreview.srcObject = stream;
    currentFacingMode = facingMode;
  } catch {
    alert("Akses kamera ditolak");
  }
}

cameraBtn.addEventListener("click", async () => {
  await startCamera("user");
  cameraOverlay.style.display = "flex";
});

switchCameraBtn.addEventListener("click", async () => {
  await startCamera(currentFacingMode === "user" ? "environment" : "user");
});

closeCameraBtn.addEventListener("click", () => {
  if (stream) stream.getTracks().forEach((t) => t.stop());
  cameraOverlay.style.display = "none";
});

captureBtn.addEventListener("click", () => {
  addMessage("📸 [Foto terkirim]", "user");
  setTimeout(() => {
    addMessage("😏 Foto diterima. Matrix nyimpen di memori.", "bot");
  }, 800);
  closeCameraBtn.click();
});

// ===============================
// VIDEO RECORD
// ===============================
recordBtn.addEventListener("click", () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordingStatus.classList.add("hidden");
  } else {
    recordedChunks = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      addMessage("🎥 [Video terkirim]", "user");
      setTimeout(() => {
        addMessage("😎 Video diterima. Matrix lagi analisis.", "bot");
      }, 1000);
      closeCameraBtn.click();
    };

    mediaRecorder.start();
    recordingStatus.classList.remove("hidden");
  }
});

// ===============================
// CHAT HELPERS
// ===============================
function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  chatContainer.appendChild(div);
  scrollToBottom();
}

// ===============================
// EMOTION FORMATTER
// ===============================
function formatEmotions(emotions) {
  if (!emotions || emotions.length === 0) return "";
  return emotions.join(", ");
}

// ===============================
// SEND MESSAGE
// ===============================
sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";
  userInput.style.height = "auto";

  const typing = document.createElement("div");
  typing.className = "message bot";
  typing.textContent = "Matrix lagi mikir...";
  chatContainer.appendChild(typing);
  scrollToBottom();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, userId }),
    });

    const data = await res.json();
    typing.remove();

    let reply = data.reply || "⚠️ Matrix lagi males jawab.";
    const emo = formatEmotions(data.emotions);
    if (emo) reply += `\n\n🧠 Emosi terdeteksi: ${emo}`;

    addMessage(reply, "bot");
  } catch (e) {
    typing.remove();
    addMessage("❌ Koneksi ke server gagal.", "bot");
  }
}

window.onload = () => userInput.focus();
