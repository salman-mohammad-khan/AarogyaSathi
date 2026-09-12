async function getJSON(url) {
  const res = await fetch(url);
  return res.json();
}

function fillTable(tbodyId, rows, keyName, valName, transform) {
  const tbody = document.querySelector(tbodyId);
  tbody.innerHTML = "";
  if (!rows || !Object.keys(rows).length) {
    tbody.innerHTML = '<tr><td colspan="2">No data yet.</td></tr>';
    return;
  }
  Object.entries(rows)
    .sort((a, b) => b[1] - a[1])
    .forEach(([k, v]) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${transform ? transform(k) : k}</td><td>${v}</td>`;
      tbody.appendChild(tr);
    });
}

async function refresh() {
  try {
    const stats = await getJSON("/api/stats");
    document.getElementById("msg24").textContent = stats.messages_24h ?? 0;
    document.getElementById("msg7").textContent = stats.messages_7d ?? 0;
    document.getElementById("ev24").textContent = stats.symptom_events_24h ?? 0;
    document.getElementById("al7").textContent = stats.alerts_7d ?? 0;
    fillTable("#intentsTable tbody", stats.intents_7d);
    fillTable("#verdictsTable tbody", stats.verdicts_7d);
    fillTable("#langsTable tbody", stats.languages_7d);

    const alerts = await getJSON("/api/surveillance/alerts");
    const tbody = document.querySelector("#alertsTable tbody");
    tbody.innerHTML = "";
    if (!alerts.spike_alerts.length) {
      tbody.innerHTML =
        '<tr><td colspan="6">No spike alerts — click "Seed demo outbreak" to simulate one.</td></tr>';
    }
    alerts.spike_alerts.forEach((a) => {
      const tr = document.createElement("tr");
      const when = new Date(a.ts * 1000).toLocaleString();
      tr.innerHTML = `<td>${a.pincode}</td><td>${a.symptom}</td><td>${a.current_count}</td>
        <td>${a.baseline}</td><td class="sev-${a.severity}">${a.severity.toUpperCase()}</td><td>${when}</td>`;
      tbody.appendChild(tr);
    });

    const ul = document.getElementById("advisories");
    ul.innerHTML = "";
    alerts.official_advisories.forEach((a) => {
      const li = document.createElement("li");
      li.innerHTML = `<b>${a.title}</b> — ${a.body}<br/><small>${a.source_name}</small>`;
      ul.appendChild(li);
    });
  } catch (e) {
    console.error(e);
  }
}

document.getElementById("seedBtn").addEventListener("click", async () => {
  const r = await fetch("/api/surveillance/seed", { method: "POST" });
  await refresh();
});
document.getElementById("runBtn").addEventListener("click", async () => {
  const r = await fetch("/api/surveillance/run", { method: "POST" });
  await refresh();
});
document.getElementById("clearBtn").addEventListener("click", async () => {
  if (!confirm("Delete all surveillance data?")) return;
  await fetch("/api/surveillance/clear", { method: "POST" });
  await refresh();
});

refresh();
setInterval(refresh, 15000);
