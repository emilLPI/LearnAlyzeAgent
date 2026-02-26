const $ = (id) => document.getElementById(id);

const write = (id, payload) => {
  const node = $(id);
  if (!node) return;
  node.textContent = JSON.stringify(payload, null, 2);
};

function setApiStatus(text, ok = false) {
  const badge = $("api-status");
  if (!badge) return;
  badge.textContent = text;
  badge.classList.toggle("ok", ok);
  badge.classList.toggle("error", !ok);
}

async function api(path, options = {}) {
  try {
    const response = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const rawText = await response.text();
    let data;
    try {
      data = rawText ? JSON.parse(rawText) : {};
    } catch {
      data = { raw: rawText };
    }

    if (response.ok) {
      setApiStatus("Connected", true);
    } else {
      setApiStatus(`API error (${response.status})`, false);
    }

    return { ok: response.ok, status: response.status, data };
  } catch (error) {
    setApiStatus("Disconnected (start backend or use npm run dev:full)", false);
    return {
      ok: false,
      status: 0,
      data: {
        error: "Network error",
        detail: String(error),
        hint: "Start full stack with npm run dev:full, or run FastAPI backend on http://127.0.0.1:8000",
      },
    };
  }
}

function bind(id, handler) {
  const node = $(id);
  if (!node) return;
  node.onclick = handler;
  $(id).textContent = JSON.stringify(payload, null, 2);
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  return { ok: response.ok, status: response.status, data };
}

async function refreshKpis() {
  const jobs = await api("/jobs");
  const list = Array.isArray(jobs.data) ? jobs.data : [];
  const total = list.length || 1;
  const success = list.filter((j) => j.status === "succeeded").length;
  const pending = list.filter((j) => ["pending", "planned", "executing"].includes(j.status)).length;
  const approvals = list.filter((j) => j.status === "requires_approval").length;

  if ($("kpi-success")) $("kpi-success").textContent = `${Math.round((success / total) * 100)}%`;
  if ($("kpi-pending")) $("kpi-pending").textContent = `${pending}`;
  if ($("kpi-approvals")) $("kpi-approvals").textContent = `${approvals}`;

  const learning = await api("/capabilities/insights");
  if ($("kpi-learned-actions")) $("kpi-learned-actions").textContent = `${learning.data?.learned_actions ?? 0}`;
  $("kpi-success").textContent = `${Math.round((success / total) * 100)}%`;
  $("kpi-pending").textContent = `${pending}`;
  $("kpi-approvals").textContent = `${approvals}`;

  const learning = await api("/capabilities/insights");
  $("kpi-learned-actions").textContent = `${learning.data?.learned_actions ?? 0}`;
}

async function refreshLearningInsights() {
  const [insights, latest] = await Promise.all([
    api("/capabilities/insights"),
    api("/capabilities/latest"),
  ]);

  write("learning-output", {
    insights: insights.data,
    latest_manifest_pages: (latest.data?.pages || []).map((p) => ({
  write("learning-output", {
    insights: insights.data,
    latest_manifest_pages: latest.data?.pages?.map((p) => ({
      id: p.id,
      route: p.route,
      actions: (p.actions || []).map((a) => a.id),
    })),
  });
}

async function refreshAiStatus() {
  write("ai-output", await api("/ai/integration/status"));
}

function loadCredentialInputs() {
  const email = sessionStorage.getItem("learnalyze_email") || "";
  if ($("learnalyze-email")) $("learnalyze-email").value = email;
  if ($("learnalyze-status")) {
    $("learnalyze-status").textContent = email
      ? `Email loaded for ${email} (saved in browser session only).`
      : "No email saved yet.";
  }
}

bind("save-local-credentials", () => {
  const email = $("learnalyze-email")?.value.trim() || "";
  sessionStorage.setItem("learnalyze_email", email);
  if ($("learnalyze-status")) {
    $("learnalyze-status").textContent = email
      ? `Email saved locally for ${email}. Password is never stored. Open LearnAlyze window and log in manually.`
      : "Please enter email first.";
  }
});

bind("clear-local-credentials", () => {
  sessionStorage.removeItem("learnalyze_email");
  if ($("learnalyze-email")) $("learnalyze-email").value = "";
  if ($("learnalyze-password")) $("learnalyze-password").value = "";
  if ($("learnalyze-status")) $("learnalyze-status").textContent = "Saved email cleared from browser session.";
});

bind("open-learnalyze-window", () => {
  window.open("https://app-eu-learnalyze.azurewebsites.net/", "_blank", "noopener,noreferrer");
  if ($("learnalyze-status")) {
    $("learnalyze-status").textContent =
      "LearnAlyze opened in a new tab/window. This avoids iframe security blocks.";
  }
});

bind("seed-email", async () => {
function loadCredentialInputs() {
  const email = sessionStorage.getItem("learnalyze_email") || "";
  $("learnalyze-email").value = email;
  $("learnalyze-status").textContent = email
    ? `Email loaded for ${email} (saved in browser session only).`
    : "No email saved yet.";
}

$("save-local-credentials").onclick = () => {
  const email = $("learnalyze-email").value.trim();
  sessionStorage.setItem("learnalyze_email", email);
  $("learnalyze-status").textContent = email
    ? `Email saved locally for ${email}. Password is never stored. Open LearnAlyze window and log in manually.`
    : "Please enter email first.";
};

$("clear-local-credentials").onclick = () => {
  sessionStorage.removeItem("learnalyze_email");
  $("learnalyze-email").value = "";
  $("learnalyze-password").value = "";
  $("learnalyze-status").textContent = "Saved email cleared from browser session.";
};

$("open-learnalyze-window").onclick = () => {
  window.open("https://app-eu-learnalyze.azurewebsites.net/", "_blank", "noopener,noreferrer");
  $("learnalyze-status").textContent =
    "LearnAlyze opened in a new tab/window. This avoids iframe security blocks.";
};

$("seed-email").onclick = async () => {
  const payload = {
    tenant_id: "tenant-ui",
    from_address: "ops@example.com",
    subject: "Please opret kunde",
    body: "new customer onboarding through email",
  };
  write("emails-output", await api("/emails", { method: "POST", body: JSON.stringify(payload) }));
  await refreshKpis();
});

bind("triage-latest", async () => {
  const emails = await api("/emails?tenant_id=tenant-ui&status=new");
  const latest = Array.isArray(emails.data) ? emails.data[0] : null;
  if (!latest) {
    write("emails-output", { error: "No new email found", details: emails.data });
    return;
  }
  write("emails-output", await api("/tasks/from-email", { method: "POST", body: JSON.stringify({ email_id: latest.id }) }));
  await refreshKpis();
});

bind("plan-latest", async () => {
  const tasks = await api("/tasks");
  const latest = Array.isArray(tasks.data) ? tasks.data[0] : null;
  if (!latest) {
    write("jobs-output", { error: "No task found", details: tasks.data });
    return;
  }
  write("jobs-output", await api(`/jobs/plan/${latest.id}`, { method: "POST" }));
  await refreshKpis();
});

bind("list-jobs", async () => {
  write("jobs-output", await api("/jobs"));
  await refreshKpis();
});

bind("rescan-capabilities", async () => {
  write("cap-output", await api("/capabilities/rescan", { method: "POST" }));
  await refreshKpis();
  await refreshLearningInsights();
});

bind("latest-capabilities", async () => write("cap-output", await api("/capabilities/latest")));
bind("refresh-learning", refreshLearningInsights);

bind("save-settings", async () => {
};

$("triage-latest").onclick = async () => {
  const emails = await api("/emails?tenant_id=tenant-ui&status=new");
  const latest = emails.data?.[0];
  if (!latest) return write("emails-output", { error: "No new email found" });
  write("emails-output", await api("/tasks/from-email", { method: "POST", body: JSON.stringify({ email_id: latest.id }) }));
  await refreshKpis();
};

$("plan-latest").onclick = async () => {
  const tasks = await api("/tasks");
  const latest = tasks.data?.[0];
  if (!latest) return write("jobs-output", { error: "No task found" });
  write("jobs-output", await api(`/jobs/plan/${latest.id}`, { method: "POST" }));
  await refreshKpis();
};

$("list-jobs").onclick = async () => {
  write("jobs-output", await api("/jobs"));
  await refreshKpis();
};
$("rescan-capabilities").onclick = async () => {
  write("cap-output", await api("/capabilities/rescan", { method: "POST" }));
  await refreshKpis();
  await refreshLearningInsights();
};
$("latest-capabilities").onclick = async () => write("cap-output", await api("/capabilities/latest"));
$("refresh-learning").onclick = refreshLearningInsights;

$("save-settings").onclick = async () => {
  const payload = {
    tenant_id: "tenant-ui",
    autonomy_mode: "SUPERVISED",
    scopes: ["Customers", "Emails"],
    kill_switch: false,
    policy: { no_delete_without_approval: true, max_bulk_updates: 100 },
    outlook_connected: true,
    require_manual_learnalyze_login: true,
  };
  write("settings-output", await api("/settings", { method: "POST", body: JSON.stringify(payload) }));
});

bind("get-settings", async () => write("settings-output", await api("/settings?tenant_id=tenant-ui")));
bind("refresh-ai-status", refreshAiStatus);
};

$("get-settings").onclick = async () => write("settings-output", await api("/settings?tenant_id=tenant-ui"));

loadCredentialInputs();
refreshKpis();
refreshLearningInsights();
refreshAiStatus();
