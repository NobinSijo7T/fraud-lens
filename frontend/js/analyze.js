(() => {
  const form = document.querySelector('#url-form');
  const input = document.querySelector('#url-input');
  const button = document.querySelector('#analyze-url-btn');
  const taskSelect = document.querySelector('#task');
  const urlSection = document.querySelector('#url-input-section');
  const transactionForm = document.querySelector('#transaction-form');
  const fields = document.querySelector('#fields');
  const result = document.querySelector('#result');

  const fraudFallback = ['Time', ...Array.from({ length: 28 }, (_, i) => `V${i + 1}`), 'Amount'];
  const friendlyLabels = {
    type: 'Transaction type',
    amount: 'Transaction amount',
    oldbalanceOrg: 'Sender balance before transaction',
    newbalanceOrig: 'Sender balance after transaction',
    oldbalanceDest: 'Receiver balance before transaction',
    newbalanceDest: 'Receiver balance after transaction',
  };

  function renderResult(data) {
    const isPhishing = data.task === 'phishing';
    const riskColor = data.risk_level === 'High' ? 'var(--color-alarm-red)' : data.risk_level === 'Medium' ? '#b7791f' : 'var(--color-spruce)';
    const probability = data.fraud_probability == null ? 'N/A' : pct(data.fraud_probability);
    result.innerHTML = `
      <div class="result-head">
        <div>
          <p class="eyebrow">${isPhishing ? 'PHISHING ASSESSMENT' : 'TRANSACTION ASSESSMENT'}</p>
          <h2 style="color:${riskColor}">${esc(data.prediction)}</h2>
        </div>
        <span class="risk-badge" style="color:${riskColor};border-color:${riskColor}">${esc(data.risk_level)} risk</span>
      </div>
      ${isPhishing ? `<p class="analyzed-url">${esc(data.url || input.value.trim())}</p>` : ''}
      <div class="result-stats">
        <div><span>Risk level</span><strong style="color:${riskColor}">${esc(data.risk_level)}</strong></div>
        <div><span>Probability</span><strong>${probability}</strong></div>
        <div><span>Model</span><strong>${esc(data.model_version || 'N/A')}</strong></div>
      </div>
      ${data.disclaimer ? `<p class="result-note">${esc(data.disclaimer)}</p>` : ''}
      ${data.contributing_factors?.length ? `<p class="result-note"><strong>Signals:</strong> ${data.contributing_factors.map(esc).join(', ')}</p>` : ''}
      <button type="button" class="button-outlined" id="analyze-another">Analyze another ${isPhishing ? 'URL' : 'transaction'}</button>
    `;
    result.classList.remove('hidden');
    result.querySelector('#analyze-another').onclick = () => {
      result.classList.add('hidden');
      if (isPhishing) { input.value = ''; input.focus(); }
      else { transactionForm.reset(); transactionForm.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    };
  }

  async function renderTransactionFields() {
    fields.innerHTML = '';
    let names = fraudFallback;
    try {
      const model = await getModelFeatures('fraud');
      if (model.features?.length) names = model.features;
    } catch (_) { /* Keep the known model schema as a fallback. */ }
    names.forEach(name => {
      const field = typeof name === 'object' ? name.name : name;
      const label = document.createElement('label');
      label.textContent = friendlyLabels[field] || field;
      const input = field === 'type' ? document.createElement('select') : document.createElement('input');
      input.name = field;
      if (field === 'type') {
        ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'].forEach(value => {
          const option = document.createElement('option'); option.value = value; option.textContent = value; input.appendChild(option);
        });
      } else {
        input.type = 'number'; input.step = 'any'; input.required = true; input.placeholder = '0';
      }
      label.appendChild(input);
      fields.appendChild(label);
    });
  }

  async function switchTask() {
    const phishing = taskSelect.value === 'phishing';
    urlSection.classList.toggle('hidden', !phishing);
    transactionForm.classList.toggle('hidden', phishing);
    result.classList.add('hidden');
    if (!phishing) await renderTransactionFields();
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    const url = input.value.trim();
    if (!url) return;
    button.disabled = true;
    button.innerHTML = 'Analyzing…';
    result.classList.remove('hidden');
    result.textContent = 'Analyzing URL…';
    try {
      renderResult(await analyzeURL(url));
    } catch (error) {
      result.innerHTML = `<div class="result-error"><h3>We couldn’t analyze that URL</h3><p>${esc(error.message)}</p></div>`;
    } finally {
      button.disabled = false;
      button.innerHTML = 'Analyze URL <span>→</span>';
    }
  });

  transactionForm.addEventListener('submit', async event => {
    event.preventDefault();
    const submit = transactionForm.querySelector('button[type="submit"]');
    const payload = Object.fromEntries(new FormData(transactionForm));
    Object.keys(payload).forEach(key => payload[key] = Number(payload[key]));
    submit.disabled = true;
    submit.textContent = 'Analyzing…';
    result.classList.remove('hidden');
    result.textContent = 'Analyzing transaction…';
    try { renderResult(await predictTransaction(payload)); }
    catch (error) { result.innerHTML = `<div class="result-error"><h3>Analysis failed</h3><p>${esc(error.message)}</p></div>`; }
    finally { submit.disabled = false; submit.innerHTML = 'Run risk assessment <span>→</span>'; }
  });

  taskSelect.addEventListener('change', switchTask);
  if (new URLSearchParams(window.location.search).get('task') === 'phishing') taskSelect.value = 'phishing';
  switchTask();
})();
