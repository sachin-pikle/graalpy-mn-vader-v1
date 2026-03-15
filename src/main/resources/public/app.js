async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.message || "The request failed.");
  }
  return body;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderSentiment(result) {
  const reviewText = document.getElementById("review-text");
  const sentimentJson = document.getElementById("sentiment-json");
  const sentimentCard = document.getElementById("sentiment-card");

  reviewText.textContent = result.reviewText || "";
  sentimentJson.textContent = JSON.stringify(result, null, 2);

  const label = result.sentiment.label.toLowerCase();
  sentimentCard.className = `sentiment-card ${label}`;
  sentimentCard.innerHTML = `
    <span class="label">${escapeHtml(result.sentiment.label)}</span>
    <strong>Compound score: ${result.sentiment.compound}</strong>
    <span>${escapeHtml(result.pythonMessage)}</span>
  `;
}

async function loadHello() {
  const data = await fetchJson("/api/hello");
  document.getElementById("hello-message").textContent = data.message;
}

document.getElementById("upload-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const fileInput = document.getElementById("file-input");
  if (!fileInput.files || fileInput.files.length === 0) {
    alert("Choose a review file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const result = await fetchJson("/api/reviews/analyze", {
      method: "POST",
      body: formData,
    });
    renderSentiment(result);
  } catch (error) {
    alert(error.message);
  }
});

loadHello().catch((error) => {
  document.getElementById("hello-message").textContent = error.message;
});
