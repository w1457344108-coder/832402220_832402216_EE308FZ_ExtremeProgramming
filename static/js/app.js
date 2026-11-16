const state = {
  view: "all", // "all" | "favorites"
  query: "",
  sort: "favorites",
  contacts: [],
};

const METHOD_TYPE_LABELS = {
  phone: "Phone",
  email: "Email",
  social: "Social",
  address: "Address",
  other: "Other",
};

const els = {
  contactsGrid: document.getElementById("contactsGrid"),
  emptyState: document.getElementById("emptyState"),
  emptyTitle: document.getElementById("emptyTitle"),
  emptyDesc: document.getElementById("emptyDesc"),
  totalCount: document.getElementById("totalCount"),
  favoriteCount: document.getElementById("favoriteCount"),
  tabAll: document.getElementById("tabAll"),
  tabFavorites: document.getElementById("tabFavorites"),
  searchInput: document.getElementById("searchInput"),
  sortSelect: document.getElementById("sortSelect"),
  contactModal: document.getElementById("contactModal"),
  contactModalTitle: document.getElementById("contactModalTitle"),
  contactForm: document.getElementById("contactForm"),
  contactIdInput: document.getElementById("contactIdInput"),
  nameInput: document.getElementById("nameInput"),
  companyInput: document.getElementById("companyInput"),
  titleInput: document.getElementById("titleInput"),
  favoriteInput: document.getElementById("favoriteInput"),
  notesInput: document.getElementById("notesInput"),
  methodsContainer: document.getElementById("methodsContainer"),
  importModal: document.getElementById("importModal"),
  importForm: document.getElementById("importForm"),
  excelFileInput: document.getElementById("excelFileInput"),
  importSummary: document.getElementById("importSummary"),
  toastContainer: document.getElementById("toastContainer"),
};

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function showToast(message, kind = "info") {
  const toast = document.createElement("div");
  toast.className = `toast ${kind}`;
  toast.textContent = message;
  els.toastContainer.appendChild(toast);
  window.setTimeout(() => {
    toast.remove();
  }, 3200);
}

function initialsForName(name) {
  const parts = String(name || "").trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

async function apiRequest(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || `Request failed (${response.status})`);
  }
  return data;
}

function updateCounts(totalCount, favoriteCount) {
  els.totalCount.textContent = String(totalCount ?? 0);
  els.favoriteCount.textContent = String(favoriteCount ?? 0);
}

async function loadContacts() {
  const params = new URLSearchParams();
  if (state.query.trim()) params.set("q", state.query.trim());
  if (state.view === "favorites") params.set("favorite", "1");
  params.set("sort", state.sort);

  try {
    const data = await apiRequest(`/api/contacts?${params.toString()}`);
    state.contacts = data.contacts || [];
    updateCounts(data.total_count, data.favorite_count);
    renderContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function renderMethodItem(method) {
  const type = method.method_type || "other";
  const badge = METHOD_TYPE_LABELS[type] || "Other";
  const labelHtml = method.label
    ? `<span class="method-label">${escapeHtml(method.label)}:</span>`
    : "";
  return `
    <li class="method-item">
      <span class="method-badge type-${escapeHtml(type)}">${escapeHtml(badge)}</span>
      ${labelHtml}
      <span class="method-value">${escapeHtml(method.value)}</span>
    </li>
  `;
}

function renderContacts() {
  if (state.contacts.length === 0) {
    els.contactsGrid.innerHTML = "";
    els.emptyState.classList.remove("hidden");

    if (state.view === "favorites") {
      els.emptyTitle.textContent = "No bookmarked contacts";
      els.emptyDesc.textContent = "Click the star icon on any contact card to bookmark important people here.";
    } else if (state.query.trim()) {
      els.emptyTitle.textContent = "No matching contacts";
      els.emptyDesc.textContent = "Try a different keyword or clear the search box.";
    } else {
      els.emptyTitle.textContent = "No contacts yet";
      els.emptyDesc.textContent = "Add a contact manually, load synthetic demo data, or import an Excel (.xlsx) spreadsheet.";
    }
    return;
  }

  els.emptyState.classList.add("hidden");
  els.contactsGrid.innerHTML = state.contacts
    .map((contact) => {
      const metaParts = [contact.title, contact.company].filter(Boolean);
      const metaText = metaParts.join(" · ");
      const methods = contact.methods || [];
      const methodsHtml = methods.length
        ? `<ul class="method-list">${methods.map(renderMethodItem).join("")}</ul>`
        : `<p class="helper-text">No contact methods added yet.</p>`;
      const notesHtml = contact.notes
        ? `<p class="contact-notes">${escapeHtml(contact.notes)}</p>`
        : "";
      const favClass = contact.is_favorite ? "is-favorite" : "";
      const starChar = contact.is_favorite ? "★" : "☆";
      const favTitle = contact.is_favorite ? "Remove bookmark" : "Bookmark contact";

      return `
        <article class="contact-card ${favClass}" data-id="${contact.id}">
          <div class="contact-card-header">
            <div class="identity-block">
              <div class="avatar">${escapeHtml(initialsForName(contact.name))}</div>
              <div>
                <h3 class="contact-name">${escapeHtml(contact.name)}</h3>
                ${metaText ? `<p class="contact-meta">${escapeHtml(metaText)}</p>` : ""}
              </div>
            </div>
            <button
              type="button"
              class="favorite-btn ${contact.is_favorite ? "active" : ""}"
              data-action="toggle-favorite"
              data-id="${contact.id}"
              title="${favTitle}"
              aria-label="${favTitle}"
            >${starChar}</button>
          </div>
          ${methodsHtml}
          ${notesHtml}
          <div class="contact-card-footer">
            <button type="button" class="btn btn-sm btn-secondary" data-action="edit" data-id="${contact.id}">Edit</button>
            <button type="button" class="btn btn-sm btn-danger-ghost" data-action="delete" data-id="${contact.id}">Delete</button>
          </div>
        </article>
      `;
    })
    .join("");
}

function addMethodRow(method = { method_type: "phone", label: "", value: "" }) {
  const row = document.createElement("div");
  row.className = "method-row";
  row.innerHTML = `
    <select class="method-type-input" aria-label="Contact method type">
      <option value="phone">Phone</option>
      <option value="email">Email</option>
      <option value="social">Social Media</option>
      <option value="address">Address</option>
      <option value="other">Other</option>
    </select>
    <input type="text" class="method-label-input" placeholder="Label (e.g. Mobile)" maxlength="40" />
    <input type="text" class="method-value-input" placeholder="Value (number, email, handle...)" maxlength="200" />
    <button type="button" class="remove-method-btn" title="Remove method" aria-label="Remove method">&times;</button>
  `;
  row.querySelector(".method-type-input").value = method.method_type || "phone";
  row.querySelector(".method-label-input").value = method.label || "";
  row.querySelector(".method-value-input").value = method.value || "";
  row.querySelector(".remove-method-btn").addEventListener("click", () => {
    row.remove();
  });
  els.methodsContainer.appendChild(row);
}

function openContactModal(contact = null) {
  els.contactForm.reset();
  els.methodsContainer.innerHTML = "";

  if (contact) {
    els.contactModalTitle.textContent = "Edit Contact";
    els.contactIdInput.value = String(contact.id);
    els.nameInput.value = contact.name || "";
    els.companyInput.value = contact.company || "";
    els.titleInput.value = contact.title || "";
    els.favoriteInput.checked = Boolean(contact.is_favorite);
    els.notesInput.value = contact.notes || "";

    const methods = contact.methods || [];
    if (methods.length > 0) {
      methods.forEach((m) => addMethodRow(m));
    } else {
      addMethodRow({ method_type: "phone", label: "Mobile", value: "" });
    }
  } else {
    els.contactModalTitle.textContent = "New Contact";
    els.contactIdInput.value = "";
    addMethodRow({ method_type: "phone", label: "Mobile", value: "" });
    addMethodRow({ method_type: "email", label: "Work", value: "" });
  }

  els.contactModal.classList.remove("hidden");
  els.nameInput.focus();
}

function closeContactModal() {
  els.contactModal.classList.add("hidden");
}

function openImportModal() {
  els.importForm.reset();
  els.importSummary.classList.add("hidden");
  els.importSummary.classList.remove("has-errors");
  els.importSummary.innerHTML = "";
  els.importModal.classList.remove("hidden");
}

function closeImportModal() {
  els.importModal.classList.add("hidden");
}

function collectContactFormPayload() {
  const methods = [];
  els.methodsContainer.querySelectorAll(".method-row").forEach((row) => {
    const methodType = row.querySelector(".method-type-input").value;
    const label = row.querySelector(".method-label-input").value.trim();
    const value = row.querySelector(".method-value-input").value.trim();
    if (value) {
      methods.push({ method_type: methodType, label, value });
    }
  });

  return {
    name: els.nameInput.value.trim(),
    company: els.companyInput.value.trim(),
    title: els.titleInput.value.trim(),
    is_favorite: els.favoriteInput.checked,
    notes: els.notesInput.value.trim(),
    methods,
  };
}

async function handleSaveContact(event) {
  event.preventDefault();
  const contactId = els.contactIdInput.value.trim();
  const payload = collectContactFormPayload();
  if (!payload.name) {
    showToast("Contact name is required.", "error");
    return;
  }

  try {
    if (contactId) {
      await apiRequest(`/api/contacts/${contactId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      showToast("Contact updated.", "success");
    } else {
      await apiRequest("/api/contacts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      showToast("Contact created.", "success");
    }
    closeContactModal();
    await loadContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleToggleFavorite(contactId) {
  try {
    const data = await apiRequest(`/api/contacts/${contactId}/favorite`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    const fav = data.contact?.is_favorite;
    showToast(fav ? "Contact bookmarked." : "Bookmark removed.", "success");
    await loadContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleDeleteContact(contactId) {
  const contact = state.contacts.find((c) => c.id === contactId);
  const label = contact ? contact.name : `#${contactId}`;
  if (!window.confirm(`Delete contact "${label}"?`)) {
    return;
  }

  try {
    await apiRequest(`/api/contacts/${contactId}`, { method: "DELETE" });
    showToast("Contact deleted.", "success");
    await loadContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleSeedDemo() {
  try {
    const data = await apiRequest("/api/contacts/seed-demo", { method: "POST" });
    if (data.created_count > 0) {
      showToast(`Loaded ${data.created_count} demo contacts.`, "success");
    } else {
      showToast("Demo contacts are already present.", "info");
    }
    await loadContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleImportSubmit(event) {
  event.preventDefault();
  const file = els.excelFileInput.files[0];
  if (!file) {
    showToast("Please choose an .xlsx file.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const data = await apiRequest("/api/contacts/import", {
      method: "POST",
      body: formData,
    });
    const hasErrors = (data.errors || []).length > 0;
    els.importSummary.classList.remove("hidden");
    els.importSummary.classList.toggle("has-errors", hasErrors);
    const errorList = hasErrors
      ? `<ul>${data.errors.map((e) => `<li>${escapeHtml(e)}</li>`).join("")}</ul>`
      : "";
    els.importSummary.innerHTML = `
      <strong>Import complete:</strong> ${data.imported_count} imported, ${data.skipped_count} skipped.
      ${errorList}
    `;
    showToast(`Imported ${data.imported_count} contacts.`, "success");
    await loadContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function setView(nextView) {
  state.view = nextView;
  els.tabAll.classList.toggle("active", nextView === "all");
  els.tabFavorites.classList.toggle("active", nextView === "favorites");
  els.tabAll.setAttribute("aria-selected", String(nextView === "all"));
  els.tabFavorites.setAttribute("aria-selected", String(nextView === "favorites"));
  loadContacts();
}

function downloadFromUrl(url) {
  window.location.href = url;
}

function bindEvents() {
  els.tabAll.addEventListener("click", () => setView("all"));
  els.tabFavorites.addEventListener("click", () => setView("favorites"));

  let searchTimer = null;
  els.searchInput.addEventListener("input", (e) => {
    state.query = e.target.value;
    window.clearTimeout(searchTimer);
    searchTimer = window.setTimeout(loadContacts, 180);
  });

  els.sortSelect.addEventListener("change", (e) => {
    state.sort = e.target.value;
    loadContacts();
  });

  document.getElementById("addContactBtn").addEventListener("click", () => openContactModal());
  document.getElementById("emptyAddBtn").addEventListener("click", () => openContactModal());
  document.getElementById("closeContactModal").addEventListener("click", closeContactModal);
  document.getElementById("cancelContactBtn").addEventListener("click", closeContactModal);
  document.getElementById("addMethodRowBtn").addEventListener("click", () =>
    addMethodRow({ method_type: "phone", label: "", value: "" })
  );
  els.contactForm.addEventListener("submit", handleSaveContact);

  document.getElementById("openImportBtn").addEventListener("click", openImportModal);
  document.getElementById("emptyImportBtn").addEventListener("click", openImportModal);
  document.getElementById("closeImportModal").addEventListener("click", closeImportModal);
  document.getElementById("cancelImportBtn").addEventListener("click", closeImportModal);
  els.importForm.addEventListener("submit", handleImportSubmit);

  document.getElementById("seedDemoBtn").addEventListener("click", handleSeedDemo);
  document.getElementById("emptyDemoBtn").addEventListener("click", handleSeedDemo);

  document.getElementById("templateBtn").addEventListener("click", () => {
    downloadFromUrl("/api/contacts/template");
  });
  document.getElementById("modalTemplateBtn").addEventListener("click", () => {
    downloadFromUrl("/api/contacts/template");
  });
  document.getElementById("exportBtn").addEventListener("click", () => {
    const params = new URLSearchParams();
    if (state.view === "favorites") params.set("favorite", "1");
    if (state.query.trim()) params.set("q", state.query.trim());
    downloadFromUrl(`/api/contacts/export?${params.toString()}`);
  });

  els.contactsGrid.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;
    const contactId = Number(btn.dataset.id);
    const action = btn.dataset.action;

    if (action === "toggle-favorite") {
      handleToggleFavorite(contactId);
    } else if (action === "edit") {
      const contact = state.contacts.find((c) => c.id === contactId);
      if (contact) openContactModal(contact);
    } else if (action === "delete") {
      handleDeleteContact(contactId);
    }
  });

  els.contactModal.addEventListener("click", (e) => {
    if (e.target === els.contactModal) closeContactModal();
  });
  els.importModal.addEventListener("click", (e) => {
    if (e.target === els.importModal) closeImportModal();
  });
}

bindEvents();
loadContacts();
