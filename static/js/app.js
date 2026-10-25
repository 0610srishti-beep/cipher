const $ = (id) => document.getElementById(id);
let latestHash = "";

function notice(id, message, type = "") {
  const el = $(id);
  el.textContent = message;
  el.className = `notice ${type}`;
}
async function jsonRequest(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}
async function fileRequest(url, file) {
  const form = new FormData();
  form.append("file", file);
  const response = await fetch(url, { method: "POST", body: form });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || "File processing failed.");
  }
  return response;
}
function updateHash(hash) {
  latestHash = hash || "";
  $("hashOutput").textContent = latestHash || "—";
  $("anchorBtn").disabled = !latestHash;
}
function downloadBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = name; a.click();
  URL.revokeObjectURL(url);
}
$("encryptBtn").addEventListener("click", async () => {
  try {
    const data = await jsonRequest("/api/encrypt-text", { text: $("plainText").value });
    $("encryptedText").value = data.encrypted;
    updateHash(data.sha256);
    notice("textNotice", "Encrypted successfully. The fingerprint is ready below.", "success");
    notice("decryptNotice", "");
  } catch (e) { notice("textNotice", e.message, "error"); }
});
$("decryptBtn").addEventListener("click", async () => {
  try {
    const data = await jsonRequest("/api/decrypt-text", { encrypted: $("encryptedText").value });
    $("decryptedText").textContent = data.decrypted;
    notice("decryptNotice", "Decryption complete.", "success");
  } catch (e) { notice("decryptNotice", e.message, "error"); }
});
$("clearBtn").addEventListener("click", () => {
  $("plainText").value = ""; $("encryptedText").value = "";
  $("decryptedText").textContent = "Nothing decrypted yet.";
  notice("textNotice", ""); notice("decryptNotice", ""); updateHash("");
});
$("copyEncrypted").addEventListener("click", async () => {
  if (!$("encryptedText").value) return notice("textNotice", "Nothing to copy yet.", "error");
  await navigator.clipboard.writeText($("encryptedText").value);
  notice("textNotice", "Encrypted output copied.", "success");
});
$("fileInput").addEventListener("change", () => {
  const file = $("fileInput").files[0];
  $("fileName").textContent = file ? `${file.name} · ${(file.size / 1024).toFixed(1)} KB` : "No file selected";
  notice("hashNotice", "");
});
$("hashBtn").addEventListener("click", async () => {
  const file = $("fileInput").files[0];
  if (!file) return notice("hashNotice", "Choose a file first.", "error");
  try {
    const response = await fileRequest("/api/hash-file", file);
    const data = await response.json();
    updateHash(data.sha256);
    notice("hashNotice", `Fingerprint calculated for ${data.filename}.`, "success");
  } catch (e) { notice("hashNotice", e.message, "error"); }
});
$("fileEncryptBtn").addEventListener("click", async () => {
  const file = $("fileInput").files[0];
  if (!file) return notice("hashNotice", "Choose a file first.", "error");
  try {
    const response = await fileRequest("/api/encrypt-file", file);
    const blob = await response.blob();
    const digest = response.headers.get("X-Content-SHA256");
    downloadBlob(blob, `${file.name}.enc`);
    if (digest) updateHash(digest);
    notice("hashNotice", "Encrypted file downloaded. Keep your local key safe to decrypt it later.", "success");
  } catch (e) { notice("hashNotice", e.message, "error"); }
});
$("copyHash").addEventListener("click", async () => {
  if (!latestHash) return;
  await navigator.clipboard.writeText(latestHash);
  notice("hashNotice", "Fingerprint copied.", "success");
});
$("anchorBtn").addEventListener("click", async () => {
  if (!latestHash) return;
  $("anchorBtn").disabled = true;
  notice("chainNotice", "Submitting digest to configured development chain…");
  try {
    const data = await jsonRequest("/api/anchor-hash", { sha256: latestHash });
    notice("chainNotice", `Transaction confirmed: ${data.transaction}`, "success");
  } catch (e) { notice("chainNotice", e.message, "error"); }
  finally { $("anchorBtn").disabled = !latestHash; }
});
fetch("/api/status").then(r => r.json()).then(data => {
  if (data.blockchain_configured) {
    $("chainStatus").innerHTML = '<i class="dot green"></i> Configured';
    notice("chainNotice", "Local blockchain settings detected. Calculate a hash to continue.");
  } else {
    $("chainStatus").innerHTML = '<i class="dot amber"></i> Optional';
  }
}).catch(() => {});
