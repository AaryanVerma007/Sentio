import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the old export logic with the chart-aware export logic
export_block_start = content.find('// ==========================================')
# Find the start of the MACRO ANALYSIS section to bound the replacement
export_block_end = content.find('// ==========================================\n// 13. MACRO ANALYSIS: LIVE PULSE & BATTLE MODE')

if export_block_start == -1 or export_block_end == -1:
    print("Could not find the export logic blocks.")
    exit(1)

# Backtrack to the actual start of the professional pdf generator we just injected
prof_start = content.find('// PROFESSIONAL PDF EXPORT GENERATOR', 0)
if prof_start != -1:
    export_block_start = content.rfind('// ==========================================', 0, prof_start)

new_export_logic = """
// ==========================================
// PROFESSIONAL PDF EXPORT GENERATOR
// ==========================================

function getSentimentClass(sentiment) {
    if (sentiment === 'POSITIVE') return 'pdf-bg-positive';
    if (sentiment === 'NEGATIVE') return 'pdf-bg-negative';
    return 'pdf-bg-neutral';
}

function renderPDFChart(canvasId, type, data, options) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: type,
        data: data,
        options: {
            ...options,
            animation: false,
            responsive: false,
            devicePixelRatio: 2 // High res for PDF
        }
    });
}

async function renderProfessionalPDF(mode) {
    const container = document.getElementById('hidden-pdf-export-container');
    container.innerHTML = ''; // clear previous
    document.body.classList.add('exporting-pdf');
    
    const dateStr = new Date().toLocaleString();
    let html = '';
    
    if (mode === 'single') {
        const data = window.latestSingleData;
        const topic = window.latestSingleTopic;
        if (!data) return showToast('Error', 'No data to export', 'error');
        
        let scoreClass = 'pdf-text-neutral';
        if (data.final_score > 2) scoreClass = 'pdf-text-positive';
        if (data.final_score < -2) scoreClass = 'pdf-text-negative';
        
        const summaryText = document.querySelector('#smart-summary .text-on-surface-variant') ? document.querySelector('#smart-summary .text-on-surface-variant').innerText : data.summary;

        html = `
            <div class="report-page">
                <div class="pdf-report-header">
                    <div>
                        <div class="pdf-report-header-brand">SENTIO INTELLIGENCE</div>
                        <h1>Analysis Report: ${topic}</h1>
                    </div>
                    <div class="pdf-report-header-meta">
                        Generated: ${dateStr}<br/>
                        Sample Size: ${data.total_analyzed || data.total} Mentions
                    </div>
                </div>
                
                <div class="pdf-exec-summary">
                    <p><strong>Executive Summary:</strong> ${summaryText || 'Analysis complete. Review the metrics below.'}</p>
                </div>
                
                <div class="pdf-metrics-grid">
                    <div class="pdf-metric-card">
                        <div class="pdf-metric-label">Sentiment Score</div>
                        <div class="pdf-metric-value ${scoreClass}">${(data.final_score).toFixed(1)}</div>
                    </div>
                    <div class="pdf-metric-card">
                        <div class="pdf-metric-label">Positive Density</div>
                        <div class="pdf-metric-value pdf-text-positive">${Math.round((data.pos/data.total)*100)}%</div>
                    </div>
                    <div class="pdf-metric-card">
                        <div class="pdf-metric-label">Negative Density</div>
                        <div class="pdf-metric-value pdf-text-negative">${Math.round((data.neg/data.total)*100)}%</div>
                    </div>
                </div>

                <div class="pdf-chart-container avoid-break" style="height: 250px;">
                    <canvas id="pdfTrendChart" width="700" height="250"></canvas>
                </div>
                
                <h3 class="force-break">Representative Evidence</h3>
                <table class="pdf-evidence-table">
                    <thead>
                        <tr>
                            <th>Sentiment</th>
                            <th>Statement</th>
                            <th>Source</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${(data.feed || []).slice(0, 15).map(item => `
                            <tr>
                                <td><span class="pdf-badge ${getSentimentClass(item.sentiment)}">${item.sentiment}</span></td>
                                <td>"${item.text}"</td>
                                <td><span class="pdf-source-tag">${item.source || 'Social'}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;
        
        // Render Chart for Single
        if (data.trend_7_days && data.trend_7_days.labels.length > 0) {
            const formattedLabels = data.trend_7_days.labels.map(dateStr => {
                const d = new Date(dateStr);
                return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            });
            renderPDFChart('pdfTrendChart', 'line', {
                labels: formattedLabels,
                datasets: [{
                    label: 'Sentiment Score',
                    data: data.trend_7_days.data,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            }, {
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: '7-Day Trend Trajectory', color: '#0f172a', font: { size: 14, family: 'Inter' } }
                },
                scales: {
                    y: { 
                        min: -10, max: 10, 
                        grid: { color: '#e2e8f0' }, 
                        ticks: { color: '#64748b' }
                    },
                    x: { 
                        grid: { display: false }, 
                        ticks: { color: '#64748b' }
                    }
                }
            });
        }
        
    } else {
        const dataA = window.latestBattleDataA;
        const dataB = window.latestBattleDataB;
        const topicA = window.latestBattleTopicA;
        const topicB = window.latestBattleTopicB;
        
        if (!dataA || !dataB) return showToast('Error', 'No data to export', 'error');
        
        const summaryText = document.querySelector('#smart-summary .text-on-surface-variant') ? document.querySelector('#smart-summary .text-on-surface-variant').innerText : '';
        
        // compute winner
        let posA = (dataA.pos / dataA.total) * 100;
        let posB = (dataB.pos / dataB.total) * 100;
        let verdict = "Too Close To Call";
        let subtext = "Difference is within margin of error.";
        if (Math.abs(posA - posB) >= 3.0) {
            if (posA > posB) { verdict = `${topicA} Wins`; subtext = `Leading by ${(posA - posB).toFixed(1)}% positive sentiment.`; }
            else { verdict = `${topicB} Wins`; subtext = `Leading by ${(posB - posA).toFixed(1)}% positive sentiment.`; }
        }

        html = `
            <div class="report-page">
                <div class="pdf-report-header">
                    <div>
                        <div class="pdf-report-header-brand">SENTIO COMPARATIVE INTELLIGENCE</div>
                        <h1>Battle Mode: ${topicA} vs ${topicB}</h1>
                    </div>
                    <div class="pdf-report-header-meta">
                        Generated: ${dateStr}<br/>
                        Total Samples: ${(dataA.total || 0) + (dataB.total || 0)} Mentions
                    </div>
                </div>
                
                <div class="pdf-battle-verdict avoid-break">
                    <h2>${verdict}</h2>
                    <p>${subtext}</p>
                </div>
                
                ${summaryText ? `<div class="pdf-exec-summary avoid-break"><p><strong>Comparative Summary:</strong> ${summaryText}</p></div>` : ''}
                
                <div class="pdf-comparison-grid avoid-break">
                    <div>
                        <div class="pdf-col-header">${topicA}</div>
                        <div class="pdf-metric-card" style="margin-bottom: 20px;">
                            <div class="pdf-metric-label">Sentiment Score</div>
                            <div class="pdf-metric-value">${(dataA.final_score).toFixed(1)}</div>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Positive</span>
                            <span class="pdf-trend-stats pdf-text-positive">${Math.round((dataA.pos/dataA.total)*100)}%</span>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Negative</span>
                            <span class="pdf-trend-stats pdf-text-negative">${Math.round((dataA.neg/dataA.total)*100)}%</span>
                        </div>
                    </div>
                    <div>
                        <div class="pdf-col-header">${topicB}</div>
                        <div class="pdf-metric-card" style="margin-bottom: 20px;">
                            <div class="pdf-metric-label">Sentiment Score</div>
                            <div class="pdf-metric-value">${(dataB.final_score).toFixed(1)}</div>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Positive</span>
                            <span class="pdf-trend-stats pdf-text-positive">${Math.round((dataB.pos/dataB.total)*100)}%</span>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Negative</span>
                            <span class="pdf-trend-stats pdf-text-negative">${Math.round((dataB.neg/dataB.total)*100)}%</span>
                        </div>
                    </div>
                </div>
                
                <div class="pdf-chart-container avoid-break" style="height: 250px;">
                    <canvas id="pdfBattleChart" width="700" height="250"></canvas>
                </div>
                
                <h3 class="force-break">Representative Evidence: ${topicA}</h3>
                <table class="pdf-evidence-table">
                    <thead><tr><th>Sentiment</th><th>Statement</th><th>Source</th></tr></thead>
                    <tbody>
                        ${(dataA.feed || []).slice(0, 10).map(item => `
                            <tr>
                                <td><span class="pdf-badge ${getSentimentClass(item.sentiment)}">${item.sentiment}</span></td>
                                <td>"${item.text}"</td>
                                <td><span class="pdf-source-tag">${item.source || 'Social'}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
                <h3 class="force-break">Representative Evidence: ${topicB}</h3>
                <table class="pdf-evidence-table">
                    <thead><tr><th>Sentiment</th><th>Statement</th><th>Source</th></tr></thead>
                    <tbody>
                        ${(dataB.feed || []).slice(0, 10).map(item => `
                            <tr>
                                <td><span class="pdf-badge ${getSentimentClass(item.sentiment)}">${item.sentiment}</span></td>
                                <td>"${item.text}"</td>
                                <td><span class="pdf-source-tag">${item.source || 'Social'}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;
        
        // Render Chart for Battle
        renderPDFChart('pdfBattleChart', 'bar', {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [
                {
                    label: topicA,
                    data: [
                        Math.round((dataA.pos/dataA.total)*100) || 0,
                        Math.round((dataA.neu/dataA.total)*100) || 0,
                        Math.round((dataA.neg/dataA.total)*100) || 0
                    ],
                    backgroundColor: 'rgba(59, 130, 246, 0.8)'
                },
                {
                    label: topicB,
                    data: [
                        Math.round((dataB.pos/dataB.total)*100) || 0,
                        Math.round((dataB.neu/dataB.total)*100) || 0,
                        Math.round((dataB.neg/dataB.total)*100) || 0
                    ],
                    backgroundColor: 'rgba(148, 163, 184, 0.8)'
                }
            ]
        }, {
            plugins: {
                legend: { display: true, position: 'top', labels: { color: '#0f172a' } },
                title: { display: true, text: 'Sentiment Distribution (%)', color: '#0f172a', font: { size: 14, family: 'Inter' } }
            },
            scales: {
                y: { 
                    beginAtZero: true, max: 100, 
                    grid: { color: '#e2e8f0' }, 
                    ticks: { color: '#64748b' }
                },
                x: { 
                    grid: { display: false }, 
                    ticks: { color: '#64748b' }
                }
            }
        });
    }
    
    // Wait a brief moment for canvas rendering to settle
    await new Promise(r => setTimeout(r, 100));
    
    const opt = {
        margin:       0,
        filename:     mode === 'single' ? 'sentio-analysis-report.pdf' : 'sentio-battle-report.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: true, logging: false },
        jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' }
    };
    
    try {
        await html2pdf().set(opt).from(container).save();
    } catch(e) {
        showToast('Export Error', 'Failed to generate PDF.', 'error');
    } finally {
        document.body.classList.remove('exporting-pdf');
    }
}

(document.getElementById('exportMacroBtn') || {addEventListener:()=>{}}).addEventListener('click', () => {
    const results = document.getElementById('topicResults');
    if (results && results.classList.contains('hidden')) {
        return showToast('Export', 'Run a Macro Analysis first.', 'warning');
    }
    showToast('Export', 'Generating Professional Report...', 'info');
    renderProfessionalPDF('single');
});

(document.getElementById('exportBattleBtn') || {addEventListener:()=>{}}).addEventListener('click', () => {
    const results = document.getElementById('battleResults');
    if (results && results.classList.contains('hidden')) {
        return showToast('Export', 'Run a Battle Analysis first.', 'warning');
    }
    showToast('Export', 'Generating Professional Report...', 'info');
    renderProfessionalPDF('battle');
});

"""

content = content[:export_block_start] + new_export_logic + content[export_block_end:]
    
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated script.js with professional chart-aware PDF generation logic.")
