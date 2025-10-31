(function() {
  const socket = io();

  // Charts setup
  const attacksPerMinuteCtx = document.getElementById('attacksPerMinute');
  const topIpsCtx = document.getElementById('topIps');
  const countryDistCtx = document.getElementById('countryDist');

  const attacksPerMinuteChart = new Chart(attacksPerMinuteCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Attacks/min', data: [], borderColor: '#60a5fa' }] },
    options: { plugins: { legend: { labels: { color: '#e2e8f0' } } }, scales: { x: { ticks: { color: '#94a3b8' } }, y: { ticks: { color: '#94a3b8' } } } }
  });

  const topIpsChart = new Chart(topIpsCtx, {
    type: 'bar',
    data: { labels: [], datasets: [{ label: 'Top IPs', data: [], backgroundColor: '#34d399' }] },
    options: { plugins: { legend: { labels: { color: '#e2e8f0' } } }, scales: { x: { ticks: { color: '#94a3b8' } }, y: { ticks: { color: '#94a3b8' } } } }
  });

  const countryDistChart = new Chart(countryDistCtx, {
    type: 'doughnut',
    data: { labels: [], datasets: [{ label: 'Countries', data: [], backgroundColor: ['#f87171','#60a5fa','#34d399','#fbbf24','#a78bfa','#f472b6','#22d3ee'] }] },
    options: { plugins: { legend: { labels: { color: '#e2e8f0' } } } }
  });

  function updateFromStats(stats) {
    // Attacks per minute
    const perMinute = stats.per_minute || {};
    const labels = Object.keys(perMinute).sort();
    const values = labels.map(k => perMinute[k]);
    attacksPerMinuteChart.data.labels = labels;
    attacksPerMinuteChart.data.datasets[0].data = values;
    attacksPerMinuteChart.update('none');

    // Top IPs
    const topIps = stats.top_ips || {};
    const ipLabels = Object.entries(topIps).sort((a,b) => b[1]-a[1]).slice(0,10).map(e => e[0]);
    const ipCounts = ipLabels.map(l => topIps[l]);
    topIpsChart.data.labels = ipLabels;
    topIpsChart.data.datasets[0].data = ipCounts;
    topIpsChart.update('none');

    // Country distribution
    const byCountry = stats.by_country || {};
    const countryLabels = Object.keys(byCountry);
    const countryCounts = countryLabels.map(l => byCountry[l]);
    countryDistChart.data.labels = countryLabels;
    countryDistChart.data.datasets[0].data = countryCounts;
    countryDistChart.update('none');
  }

  // Initial metrics fetch
  fetch('/metrics').then(r => r.json()).then(updateFromStats).catch(() => {});

  socket.on('attack_event', function(evt) {
    // Could add toast/notification here if desired
  });

  socket.on('stats_update', function(stats) {
    updateFromStats(stats);
  });
})();
