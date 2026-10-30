(async () => {
  try {
    const [d, h] = await Promise.all([getDashboardData(), getHealth()]);
    const healthEl = document.querySelector('#health');
    if (healthEl) healthEl.textContent = '● API online';

    const heroModel = document.querySelector('#hero-model');
    if (heroModel) heroModel.textContent = d.selected_model || 'Awaiting training';

    const s = d.dataset || {};
    const setElemText = (selector, text) => {
      const el = document.querySelector(selector);
      if (el) el.textContent = text;
    };

    setElemText('#records', fmt(s.row_count || 0));
    setElemText('#dataset-name', s.dataset_filename || 'No dataset');

    const dist = s.target_class_distribution || {};
    setElemText('#legit', fmt(dist['0'] || 0));
    setElemText('#fraud', fmt(dist['1'] || 0));
    setElemText('#recall', pct(d.evaluation?.recall));
    setElemText('#model-label', d.selected_model || 'Train a model');

    const distCanvas = document.querySelector('#distribution');
    if (distCanvas && typeof Chart !== 'undefined') {
      new Chart(distCanvas, {
        type: 'doughnut',
        data: {
          labels: ['Legitimate', 'Fraud'],
          datasets: [{
            data: [dist['0'] || 0, dist['1'] || 0],
            backgroundColor: ['#14b8a6', '#f56565'],
            borderWidth: 0
          }]
        },
        options: {
          plugins: { legend: { position: 'bottom' } },
          cutout: '70%'
        }
      });
    }

    const box = document.querySelector('#recent');
    if (box) {
      box.textContent = '';
      (d.recent_predictions || []).forEach(x => {
        const row = document.createElement('div');
        row.className = 'activity-row';
        row.innerHTML = `<span><strong>${esc(x.prediction)}</strong><br><small class="muted">${esc(x.risk_level)} risk</small></span><small class="muted">${new Date(x.created_at).toLocaleString()}</small>`;
        box.appendChild(row);
      });
      if (!d.recent_predictions?.length) {
        box.innerHTML = '<p class="muted">No predictions yet. Analyze a transaction to begin.</p>';
      }
    }
  } catch (e) {
    const healthEl = document.querySelector('#health');
    if (healthEl) healthEl.textContent = '● API unavailable';
    const msgEl = document.querySelector('#message');
    if (msgEl) {
      msgEl.textContent = e.message;
      msgEl.classList.remove('hidden');
    }
  }
})();
