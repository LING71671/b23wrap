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
    setStatus("error", "请先填写目标网址");
    return;
  }
  btn.disabled = true;
  resultEl.hidden = true;
  setStatus("loading", "正在包装长链并请求 B 站签发 b23…");

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    if (!data.ok) {
      setStatus("error", data.error || "生成失败");
      return;
    }

    $("short").textContent = data.short_url;
    $("short").href = data.short_url;
    $("long").textContent = data.long_url;
    $("loc").textContent = data.location || "(未取到 Location)";
    $("note").textContent = data.note || "";
    resultEl.hidden = false;
    setStatus("ok", "生成成功：已拿到官方 b23 短链");
  } catch (e) {
    setStatus("error", "请求失败：" + e);
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
    const id = el.getAttribute("data-copy");
    const node = $(id);
    const text = node.href && node.tagName === "A" ? node.href : node.textContent;
    try {
      await navigator.clipboard.writeText(text);
      el.textContent = "已复制";
      setTimeout(() => (el.textContent = "复制"), 1200);
    } catch {
      el.textContent = "失败";
      setTimeout(() => (el.textContent = "复制"), 1200);
    }
  });
});
