const REPO_URL = "https://github.com/LING71671/b23wrap";
const SHARE_API = "https://api.bilibili.com/x/share/click";
const SHARE_API_BILIAPI = "https://api.biliapi.net/x/share/click";

const I18N = {
  zh: {
    navTool: "工具",
    heroTitle: "网址 → b23.tv",
    genTitle: "生成",
    genDesc: "包装网址，签发官方 b23 短链。可选已验证链路 C1–C5。",
    urlPh: "https://www.example.com",
    chainLabel: "链路（App 已验证）",
    chainHint: "C1 默认；C2 换签发接口；C4/C5 多层包装。Pages 上可能仅能出长链（跨域）。",
    chainC1s: "标准三层",
    chainC2s: "备用域名",
    chainC4s: "双层嵌套",
    chainC5s: "jump 套 jump",
    genBtn: "生成",
    lblChain: "链路",
    lblShort: "短链",
    lblLong: "长链",
    copy: "复制",
    copyOk: "已复制",
    copyErr: "失败",
    appTitle: "在 App 内打开",
    appDesc: "仅在 B 站 App 内打开短链，才可能跳到目标站；浏览器一般不会跳转。",
    disTitle: "免责声明",
    disDesc: "非 B 站官方产品。详见 DISCLAIMER.md。许可证 GPL-3.0。",
    footer: "b23wrap · 本地 / Pages",
    needUrl: "请填写网址",
    working: "生成中…",
    failed: "生成失败",
    done: "完成 · 请在 B 站 App 内打开短链",
    doneLongOnly: "已生成长链（浏览器跨域，未能签发 b23；请本地运行完整服务）",
    langBtn: "EN",
  },
  en: {
    navTool: "Tool",
    heroTitle: "URL → b23.tv",
    genTitle: "Generate",
    genDesc: "Wrap a URL, mint official b23. Pick verified chain C1–C5.",
    urlPh: "https://www.example.com",
    chainLabel: "Chain (App-verified)",
    chainHint: "C1 default; C2 alt mint host; C4/C5 nested wrap. Pages may only get long URL (CORS).",
    chainC1s: "Standard",
    chainC2s: "Alt host",
    chainC4s: "Double nest",
    chainC5s: "jump-of-jump",
    genBtn: "Generate",
    lblChain: "chain",
    lblShort: "b23",
    lblLong: "long",
    copy: "Copy",
    copyOk: "OK",
    copyErr: "Err",
    appTitle: "Open in App",
    appDesc: "Target opens only inside Bilibili app. Browser stays on official pages.",
    disTitle: "Disclaimer",
    disDesc: "Not affiliated with Bilibili. See DISCLAIMER.md. GPL-3.0.",
    footer: "b23wrap · local / Pages",
    needUrl: "URL required",
    working: "Working…",
    failed: "Failed",
    done: "Done · open b23 in Bilibili app",
    doneLongOnly: "Long URL ready (CORS blocked short mint; run local server for full b23)",
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

function uuid() {
  if (crypto.randomUUID) return crypto.randomUUID();
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function normalizeTarget(url) {
  url = (url || "").trim();
  if (!url) throw new Error(t("needUrl"));
  if (!/^https?:\/\//i.test(url)) url = "https://" + url;
  let u;
  try {
    u = new URL(url);
  } catch {
    throw new Error(t("needUrl"));
  }
  if (!u.hostname || !u.hostname.includes(".")) throw new Error(t("needUrl"));
  if (u.protocol !== "http:" && u.protocol !== "https:") throw new Error(t("needUrl"));
  return u.toString();
}

/** C1 standard: mall/web → d. → jump */
function buildJumpLongUrl(target) {
  target = normalizeTarget(target);
  const schema = "bilibili://mall/web?url=" + encodeURIComponent(target);
  const dUrl = "https://d.bilibili.com/?" + new URLSearchParams({ schema }).toString();
  return "https://mall.bilibili.com/jump.html?" + new URLSearchParams({ Url: dUrl }).toString();
}

/**
 * Match app/core.py build_long_url
 * c1/c3 standard, c4 nest2, c5 nest-jump
 */
function buildLongUrl(target, chain) {
  const c = (chain || "c1").toLowerCase();
  if (c === "c4" || c === "nest2" || c === "double") {
    return buildJumpLongUrl(buildJumpLongUrl(target));
  }
  if (c === "c5" || c === "nest-jump" || c === "jump-jump") {
    const inner = buildJumpLongUrl(target);
    return "https://mall.bilibili.com/jump.html?" + new URLSearchParams({ Url: inner }).toString();
  }
  // c1, c2 (wrap same), c3
  return buildJumpLongUrl(target);
}

function selectedChain() {
  const el = $("chain");
  return (el && el.value) || "c1";
}

function resolveMintApi(chain) {
  return chain === "c2" ? SHARE_API_BILIAPI : SHARE_API;
}

function chainLabel(chain) {
  const map = { c1: "C1", c2: "C2", c3: "C3", c4: "C4", c5: "C5" };
  return map[chain] || chain;
}

async function mintB23Browser(longUrl, shareApi) {
  const buvid = "XY" + uuid().replace(/-/g, "").slice(0, 30).toUpperCase();
  const body = new URLSearchParams({
    platform: "android",
    share_channel: "COPY",
    share_id: "public.webview.0.0.pv",
    share_mode: "4",
    oid: longUrl,
    buvid,
    build: "7710300",
    share_session_id: uuid(),
    ts: String(Math.floor(Date.now() / 1000)),
  });
  const res = await fetch(shareApi || SHARE_API, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  const payload = await res.json();
  if (payload.code !== 0 && payload.code !== "0") {
    throw new Error(`API ${payload.code}: ${payload.message || ""}`);
  }
  const content = (((payload.data || {}).content) || "").trim();
  const m = content.match(/https?:\/\/b23\.tv\/[A-Za-z0-9]+/);
  if (!m) throw new Error(t("failed"));
  return { short_url: m[0], location: null, share_api: shareApi || SHARE_API };
}

async function generateViaLocalApi(url, chain) {
  const body = { url, chain };
  if (chain === "c2") body.api_host = "biliapi";
  const res = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!data.ok) throw new Error(data.error || t("failed"));
  return data;
}

async function generate() {
  const urlInput = $("url");
  const btn = $("btn");
  const resultEl = $("result");
  const url = urlInput.value.trim();
  const chain = selectedChain();
  if (!url) {
    setStatus("error", t("needUrl"));
    return;
  }
  btn.disabled = true;
  resultEl.hidden = true;
  setStatus("loading", t("working"));

  try {
    let data;
    let longOnly = false;
    try {
      data = await generateViaLocalApi(url, chain);
    } catch {
      const long_url = buildLongUrl(url, chain);
      const shareApi = resolveMintApi(chain);
      try {
        const minted = await mintB23Browser(long_url, shareApi);
        data = {
          ok: true,
          target: normalizeTarget(url),
          chain: chain === "c2" ? "c2" : chain,
          long_url,
          short_url: minted.short_url,
          location: minted.location || "",
          share_api: minted.share_api,
        };
      } catch {
        longOnly = true;
        data = {
          ok: true,
          target: normalizeTarget(url),
          chain,
          long_url,
          short_url: "",
          location: "",
        };
      }
    }

    const outChain = data.chain || chain;
    $("chainOut").textContent = chainLabel(outChain) + (data.share_api ? ` · ${data.share_api.replace(/^https:\/\//, "")}` : "");
    $("short").textContent = data.short_url || "—";
    $("short").href = data.short_url || "#";
    if (!data.short_url) $("short").removeAttribute("href");
    else $("short").setAttribute("href", data.short_url);
    $("long").textContent = data.long_url;
    $("loc").textContent = data.location || "";
    resultEl.hidden = false;
    setStatus("ok", longOnly || !data.short_url ? t("doneLongOnly") : t("done"));
  } catch (e) {
    setStatus("error", String(e.message || e));
  } finally {
    btn.disabled = false;
  }
}

function toggleLang() {
  lang = lang === "zh" ? "en" : "zh";
  localStorage.setItem("b23wrap_lang", lang);
  applyI18n();
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

// chain pills
function setChain(value) {
  const v = value || "c1";
  const hidden = $("chain");
  if (hidden) hidden.value = v;
  localStorage.setItem("b23wrap_chain", v);
  document.querySelectorAll(".chain-pill").forEach((btn) => {
    const on = btn.getAttribute("data-chain") === v;
    btn.classList.toggle("is-active", on);
    btn.setAttribute("aria-checked", on ? "true" : "false");
  });
}

const savedChain = localStorage.getItem("b23wrap_chain") || "c1";
setChain(savedChain);
document.querySelectorAll(".chain-pill").forEach((btn) => {
  btn.addEventListener("click", () => setChain(btn.getAttribute("data-chain")));
});

document.querySelectorAll("[data-copy]").forEach((el) => {
  el.addEventListener("click", async () => {
    const node = $(el.getAttribute("data-copy"));
    const text = node.href && node.tagName === "A" && node.getAttribute("href") !== "#"
      ? node.href
      : node.textContent;
    if (!text || text === "—") return;
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

document.querySelectorAll('a[href*="github.com/LING71671/b23wrap"]').forEach((a) => {
  a.href = REPO_URL;
});

applyI18n();
