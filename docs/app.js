/**
 * RISK Enterprise Decision Intelligence Platform
 * Client-Side Interactivity, Dynamic Simulator, and Tab Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initFinancialSimulator();
  initDaxCopy();
  initTableSearch();
});

// -----------------------------------------------------------------------------
// 1. NAVIGATION TAB CONTROLLER
// -----------------------------------------------------------------------------
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const tabPanes = document.querySelectorAll('.tab-pane');
  const pageTitle = document.getElementById('page-title');
  const pageSubtitle = document.getElementById('page-subtitle');

  const titleMap = {
    'cmd-center': {
      title: 'Executive Command Center',
      sub: 'Portfolio KPI Scorecard & Unified System Architecture'
    },
    'retail': {
      title: 'Module A: Retail Revenue Intelligence',
      sub: 'Transactional Profitability, Discount Sensitivity & Loss Leadership'
    },
    'powerbi': {
      title: 'Module B: Executive Power BI & DAX',
      sub: 'Kimball Star Schema Architecture & Enterprise DAX Measure Library'
    },
    'retention': {
      title: 'Module C: Customer Retention Intelligence',
      sub: 'Subscriber Tenure Cohorts, Service Friction & Machine Learning Benchmarks'
    },
    'finance': {
      title: 'Module D: Financial Performance & Simulator',
      sub: 'Audited Statement Diagnostics & Real-Time What-If Scenario Engine'
    },
    'evidence': {
      title: 'Formal Evidence Register & Forensics',
      sub: 'Reproducible Formulas, Empirical Observations & Audit Traceability'
    }
  };

  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const targetTab = item.getAttribute('data-tab');

      // Update active nav item
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');

      // Update active tab pane
      tabPanes.forEach(pane => {
        pane.classList.remove('active');
        if (pane.id === targetTab) {
          pane.classList.add('active');
        }
      });

      // Update header
      if (titleMap[targetTab]) {
        pageTitle.textContent = titleMap[targetTab].title;
        pageSubtitle.textContent = titleMap[targetTab].sub;
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
}

// -----------------------------------------------------------------------------
// 2. INTERACTIVE FINANCIAL WHAT-IF SIMULATOR
// -----------------------------------------------------------------------------
function initFinancialSimulator() {
  const BASELINE = {
    grossSales: 127931598.50,
    discounts: 9205248.24,
    netSales: 118726350.26,
    cogs: 101832648.00,
    profit: 16893702.26,
    marginPct: 14.23
  };

  const discountSlider = document.getElementById('sim-discount');
  const cogsSlider = document.getElementById('sim-cogs');
  const volumeSlider = document.getElementById('sim-volume');

  const discountVal = document.getElementById('val-discount');
  const cogsVal = document.getElementById('val-cogs');
  const volumeVal = document.getElementById('val-volume');

  const simProfitEl = document.getElementById('sim-profit-value');
  const simMarginEl = document.getElementById('sim-margin-value');
  const simDeltaDollarEl = document.getElementById('sim-delta-dollar');
  const simDeltaPctEl = document.getElementById('sim-delta-pct');

  function calculateSimulation() {
    const discRedPct = parseFloat(discountSlider.value) / 100;
    const cogsRedPct = parseFloat(cogsSlider.value) / 100;
    const volChangePct = parseFloat(volumeSlider.value) / 100;

    // Display labels
    discountVal.textContent = `${discountSlider.value}% Cut`;
    cogsVal.textContent = `${cogsSlider.value}% Cut`;
    volumeVal.textContent = `${volumeSlider.value > 0 ? '+' : ''}${volumeSlider.value}% Shift`;

    // Mathematical adjustments
    const simVolume = 1.0 + volChangePct;
    const simGross = BASELINE.grossSales * simVolume;
    const simDiscounts = (BASELINE.discounts * (1.0 - discRedPct)) * simVolume;
    const simNetSales = simGross - simDiscounts;
    const simCogs = (BASELINE.cogs * (1.0 - cogsRedPct)) * simVolume;
    const simProfit = simNetSales - simCogs;
    const simMargin = (simProfit / simNetSales) * 100;

    const deltaDollar = simProfit - BASELINE.profit;
    const deltaPct = (deltaDollar / BASELINE.profit) * 100;

    // Format outputs
    simProfitEl.textContent = formatCurrency(simProfit);
    simMarginEl.textContent = `${simMargin.toFixed(2)}%`;

    const sign = deltaDollar >= 0 ? '+' : '';
    simDeltaDollarEl.textContent = `${sign}${formatCurrency(deltaDollar)}`;
    simDeltaPctEl.textContent = `(${sign}${deltaPct.toFixed(2)}%)`;

    if (deltaDollar >= 0) {
      simDeltaDollarEl.className = 'kpi-pill pill-success';
    } else {
      simDeltaDollarEl.className = 'kpi-pill pill-danger';
    }
  }

  if (discountSlider && cogsSlider && volumeSlider) {
    discountSlider.addEventListener('input', calculateSimulation);
    cogsSlider.addEventListener('input', calculateSimulation);
    volumeSlider.addEventListener('input', calculateSimulation);
    calculateSimulation();
  }
}

function formatCurrency(val) {
  return '$' + Math.round(val).toLocaleString();
}

// -----------------------------------------------------------------------------
// 3. DAX MEASURE COPY TO CLIPBOARD
// -----------------------------------------------------------------------------
function initDaxCopy() {
  const copyButtons = document.querySelectorAll('.copy-btn');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('.dax-item');
      const codeBlock = parent.querySelector('.dax-body');
      if (codeBlock) {
        navigator.clipboard.writeText(codeBlock.innerText).then(() => {
          const original = btn.textContent;
          btn.textContent = 'Copied!';
          btn.style.backgroundColor = '#ECFDF5';
          btn.style.color = '#047857';
          setTimeout(() => {
            btn.textContent = original;
            btn.style.backgroundColor = '';
            btn.style.color = '';
          }, 1500);
        });
      }
    });
  });
}

// -----------------------------------------------------------------------------
// 4. TABLE SEARCH & FILTER
// -----------------------------------------------------------------------------
function initTableSearch() {
  const searchInput = document.getElementById('evidence-search');
  if (!searchInput) return;

  searchInput.addEventListener('input', () => {
    const term = searchInput.value.toLowerCase();
    const rows = document.querySelectorAll('#evidence-table tbody tr');

    rows.forEach(row => {
      const text = row.innerText.toLowerCase();
      row.style.display = text.includes(term) ? '' : 'none';
    });
  });
}
