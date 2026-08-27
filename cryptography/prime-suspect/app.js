const EXPECTED_FLAG_HASH = "f19aca3d3fd58ac4ce4bb2a0ba755283dcfcb542b9b7a32c974e63baecef4b5d";

async function sha256(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("");
}

const copyButton = document.querySelector("#copy-evidence");
const evidence = document.querySelector("#evidence-text");
const flagForm = document.querySelector("#flag-form");
const flagInput = document.querySelector("#flag");
const flagResult = document.querySelector("#flag-result");

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(evidence.innerText);
    copyButton.textContent = "Copied";
    window.setTimeout(() => { copyButton.textContent = "Copy evidence"; }, 1600);
  } catch {
    copyButton.textContent = "Copy failed";
  }
});

flagForm.addEventListener("submit", async event => {
  event.preventDefault();
  const candidate = flagInput.value.trim();

  if (!candidate) {
    flagResult.textContent = "Enter a recovered flag first.";
    flagResult.className = "flag-result failure";
    return;
  }

  const candidateHash = await sha256(candidate);
  const solved = candidateHash === EXPECTED_FLAG_HASH;
  flagResult.textContent = solved
    ? "ACCESS GRANTED: correct flag. Challenge complete."
    : "ACCESS DENIED: that flag is not correct.";
  flagResult.className = `flag-result ${solved ? "success" : "failure"}`;
});
