const $ = (id) => document.getElementById(id);

const write = (id, payload) => {
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

$("seed-email").onclick = async () => {
  const payload = {
    tenant_id: "tenant-ui",
    from_address: "ops@example.com",
    subject: "Please opret kunde",
    body: "new customer onboarding through email",
  };
  write("emails-output", await api("/emails", { method: "POST", body: JSON.stringify(payload) }));
};

$("triage-latest").onclick = async () => {
  const emails = await api("/emails?tenant_id=tenant-ui&status=new");
  const latest = emails.data?.[0];
  if (!latest) return write("emails-output", { error: "No new email found" });
  write("emails-output", await api("/tasks/from-email", { method: "POST", body: JSON.stringify({ email_id: latest.id }) }));
};

$("plan-latest").onclick = async () => {
  const tasks = await api("/tasks");
  const latest = tasks.data?.[0];
  if (!latest) return write("jobs-output", { error: "No task found" });
  write("jobs-output", await api(`/jobs/plan/${latest.id}`, { method: "POST" }));
};

$("list-jobs").onclick = async () => write("jobs-output", await api("/jobs"));
$("rescan-capabilities").onclick = async () => write("cap-output", await api("/capabilities/rescan", { method: "POST" }));
$("latest-capabilities").onclick = async () => write("cap-output", await api("/capabilities/latest"));

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
};

$("get-settings").onclick = async () => write("settings-output", await api("/settings?tenant_id=tenant-ui"));
