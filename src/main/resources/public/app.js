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

const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const reviewText = document.getElementById("review-text");
const sentimentJson = document.getElementById("sentiment-json");
const sentimentCard = document.getElementById("sentiment-card");

function resetResults() {
  reviewText.textContent = "Upload a file to see its decoded review text here.";
  sentimentJson.textContent = "The VADER output will appear here.";
  sentimentCard.className = "sentiment-card neutral";
  sentimentCard.innerHTML = `
    <span class="label">Waiting</span>
    <strong>No analysis yet.</strong>
  `;
}

function renderSentiment(result) {
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

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

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

document.getElementById("clear-button").addEventListener("click", () => {
  uploadForm.reset();
  resetResults();
});
