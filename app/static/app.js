const $ = (id) => document.getElementById(id);
const urlInput = $("url");
const btn = $("btn");
const statusEl = $("status");
const resultEl = $("result");

function setStatus(kind, text) {
  statusEl.hidden = false;
  statusEl.className = `status ${kind}`;
  statusEl.textContent = text;
}

async function generate() {
  const url = urlInput.value.trim();
  if (!url) {
    setStatus("error", "URL required");
    return;
  }
  btn.disabled = true;
  resultEl.hidden = true;
  setStatus("loading", "Working…");

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    if (!data.ok) {
      setStatus("error", data.error || "Failed");
      return;
    }
    $("short").textContent = data.short_url;
    $("short").href = data.short_url;
    $("long").textContent = data.long_url;
    $("loc").textContent = data.location || "";
    resultEl.hidden = false;
    setStatus("ok", "Done · open b23 in Bilibili app");
  } catch (e) {
    setStatus("error", String(e));
  } finally {
    btn.disabled = false;
  }
}

btn.addEventListener("click", generate);
urlInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") generate();
});

document.querySelectorAll("[data-copy]").forEach((el) => {
  el.addEventListener("click", async () => {
    const node = $(el.getAttribute("data-copy"));
    const text = node.href && node.tagName === "A" ? node.href : node.textContent;
    try {
      await navigator.clipboard.writeText(text);
      el.textContent = "OK";
      setTimeout(() => (el.textContent = "Copy"), 900);
    } catch {
      el.textContent = "Err";
      setTimeout(() => (el.textContent = "Copy"), 900);
    }
  });
});
