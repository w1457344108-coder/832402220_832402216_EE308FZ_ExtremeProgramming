const STORAGE_KEYS = {
  theme: "ab_theme",
  lang: "ab_lang",
};

const VALID_THEMES = ["light", "dark", "ocean", "warm"];

const I18N = {
  en: {
    pageTitle: "Address Book — Extreme Programming",
    appTitle: "Address Book",
    appSubtitle: "Bookmark contacts, manage multiple contact methods, and import/export Excel",
    themeLight: "Theme: Light",
    themeDark: "Theme: Dark",
    themeOcean: "Theme: Ocean Breeze",
    themeWarm: "Theme: Warm Paper",
    langButton: "中文 / EN",
    btnLoadDemo: "Load Demo",
    btnLoadDemoContacts: "Load Demo Contacts",
    btnTemplate: "Template",
    btnImportExcel: "Import Excel",
    btnExportExcel: "Export Excel",
    btnExportBookmarked: "Export Bookmarked",
    btnNewContact: "+ New Contact",
    tabAll: "All Contacts",
    tabBookmarked: "Bookmarked",
    searchPlaceholder: "Search name, company, phone, email, social, or address...",
    searchLabel: "Search contacts (/)",
    btnClearSearch: "Clear",
    clearSearchLabel: "Clear search",
    sortFavorites: "Sort: Bookmarked First",
    sortName: "Sort: Name (A–Z)",
    sortRecent: "Sort: Recently Updated",
    showingCount: "{count} shown",
    emptyTitleDefault: "No contacts yet",
    emptyDescDefault: "Add a contact manually, load synthetic demo data, or import an Excel (.xlsx) spreadsheet.",
    emptyTitleFavorites: "No bookmarked contacts",
    emptyDescFavorites: "Click the star icon on any contact card to bookmark important people here.",
    emptyTitleSearch: "No matching contacts",
    emptyDescSearch: "Try a different keyword or clear the search box.",
    noMethods: "No contact methods added yet.",
    btnEdit: "Edit",
    btnDelete: "Delete",
    btnCopy: "Copy",
    bookmarkAdd: "Bookmark contact",
    bookmarkRemove: "Remove bookmark",
    modalNewContact: "New Contact",
    modalEditContact: "Edit Contact",
    fieldName: "Name",
    fieldCompany: "Company",
    fieldTitle: "Title / Role",
    fieldBookmark: "★ Bookmark this contact",
    fieldNotes: "Notes",
    namePlaceholder: "e.g. Lin Wei",
    companyPlaceholder: "e.g. Fuzhou Cloud Tech",
    titlePlaceholder: "e.g. Backend Engineer",
    notesPlaceholder: "Optional notes...",
    methodsHeading: "Contact Methods",
    methodsSubtext: "Add multiple phone numbers, emails, social handles, or addresses.",
    btnAddMethod: "+ Add Method",
    btnCancel: "Cancel",
    btnSaveContact: "Save Contact",
    importModalTitle: "Import Contacts from Excel",
    importHelp:
      "Upload an .xlsx spreadsheet where each contact occupies one row and each category occupies a separate column (Name, Favorite, Company, Title, Phone Numbers, Emails, Social Media, Addresses, Other Contacts, Notes).",
    duplicateModeLabel: "Duplicate Name Handling",
    dupSkip: "Skip contacts whose name already exists",
    dupUpdate: "Update existing contact with matching name",
    dupAllow: "Import all rows as new contacts",
    btnDownloadTemplate: "Download Template",
    btnClose: "Close",
    btnUploadImport: "Upload & Import",
    methodTypes: {
      phone: "Phone",
      email: "Email",
      social: "Social",
      address: "Address",
      other: "Other",
    },
    methodPlaceholders: {
      phone: { label: "Mobile / Work", value: "e.g. 13800138000 or 0591-88886666" },
      email: { label: "Work / Personal", value: "e.g. name@example.com" },
      social: { label: "WeChat / GitHub", value: "e.g. @username or wx_id" },
      address: { label: "Home / Office", value: "e.g. No. 2 Xueyuan Rd, Fuzhou" },
      other: { label: "Website / Note", value: "e.g. https://example.com" },
    },
    toastNameRequired: "Contact name is required.",
    toastCreated: "Contact created.",
    toastUpdated: "Contact updated.",
    toastBookmarked: "Contact bookmarked.",
    toastUnbookmarked: "Bookmark removed.",
    toastDeleted: "Contact deleted.",
    toastCopied: "Copied to clipboard: {value}",
    toastCopyFailed: "Copy failed. Please copy manually.",
    toastDemoLoaded: "Loaded {count} demo contacts.",
    toastDemoExists: "Demo contacts are already present.",
    toastSelectXlsx: "Please choose an .xlsx file.",
    toastImported: "Imported {imported}, updated {updated}, skipped {skipped}.",
    confirmDelete: 'Delete contact "{name}"?',
    importSummaryText: "Import complete: {imported} imported, {updated} updated, {skipped} skipped.",
  },
  zh: {
    pageTitle: "个人通讯录 — 极限编程作业",
    appTitle: "通讯录",
    appSubtitle: "支持联系人收藏、多种联系方式管理与 Excel 表格导入导出",
    themeLight: "风格：浅色简约",
    themeDark: "风格：深色夜间",
    themeOcean: "风格：海风青蓝",
    themeWarm: "风格：暖纸手账",
    langButton: "EN / 中文",
    btnLoadDemo: "加载示例",
    btnLoadDemoContacts: "加载示例联系人",
    btnTemplate: "下载模板",
    btnImportExcel: "导入 Excel",
    btnExportExcel: "导出 Excel",
    btnExportBookmarked: "导出已收藏",
    btnNewContact: "+ 新建联系人",
    tabAll: "全部联系人",
    tabBookmarked: "已收藏",
    searchPlaceholder: "搜索姓名、公司、电话、邮箱、社交账号或地址...",
    searchLabel: "搜索联系人（/）",
    btnClearSearch: "清空",
    clearSearchLabel: "清空搜索",
    sortFavorites: "排序：收藏优先",
    sortName: "排序：姓名 A–Z",
    sortRecent: "排序：最近更新",
    showingCount: "显示 {count} 位",
    emptyTitleDefault: "暂无联系人",
    emptyDescDefault: "你可以手动新建联系人、点击加载示例数据，或导入 Excel（.xlsx）表格。",
    emptyTitleFavorites: "暂无已收藏联系人",
    emptyDescFavorites: "点击任意联系人卡片右上角的星标按钮，即可收藏重要或常用联系人。",
    emptyTitleSearch: "未找到匹配的联系人",
    emptyDescSearch: "请尝试更换关键词或清空搜索框。",
    noMethods: "暂未添加联系方式。",
    btnEdit: "编辑",
    btnDelete: "删除",
    btnCopy: "复制",
    bookmarkAdd: "收藏联系人",
    bookmarkRemove: "取消收藏",
    modalNewContact: "新建联系人",
    modalEditContact: "编辑联系人",
    fieldName: "姓名",
    fieldCompany: "公司 / 单位",
    fieldTitle: "职位 / 身份",
    fieldBookmark: "★ 收藏该联系人",
    fieldNotes: "备注",
    namePlaceholder: "例如：林伟",
    companyPlaceholder: "例如：福州云科技有限公司",
    titlePlaceholder: "例如：后端工程师",
    notesPlaceholder: "可选备注信息...",
    methodsHeading: "联系方式",
    methodsSubtext: "可为同一联系人添加多条电话、邮箱、社交账号或实体地址。",
    btnAddMethod: "+ 添加联系方式",
    btnCancel: "取消",
    btnSaveContact: "保存联系人",
    importModalTitle: "从 Excel 导入联系人",
    importHelp:
      "请上传 .xlsx 表格，每位联系人占一行、每类信息占一列（Name、Favorite、Company、Title、Phone Numbers、Emails、Social Media、Addresses、Other Contacts、Notes）。",
    duplicateModeLabel: "同名联系人处理方式",
    dupSkip: "跳过系统中已存在的同名联系人",
    dupUpdate: "覆盖更新同名联系人的信息",
    dupAllow: "全部作为新联系人导入",
    btnDownloadTemplate: "下载示例模板",
    btnClose: "关闭",
    btnUploadImport: "上传并导入",
    methodTypes: {
      phone: "电话",
      email: "邮箱",
      social: "社交",
      address: "地址",
      other: "其他",
    },
    methodPlaceholders: {
      phone: { label: "标签（如手机/办公）", value: "例如：13800138000 或 0591-88886666" },
      email: { label: "标签（如工作/个人）", value: "例如：name@example.com" },
      social: { label: "标签（如微信/GitHub）", value: "例如：@username 或微信号" },
      address: { label: "标签（如家庭/公司）", value: "例如：福州市大学城学园路2号" },
      other: { label: "标签（如主页/备注）", value: "例如：https://example.com" },
    },
    toastNameRequired: "请填写联系人姓名。",
    toastCreated: "联系人已创建。",
    toastUpdated: "联系人已更新。",
    toastBookmarked: "已加入收藏。",
    toastUnbookmarked: "已取消收藏。",
    toastDeleted: "联系人已删除。",
    toastCopied: "已复制：{value}",
    toastCopyFailed: "复制失败，请手动选中复制。",
    toastDemoLoaded: "已加载 {count} 位示例联系人。",
    toastDemoExists: "示例联系人已存在。",
    toastSelectXlsx: "请选择一个 .xlsx 文件。",
    toastImported: "导入完成：新增 {imported}，更新 {updated}，跳过 {skipped}。",
    confirmDelete: "确定要删除联系人“{name}”吗？",
    importSummaryText: "导入结果：新增 {imported} 位，更新 {updated} 位，跳过 {skipped} 位。",
  },
};

const state = {
  view: "all", // "all" | "favorites"
  query: "",
  sort: "favorites",
  theme: "light",
  lang: "en",
  contacts: [],
};

const els = {
  contactsGrid: document.getElementById("contactsGrid"),
  emptyState: document.getElementById("emptyState"),
  emptyTitle: document.getElementById("emptyTitle"),
  emptyDesc: document.getElementById("emptyDesc"),
  totalCount: document.getElementById("totalCount"),
  favoriteCount: document.getElementById("favoriteCount"),
  resultBadge: document.getElementById("resultBadge"),
  tabAll: document.getElementById("tabAll"),
  tabFavorites: document.getElementById("tabFavorites"),
  searchInput: document.getElementById("searchInput"),
  clearSearchBtn: document.getElementById("clearSearchBtn"),
  sortSelect: document.getElementById("sortSelect"),
  exportBtn: document.getElementById("exportBtn"),
  themeSelect: document.getElementById("themeSelect"),
  quickDarkToggleBtn: document.getElementById("quickDarkToggleBtn"),
  langToggleBtn: document.getElementById("langToggleBtn"),
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
  duplicateModeSelect: document.getElementById("duplicateModeSelect"),
  excelFileInput: document.getElementById("excelFileInput"),
  importSummary: document.getElementById("importSummary"),
  toastContainer: document.getElementById("toastContainer"),
};

function t(key, vars = {}) {
  const dict = I18N[state.lang] || I18N.en;
  let template = dict[key] ?? I18N.en[key] ?? key;
  Object.entries(vars).forEach(([k, v]) => {
    template = template.replaceAll(`{${k}}`, String(v));
  });
  return template;
}

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

function applyTheme(themeName) {
  const safeTheme = VALID_THEMES.includes(themeName) ? themeName : "light";
  state.theme = safeTheme;
  document.documentElement.setAttribute("data-theme", safeTheme);
  els.themeSelect.value = safeTheme;
  els.quickDarkToggleBtn.textContent = safeTheme === "dark" ? "☀️" : "🌙";
  try {
    localStorage.setItem(STORAGE_KEYS.theme, safeTheme);
  } catch (_err) {
    // Ignore storage unavailability
  }
}

function applyLanguage(lang) {
  state.lang = lang === "zh" ? "zh" : "en";
  document.documentElement.lang = state.lang === "zh" ? "zh-CN" : "en";
  document.title = t("pageTitle");

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.getAttribute("data-i18n");
    if (key) node.textContent = t(key);
  });

  els.langToggleBtn.textContent = t("langButton");
  els.searchInput.placeholder = t("searchPlaceholder");
  els.searchInput.setAttribute("aria-label", t("searchLabel"));
  els.clearSearchBtn.setAttribute("aria-label", t("clearSearchLabel"));
  els.clearSearchBtn.title = t("clearSearchLabel");
  els.nameInput.placeholder = t("namePlaceholder");
  els.companyInput.placeholder = t("companyPlaceholder");
  els.titleInput.placeholder = t("titlePlaceholder");
  els.notesInput.placeholder = t("notesPlaceholder");

  updateExportButtonLabel();
  updateResultBadge();
  updateMethodRowLanguage();
  renderContacts();

  if (!els.contactModal.classList.contains("hidden")) {
    els.contactModalTitle.textContent = els.contactIdInput.value.trim()
      ? t("modalEditContact")
      : t("modalNewContact");
  }

  try {
    localStorage.setItem(STORAGE_KEYS.lang, state.lang);
  } catch (_err) {
    // Ignore storage unavailability
  }
}

function updateExportButtonLabel() {
  const isFavoritesView = state.view === "favorites";
  els.exportBtn.textContent = isFavoritesView ? t("btnExportBookmarked") : t("btnExportExcel");
  els.exportBtn.classList.toggle("btn-accent-soft", isFavoritesView);
  els.exportBtn.classList.toggle("btn-secondary", !isFavoritesView);
}

function updateResultBadge() {
  els.resultBadge.textContent = t("showingCount", { count: state.contacts.length });
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
    updateResultBadge();
    renderContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function renderMethodValue(type, rawValue) {
  const safeText = escapeHtml(rawValue);
  if (type === "phone") {
    const telTarget = escapeHtml(rawValue.replace(/[^\d+*#]/g, ""));
    return telTarget ? `<a class="method-link" href="tel:${telTarget}">${safeText}</a>` : safeText;
  }
  if (type === "email") {
    return `<a class="method-link" href="mailto:${safeText}">${safeText}</a>`;
  }
  if (/^https?:\/\//i.test(rawValue)) {
    return `<a class="method-link" href="${safeText}" target="_blank" rel="noopener noreferrer">${safeText}</a>`;
  }
  return safeText;
}

function renderMethodItem(method) {
  const dict = I18N[state.lang] || I18N.en;
  const type = method.method_type || "other";
  const badge = dict.methodTypes[type] || dict.methodTypes.other;
  const labelHtml = method.label
    ? `<span class="method-label">${escapeHtml(method.label)}:</span>`
    : "";
  return `
    <li class="method-item">
      <span class="method-badge type-${escapeHtml(type)}">${escapeHtml(badge)}</span>
      ${labelHtml}
      <span class="method-value">${renderMethodValue(type, method.value)}</span>
      <button
        type="button"
        class="copy-method-btn"
        data-action="copy-method"
        data-value="${escapeHtml(method.value)}"
      >${escapeHtml(t("btnCopy"))}</button>
    </li>
  `;
}

function renderContacts() {
  if (state.contacts.length === 0) {
    els.contactsGrid.innerHTML = "";
    els.emptyState.classList.remove("hidden");

    if (state.view === "favorites") {
      els.emptyTitle.textContent = t("emptyTitleFavorites");
      els.emptyDesc.textContent = t("emptyDescFavorites");
    } else if (state.query.trim()) {
      els.emptyTitle.textContent = t("emptyTitleSearch");
      els.emptyDesc.textContent = t("emptyDescSearch");
    } else {
      els.emptyTitle.textContent = t("emptyTitleDefault");
      els.emptyDesc.textContent = t("emptyDescDefault");
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
        : `<p class="helper-text">${escapeHtml(t("noMethods"))}</p>`;
      const notesHtml = contact.notes
        ? `<p class="contact-notes">${escapeHtml(contact.notes)}</p>`
        : "";
      const favClass = contact.is_favorite ? "is-favorite" : "";
      const starChar = contact.is_favorite ? "★" : "☆";
      const favTitle = contact.is_favorite ? t("bookmarkRemove") : t("bookmarkAdd");

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
              title="${escapeHtml(favTitle)}"
              aria-label="${escapeHtml(favTitle)}"
            >${starChar}</button>
          </div>
          ${methodsHtml}
          ${notesHtml}
          <div class="contact-card-footer">
            <button type="button" class="btn btn-sm btn-secondary" data-action="edit" data-id="${contact.id}">${escapeHtml(t("btnEdit"))}</button>
            <button type="button" class="btn btn-sm btn-danger-ghost" data-action="delete" data-id="${contact.id}">${escapeHtml(t("btnDelete"))}</button>
          </div>
        </article>
      `;
    })
    .join("");
}

function applyPlaceholdersForMethodRow(row) {
  const dict = I18N[state.lang] || I18N.en;
  const typeSelect = row.querySelector(".method-type-input");
  const labelInput = row.querySelector(".method-label-input");
  const valueInput = row.querySelector(".method-value-input");
  const type = typeSelect.value || "phone";
  const placeholders = dict.methodPlaceholders[type] || dict.methodPlaceholders.other;
  labelInput.placeholder = placeholders.label;
  valueInput.placeholder = placeholders.value;
}

function updateMethodRowLanguage() {
  const dict = I18N[state.lang] || I18N.en;
  els.methodsContainer.querySelectorAll(".method-row").forEach((row) => {
    const select = row.querySelector(".method-type-input");
    Array.from(select.options).forEach((opt) => {
      if (dict.methodTypes[opt.value]) {
        opt.textContent = dict.methodTypes[opt.value];
      }
    });
    applyPlaceholdersForMethodRow(row);
  });
}

function addMethodRow(method = { method_type: "phone", label: "", value: "" }) {
  const dict = I18N[state.lang] || I18N.en;
  const row = document.createElement("div");
  row.className = "method-row";
  row.innerHTML = `
    <select class="method-type-input" aria-label="Contact method type">
      <option value="phone">${escapeHtml(dict.methodTypes.phone)}</option>
      <option value="email">${escapeHtml(dict.methodTypes.email)}</option>
      <option value="social">${escapeHtml(dict.methodTypes.social)}</option>
      <option value="address">${escapeHtml(dict.methodTypes.address)}</option>
      <option value="other">${escapeHtml(dict.methodTypes.other)}</option>
    </select>
    <input type="text" class="method-label-input" maxlength="40" />
    <input type="text" class="method-value-input" maxlength="200" />
    <button type="button" class="remove-method-btn" title="Remove" aria-label="Remove method">&times;</button>
  `;

  const typeSelect = row.querySelector(".method-type-input");
  typeSelect.value = method.method_type || "phone";
  row.querySelector(".method-label-input").value = method.label || "";
  row.querySelector(".method-value-input").value = method.value || "";

  applyPlaceholdersForMethodRow(row);
  typeSelect.addEventListener("change", () => applyPlaceholdersForMethodRow(row));
  row.querySelector(".remove-method-btn").addEventListener("click", () => row.remove());

  els.methodsContainer.appendChild(row);
}

function openContactModal(contact = null) {
  els.contactForm.reset();
  els.methodsContainer.innerHTML = "";

  if (contact) {
    els.contactModalTitle.textContent = t("modalEditContact");
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
    els.contactModalTitle.textContent = t("modalNewContact");
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
  els.duplicateModeSelect.value = "skip";
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
    showToast(t("toastNameRequired"), "error");
    return;
  }

  try {
    if (contactId) {
      await apiRequest(`/api/contacts/${contactId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      showToast(t("toastUpdated"), "success");
    } else {
      await apiRequest("/api/contacts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      showToast(t("toastCreated"), "success");
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
    showToast(fav ? t("toastBookmarked") : t("toastUnbookmarked"), "success");
    await loadContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleDeleteContact(contactId) {
  const contact = state.contacts.find((c) => c.id === contactId);
  const label = contact ? contact.name : `#${contactId}`;
  if (!window.confirm(t("confirmDelete", { name: label }))) {
    return;
  }

  try {
    await apiRequest(`/api/contacts/${contactId}`, { method: "DELETE" });
    showToast(t("toastDeleted"), "success");
    await loadContacts();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleCopyMethod(value) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(value);
    } else {
      const temp = document.createElement("textarea");
      temp.value = value;
      document.body.appendChild(temp);
      temp.select();
      document.execCommand("copy");
      temp.remove();
    }
    showToast(t("toastCopied", { value }), "success");
  } catch (_err) {
    showToast(t("toastCopyFailed"), "error");
  }
}

async function handleSeedDemo() {
  try {
    const data = await apiRequest("/api/contacts/seed-demo", { method: "POST" });
    if (data.created_count > 0) {
      showToast(t("toastDemoLoaded", { count: data.created_count }), "success");
    } else {
      showToast(t("toastDemoExists"), "info");
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
    showToast(t("toastSelectXlsx"), "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("duplicate_mode", els.duplicateModeSelect.value || "skip");

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
    const summaryVars = {
      imported: data.imported_count ?? 0,
      updated: data.updated_count ?? 0,
      skipped: data.skipped_count ?? 0,
    };
    els.importSummary.innerHTML = `
      <strong>${escapeHtml(t("importSummaryText", summaryVars))}</strong>
      ${errorList}
    `;
    showToast(t("toastImported", summaryVars), "success");
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
  updateExportButtonLabel();
  loadContacts();
}

function downloadFromUrl(url) {
  window.location.href = url;
}

function initPreferences() {
  let savedTheme = "light";
  let savedLang = "en";
  try {
    savedTheme = localStorage.getItem(STORAGE_KEYS.theme) || "light";
    savedLang = localStorage.getItem(STORAGE_KEYS.lang) || "en";
  } catch (_err) {
    // Ignore storage unavailability
  }
  applyTheme(savedTheme);
  applyLanguage(savedLang);
}

function bindEvents() {
  els.themeSelect.addEventListener("change", (e) => applyTheme(e.target.value));
  els.quickDarkToggleBtn.addEventListener("click", () => {
    applyTheme(state.theme === "dark" ? "light" : "dark");
  });
  els.langToggleBtn.addEventListener("click", () => {
    applyLanguage(state.lang === "en" ? "zh" : "en");
  });

  els.tabAll.addEventListener("click", () => setView("all"));
  els.tabFavorites.addEventListener("click", () => setView("favorites"));

  let searchTimer = null;
  els.searchInput.addEventListener("input", (e) => {
    state.query = e.target.value;
    els.clearSearchBtn.classList.toggle("hidden", !state.query);
    window.clearTimeout(searchTimer);
    searchTimer = window.setTimeout(loadContacts, 180);
  });
  els.clearSearchBtn.addEventListener("click", () => {
    window.clearTimeout(searchTimer);
    els.searchInput.value = "";
    state.query = "";
    els.clearSearchBtn.classList.add("hidden");
    els.searchInput.focus();
    loadContacts();
  });

  document.addEventListener("keydown", (event) => {
    if (event.isComposing || event.ctrlKey || event.metaKey || event.altKey) return;
    const openModal = [els.importModal, els.contactModal].find(
      (modal) => !modal.classList.contains("hidden")
    );
    if (event.key === "Escape" && openModal) {
      event.preventDefault();
      if (openModal === els.contactModal) {
        closeContactModal();
        document.getElementById("addContactBtn").focus();
      } else {
        closeImportModal();
        document.getElementById("openImportBtn").focus();
      }
      return;
    }
    const target = event.target;
    const isEditing = target instanceof Element && (
      target.closest("input, textarea, select") || target.isContentEditable
    );
    if (event.key === "/" && !openModal && !isEditing) {
      event.preventDefault();
      els.searchInput.focus();
    }
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
  els.exportBtn.addEventListener("click", () => {
    const params = new URLSearchParams();
    if (state.view === "favorites") params.set("favorite", "1");
    if (state.query.trim()) params.set("q", state.query.trim());
    downloadFromUrl(`/api/contacts/export?${params.toString()}`);
  });

  els.contactsGrid.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;
    const action = btn.dataset.action;

    if (action === "copy-method") {
      handleCopyMethod(btn.dataset.value || "");
      return;
    }

    const contactId = Number(btn.dataset.id);
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

initPreferences();
bindEvents();
loadContacts();
