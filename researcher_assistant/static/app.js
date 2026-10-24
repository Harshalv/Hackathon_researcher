// Researcher Assistant Frontend Application
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons
  lucide.createIcons();

  // Elements
  const claimForm = document.getElementById('claimForm');
  const claimInput = document.getElementById('claimInput');
  const submitBtn = document.getElementById('submitBtn');
  const charCount = document.getElementById('charCount');
  const samplePillsContainer = document.getElementById('samplePillsContainer');

  const pipelineSection = document.getElementById('pipelineSection');
  const pipelineStatusBadge = document.getElementById('pipelineStatusBadge');
  const liveLogConsole = document.getElementById('liveLogConsole');

  const resultsSection = document.getElementById('resultsSection');
  const decisionCard = document.getElementById('decisionCard');
  const decisionBadge = document.getElementById('decisionBadge');
  const confidencePill = document.getElementById('confidencePill');
  const evaluatedClaimTitle = document.getElementById('evaluatedClaimTitle');
  const compoundIdLabel = document.getElementById('compoundIdLabel');
  const sourcesCountMetric = document.getElementById('sourcesCountMetric');
  const precedentsCountMetric = document.getElementById('precedentsCountMetric');

  const explanationContent = document.getElementById('explanationContent');
  const precedentCalloutBox = document.getElementById('precedentCalloutBox');
  const precedentCalloutText = document.getElementById('precedentCalloutText');
  const contributingArticlesGrid = document.getElementById('contributingArticlesGrid');
  const sourcesTabCount = document.getElementById('sourcesTabCount');

  const preliminaryVerdictText = document.getElementById('preliminaryVerdictText');
  const supportRatioText = document.getElementById('supportRatioText');
  const refuteRatioText = document.getElementById('refuteRatioText');
  const notesBreakdownList = document.getElementById('notesBreakdownList');

  // H-MEM Drawer elements
  const hmemDrawer = document.getElementById('hmemDrawer');
  const drawerBackdrop = document.getElementById('drawerBackdrop');
  const toggleHmemBtn = document.getElementById('toggleHmemBtn');
  const closeHmemDrawerBtn = document.getElementById('closeHmemDrawerBtn');
  const hmemDecisionsCount = document.getElementById('hmemDecisionsCount');
  const hmemL0Count = document.getElementById('hmemL0Count');
  const hmemL1Count = document.getElementById('hmemL1Count');
  const hmemL2Count = document.getElementById('hmemL2Count');
  const hmemDecisionList = document.getElementById('hmemDecisionList');
  const runMetabolismBtn = document.getElementById('runMetabolismBtn');
  const refreshSystemBtn = document.getElementById('refreshSystemBtn');

  // Agent Step Elements
  const stepHmem = document.getElementById('agentStep-hmem');
  const stepSource = document.getElementById('agentStep-source');
  const stepAnalyser = document.getElementById('agentStep-analyser');
  const stepEvaluator = document.getElementById('agentStep-evaluator');

  // Input Character Counter
  claimInput.addEventListener('input', () => {
    charCount.textContent = `${claimInput.value.length} chars`;
  });

  // Tab Switching
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      document.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('active', 'text-teal-400', 'border-teal-400');
        b.classList.add('text-slate-400', 'border-transparent');
      });
      btn.classList.add('active', 'text-teal-400', 'border-teal-400');
      btn.classList.remove('text-slate-400', 'border-transparent');

      document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.add('hidden'));
      const activePane = document.getElementById(targetTab);
      if (activePane) activePane.classList.remove('hidden');
    });
  });

  // Load Initial Status
  loadZetarisStatus();
  loadHmemVault();
  loadSampleClaims();

  // Handle Form Submission
  claimForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const claim = claimInput.value.trim();
    if (!claim) return;

    startEvaluation(claim);
  });

  async function startEvaluation(claim) {
    // UI state updates
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Evaluating...</span>`;
    lucide.createIcons();

    pipelineSection.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    liveLogConsole.innerHTML = '';
    resetStepIndicators();
    updatePipelineBadge('Executing Agent Pipeline...', 'bg-amber-900/60 text-amber-300 border-amber-700');

    // Use SSE for real-time progress
    const eventSource = new EventSource(`/api/evaluate/stream?claim=${encodeURIComponent(claim)}`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleStreamEvent(data);

        if (data.type === 'complete') {
          eventSource.close();
          renderCompleteResult(data);
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<i data-lucide="play" class="w-4 h-4 fill-current"></i><span>Evaluate Claim</span>`;
          lucide.createIcons();
          loadHmemVault(); // refresh memory count
        }
      } catch (err) {
        console.error("SSE parse error:", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE connection error:", err);
      eventSource.close();
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i data-lucide="play" class="w-4 h-4 fill-current"></i><span>Evaluate Claim</span>`;
      lucide.createIcons();
      updatePipelineBadge('Stream Finished', 'bg-slate-800 text-slate-300 border-slate-700');
    };
  }

  function handleStreamEvent(data) {
    if (data.type === 'step') {
      logMessage(`[${data.agent}] ${data.message}`);

      if (data.step === 'hmem_lookup') {
        activateStep(stepHmem);
      } else if (data.step === 'hmem_lookup_complete') {
        completeStep(stepHmem);
      } else if (data.step === 'source_agent_started') {
        activateStep(stepSource);
      } else if (data.step === 'source_agent_complete') {
        completeStep(stepSource);
      } else if (data.step === 'analyser_agent_started') {
        activateStep(stepAnalyser);
      } else if (data.step === 'analyser_agent_complete') {
        completeStep(stepAnalyser);
      } else if (data.step === 'evaluator_agent_started') {
        activateStep(stepEvaluator);
      }
    }
  }

  function logMessage(msg) {
    const time = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = "flex items-start gap-2 py-0.5 text-slate-300";
    entry.innerHTML = `<span class="text-slate-500 shrink-0 font-mono text-[10px]">[${time}]</span><span>${escapeHtml(msg)}</span>`;
    liveLogConsole.appendChild(entry);
    liveLogConsole.scrollTop = liveLogConsole.scrollHeight;
  }

  function resetStepIndicators() {
    [stepHmem, stepSource, stepAnalyser, stepEvaluator].forEach(step => {
      step.classList.remove('agent-step-active', 'agent-step-completed');
    });
  }

  function activateStep(el) {
    el.classList.add('agent-step-active');
    el.classList.remove('agent-step-completed');
  }

  function completeStep(el) {
    el.classList.remove('agent-step-active');
    el.classList.add('agent-step-completed');
  }

  function updatePipelineBadge(text, classNames) {
    pipelineStatusBadge.textContent = text;
    pipelineStatusBadge.className = `text-xs px-2.5 py-1 rounded-full font-mono border ${classNames}`;
  }

  // Render Full Evaluation Result
  function renderCompleteResult(data) {
    completeStep(stepEvaluator);
    updatePipelineBadge('Evaluation Complete', 'bg-teal-900/60 text-teal-300 border-teal-700');

    resultsSection.classList.remove('hidden');

    // Decision styling
    decisionCard.className = "rounded-2xl p-6 sm:p-8 border shadow-xl relative overflow-hidden transition-all " + getDecisionCardClass(data.decision);
    decisionBadge.className = "px-4 py-1.5 rounded-full font-extrabold text-sm tracking-wider uppercase inline-flex items-center gap-2 " + getDecisionBadgeClass(data.decision);
    decisionBadge.innerHTML = getDecisionIconHtml(data.decision) + `<span>${data.decision.replace('_', ' ')}</span>`;

    confidencePill.textContent = `Confidence: ${data.confidence_percentage}`;
    compoundIdLabel.textContent = data.hmem_record?.compound_id || "DEC.L2.RECORDED";
    evaluatedClaimTitle.textContent = data.claim;

    sourcesCountMetric.textContent = data.contributing_articles?.length || 0;
    precedentsCountMetric.textContent = data.historical_precedents?.length || 0;
    sourcesTabCount.textContent = data.contributing_articles?.length || 0;

    // Render Explanation
    explanationContent.innerHTML = formatMarkdown(data.explanation);

    // Precedent Box
    if (data.historical_precedents && data.historical_precedents.length > 0) {
      precedentCalloutBox.classList.remove('hidden');
      const p = data.historical_precedents[0];
      precedentCalloutText.innerHTML = `
        Matched historical precedent <strong>${p.compound_id}</strong>: <em>"${escapeHtml(p.claim)}"</em> &rarr; 
        <span class="px-2 py-0.5 rounded bg-indigo-900/80 text-indigo-300 font-mono">${p.decision}</span> 
        (Match score: ${Math.round(p.similarity * 100)}%). Evaluator cross-referenced this to ensure long-term reasoning consistency.
      `;
    } else {
      precedentCalloutBox.classList.add('hidden');
    }

    // Render Contributing Articles Grid
    renderContributingArticles(data.contributing_articles || []);

    // Render Analyser Breakdown
    if (data.analyser_data) {
      preliminaryVerdictText.textContent = (data.analyser_data.preliminary_verdict || '--').replace('_', ' ');
      supportRatioText.textContent = `${Math.round((data.analyser_data.support_ratio || 0) * 100)}%`;
      refuteRatioText.textContent = `${Math.round((data.analyser_data.refute_ratio || 0) * 100)}%`;
      renderNotesBreakdown(data.analyser_data.detailed_evaluations || []);
    }

    lucide.createIcons();
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderContributingArticles(articles) {
    contributingArticlesGrid.innerHTML = '';
    if (!articles || articles.length === 0) {
      contributingArticlesGrid.innerHTML = `<p class="text-xs text-slate-500 italic col-span-2">No contributing articles returned.</p>`;
      return;
    }

    articles.forEach(art => {
      const card = document.createElement('div');
      card.className = "p-5 rounded-xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4 group";

      const stanceClass = getStancePillClass(art.stance);

      card.innerHTML = `
        <div class="space-y-2.5">
          <div class="flex items-center justify-between gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold uppercase ${stanceClass}">
              ${art.stance}
            </span>
            <span class="text-[11px] font-mono text-slate-400 flex items-center gap-1">
              <i data-lucide="shield" class="w-3 h-3 text-teal-400"></i>
              Rel: ${Math.round(art.reliability_score * 100)}%
            </span>
          </div>

          <h5 class="text-sm font-bold text-white group-hover:text-teal-400 transition leading-snug">
            <a href="${escapeHtml(art.url)}" target="_blank" rel="noopener noreferrer" class="hover:underline flex items-center justify-between gap-2">
              <span>${escapeHtml(art.title)}</span>
              <i data-lucide="external-link" class="w-3.5 h-3.5 text-slate-500 group-hover:text-teal-400 shrink-0"></i>
            </a>
          </h5>

          <p class="text-xs text-slate-400 line-clamp-3 italic bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80">
            "${escapeHtml(art.key_excerpt || '')}"
          </p>
        </div>

        <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500 font-mono">
          <span>${escapeHtml(art.domain || 'archive')}</span>
          <span>${escapeHtml(art.published_date || '2024')}</span>
        </div>
      `;
      contributingArticlesGrid.appendChild(card);
    });
    lucide.createIcons();
  }

  function renderNotesBreakdown(evaluations) {
    notesBreakdownList.innerHTML = '';
    evaluations.forEach((item, idx) => {
      const row = document.createElement('div');
      row.className = "p-3.5 rounded-xl bg-slate-950/50 border border-slate-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs";
      
      const stanceClass = getStancePillClass(item.stance);

      row.innerHTML = `
        <div class="space-y-1 max-w-xl">
          <div class="flex items-center gap-2">
            <span class="text-slate-500 font-mono text-[10px]">#0${idx + 1}</span>
            <span class="font-semibold text-slate-200">${escapeHtml(item.title)}</span>
          </div>
          <p class="text-slate-400 text-[11px]">${escapeHtml(item.reasoning || item.excerpt)}</p>
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono uppercase ${stanceClass}">
            ${item.stance}
          </span>
          <span class="text-slate-400 font-mono text-[11px]">
            ${Math.round(item.confidence * 100)}%
          </span>
        </div>
      `;
      notesBreakdownList.appendChild(row);
    });
  }

  // Load Zetaris Status
  async function loadZetarisStatus() {
    try {
      const res = await fetch('/api/zetaris/status');
      const data = await res.json();
      const modeLabel = document.getElementById('zetarisModeLabel');
      if (data.status === 'connected') {
        modeLabel.textContent = data.mode === 'live_zetaris_fabric' ? 'Live Fabric' : 'Federated Lakehouse';
      }
    } catch (e) {
      console.warn("Could not fetch Zetaris status:", e);
    }
  }

  // Load H-MEM Vault Data
  async function loadHmemVault() {
    try {
      const [resDec, resStats] = await Promise.all([
        fetch('/api/hmem/decisions'),
        fetch('/api/hmem/stats')
      ]);
      const dataDec = await resDec.json();
      const dataStats = await resStats.json();

      hmemDecisionsCount.textContent = dataDec.count || 0;
      hmemL2Count.textContent = dataDec.count || 0;
      hmemL0Count.textContent = dataStats.stats?.l0_ephemeral_count || 0;
      hmemL1Count.textContent = dataStats.stats?.l1_working_count || 0;

      renderHmemDecisionsList(dataDec.decisions || []);
    } catch (e) {
      console.warn("Could not fetch H-MEM vault:", e);
    }
  }

  function renderHmemDecisionsList(decisions) {
    hmemDecisionList.innerHTML = '';
    if (!decisions || decisions.length === 0) {
      hmemDecisionList.innerHTML = `<p class="text-xs text-slate-500 p-4 text-center">No decisions in vault yet.</p>`;
      return;
    }

    decisions.forEach(d => {
      const item = document.createElement('div');
      item.className = "p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-indigo-600/50 transition space-y-2 cursor-pointer";
      item.onclick = () => {
        claimInput.value = d.claim;
        charCount.textContent = `${d.claim.length} chars`;
        toggleHmemDrawer();
        startEvaluation(d.claim);
      };

      const badgeClass = getDecisionBadgeClass(d.decision);

      item.innerHTML = `
        <div class="flex items-center justify-between gap-2">
          <span class="text-xs font-mono font-semibold text-indigo-400">${d.compound_id}</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase ${badgeClass}">
            ${d.decision}
          </span>
        </div>
        <p class="text-xs text-slate-200 font-medium line-clamp-2">${escapeHtml(d.claim)}</p>
        <div class="flex items-center justify-between text-[10px] text-slate-500 font-mono pt-1 border-t border-slate-800/80">
          <span>Confidence: ${Math.round(d.confidence * 100)}%</span>
          <span>Hash: ${d.lineage?.audit_hash ? d.lineage.audit_hash.slice(0, 8) : 'ledger'}</span>
        </div>
      `;
      hmemDecisionList.appendChild(item);
    });
  }

  // Load Sample Claims
  async function loadSampleClaims() {
    try {
      const res = await fetch('/api/sample-claims');
      const claims = await res.json();
      samplePillsContainer.innerHTML = '';

      claims.forEach(c => {
        const pill = document.createElement('button');
        pill.type = 'button';
        pill.className = "px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/80 text-xs text-slate-300 hover:text-white transition text-left flex items-center gap-2 group";
        pill.innerHTML = `
          <span class="w-1.5 h-1.5 rounded-full ${c.expected === 'VALID' ? 'bg-teal-400' : 'bg-rose-400'}"></span>
          <span class="truncate max-w-xs">${escapeHtml(c.claim)}</span>
        `;
        pill.onclick = () => {
          claimInput.value = c.claim;
          charCount.textContent = `${c.claim.length} chars`;
          startEvaluation(c.claim);
        };
        samplePillsContainer.appendChild(pill);
      });
    } catch (e) {
      console.warn("Could not load sample claims:", e);
    }
  }

  // H-MEM Drawer Toggle
  window.toggleHmemDrawer = function() {
    const isOpen = !hmemDrawer.classList.contains('translate-x-full');
    if (isOpen) {
      hmemDrawer.classList.add('translate-x-full');
      drawerBackdrop.classList.add('hidden');
    } else {
      hmemDrawer.classList.remove('translate-x-full');
      drawerBackdrop.classList.remove('hidden');
      loadHmemVault();
    }
  };

  toggleHmemBtn.addEventListener('click', toggleHmemDrawer);
  closeHmemDrawerBtn.addEventListener('click', toggleHmemDrawer);
  drawerBackdrop.addEventListener('click', toggleHmemDrawer);

  // Trigger Metabolic Consolidation
  runMetabolismBtn.addEventListener('click', async () => {
    runMetabolismBtn.disabled = true;
    runMetabolismBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Consolidating Memory...</span>`;
    lucide.createIcons();

    try {
      const res = await fetch('/api/hmem/consolidate', { method: 'POST' });
      const data = await res.json();
      alert(`H-MEM Sleep/Dream consolidation completed! Audited ${data.total_decisions_audited} decisions.`);
      loadHmemVault();
    } catch (e) {
      alert("Metabolic consolidation failed.");
    } finally {
      runMetabolismBtn.disabled = false;
      runMetabolismBtn.innerHTML = `<i data-lucide="sparkles" class="w-4 h-4"></i><span>Trigger Sleep/Dream Consolidation</span>`;
      lucide.createIcons();
    }
  });

  refreshSystemBtn.addEventListener('click', () => {
    loadZetarisStatus();
    loadHmemVault();
  });

  // Helpers
  function getDecisionCardClass(decision) {
    if (decision === 'VALID') return 'decision-valid';
    if (decision === 'REFUTED') return 'decision-refuted';
    if (decision === 'PARTIALLY_VALID') return 'decision-partially-valid';
    return 'decision-inconclusive';
  }

  function getDecisionBadgeClass(decision) {
    if (decision === 'VALID') return 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40';
    if (decision === 'REFUTED') return 'bg-rose-500/20 text-rose-400 border border-rose-500/40';
    if (decision === 'PARTIALLY_VALID') return 'bg-amber-500/20 text-amber-400 border border-amber-500/40';
    return 'bg-slate-500/20 text-slate-300 border border-slate-500/40';
  }

  function getDecisionIconHtml(decision) {
    if (decision === 'VALID') return `<i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-400"></i>`;
    if (decision === 'REFUTED') return `<i data-lucide="x-circle" class="w-4 h-4 text-rose-400"></i>`;
    if (decision === 'PARTIALLY_VALID') return `<i data-lucide="alert-triangle" class="w-4 h-4 text-amber-400"></i>`;
    return `<i data-lucide="help-circle" class="w-4 h-4 text-slate-300"></i>`;
  }

  function getStancePillClass(stance) {
    if (stance === 'SUPPORTS') return 'stance-supports';
    if (stance === 'REFUTES') return 'stance-refutes';
    if (stance === 'PARTIALLY_SUPPORTS') return 'stance-partially-supports';
    return 'stance-inconclusive';
  }

  function formatMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code class="bg-slate-800 px-1.5 py-0.5 rounded text-teal-300 font-mono text-xs">$1</code>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/^- (.*$)/gim, '<li class="ml-4 list-disc">$1</li>');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }
});
