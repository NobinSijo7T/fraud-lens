/**
 * Simplified Transaction Fraud Analysis
 * Uses pre-defined transaction scenarios since V1-V28 cannot be calculated from raw data
 */

(async()=>{
  const taskSelect=document.querySelector('#task');
  const simpleSection=document.querySelector('#simple-transaction-section');
  const advancedSection=document.querySelector('#advanced-section');
  const urlSection=document.querySelector('#url-input-section');
  const resultDiv=document.querySelector('#result');
  const msgDiv=document.querySelector('#form-message');
  
  // Transaction scenarios with real-world context + actual V1-V28 values
  const scenarios = {
    small_purchase: {
      name: "Small Online Purchase ($25)",
      description: "Legitimate small amount, regular merchant, domestic",
      realWorld: {amount: 25, merchant: "Amazon", type: "Online", country: "Domestic"},
      features: {Time:0,V1:-1.36,V2:-0.07,V3:2.54,V4:1.38,V5:-0.34,V6:0.46,V7:0.24,V8:0.10,V9:0.36,V10:0.09,V11:-0.55,V12:-0.62,V13:-0.99,V14:-0.31,V15:1.47,V16:-0.47,V17:0.21,V18:0.03,V19:0.40,V20:0.25,V21:-0.02,V22:0.28,V23:-0.11,V24:0.07,V25:0.13,V26:-0.19,V27:0.13,V28:-0.02,Amount:25}
    },
    large_purchase: {
      name: "Large Purchase ($500)",
      description: "Legitimate large amount, established merchant",
      realWorld: {amount: 500, merchant: "Best Buy", type: "In-Store", country: "Domestic"},
      features: {Time:100,V1:-0.85,V2:0.12,V3:1.95,V4:0.92,V5:-0.18,V6:0.35,V7:0.15,V8:0.08,V9:0.28,V10:0.12,V11:-0.42,V12:-0.48,V13:-0.76,V14:-0.24,V15:1.12,V16:-0.36,V17:0.16,V18:0.02,V19:0.31,V20:0.19,V21:-0.01,V22:0.22,V23:-0.08,V24:0.05,V25:0.10,V26:-0.15,V27:0.10,V28:-0.02,Amount:500}
    },
    subscription: {
      name: "Monthly Subscription ($15)",
      description: "Recurring payment, familiar pattern",
      realWorld: {amount: 15, merchant: "Netflix", type: "Subscription", country: "Domestic"},
      features: {Time:2000,V1:-0.52,V2:0.05,V3:1.25,V4:0.48,V5:-0.09,V6:0.18,V7:0.08,V8:0.04,V9:0.14,V10:0.06,V11:-0.22,V12:-0.25,V13:-0.39,V14:-0.12,V15:0.58,V16:-0.19,V17:0.08,V18:0.01,V19:0.16,V20:0.10,V21:-0.01,V22:0.11,V23:-0.04,V24:0.03,V25:0.05,V26:-0.08,V27:0.05,V28:-0.01,Amount:15}
    },
    suspicious_small: {
      name: "🚨 Suspicious: Unusual Small Amount ($0.50)",
      description: "Testing transaction, common fraud pattern",
      realWorld: {amount: 0.50, merchant: "Unknown Merchant", type: "Online", country: "Foreign"},
      features: {Time:350,V1:-2.15,V2:1.85,V3:-1.45,V4:3.67,V5:-0.48,V6:-1.32,V7:-2.34,V8:1.28,V9:-2.56,V10:-2.56,V11:2.95,V12:-2.67,V13:-0.55,V14:-3.96,V15:0.36,V16:-1.05,V17:-2.61,V18:-0.02,V19:0.38,V20:0.12,V21:-0.01,V22:0.48,V23:-0.03,V24:-0.43,V25:0.30,V26:-0.13,V27:-0.05,V28:-0.06,Amount:0.50}
    },
    suspicious_rapid: {
      name: "🚨 Suspicious: Rapid Multiple Transactions",
      description: "Multiple transactions in short time, unusual pattern",
      realWorld: {amount: 0.77, merchant: "Random Store", type: "Online", country: "Foreign"},
      features: {Time:406,V1:-2.31,V2:1.95,V3:-1.61,V4:4.00,V5:-0.52,V6:-1.43,V7:-2.54,V8:1.39,V9:-2.77,V10:-2.77,V11:3.20,V12:-2.90,V13:-0.60,V14:-4.29,V15:0.39,V16:-1.14,V17:-2.83,V18:-0.02,V19:0.42,V20:0.13,V21:-0.01,V22:0.52,V23:-0.04,V24:-0.47,V25:0.32,V26:-0.14,V27:-0.06,V28:-0.06,Amount:0.77}
    },
    high_value_fraud: {
      name: "🚨 Suspicious: High Value Foreign Transaction",
      description: "Large amount, foreign location, unusual time",
      realWorld: {amount: 1200, merchant: "Unknown", type: "Online", country: "Foreign"},
      features: {Time:450,V1:-3.12,V2:2.45,V3:-2.01,V4:4.85,V5:-0.65,V6:-1.78,V7:-3.12,V8:1.67,V9:-3.22,V10:-3.15,V11:3.89,V12:-3.34,V13:-0.72,V14:-5.12,V15:0.48,V16:-1.35,V17:-3.25,V18:-0.03,V19:0.52,V20:0.16,V21:-0.01,V22:0.65,V23:-0.05,V24:-0.58,V25:0.39,V26:-0.17,V27:-0.07,V28:-0.07,Amount:1200}
    }
  };
  
  function renderSimpleTransactionForm() {
    simpleSection.innerHTML = `
      <div style="background:#1a1a1a;border:1px solid #333;border-radius:12px;padding:2rem;margin-bottom:2rem;">
        <h3 style="color:#667eea;margin:0 0 1rem 0;">💳 Select Transaction Scenario</h3>
        <p style="color:#999;margin:0 0 1.5rem 0;font-size:0.9rem;">Choose a realistic transaction scenario below. Each scenario includes real-world context and actual model features.</p>
        
        <div style="display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));">
          ${Object.keys(scenarios).map(key => {
            const s = scenarios[key];
            const isSuspicious = s.name.includes('🚨');
            return `
              <div class="scenario-card" data-scenario="${key}" style="background:${isSuspicious?'#2a1a1a':'#2a2a2a'};border:2px solid ${isSuspicious?'#ff4444':'#444'};border-radius:8px;padding:1.25rem;cursor:pointer;transition:all 0.2s;" onmouseover="this.style.borderColor='${isSuspicious?'#ff6666':'#667eea'}';this.style.transform='scale(1.02)'" onmouseout="this.style.borderColor='${isSuspicious?'#ff4444':'#444'}';this.style.transform='scale(1)'">
                <h4 style="color:${isSuspicious?'#ff6666':'#fff'};margin:0 0 0.5rem 0;font-size:1rem;">${s.name}</h4>
                <p style="color:#999;font-size:0.85rem;margin:0 0 0.75rem 0;">${s.description}</p>
                <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.75rem;">
                  <span style="background:#333;padding:0.25rem 0.5rem;border-radius:4px;font-size:0.75rem;color:#14B8A6;">$${s.realWorld.amount}</span>
                  <span style="background:#333;padding:0.25rem 0.5rem;border-radius:4px;font-size:0.75rem;color:#888;">${s.realWorld.type}</span>
                  <span style="background:#333;padding:0.25rem 0.5rem;border-radius:4px;font-size:0.75rem;color:#888;">${s.realWorld.country}</span>
                </div>
                <button type="button" class="analyze-scenario-btn" data-scenario="${key}" style="width:100%;padding:0.75rem;background:#667eea;color:white;border:none;border-radius:6px;font-weight:600;cursor:pointer;">Analyze This Scenario →</button>
              </div>
            `;
          }).join('')}
        </div>
        
        <details style="margin-top:2rem;padding:1rem;background:#2a2a2a;border-radius:8px;">
          <summary style="cursor:pointer;color:#667eea;font-weight:600;">⚙️ Advanced: Enter V1-V28 Features Manually</summary>
          <p style="color:#999;margin:0.75rem 0;font-size:0.85rem;">If you have actual PCA-transformed features (V1-V28), you can enter them manually below.</p>
          <button type="button" id="show-advanced-btn" style="padding:0.5rem 1rem;background:#444;color:white;border:none;border-radius:6px;cursor:pointer;">Show Manual Input Form</button>
        </details>
      </div>
    `;
    
    // Add click handlers
    document.querySelectorAll('.analyze-scenario-btn').forEach(btn => {
      btn.onclick = async () => {
        const scenario = scenarios[btn.dataset.scenario];
        await analyzeTransaction(scenario.features, scenario.name, scenario.realWorld);
      };
    });
    
    document.querySelector('#show-advanced-btn').onclick = () => {
      simpleSection.classList.add('hidden');
      advancedSection.classList.remove('hidden');
      renderAdvancedForm();
    };
  }
  
  function renderAdvancedForm() {
    const fields = document.querySelector('#fields');
    fields.innerHTML = '';
    
    const hint = document.createElement('div');
    hint.style.cssText = 'margin:0 0 1.5rem 0;padding:1rem;background:#2a2a2a;border:1px solid #444;border-radius:8px;';
    hint.innerHTML = `
      <p style="color:#999;margin:0 0 0.5rem 0;">Enter all 30 PCA-transformed features manually.</p>
      <button type="button" id="back-to-simple-btn" style="padding:0.5rem 1rem;background:#444;color:white;border:none;border-radius:6px;cursor:pointer;font-size:0.85rem;">← Back to Simple Mode</button>
    `;
    fields.appendChild(hint);
    
    setTimeout(() => {
      document.querySelector('#back-to-simple-btn').onclick = () => {
        advancedSection.classList.add('hidden');
        simpleSection.classList.remove('hidden');
      };
    }, 100);
    
    const featureNames = ['Time',...Array.from({length:28},(_,i)=>`V${i+1}`),'Amount'];
    featureNames.forEach(name => {
      const label = document.createElement('label');
      label.textContent = name;
      label.style.cssText = 'display:block;margin-bottom:1rem;color:#ccc;';
      
      const input = document.createElement('input');
      input.name = name;
      input.type = 'number';
      input.step = 'any';
      input.required = true;
      input.placeholder = '0';
      input.style.cssText = 'width:100%;padding:0.75rem;background:#2a2a2a;border:1px solid #444;border-radius:6px;color:#fff;font-size:0.95rem;';
      
      label.appendChild(input);
      fields.appendChild(label);
    });
  }
  
  async function analyzeTransaction(features, scenarioName, realWorld) {
    resultDiv.innerHTML = '<p style="color:#999;">Analyzing...</p>';
    resultDiv.classList.remove('hidden');
    
    try {
      const result = await predictTransaction(features);
      const isHighRisk = result.risk_level === 'High';
      const riskColor = isHighRisk ? '#F56565' : result.risk_level === 'Medium' ? '#F59E0B' : '#14B8A6';
      
      resultDiv.innerHTML = `
        <div style="background:#1a1a1a;border-radius:12px;padding:2rem;box-shadow:0 4px 6px rgba(0,0,0,0.3);border:1px solid #333;margin-top:2rem;">
          <p class="eyebrow">FRAUD ASSESSMENT</p>
          <h2 style="color:${riskColor};margin:1rem 0;font-size:2rem;">${esc(result.prediction)}</h2>
          
          ${realWorld ? `
            <div style="background:#2a2a2a;padding:1rem;border-radius:8px;margin-bottom:1.5rem;">
              <h4 style="color:#999;margin:0 0 0.5rem 0;font-size:0.85rem;">SCENARIO ANALYZED</h4>
              <p style="color:#fff;margin:0;font-size:1.1rem;">${esc(scenarioName)}</p>
              <div style="display:flex;gap:1rem;margin-top:0.75rem;flex-wrap:wrap;">
                <span style="color:#14B8A6;">Amount: $${realWorld.amount}</span>
                <span style="color:#888;">Type: ${realWorld.type}</span>
                <span style="color:#888;">Location: ${realWorld.country}</span>
              </div>
            </div>
          ` : ''}
          
          <div style="display:flex;gap:1rem;margin:1.5rem 0;flex-wrap:wrap;">
            <div style="flex:1;min-width:200px;padding:1rem;background:${riskColor}15;border-left:3px solid ${riskColor};border-radius:6px;">
              <div style="font-size:0.85rem;color:#999;margin-bottom:0.25rem;">Risk Level</div>
              <div style="font-size:1.5rem;font-weight:700;color:${riskColor};">${esc(result.risk_level)}</div>
            </div>
            <div style="flex:1;min-width:200px;padding:1rem;background:#2a2a2a;border-radius:6px;">
              <div style="font-size:0.85rem;color:#999;margin-bottom:0.25rem;">Probability</div>
              <div style="font-size:1.5rem;font-weight:700;color:#fff;">${result.fraud_probability ? pct(result.fraud_probability) : 'N/A'}</div>
            </div>
            <div style="flex:1;min-width:200px;padding:1rem;background:#2a2a2a;border-radius:6px;">
              <div style="font-size:0.85rem;color:#999;margin-bottom:0.25rem;">Model</div>
              <div style="font-size:0.9rem;font-weight:600;color:#fff;">${esc(result.model_version || 'N/A')}</div>
            </div>
          </div>
          
          ${result.disclaimer ? `
            <div style="padding:1rem;background:#3a2f0f;border:1px solid #6a5f1f;border-radius:6px;font-size:0.85rem;color:#ffd666;">
              <strong>⚠️ Important:</strong> ${esc(result.disclaimer)}
            </div>
          ` : ''}
          
          <div style="margin-top:1.5rem;text-align:center;">
            <button type="button" id="analyze-another-btn" style="padding:0.75rem 2rem;background:#667eea;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;font-size:0.95rem;">Analyze Another Scenario</button>
          </div>
        </div>
      `;
      
      setTimeout(() => {
        document.querySelector('#analyze-another-btn').onclick = () => {
          resultDiv.classList.add('hidden');
          window.scrollTo({top: 0, behavior: 'smooth'});
        };
      }, 100);
      
    } catch (err) {
      resultDiv.innerHTML = `
        <div style="background:#3a1a1a;border:1px solid #5a2a2a;border-radius:8px;padding:1.5rem;color:#ff6b6b;">
          <h3 style="margin:0 0 0.5rem 0;">❌ Error</h3>
          <p style="margin:0;">${esc(err.message)}</p>
          <button type="button" onclick="document.querySelector('#result').classList.add('hidden');" style="margin-top:1rem;padding:0.5rem 1rem;background:#C33;color:white;border:none;border-radius:6px;cursor:pointer;">Close</button>
        </div>
      `;
    }
  }
  
  // Handle task switching
  taskSelect.addEventListener('change', () => {
    const task = taskSelect.value;
    if (task === 'fraud') {
      simpleSection.classList.remove('hidden');
      advancedSection.classList.add('hidden');
      urlSection.classList.add('hidden');
      renderSimpleTransactionForm();
    } else if (task === 'phishing') {
      simpleSection.classList.add('hidden');
      advancedSection.classList.add('hidden');
      urlSection.classList.remove('hidden');
    }
  });
  
  // Handle advanced form submission
  document.querySelector('#transaction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(e.target));
    Object.keys(payload).forEach(k => payload[k] = Number(payload[k]));
    await analyzeTransaction(payload, null, null);
  });
  
  // Initial render
  if (taskSelect.value === 'fraud') {
    renderSimpleTransactionForm();
  }
  
  // URL extraction (phishing) - keeping existing functionality
  const extractBtn = document.querySelector('#extract-features-btn');
  const urlInput = document.querySelector('#url-input');
  
  if (extractBtn) {
    extractBtn.addEventListener('click', async () => {
      const url = urlInput.value.trim();
      if (!url) {alert('Please enter a URL'); return}
      try {
        extractBtn.disabled = true;
        extractBtn.textContent = 'Extracting...';
        
        const result = await analyzeURL(url);
        
        // Show result immediately on the same page
        resultDiv.innerHTML = `
          <div style="background:#1a1a1a;border-radius:12px;padding:2rem;box-shadow:0 4px 6px rgba(0,0,0,0.3);border:1px solid #333;margin-top:2rem;">
            <p class="eyebrow">PHISHING ASSESSMENT</p>
            <h2 style="color:${result.risk_level==='High'?'#F56565':'#14B8A6'};margin:1rem 0;font-size:2rem;">${esc(result.prediction)}</h2>
            
            <div style="background:#2a2a2a;padding:1rem;border-radius:8px;margin-bottom:1.5rem;">
              <h4 style="color:#999;margin:0 0 0.5rem 0;font-size:0.85rem;">URL ANALYZED</h4>
              <p style="color:#fff;margin:0;font-size:0.9rem;word-break:break-all;">${esc(result.url)}</p>
            </div>
            
            <div style="display:flex;gap:1rem;margin:1.5rem 0;flex-wrap:wrap;">
              <div style="flex:1;min-width:200px;padding:1rem;background:${result.risk_level==='High'?'#F5656515':'#14B8A615'};border-left:3px solid ${result.risk_level==='High'?'#F56565':'#14B8A6'};border-radius:6px;">
                <div style="font-size:0.85rem;color:#999;margin-bottom:0.25rem;">Risk Level</div>
                <div style="font-size:1.5rem;font-weight:700;color:${result.risk_level==='High'?'#F56565':'#14B8A6'};">${esc(result.risk_level)}</div>
              </div>
              <div style="flex:1;min-width:200px;padding:1rem;background:#2a2a2a;border-radius:6px;">
                <div style="font-size:0.85rem;color:#999;margin-bottom:0.25rem;">Probability</div>
                <div style="font-size:1.5rem;font-weight:700;color:#fff;">${result.fraud_probability ? pct(result.fraud_probability) : 'N/A'}</div>
              </div>
            </div>
            
            <div style="margin-top:1.5rem;text-align:center;">
              <button type="button" onclick="document.querySelector('#result').classList.add('hidden');document.querySelector('#url-input').value='';" style="padding:0.75rem 2rem;background:#667eea;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;font-size:0.95rem;">Analyze Another URL</button>
            </div>
          </div>
        `;
        resultDiv.classList.remove('hidden');
        
        extractBtn.disabled = false;
        extractBtn.textContent = 'Extract Features';
      } catch (e) {
        msgDiv.textContent = '❌ ' + e.message;
        msgDiv.style.cssText = 'color:#F56565;';
        msgDiv.classList.remove('hidden');
        extractBtn.disabled = false;
        extractBtn.textContent = 'Extract Features';
      }
    });
  }
})();
