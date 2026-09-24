import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We need to add global variables at the top of script.js to store the latest analysis data
if 'window.latestSingleData' not in content:
    globals_injection = """
window.latestSingleData = null;
window.latestSingleTopic = "";
window.latestBattleDataA = null;
window.latestBattleDataB = null;
window.latestBattleTopicA = "";
window.latestBattleTopicB = "";
"""
    # inject after const API
    content = content.replace("const API = 'http://127.0.0.1:5000';", "const API = 'http://127.0.0.1:5000';\n" + globals_injection)

# 2. Update single stream to store data
single_hook = "renderFinalSingleData(finalData);"
if single_hook in content:
    content = content.replace(single_hook, "window.latestSingleData = finalData;\n                window.latestSingleTopic = topic;\n                " + single_hook)

# 3. Update battle stream to store data
battle_hook = "finalizeBattle(finalDataA, finalDataB, topicA, topicB);"
if battle_hook in content:
    content = content.replace(
        "if (completedB) finalizeBattle(finalDataA, finalDataB, topicA, topicB);",
        "if (completedB) { window.latestBattleDataA = finalDataA; window.latestBattleDataB = finalDataB; window.latestBattleTopicA = topicA; window.latestBattleTopicB = topicB; finalizeBattle(finalDataA, finalDataB, topicA, topicB); }"
    )
    content = content.replace(
        "if (completedA) finalizeBattle(finalDataA, finalDataB, topicA, topicB);",
        "if (completedA) { window.latestBattleDataA = finalDataA; window.latestBattleDataB = finalDataB; window.latestBattleTopicA = topicA; window.latestBattleTopicB = topicB; finalizeBattle(finalDataA, finalDataB, topicA, topicB); }"
    )

# 4. Replace the old export logic with the new one
export_block_start = content.find('// Export Helper for combining elements')
export_block_end = content.find('// ==========================================\n// 13. MACRO ANALYSIS: LIVE PULSE & BATTLE MODE')

new_export_logic = """
// ==========================================
// PROFESSIONAL PDF EXPORT GENERATOR
// ==========================================

function getSentimentClass(sentiment) {
    if (sentiment === 'POSITIVE') return 'pdf-bg-positive';
    if (sentiment === 'NEGATIVE') return 'pdf-bg-negative';
    return 'pdf-bg-neutral';
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
                
                <div class="pdf-battle-verdict">
                    <h2>${verdict}</h2>
                    <p>${subtext}</p>
                </div>
                
                ${summaryText ? `<div class="pdf-exec-summary"><p><strong>Comparative Summary:</strong> ${summaryText}</p></div>` : ''}
                
                <div class="pdf-comparison-grid">
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
    }
    
    container.innerHTML = html;
    
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

if export_block_start != -1 and export_block_end != -1:
    content = content[:export_block_start] + new_export_logic + content[export_block_end:]
    
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated script.js with professional PDF generation logic.")
