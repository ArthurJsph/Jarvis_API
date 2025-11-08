(() => {
  const apiKeyInput = document.getElementById('api_key');
  const toggleBtn = document.getElementById('toggle_key');
  const saveBtn = document.getElementById('save_key');
  const clearKeyBtn = document.getElementById('clear_key');
  // task UI elements
  const btnListRoot = document.getElementById('btn_list_root');
  const btnListPath = document.getElementById('btn_list_path');
  const listPathEl = document.getElementById('list_path');
  const btnRead = document.getElementById('btn_read');
  const readPathEl = document.getElementById('read_path');
  const btnDelete = document.getElementById('btn_delete');
  const deletePathEl = document.getElementById('delete_path');
  const btnExecListRoot = document.getElementById('btn_exec_list_root');
  const btnExecCustom = document.getElementById('btn_exec_custom');
  const btnWrite = document.getElementById('btn_write');
  const writePathEl = document.getElementById('write_path');
  const writeContentEl = document.getElementById('write_content');
  const overwriteEl = document.getElementById('overwrite');
  const resEl = document.getElementById('result');

  // load saved key
  const SAVED_KEY = 'jarvis_api_key_v1';
  const saved = localStorage.getItem(SAVED_KEY);
  if (saved) apiKeyInput.value = saved;

  const authIndicator = document.getElementById('auth_indicator');
  const authText = document.getElementById('auth_text');
  const fetchLogsBtn = document.getElementById('fetch_logs');
  const logsEl = document.getElementById('logs');
  const logLinesEl = document.getElementById('log_lines');

  toggleBtn.addEventListener('click', () => {
    if (apiKeyInput.type === 'password') {
      apiKeyInput.type = 'text';
      toggleBtn.textContent = 'Ocultar';
    } else {
      apiKeyInput.type = 'password';
      toggleBtn.textContent = 'Mostrar';
    }
  });

  saveBtn.addEventListener('click', () => {
    if (apiKeyInput.value) {
      localStorage.setItem(SAVED_KEY, apiKeyInput.value);
      saveBtn.textContent = 'Salvo';
      setTimeout(() => (saveBtn.textContent = 'Salvar'), 1500);
      checkAuth();
      showToast('Chave salva localmente', 'success');
    }
  });

  if (clearKeyBtn) {
    clearKeyBtn.addEventListener('click', () => {
      localStorage.removeItem(SAVED_KEY);
      apiKeyInput.value = '';
      setAuthStatus(null);
    });
  }

  function setResult(text) {
    const resEl = document.getElementById('result');
    if (!resEl) return;
    // allow structured results: {text, type}
    if (typeof text === 'object' && text !== null) {
      resEl.innerHTML = '<div class="' + (text.type === 'error' ? 'result-error' : (text.type === 'success' ? 'result-success' : 'result-info')) + '">' + escapeHtml(String(text.text)) + '</div>';
    } else {
      resEl.textContent = String(text);
    }
  }

  // Toast implementation (floating messages)
  function getToastContainer() {
    let c = document.querySelector('.toast-container');
    if (!c) {
      c = document.createElement('div');
      c.className = 'toast-container';
      document.body.appendChild(c);
    }
    return c;
  }

  function showToast(msg, type = 'info', timeout = 4000) {
    try {
      const container = getToastContainer();
      const t = document.createElement('div');
      t.className = 'toast ' + (type === 'error' ? 'toast-error' : (type === 'success' ? 'toast-success' : 'toast-info'));
      t.textContent = msg;
      container.appendChild(t);
      setTimeout(() => { t.style.opacity = '1'; }, 10);
      setTimeout(() => { t.style.opacity = '0'; t.addEventListener('transitionend', () => t.remove()); }, timeout);
    } catch (e) {
      console.error('Toast error', e);
    }
  }

  function escapeHtml(s) {
    return s.replace(/[&<>\"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":"&#39;"}[c]; });
  }

  function setButtonLoading(btn, loading) {
    if (!btn) return;
    if (loading) {
      btn.disabled = true;
      if (!btn.querySelector('.spinner')) {
        const sp = document.createElement('span'); sp.className = 'spinner'; btn.appendChild(sp);
      }
    } else {
      btn.disabled = false;
      const sp = btn.querySelector('.spinner'); if (sp) sp.remove();
    }
  }

  // Note: legacy chat/LLM UI removed; this page uses task-based buttons that call file/execute endpoints.

  async function setAuthStatus(status) {
    if (status === true) {
      authIndicator.classList.remove('auth-unknown','auth-no');
      authIndicator.classList.add('auth-yes');
      authText.textContent = 'Autenticado';
    } else if (status === false) {
      authIndicator.classList.remove('auth-unknown','auth-yes');
      authIndicator.classList.add('auth-no');
      authText.textContent = 'Não autenticado';
    } else {
      authIndicator.classList.remove('auth-yes','auth-no');
      authIndicator.classList.add('auth-unknown');
      authText.textContent = 'Não verificado';
    }
  }

  async function checkAuth() {
    const key = apiKeyInput.value;
    if (!key) { setAuthStatus(false); return; }
    try {
      const res = await fetch('/health', { headers: { 'x-api-key': key } });
      if (res.ok) { setAuthStatus(true); } else { setAuthStatus(false); }
    } catch (e) {
      setAuthStatus(false);
    }
  }

  // initial auth check if saved
  if (saved) checkAuth();

  // detect server capabilities and enable/disable UI accordingly
  async function detectCapabilities() {
    const key = apiKeyInput.value || saved;
    // disable all actionable buttons by default
    const allButtons = [btnListRoot, btnListPath, btnRead, btnDelete, btnWrite, btnExecListRoot, btnExecCustom, fetchLogsBtn];
    allButtons.forEach(b => { if (b) b.disabled = true; });

    if (!key) {
      showToast('Forneça a API key (salve para reaproveitar) para habilitar ações', 'info');
      return;
    }
    try {
      const res = await fetch('/capabilities', { headers: { 'x-api-key': key } });
      if (!res.ok) {
        showToast('Não foi possível ler capacidades (verifique a API key)', 'error');
        return;
      }
      const caps = await res.json();
      showToast('Capacidades carregadas', 'success');
      if (caps.files) {
        if (btnListRoot) btnListRoot.disabled = false;
        if (btnListPath) btnListPath.disabled = false;
        if (btnRead) btnRead.disabled = false;
        if (btnDelete) btnDelete.disabled = false;
        if (btnWrite) btnWrite.disabled = false;
      }
      if (caps.execute) {
        if (btnExecListRoot) btnExecListRoot.disabled = false;
        if (btnExecCustom) btnExecCustom.disabled = false;
      }
      if (caps.logs) {
        if (fetchLogsBtn) fetchLogsBtn.disabled = false;
      }
    } catch (e) {
      showToast('Erro ao detectar capacidades: ' + e, 'error');
    }
  }

  // run detection on load
  detectCapabilities();

  // allow opening /ui/authed?api_key=... to prefill key server-side (the server must verify the key)
  // If the page is loaded with ?prefill_key=..., the server can inject the key into localStorage.
  // Nothing to do here in JS; server-side injection will set localStorage before this script runs.

  // Fetch logs
  if (fetchLogsBtn) {
    fetchLogsBtn.addEventListener('click', async () => {
      const lines = logLinesEl.value || '200';
      const key = apiKeyInput.value;
      if (!key) { alert('Please provide API key'); return; }
      setButtonLoading(fetchLogsBtn, true);
      logsEl.textContent = '...fetching logs';
      try {
        const res = await fetch(`/logs?lines=${encodeURIComponent(lines)}`, { headers: { 'x-api-key': key } });
        if (!res.ok) {
          const err = await res.json().catch(() => null);
          logsEl.textContent = 'Error: ' + (err?.detail || res.statusText || res.status);
          setButtonLoading(fetchLogsBtn, false);
          return;
        }
        const text = await res.text();
        logsEl.textContent = text || '(no logs)';
      } catch (err) {
        logsEl.textContent = 'Error: ' + err;
      } finally {
        setButtonLoading(fetchLogsBtn, false);
      }
    });
  }

    // Quick task handlers
    async function apiFetch(path, opts = {}) {
      const key = apiKeyInput.value;
  if (!key) { alert('Forneça a API key'); return null; }
      try {
        const url = path + (opts.query ? ('?' + new URLSearchParams(opts.query)) : '');
        const res = await fetch(url, { headers: { 'x-api-key': key } });
        if (!res.ok) {
          const err = await res.json().catch(() => null);
          setResult({ text: 'Erro: ' + (err?.detail || res.statusText || res.status), type: 'error' });
          return null;
        }
        return await res.json();
      } catch (e) {
        setResult('Error: ' + e);
        return null;
      }
    }

    if (btnListRoot) btnListRoot.addEventListener('click', async () => {
      setResult('Listando raiz...');
      setButtonLoading(btnListRoot, true);
      try {
        const r = await apiFetch('/files/list', { query: { path: '' } });
        if (r) setResult(JSON.stringify(r, null, 2));
      } catch (e) {
        setResult({ text: 'Error: ' + e, type: 'error' });
      } finally {
        setButtonLoading(btnListRoot, false);
      }
    });

    if (btnListPath) btnListPath.addEventListener('click', async () => {
      const p = listPathEl.value || '';
      setResult('Listando ' + p + ' ...');
      setButtonLoading(btnListPath, true);
      try {
        const r = await apiFetch('/files/list', { query: { path: p } });
        if (r) setResult(JSON.stringify(r, null, 2));
      } catch (e) {
        setResult({ text: 'Error: ' + e, type: 'error' });
      } finally {
        setButtonLoading(btnListPath, false);
      }
    });

    if (btnRead) btnRead.addEventListener('click', async () => {
      const p = readPathEl.value;
      if (!p) return alert('Forneça um caminho');
      setResult('Lendo ' + p + ' ...');
      setButtonLoading(btnRead, true);
      try {
        const r = await apiFetch('/files/read', { query: { path: p } });
        if (r) setResult(r.content || JSON.stringify(r, null, 2));
      } catch (e) {
        setResult({ text: 'Error: ' + e, type: 'error' });
      } finally {
        setButtonLoading(btnRead, false);
      }
    });

    if (btnDelete) btnDelete.addEventListener('click', async () => {
      const p = deletePathEl.value;
      if (!p) return alert('Forneça um caminho');
      if (!confirm('Excluir ' + p + '?')) return;
      setResult('Excluindo ' + p + ' ...');
      setButtonLoading(btnDelete, true);
      try {
        const key = apiKeyInput.value;
        const res = await fetch('/files/delete', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': key }, body: JSON.stringify({ path: p }) });
        const body = await res.json();
        setResult(JSON.stringify(body, null, 2));
      } catch (e) { setResult({ text: 'Error: ' + e, type: 'error' }); }
      finally { setButtonLoading(btnDelete, false); }
    });

    if (btnWrite) btnWrite.addEventListener('click', async () => {
      const p = writePathEl.value;
      const content = writeContentEl.value || '';
      const overwrite = !!overwriteEl.checked;
      if (!p) return alert('Forneça um caminho');
      setResult('Gravando ' + p + ' ...');
      setButtonLoading(btnWrite, true);
      try {
        const key = apiKeyInput.value;
        const res = await fetch('/files/write', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': key }, body: JSON.stringify({ path: p, content, overwrite }) });
        const body = await res.json();
        setResult(JSON.stringify(body, null, 2));
      } catch (e) { setResult({ text: 'Error: ' + e, type: 'error' }); }
      finally { setButtonLoading(btnWrite, false); }
    });

    if (btnExecListRoot) btnExecListRoot.addEventListener('click', async () => {
      setResult('Executando list_root...');
      setButtonLoading(btnExecListRoot, true);
      try {
        const key = apiKeyInput.value;
        const res = await fetch('/execute', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': key }, body: JSON.stringify({ command: 'list_root' }) });
        const body = await res.json();
        setResult(JSON.stringify(body, null, 2));
      } catch (e) { setResult({ text: 'Error: ' + e, type: 'error' }); }
      finally { setButtonLoading(btnExecListRoot, false); }
    });

    if (btnExecCustom) btnExecCustom.addEventListener('click', async () => {
      const cmd = prompt('Insira o token do comando (ex: list_root)');
      if (!cmd) return;
      setResult('Executando ' + cmd + '...');
      setButtonLoading(btnExecCustom, true);
      try {
        const key = apiKeyInput.value;
        const res = await fetch('/execute', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': key }, body: JSON.stringify({ command: cmd }) });
        const body = await res.json();
        setResult(JSON.stringify(body, null, 2));
      } catch (e) { setResult({ text: 'Error: ' + e, type: 'error' }); }
      finally { setButtonLoading(btnExecCustom, false); }
    });
})();
