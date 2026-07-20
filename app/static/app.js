const I18N = {
  zh: {
    navTool: "工具",
    heroTitle: "网址 → b23.tv",
    heroTag: "简介",
    genTitle: "生成",
    genDesc: "包装网址，签发官方 b23 短链。",
    urlPh: "https://www.example.com",
    genBtn: "生成",
    lblShort: "短链",
    lblLong: "长链",
    copy: "复制",
    copyOk: "已复制",
    copyErr: "失败",
    appTitle: "在 App 内打开",
    appDesc: "仅在 B 站 App 内打开短链，才可能跳到目标站；浏览器一般不会跳转。",
    disTitle: "免责声明",
    disDesc: "非 B 站官方产品。详见 DISCLAIMER.md。许可证 GPL-3.0。",
    footer: "b23wrap · 本地 · 127.0.0.1:8765",
    needUrl: "请填写网址",
    working: "生成中…",
    failed: "生成失败",
    done: "完成 · 请在 B 站 App 内打开短链",
    langBtn: "EN",
  },
  en: {
    navTool: "Tool",
    heroTitle: "URL → b23.tv",
    heroTag: "ABOUT",
    genTitle: "Generate",
    genDesc: "Wrap a URL, mint official b23.",
    urlPh: "https://www.example.com",
    genBtn: "Generate",
    lblShort: "b23",
    lblLong: "long",
    copy: "Copy",
    copyOk: "OK",
    copyErr: "Err",
    appTitle: "Open in App",
    appDesc: "Target opens only inside Bilibili app. Browser stays on official pages.",
    disTitle: "Disclaimer",
    disDesc: "Not affiliated with Bilibili. See DISCLAIMER.md. GPL-3.0.",
    footer: "b23wrap · local · 127.0.0.1:8765",
    needUrl: "URL required",
    working: "Working…",
    failed: "Failed",
    done: "Done · open b23 in Bilibili app",
    langBtn: "中文",
  },
};

const $ = (id) => document.getElementById(id);
let lang = localStorage.getItem("b23wrap_lang") || "zh";

function t(key) {
  return (I18N[lang] && I18N[lang][key]) || I18N.zh[key] || key;
}

function applyI18n() {
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (key && t(key) != null) el.textContent = t(key);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key) el.setAttribute("placeholder", t(key));
  });
  // copy buttons may have been changed to OK — reset labels
  document.querySelectorAll(".copy").forEach((el) => {
    el.textContent = t("copy");
  });
  const langBtn = $("langBtn");
  if (langBtn) langBtn.textContent = t("langBtn");
  document.title = "b23wrap";
}

function setStatus(kind, text) {
  const statusEl = $("status");
  statusEl.hidden = false;
  statusEl.className = `status ${kind}`;
  statusEl.textContent = text;
}

async function generate() {
  const urlInput = $("url");
  const btn = $("btn");
  const resultEl = $("result");
  const url = urlInput.value.trim();
  if (!url) {
    setStatus("error", t("needUrl"));
    return;
  }
  btn.disabled = true;
  resultEl.hidden = true;
  setStatus("loading", t("working"));

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    if (!data.ok) {
      setStatus("error", data.error || t("failed"));
      return;
    }
    $("short").textContent = data.short_url;
    $("short").href = data.short_url;
    $("long").textContent = data.long_url;
    $("loc").textContent = data.location || "";
    resultEl.hidden = false;
    setStatus("ok", t("done"));
  } catch (e) {
    setStatus("error", String(e));
  } finally {
    btn.disabled = false;
  }
}

function toggleLang() {
  lang = lang === "zh" ? "en" : "zh";
  localStorage.setItem("b23wrap_lang", lang);
  applyI18n();
  // clear status when switching language
  const statusEl = $("status");
  if (statusEl && !statusEl.hidden && statusEl.classList.contains("ok")) {
    statusEl.textContent = t("done");
  }
}

$("btn").addEventListener("click", generate);
$("url").addEventListener("keydown", (e) => {
  if (e.key === "Enter") generate();
});
$("langBtn").addEventListener("click", toggleLang);

document.querySelectorAll("[data-copy]").forEach((el) => {
  el.addEventListener("click", async () => {
    const node = $(el.getAttribute("data-copy"));
    const text = node.href && node.tagName === "A" ? node.href : node.textContent;
    try {
      await navigator.clipboard.writeText(text);
      el.textContent = t("copyOk");
      setTimeout(() => (el.textContent = t("copy")), 900);
    } catch {
      el.textContent = t("copyErr");
      setTimeout(() => (el.textContent = t("copy")), 900);
    }
  });
});

applyI18n();
