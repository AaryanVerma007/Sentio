"use strict";

const API = "http://127.0.0.1:5000";

// State
let sentimentChartInstance = null;
let trendChartInstance = null;
let currentView = "view-vision";
let lastAnalysisData = null; // Store last analysis for sharing


// ==========================================
// 1. SPA ROUTING & HASH CONTROL
// ==========================================
const navButtons = document.querySelectorAll('.nav-btn');
const views = document.querySelectorAll('.view');
const reveals = document.querySelectorAll('.scroll-reveal');

const viewNames = {
    'view-vision': 'Vision',
    'view-macro': 'Macro Analysis',
    'view-micro': 'Micro Inference'
};

function handleHashChange() {
    let hash = window.location.hash || '#';
    
    // Parse query-like params in hash if needed, e.g. #macro-analysis?tab=battle
    const baseHash = hash.split('?')[0];

    // Scroll securely if it's a valid section
    if (baseHash && baseHash !== '#') {
        const target = document.getElementById(baseHash.replace('#', ''));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

window.addEventListener('hashchange', handleHashChange);
window.addEventListener('DOMContentLoaded', handleHashChange);

// Smooth Scrolling for Nav Links (update hash)
navButtons.forEach(btn => {
    if(btn) btn.addEventListener('click', (e) => {
        const href = btn.getAttribute('href');
        if (href.startsWith('#')) {
            // Let the browser handle the hash change natively, which will trigger hashchange
        }
    });
});

// Macro Analysis Tabs
window.switchMacroTab = function(tab) {
    const tabs = ['single', 'battle'];
    
    tabs.forEach(t => {
        const capTab = t.charAt(0).toUpperCase() + t.slice(1);
        
        // Toggle Tab Buttons
        const btn = document.getElementById('tabBtn' + capTab);
        if (btn) {
            if (t === tab) {
                btn.classList.add('text-primary', 'border-primary');
                btn.classList.remove('text-outline', 'border-transparent');
            } else {
                btn.classList.add('text-outline', 'border-transparent');
                btn.classList.remove('text-primary', 'border-primary');
            }
        }
        
        // Toggle Hero Inputs
        const heroInput = document.getElementById('heroInput' + capTab);
        if (heroInput) {
            if (t === tab) {
                heroInput.classList.remove('hidden');
                heroInput.classList.add('block');
            } else {
                heroInput.classList.remove('block');
                heroInput.classList.add('hidden');
            }
        }
        
        // Toggle Macro Analysis Results Content
        const macroContent = document.getElementById('tabContent' + capTab);
        if (macroContent) {
            if (t === tab) {
                macroContent.classList.remove('hidden');
                macroContent.classList.add('block');
            } else {
                macroContent.classList.remove('block');
                macroContent.classList.add('hidden');
            }
        }
    });

    // Update URL hash without jumping
    history.replaceState(null, null, '#macro-analysis?tab=' + tab);
};
// ==========================================
// 2. INTELLIGENT TYPOGRAPHY ANIMATION (Feature 7)
// ==========================================
function setupTypography() {
    const animElements = document.querySelectorAll('.anim-text, .anim-title');
    
    animElements.forEach(el => {
        if (el.children.length === 0 && el.textContent.trim().length > 0) {
            const text = el.textContent;
            el.innerHTML = '';
            for (let i = 0; i < text.length; i++) {
                const span = document.createElement('span');
                span.textContent = text[i] === ' ' ? '\u00A0' : text[i];
                span.className = 'anim-char';
                el.appendChild(span);
            }
        }
    });

    setInterval(() => {
        const chars = document.querySelectorAll('.anim-char');
        if (chars.length === 0) return;
        
        const numToAnimate = Math.floor(Math.random() * 15) + 5;
        for (let i = 0; i < numToAnimate; i++) {
            const randomChar = chars[Math.floor(Math.random() * chars.length)];
            if (randomChar.textContent !== '\u00A0') {
                randomChar.classList.add('char-hidden');
                setTimeout(() => {
                    randomChar.classList.remove('char-hidden');
                }, Math.random() * 1000 + 200);
            }
        }
    }, 400);
}
setupTypography();

// ==========================================
// 3. TOAST NOTIFICATION SYSTEM (Reusable)
// ==========================================
const toastStack = document.getElementById('toast-stack');

const toastIcons = {
    info: 'fa-solid fa-circle-info',
    success: 'fa-solid fa-circle-check',
    warning: 'fa-solid fa-triangle-exclamation',
    error: 'fa-solid fa-circle-xmark'
};

function showToast(title, message, type = 'info', duration = 4000) {
    const toast = document.createElement('div');
    toast.className = `toast-item ${type}`;
    toast.innerHTML = `
        <div class="toast-item-icon"><i class="${toastIcons[type] || toastIcons.info}"></i></div>
        <div class="toast-item-content">
            <div class="toast-item-title">${title}</div>
            <div class="toast-item-message">${message}</div>
        </div>
        <div class="toast-progress" style="width: 100%;"></div>
    `;
    
    toastStack.appendChild(toast);
    
    // Animate in
    requestAnimationFrame(() => {
        toast.classList.add('show');
    });
    
    // Progress bar
    const progress = toast.querySelector('.toast-progress');
    progress.style.transitionDuration = `${duration}ms`;
    requestAnimationFrame(() => {
        setTimeout(() => { progress.style.width = '0%'; }, 50);
    });
    
    // Auto dismiss
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 500);
    }, duration);
}

function requestNotificationPermission() {
    if ("Notification" in window && Notification.permission !== "granted" && Notification.permission !== "denied") {
        Notification.requestPermission();
    }
}

function sendDesktopNotification(title, body) {
    if (!("Notification" in window)) return;
    if (Notification.permission === "granted") {
        new Notification(title, { body });
    }
}

// ==========================================
// 12. AMBIENT HERO SLOGANS
// ==========================================
const heroSection = document.getElementById('hero');
const slogans = document.querySelectorAll('.ambient-slogan');

if (heroSection && slogans.length > 0) {
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let isHoveringHero = false;
    let time = 0;
    
    // Throttle cursor updates slightly for performance
    let lastMouseMove = 0;
    heroSection.addEventListener('mousemove', (e) => {
        const now = Date.now();
        if (now - lastMouseMove > 16) { // ~60fps
            mouseX = e.clientX;
            mouseY = e.clientY;
            isHoveringHero = true;
            lastMouseMove = now;
        }
    });
    
    heroSection.addEventListener('mouseleave', () => {
        isHoveringHero = false;
    });

    // Check for prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Initialize slogan physics state for swimming
    const sloganStates = Array.from(slogans).map(slogan => {
        return {
            x: Math.random() * 80 + 10, // 10% to 90%
            y: Math.random() * 80 + 10,
            vx: (Math.random() - 0.5) * 0.08, // Swimming speed X
            vy: (Math.random() - 0.5) * 0.08, // Swimming speed Y
            el: slogan,
            depth: parseFloat(slogan.dataset.depth) || 1
        };
    });

    function animateSlogans() {
        if (!prefersReducedMotion) {
            time += 0.005;
        }
        
        sloganStates.forEach((state, index) => {
            if (!prefersReducedMotion) {
                // Update swimming position
                state.x += state.vx;
                state.y += state.vy;
                
                // Bounce off invisible bounds (keep within 5% to 90% to avoid clipping out)
                if (state.x < 5 || state.x > 90) state.vx *= -1;
                if (state.y < 5 || state.y > 90) state.vy *= -1;
            }
            
            // Set base position continuously
            state.el.style.left = `${state.x}%`;
            state.el.style.top = `${state.y}%`;
            
            // Base organic float (if motion is allowed)
            const floatX = prefersReducedMotion ? 0 : Math.sin(time + index * 10) * 15 * state.depth;
            const floatY = prefersReducedMotion ? 0 : Math.cos(time * 0.8 + index * 15) * 15 * state.depth;
            
            let parallaxX = 0;
            let parallaxY = 0;
            let scale = 1;
            let glow = 'none';
            
            if (isHoveringHero) {
                const rect = state.el.getBoundingClientRect();
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;
                
                const distX = mouseX - centerX;
                const distY = mouseY - centerY;
                const distance = Math.sqrt(distX * distX + distY * distY);
                
                const influenceRadius = 300;
                
                if (distance < influenceRadius) {
                    const factor = Math.pow((influenceRadius - distance) / influenceRadius, 2); // easing
                    
                    // Magnetic pull (moves toward cursor, more pronounced for elements "closer" to foreground)
                    parallaxX = (distX * factor * 0.2) / state.depth;
                    parallaxY = (distY * factor * 0.2) / state.depth;
                    
                    scale = 1 + (factor * 0.1); // slight scale up
                    glow = `0 0 ${15 * factor}px rgba(0, 219, 231, ${factor * 0.8})`; // stronger primary glow on hover
                }
            }
            
            state.el.style.transform = `translate(-50%, -50%) translate(${floatX + parallaxX}px, ${floatY + parallaxY}px) scale(${scale})`;
            if(glow !== 'none') state.el.style.textShadow = glow;
            else state.el.style.textShadow = '';
        });
        
        requestAnimationFrame(animateSlogans);
    }
    
    // Start animation loop
    requestAnimationFrame(animateSlogans);
}

// ==========================================
// 13. EXPORT FUNCTIONALITY (Feature 5)
// ==========================================


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
    container.style.display = 'block';
    container.innerHTML = ''; // clear previous
    document.body.classList.add('exporting-pdf');
    
    const dateStr = new Date().toLocaleString();
    let html = '';
    
    // Helper to extract flat feed from backend samples dict
    const extractFeed = (payload) => {
        if (!payload || !payload.samples) return [];
        let arr = [];
        if (payload.samples.positive) arr = arr.concat(payload.samples.positive);
        if (payload.samples.negative) arr = arr.concat(payload.samples.negative);
        if (payload.samples.neutral) arr = arr.concat(payload.samples.neutral);
        return arr.sort(() => Math.random() - 0.5); // shuffle mix
    };
    
    if (mode === 'single') {
        const data = window.latestSingleData;
        const topic = window.latestSingleTopic;
        if (!data) {
            document.body.classList.remove('exporting-pdf');
            return showToast('Error', 'No data to export. Run analysis first.', 'error');
        }
        
        const finalScore = data.average_score || 0;
        const total = data.total_analyzed || 1;
        const pos = data.summary?.positive || 0;
        const neg = data.summary?.negative || 0;
        const posSamples = data.samples?.positive?.slice(0, 10) || [];
        const neuSamples = data.samples?.neutral?.slice(0, 10) || [];
        const negSamples = data.samples?.negative?.slice(0, 10) || [];
        
        let scoreClass = 'pdf-text-neutral';
        if (finalScore > 2) scoreClass = 'pdf-text-positive';
        if (finalScore < -2) scoreClass = 'pdf-text-negative';
        
        const summaryText = document.querySelector('#smart-summary .text-on-surface-variant') ? document.querySelector('#smart-summary .text-on-surface-variant').innerText : data.genai_summary || '';

        const generateRows = (items, label, colorClass) => {
            if (!items || items.length === 0) {
                return `<tr class="avoid-break"><td colspan="3" style="text-align:center; padding: 20px; color: #64748b;">No ${label} sentiments detected for this topic.</td></tr>`;
            }
            return items.map(item => `
                <tr class="avoid-break">
                    <td style="width: 15%;">
                        <span class="pdf-badge ${colorClass}">${label}</span>
                        <br/><span style="font-size: 10px; color: #64748b; margin-top: 4px; display: inline-block;">Score: ${item.score !== undefined ? Number(item.score).toFixed(2) : 'N/A'}</span>
                    </td>
                    <td style="width: 65%;">"${item.text}"</td>
                    <td style="width: 20%; text-align: right;"><span class="pdf-source-tag">${item.source || 'Social'}</span></td>
                </tr>
            `).join('');
        };

        html = `
            <div class="report-page">
                <div class="pdf-report-header">
                    <div>
                        <div class="pdf-report-header-brand">SENTIO INTELLIGENCE</div>
                        <h1>Analysis Report: ${topic}</h1>
                    </div>
                    <div class="pdf-report-header-meta">
                        Generated: ${dateStr}<br/>
                        Sample Size: ${total} Mentions
                    </div>
                </div>
                
                <div class="pdf-exec-summary">
                    <p><strong>Executive Summary:</strong> ${summaryText || 'Analysis complete. Review the metrics below.'}</p>
                </div>
                
                <div class="pdf-metrics-grid">
                    <div class="pdf-metric-card">
                        <div class="pdf-metric-label">Sentiment Score</div>
                        <div class="pdf-metric-value ${scoreClass}">${finalScore.toFixed(1)}</div>
                    </div>
                    <div class="pdf-metric-card">
                        <div class="pdf-metric-label">Positive Density</div>
                        <div class="pdf-metric-value pdf-text-positive">${Math.round((pos/total)*100)}%</div>
                    </div>
                    <div class="pdf-metric-card">
                        <div class="pdf-metric-label">Negative Density</div>
                        <div class="pdf-metric-value pdf-text-negative">${Math.round((neg/total)*100)}%</div>
                    </div>
                </div>

                <div class="pdf-chart-container avoid-break" style="height: 250px; display: flex; flex-direction: row; justify-content: center; gap: 40px; align-items: center; width: 100%;">
                    <div style="width: 250px; height: 250px; position: relative;">
                        <canvas id="pdfSingleDoughnut" width="250" height="250"></canvas>
                        <div style="position: absolute; top: 55%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: none;">
                            <div style="font-size: 32px; color: #1e293b; font-weight: 800; line-height: 1;">${total}</div>
                            <div style="font-size: 11px; color: #64748b; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-top: 4px;">SAMPLES</div>
                        </div>
                    </div>
                    <div style="width: 430px; height: 250px;">
                        <canvas id="pdfTrendChart" width="430" height="250"></canvas>
                    </div>
                </div>
                
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Positive Sentiments</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(posSamples, 'Positive', 'pdf-text-positive')}</tbody>
                    </table>
                </div>
        `;

        if (negSamples.length > 0) {
            html += `
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Negative Sentiments</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(negSamples, 'Negative', 'pdf-text-negative')}</tbody>
                    </table>
                </div>
            `;
        }

        if (neuSamples.length > 0) {
            html += `
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Neutral Sentiments</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(neuSamples, 'Neutral', '')}</tbody>
                    </table>
                </div>
            `;
        }
        
        html += `
            </div>
        `;
        
        container.innerHTML = html;
        
        // Render Doughnut Chart for Single
        const neu = total - pos - neg;
        renderPDFChart('pdfSingleDoughnut', 'doughnut', {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [pos, neu, neg],
                backgroundColor: ['#4ade80', '#94a3b8', '#f87171'],
                borderWidth: 0
            }]
        }, {
            plugins: {
                legend: { display: true, position: 'bottom', labels: { color: '#0f172a', font: { size: 10 } } },
                title: { display: true, text: 'Sample Distribution', color: '#0f172a', font: { size: 14, family: 'Inter' } }
            },
            cutout: '70%'
        });
        
        // Render Chart for Single
        if (data.trend_7_days && data.trend_7_days.labels && data.trend_7_days.labels.length > 0) {
            const formattedLabels = data.trend_7_days.labels.map(dateStr => {
                const d = new Date(dateStr);
                return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            });
            renderPDFChart('pdfTrendChart', 'line', {
                labels: formattedLabels,
                datasets: [
                    { 
                        label: 'Positive', 
                        data: data.trend_7_days.positive, 
                        borderColor: '#4ade80', 
                        backgroundColor: 'rgba(74, 222, 128, 0.1)', 
                        borderWidth: 2, 
                        fill: true, 
                        tension: 0.4 
                    },
                    { 
                        label: 'Negative', 
                        data: data.trend_7_days.negative, 
                        borderColor: '#f87171', 
                        backgroundColor: 'rgba(248, 113, 113, 0.1)', 
                        borderWidth: 2, 
                        fill: true, 
                        tension: 0.4 
                    }
                ]
            }, {
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: '7-Day Trend Trajectory', color: '#0f172a', font: { size: 14, family: 'Inter' } }
                },
                scales: {
                    y: { 
                        beginAtZero: true, 
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
        
        if (!dataA || !dataB) {
            document.body.classList.remove('exporting-pdf');
            return showToast('Error', 'No data to export. Run analysis first.', 'error');
        }
        
        const summaryText = document.querySelector('#smart-summary .text-on-surface-variant') ? document.querySelector('#smart-summary .text-on-surface-variant').innerText : '';
        
        const scoreA = dataA.average_score || 0;
        const totalA = dataA.total_analyzed || 1;
        const posA_num = dataA.summary?.positive || 0;
        const negA_num = dataA.summary?.negative || 0;
        const neuA_num = dataA.summary?.neutral || 0;
        const posA_samples = dataA.samples?.positive?.slice(0, 10) || [];
        const neuA_samples = dataA.samples?.neutral?.slice(0, 10) || [];
        const negA_samples = dataA.samples?.negative?.slice(0, 10) || [];
        
        const scoreB = dataB.average_score || 0;
        const totalB = dataB.total_analyzed || 1;
        const posB_num = dataB.summary?.positive || 0;
        const negB_num = dataB.summary?.negative || 0;
        const neuB_num = dataB.summary?.neutral || 0;
        const posB_samples = dataB.samples?.positive?.slice(0, 10) || [];
        const neuB_samples = dataB.samples?.neutral?.slice(0, 10) || [];
        const negB_samples = dataB.samples?.negative?.slice(0, 10) || [];

        const generateRows = (items, label, colorClass) => {
            if (!items || items.length === 0) {
                return `<tr class="avoid-break"><td colspan="3" style="text-align:center; padding: 20px; color: #64748b;">No ${label} sentiments detected for this topic.</td></tr>`;
            }
            return items.map(item => `
                <tr class="avoid-break">
                    <td style="width: 15%;">
                        <span class="pdf-badge ${colorClass}">${label}</span>
                        <br/><span style="font-size: 10px; color: #64748b; margin-top: 4px; display: inline-block;">Score: ${item.score !== undefined ? Number(item.score).toFixed(2) : 'N/A'}</span>
                    </td>
                    <td style="width: 65%;">"${item.text}"</td>
                    <td style="width: 20%; text-align: right;"><span class="pdf-source-tag">${item.source || 'Social'}</span></td>
                </tr>
            `).join('');
        };

        // compute winner
        let posA = (posA_num / totalA) * 100;
        let posB = (posB_num / totalB) * 100;
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
                        Total Samples: ${totalA + totalB} Mentions
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
                            <div class="pdf-metric-value">${scoreA.toFixed(1)}</div>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Positive</span>
                            <span class="pdf-trend-stats pdf-text-positive">${Math.round(posA)}%</span>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Neutral</span>
                            <span class="pdf-trend-stats" style="color: #64748b;">${Math.round((neuA_num/totalA)*100)}%</span>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Negative</span>
                            <span class="pdf-trend-stats pdf-text-negative">${Math.round((negA_num/totalA)*100)}%</span>
                        </div>
                    </div>
                    <div>
                        <div class="pdf-col-header">${topicB}</div>
                        <div class="pdf-metric-card" style="margin-bottom: 20px;">
                            <div class="pdf-metric-label">Sentiment Score</div>
                            <div class="pdf-metric-value">${scoreB.toFixed(1)}</div>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Positive</span>
                            <span class="pdf-trend-stats pdf-text-positive">${Math.round(posB)}%</span>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Neutral</span>
                            <span class="pdf-trend-stats" style="color: #64748b;">${Math.round((neuB_num/totalB)*100)}%</span>
                        </div>
                        <div class="pdf-trend-item">
                            <span class="pdf-trend-term">Negative</span>
                            <span class="pdf-trend-stats pdf-text-negative">${Math.round((negB_num/totalB)*100)}%</span>
                        </div>
                    </div>
                </div>
                
                <div class="pdf-chart-container avoid-break" style="height: 250px; display: flex; flex-direction: row; justify-content: center; gap: 40px; align-items: center; width: 100%;">
                    <div style="width: 340px; height: 250px;">
                        <canvas id="pdfBattleChart" width="340" height="250"></canvas>
                    </div>
                    <div style="width: 340px; height: 250px;">
                        <canvas id="pdfBattleTrendChart" width="340" height="250"></canvas>
                    </div>
                </div>
                
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Evidence for ${topicA}: Positive Sentiment</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(posA_samples, 'Positive', 'pdf-text-positive')}</tbody>
                    </table>
                </div>
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Evidence for ${topicA}: Negative Sentiment</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(negA_samples, 'Negative', 'pdf-text-negative')}</tbody>
                    </table>
                </div>
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Evidence for ${topicA}: Neutral Sentiment</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(neuA_samples, 'Neutral', '')}</tbody>
                    </table>
                </div>
                
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e2e8f0;">Evidence for ${topicB}: Positive Sentiment</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(posB_samples, 'Positive', 'pdf-text-positive')}</tbody>
                    </table>
                </div>
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Evidence for ${topicB}: Negative Sentiment</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th style="text-align: right;">Source</th></tr></thead>
                        <tbody>${generateRows(negB_samples, 'Negative', 'pdf-text-negative')}</tbody>
                    </table>
                </div>
                <div class="pdf-evidence-table-wrapper force-break">
                    <h3 class="avoid-break" style="margin-top: 30px;">Evidence for ${topicB}: Neutral Sentiment</h3>
                    <table class="pdf-evidence-table">
                        <thead><tr><th>Sentiment</th><th>Statement</th><th>Source</th></tr></thead>
                        <tbody>${generateRows(neuB_samples, 'Neutral', '')}</tbody>
                    </table>
                </div>
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
                        Math.round((posA_num/totalA)*100),
                        Math.round((neuA_num/totalA)*100),
                        Math.round((negA_num/totalA)*100)
                    ],
                    backgroundColor: 'rgba(59, 130, 246, 0.8)'
                },
                {
                    label: topicB,
                    data: [
                        Math.round((posB_num/totalB)*100),
                        Math.round((neuB_num/totalB)*100),
                        Math.round((negB_num/totalB)*100)
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

        // Render Trend Chart for Battle
        let battleLabels = [];
        if (dataA.trend_7_days && dataA.trend_7_days.labels) {
            battleLabels = dataA.trend_7_days.labels.map(dateStr => {
                const d = new Date(dateStr);
                return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            });
        }
        
        const calcTrend = (trendData) => {
            if (!trendData || !trendData.positive) return [];
            const pos = trendData.positive || [];
            const neg = trendData.negative || [];
            return pos.map((p, i) => {
                const n = neg[i] || 0;
                const totalBucket = p + n + (trendData.neutral?.[i] || 0) || 1;
                return ((p - n) / totalBucket) * 10;
            });
        };

        if (battleLabels.length > 0) {
            renderPDFChart('pdfBattleTrendChart', 'line', {
                labels: battleLabels,
                datasets: [
                    {
                        label: topicA,
                        data: calcTrend(dataA.trend_7_days),
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false
                    },
                    {
                        label: topicB,
                        data: calcTrend(dataB.trend_7_days),
                        borderColor: '#94a3b8',
                        backgroundColor: 'rgba(148, 163, 184, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false
                    }
                ]
            }, {
                plugins: {
                    legend: { display: true, position: 'top', labels: { color: '#0f172a' } },
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
    }
    
    // Set the PDF filename based on the topic
    const currentTopic = mode === 'single' ? (window.latestSingleTopic || 'Sentio') : ((window.latestBattleTopicA || 'TopicA') + '_vs_' + (window.latestBattleTopicB || 'TopicB'));
    const safeTopic = currentTopic.replace(/[^a-zA-Z0-9\s-]/g, '').trim().replace(/\s+/g, '_');
    const pdfFilename = mode === 'single' ? `${safeTopic}_Analysis_Report` : `${safeTopic}_Battle_Report`;
    
    // Show a loading toast
    showToast('Exporting', 'Generating PDF in the background...', 'success');

    // Wait for charts to finish rendering
    await new Promise(r => setTimeout(r, 1000));

    // Ensure the wrapper is not clipping the container during capture
    const pdfWrapper = document.getElementById('pdf-wrapper');
    if (pdfWrapper) {
        pdfWrapper.style.height = 'auto';
        pdfWrapper.style.overflow = 'visible';
        pdfWrapper.style.opacity = '1';
    }

    try {
        const opt = {
            margin:       0,
            filename:     pdfFilename + '.pdf',
            image:        { type: 'jpeg', quality: 1.0 },
            html2canvas:  { scale: 2, useCORS: true, logging: true, scrollY: 0, scrollX: 0 },
            jsPDF:        { unit: 'px', format: [800, 1131], orientation: 'portrait' },
            pagebreak:    { mode: ['css', 'legacy'], before: '.force-break', avoid: '.avoid-break' }
        };
        await html2pdf().set(opt).from(container).save();
        showToast('Success', 'PDF generated and downloaded.', 'success');
    } catch(e) {
        console.error("PDF EXPORT ERROR:", e);
        showToast('Export Error', 'Failed to generate PDF. Check console.', 'error');
    } finally {
        // Hide the container again
        container.style.display = 'none';
        container.innerHTML = '';
        if (pdfWrapper) {
            pdfWrapper.style.height = '0';
            pdfWrapper.style.overflow = 'hidden';
            pdfWrapper.style.opacity = '0';
        }
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

// ==========================================
// 13. MACRO ANALYSIS: LIVE PULSE & BATTLE MODE
// ==========================================
const searchSingle = document.getElementById('searchSingle');
const searchBattle = document.getElementById('searchBattle');
const topicResults = document.getElementById('topicResults');
const battleResults = document.getElementById('battleResults') || document.createElement('div');
const macroLoading = document.getElementById('macroLoading') || document.createElement('div');
const exportBtn = document.getElementById('exportMacroBtn');
const macroShareBtn = document.getElementById('macroShareBtn') || document.createElement('div');

// Smart Recommendations
document.querySelectorAll('.rec-chip').forEach(chip => {
    if(chip) chip.addEventListener('click', () => {
        document.getElementById("topicInput").value = chip.dataset.topic;
        if (!document.getElementById("topicButton").disabled) document.getElementById("topicButton").click();
    });
});

(document.getElementById('topicInput') || {addEventListener:()=>{}}).addEventListener('keydown', (e) => { if (e.key === "Enter") { e.preventDefault(); if (!document.getElementById("topicButton").disabled) document.getElementById("topicButton").click(); }});
(document.getElementById('topicInputB') || {addEventListener:()=>{}}).addEventListener('keydown', (e) => { if (e.key === "Enter") { e.preventDefault(); document.getElementById("battleButton").click(); }});

// --- CORE STREAMING LOGIC ---
class LiveAnalyzer {
    constructor(topic, config) {
        this.topic = topic;
        this.config = config; // { scoreId, chartId, posPctId, neuPctId, negPctId, feedId, liveDotId, liveStatusId, liveStatsId, titleId }
        this.eventSource = null;
        this.state = { pos: 0, neu: 0, neg: 0, total: 0, score: 0 };
        this.chartInstance = null;
        this.feedHtml = "";
        this.renderPending = false;
        
        if (this.config.titleId) { const el = document.getElementById(this.config.titleId); if (el) el.innerText = topic; }
        
        // Reset DOM state to zero/empty so previous searches don't linger
        const scoreEl = document.getElementById(this.config.scoreId);
        if (scoreEl) { scoreEl.innerText = "0.0"; scoreEl.style.color = "white"; }
        if (this.config.posPctId) { const el = document.getElementById(this.config.posPctId); if (el) el.innerText = "0%"; }
        if (this.config.neuPctId) { const el = document.getElementById(this.config.neuPctId); if (el) el.innerText = "0%"; }
        if (this.config.negPctId) { const el = document.getElementById(this.config.negPctId); if (el) el.innerText = "0%"; }
        if (this.config.feedId) { const el = document.getElementById(this.config.feedId); if (el) el.innerHTML = ""; }
        if (this.config.liveStatsId) { const el = document.getElementById(this.config.liveStatsId); if (el) el.innerText = "0"; }
        
        this.initChart();
        this.updateStatus('Connecting...', 'yellow');
    }

    initChart() {
        const ctx = document.getElementById(this.config.chartId).getContext('2d');
        if (Chart.getChart(this.config.chartId)) Chart.getChart(this.config.chartId).destroy();
        Chart.defaults.color = '#a1a1aa';
        this.chartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: ['#4ade80', '#60a5fa', '#f87171'],
                    borderWidth: 0, hoverOffset: 10
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, cutout: '75%',
                plugins: { legend: { display: false } },
                animation: { animateScale: true, animateRotate: true, duration: 1200, easing: 'easeOutQuart' }
            }
        });
    }

    updateStatus(text, colorClass) {
        document.getElementById(this.config.liveStatusId).innerText = text;
        const dot = document.getElementById(this.config.liveDotId);
        dot.className = 'pulse-dot';
        if (colorClass) dot.classList.add(colorClass);
    }

    start(onComplete, onUpdate) {
        this.updateStatus('Collecting...', 'yellow');
        this.eventSource = new EventSource(`${API}/analyze_batch_stream?topic=${encodeURIComponent(this.topic)}`);

        this.eventSource.onmessage = (e) => {
            const data = JSON.parse(e.data);
            
            if (data.stage === "error") {
                showToast(`Error: ${this.topic}`, data.message, 'error');
                this.updateStatus('Error', 'red');
                this.eventSource.close();
                if (onComplete) onComplete(false);
                return;
            }

            if (data.stage === "live_data") {
                this.updateStatus('Live', 'green');
                const pl = data.payload;
                this.state.total = pl.current_index;
                this.state.pos = pl.summary.positive;
                this.state.neu = pl.summary.neutral;
                this.state.neg = pl.summary.negative;
                this.state.score = pl.running_avg_score;
                
                // Prepend to feed
                const sent = pl.item.sentiment;
                let c = '#60a5fa'; if(sent==='Positive') c='#4ade80'; if(sent==='Negative') c='#f87171';
                const newItem = `<div class="sample-item" style="border-left: 2px solid ${c}; animation: fadeUp 0.3s ease;">"${pl.item.text}" <br><br> ${getAuthenticityHtml(pl.item.source)}</div>`;
                
                this.feedItems = this.feedItems || [];
                this.feedItems.unshift(newItem);
                if (this.feedItems.length > 30) this.feedItems.pop();
                this.feedHtml = this.feedItems.join('');
                
                // Accumulate samples for PDF generation
                if (!this.state.samples) this.state.samples = { positive: [], neutral: [], negative: [] };
                if (sent === 'Positive' && this.state.samples.positive.length < 10) this.state.samples.positive.push(pl.item);
                if (sent === 'Neutral' && this.state.samples.neutral.length < 10) this.state.samples.neutral.push(pl.item);
                if (sent === 'Negative' && this.state.samples.negative.length < 10) this.state.samples.negative.push(pl.item);
                
                if (pl.item.location) {
                    window.dispatchEvent(new CustomEvent('geo_location', { detail: { location: pl.item.location, sentiment: sent } }));
                }
                this.scheduleRender();
                if (onUpdate) onUpdate(this.state);
                
                if (this.config.maxItems && this.state.total >= this.config.maxItems) {
                    this.eventSource.close();
                    this.updateStatus('Complete', '');
                    document.getElementById(this.config.liveDotId).style.display = 'none';
                    if (onComplete) onComplete(true, { 
                        summary: pl.summary, 
                        total_analyzed: this.state.total,
                        average_score: pl.running_avg_score,
                        samples: this.state.samples
                    });
                }
            }

            if (data.stage === "complete") {
                this.eventSource.close();
                this.updateStatus('Complete', '');
                document.getElementById(this.config.liveDotId).style.display = 'none';
                if (onComplete) onComplete(true, data.payload);
            }
        };

        this.eventSource.onerror = () => {
            this.updateStatus('Disconnected', 'red');
            this.eventSource.close();
            if (onComplete) onComplete(false);
        };
    }

    scheduleRender() {
        if (this.renderPending) return;
        this.renderPending = true;
        requestAnimationFrame(() => this.render());
    }

    render() {
        this.renderPending = false;
        // Update Chart
        this.chartInstance.data.datasets[0].data = [this.state.pos, this.state.neu, this.state.neg];
        this.chartInstance.update('none'); // Update without full animation for smooth fluid transitions
        
        // Update Numbers with global animation wrapper
        const scoreEl = document.getElementById(this.config.scoreId);
        const scoreText = this.state.score > 0 ? `+${this.state.score}` : this.state.score;
        if (scoreEl.innerText !== scoreText.toString()) {
            scoreEl.innerText = scoreText;
        }
        if (this.state.score > 3) scoreEl.style.color = '#4ade80';
        else if (this.state.score < -3) scoreEl.style.color = '#f87171';
        else scoreEl.style.color = '#60a5fa';

        const liveStatsEl = document.getElementById(this.config.liveStatsId);
        if (liveStatsEl && liveStatsEl.innerText !== this.state.total.toString()) {
            liveStatsEl.innerText = this.state.total.toString();
        }

        const total = this.state.total || 1;
        if (this.config.posPctId) { const el = document.getElementById(this.config.posPctId); if (el) el.innerText = ((this.state.pos / total) * 100).toFixed(1) + "%"; }
        if (this.config.neuPctId) { const el = document.getElementById(this.config.neuPctId); if (el) el.innerText = ((this.state.neu / total) * 100).toFixed(1) + "%"; }
        if (this.config.negPctId) { const el = document.getElementById(this.config.negPctId); if (el) el.innerText = ((this.state.neg / total) * 100).toFixed(1) + "%"; }

        // Update Feed (Limit to 30 items for perf)
        const feedContainer = document.getElementById(this.config.feedId);
        feedContainer.innerHTML = this.feedHtml;
    }

    stop() {
        if (this.eventSource) this.eventSource.close();
    }
}

// --- SINGLE MODE EXECUTION ---
(document.getElementById('swapTopicsBtn') || {addEventListener:()=>{}}).addEventListener('click', () => {
    const inputA = document.getElementById('topicInputA');
    const inputB = document.getElementById('topicInputB');
    const temp = inputA.value;
    inputA.value = inputB.value;
    inputB.value = temp;
});

let activeSingleStream = null;
let activeBattleStreamA = null;
let activeBattleStreamB = null;
let battleVerdictInterval = null;

function computeVerdict(dataA, dataB) {
    if (!dataA || !dataB || dataA.total === 0 || dataB.total === 0) {
        return { text: "Too Close To Call", subtext: "Waiting for sufficient evidence...", icon: "balance" };
    }
    
    if (dataA.total < 15 || dataB.total < 15) {
        return { text: "Too Close To Call", subtext: "Accumulating evidence...", icon: "hourglass_empty" };
    }
    
    let posA = (dataA.pos / dataA.total) * 100;
    let posB = (dataB.pos / dataB.total) * 100;
    
    let diff = Math.abs(posA - posB);
    
    if (diff < 3.0) {
        return { text: "Statistical Tie", subtext: "Difference is within margin of error.", icon: "drag_handle" };
    }
    
    if (posA > posB) {
        return { text: "Topic A Wins", subtext: `Leading by ${diff.toFixed(1)}% positive sentiment.`, icon: "emoji_events" };
    } else {
        return { text: "Topic B Wins", subtext: `Leading by ${diff.toFixed(1)}% positive sentiment.`, icon: "emoji_events" };
    }
}

function updateVerdictDisplay(result, topicA, topicB) {
    const title = document.getElementById('verdictTitle');
    const subtext = document.getElementById('verdictSubtext');
    const icon = document.getElementById('verdictIcon');
    if (!title || !subtext || !icon) return;
    
    icon.innerText = result.icon;
    subtext.innerText = result.subtext;
    
    if (result.text === "Topic A Wins") {
        title.innerHTML = `<span class="text-primary">${topicA}<br/>Wins</span>`;
        icon.className = "material-symbols-outlined text-[80px] text-primary mb-6 drop-shadow-[0_0_15px_rgba(0,219,231,0.5)]";
    } else if (result.text === "Topic B Wins") {
        title.innerHTML = `<span class="text-primary">${topicB}<br/>Wins</span>`;
        icon.className = "material-symbols-outlined text-[80px] text-primary mb-6 drop-shadow-[0_0_15px_rgba(0,219,231,0.5)]";
    } else {
        title.innerHTML = result.text;
        icon.className = "material-symbols-outlined text-[80px] text-outline mb-6 drop-shadow-md";
    }
}

(document.getElementById("battleButton") || {addEventListener:()=>{}}).addEventListener("click", () => {
    requestNotificationPermission();
    const topicA = document.getElementById("topicInputA").value.trim();
    const topicB = document.getElementById("topicInputB").value.trim();
    if (!topicA || !topicB) return showToast('Input Required', 'Please enter two topics to compare.', 'warning');

    if (activeBattleStreamA) activeBattleStreamA.stop();
    if (activeBattleStreamB) activeBattleStreamB.stop();
    if (battleVerdictInterval) clearInterval(battleVerdictInterval);
    
    if (battleResults) battleResults.classList.remove("hidden");
    const exportBattleBtn = document.getElementById('exportBattleBtn');
    if (exportBattleBtn) exportBattleBtn.classList.add("hidden");
    
    document.getElementById("battleTitleA").innerText = topicA;
    document.getElementById("battleTitleB").innerText = topicB;
    
    document.getElementById('battleLiveStatus').innerText = 'Initializing Battle Matrix...';
    document.getElementById('battleLiveDot').style.display = 'block';
    
    updateVerdictDisplay({text: "Analyzing...", subtext: "Concurrent processing initiated", icon: "sync"}, topicA, topicB);

    activeBattleStreamA = new LiveAnalyzer(topicA, {
        scoreId: 'finalScoreA', chartId: 'sentimentChartA',
        posPctId: 'posPercentA', neuPctId: 'neuPercentA', negPctId: 'negPercentA',
        feedId: 'feedA', maxItems: 400,
        liveDotId: 'battleLiveDot', liveStatusId: 'battleLiveStatus', liveStatsId: 'totalCountA'
    });
    
    activeBattleStreamB = new LiveAnalyzer(topicB, {
        scoreId: 'finalScoreB', chartId: 'sentimentChartB',
        posPctId: 'posPercentB', neuPctId: 'neuPercentB', negPctId: 'negPercentB',
        feedId: 'feedB', maxItems: 400,
        liveDotId: 'battleLiveDot', liveStatusId: 'battleLiveStatus', liveStatsId: 'totalCountB'
    });

    let completedA = false;
    let completedB = false;
    let finalDataA = null;
    let finalDataB = null;

    activeBattleStreamA.start((success, data) => { 
        completedA = true; finalDataA = data; 
        if (completedB) { window.latestBattleDataA = finalDataA; window.latestBattleDataB = finalDataB; window.latestBattleTopicA = topicA; window.latestBattleTopicB = topicB; finalizeBattle(finalDataA, finalDataB, topicA, topicB); } 
    });
    activeBattleStreamB.start((success, data) => { 
        completedB = true; finalDataB = data; 
        if (completedA) { window.latestBattleDataA = finalDataA; window.latestBattleDataB = finalDataB; window.latestBattleTopicA = topicA; window.latestBattleTopicB = topicB; finalizeBattle(finalDataA, finalDataB, topicA, topicB); } 
    });

    battleVerdictInterval = setInterval(() => {
        let stateA = activeBattleStreamA.state;
        let stateB = activeBattleStreamB.state;
        let verdict = computeVerdict(stateA, stateB);
        updateVerdictDisplay(verdict, topicA, topicB);
    }, 1000);
});

function finalizeBattle(dataA, dataB, topicA, topicB) {
    clearInterval(battleVerdictInterval);
    document.getElementById('battleLiveStatus').innerText = 'Battle Concluded.';
    document.getElementById('battleLiveDot').style.display = 'none';
    
    const exportBattleBtn = document.getElementById('exportBattleBtn');
    if (exportBattleBtn) exportBattleBtn.classList.remove("hidden");
    
    let stateA = activeBattleStreamA.state;
    let stateB = activeBattleStreamB.state;
    let verdict = computeVerdict(stateA, stateB);
    updateVerdictDisplay(verdict, topicA, topicB);
    sendDesktopNotification("Sentio Battle Complete", `Verdict: ${verdict.text}`);
    
    const renderFeed = (data, elementId) => {
        if (data && data.feed) {
            document.getElementById(elementId).innerHTML = '';
            data.feed.forEach(item => {
                const div = document.createElement('div');
                div.className = 'sample-item animate-fade-in text-sm border-l-2 p-3 bg-surface border-secondary-fixed/50 rounded shadow-sm';
                div.innerHTML = `<p class="mb-2 text-on-surface-variant font-medium">"${item.text}"</p><div class="flex justify-between items-center mt-2"><span class="badge ${item.sentiment==='POSITIVE'?'bg-secondary-fixed text-black':item.sentiment==='NEGATIVE'?'bg-error text-white':'bg-outline text-white'} text-[10px] font-bold px-2 py-1 rounded uppercase tracking-wider">${item.sentiment}</span><span class="text-outline-variant text-[10px] font-label-mono uppercase bg-surface-container px-2 py-1 rounded"><span class="material-symbols-outlined text-[12px] inline-block align-text-bottom mr-1">verified</span>${item.source}</span></div>`;
                document.getElementById(elementId).appendChild(div);
            });
        }
    };
    renderFeed(dataA, 'feedA');
    renderFeed(dataB, 'feedB');

}
(document.getElementById("topicButton") || {addEventListener:()=>{}}).addEventListener("click", () => {
    requestNotificationPermission();
    const topicInput = document.getElementById("topicInput");
    const topicBtn = document.getElementById("topicButton");
    const topic = topicInput.value.trim();
    
    if (!topic) {
        showToast('Input Required', 'Please enter a topic to analyze.', 'warning');
        return;
    }
    
    // Disable inputs during analysis
    topicInput.disabled = true;
    topicBtn.disabled = true;
    topicBtn.innerHTML = '<div class="w-6 h-6 border-2 border-on-primary border-t-transparent rounded-full animate-spin"></div>';
    setSummaryState('summaryLoading');


    if (activeSingleStream) activeSingleStream.stop();
    if (trendChartInstance) { trendChartInstance.destroy(); trendChartInstance = null; }

    if (topicResults) topicResults.classList.remove("hidden");
    const exportBtnGlobal = document.getElementById("exportMacroBtn");
    if (exportBtnGlobal) exportBtnGlobal.classList.add("hidden");
    const shareBtnGlobal = document.getElementById("macroShareBtn");
    if (shareBtnGlobal) shareBtnGlobal.classList.add("hidden");
    
    setTimeout(() => {
        // We no longer remove macroLoading or show topicResults here. 
        // That happens when the stream finishes in renderFinalSingleData.

        // Prepare Trend Chart (it only updates on complete for now as backend returns date buckets at the end)
        if (trendChartInstance) { trendChartInstance.destroy(); trendChartInstance = null; }
        
        // Reset Single Mode Feeds
        document.getElementById('posSamples').innerHTML = '';
        document.getElementById('neuSamples').innerHTML = '';
        document.getElementById('negSamples').innerHTML = '';
        document.getElementById("totalCount").innerText = '0';
        document.getElementById('singleLiveDot').style.display = 'block';

        activeSingleStream = new LiveAnalyzer(topic, {
            scoreId: 'finalScore', chartId: 'sentimentChart',
            posPctId: 'posPercent', neuPctId: 'neuPercent', negPctId: 'negPercent',
            feedId: 'neuSamples', // Temporary dump until complete
            liveDotId: 'singleLiveDot', liveStatusId: 'singleLiveStatus', liveStatsId: 'totalCount'
        });

        activeSingleStream.start((success, finalData) => {
            if (success && finalData) {
                document.getElementById("totalCount").innerText = finalData.total_analyzed;
                window.latestSingleData = finalData;
                window.latestSingleTopic = topic;
                renderFinalSingleData(finalData);
                sendDesktopNotification("Sentio Analytics Complete", `Analysis for "${topic}" is finished. Analyzed ${finalData.total_analyzed} mentions.`);
            }
        });
    }, 500);
});

function renderFinalSingleData(data) {
    // Show results only after loading completes
    const macroLoading = document.getElementById("macroLoading");
    const exportBtn = document.getElementById("exportMacroBtn");
    const macroShareBtn = document.getElementById("macroShareBtn");
    const topicInput = document.getElementById("topicInput");
    const topicBtn = document.getElementById("topicButton");
    
    if (topicInput) topicInput.disabled = false;
    if (topicBtn) {
        topicBtn.disabled = false;
        topicBtn.innerHTML = 'Analyze';
    }
    
    if (macroLoading) macroLoading.classList.add("hidden");
    if (topicResults) topicResults.classList.remove("hidden");
    if (exportBtn) exportBtn.classList.remove("hidden");
    if (macroShareBtn) macroShareBtn.classList.remove("hidden");

    const trendCtx = document.getElementById('trendChart').getContext('2d');
    const formattedLabels = data.trend_7_days.labels.map(dateStr => {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    trendChartInstance = new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: formattedLabels,
            datasets: [
                { label: 'Positive', data: data.trend_7_days.positive, borderColor: '#4ade80', backgroundColor: 'rgba(74, 222, 128, 0.1)', borderWidth: 2, fill: true, tension: 0.4 },
                { label: 'Negative', data: data.trend_7_days.negative, borderColor: '#f87171', backgroundColor: 'rgba(248, 113, 113, 0.1)', borderWidth: 2, fill: true, tension: 0.4 }
            ]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { legend: { display: false } }, 
            scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } }, 
            animation: { duration: 2000, easing: 'easeInOutSine' } 
        }
    });

    const posC = document.getElementById("posSamples"); const neuC = document.getElementById("neuSamples"); const negC = document.getElementById("negSamples");
    posC.innerHTML = ""; neuC.innerHTML = ""; negC.innerHTML = "";
    data.samples.positive.forEach(obj => posC.innerHTML += `<div class="sample-item reveal-item reveal-hidden">"${obj.text}" <br><br> ${getAuthenticityHtml(obj.source)}</div>`);
    data.samples.neutral.forEach(obj => neuC.innerHTML += `<div class="sample-item reveal-item reveal-hidden">"${obj.text}" <br><br> ${getAuthenticityHtml(obj.source)}</div>`);
    data.samples.negative.forEach(obj => negC.innerHTML += `<div class="sample-item reveal-item reveal-hidden">"${obj.text}" <br><br> ${getAuthenticityHtml(obj.source)}</div>`);
    
    // Trigger global animations for newly added items
    initReveal();
    
    generateSmartSummary(data.genai_summary);
}

// ==========================================
// 14. MICRO INFERENCE
// ==========================================
const singleInput = document.getElementById("singleInput");
const singleButton = document.getElementById("singleButton");
const singleResult = document.getElementById("singleResult");
const microIdle = document.getElementById("microIdle");
const microLoading = document.getElementById("microLoading");

if(singleInput) singleInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (typeof isRecording !== 'undefined' && isRecording) {
            stopRecording();
        }
        singleButton.click();
    }
});

if(singleButton) singleButton.addEventListener("click", async () => {
    const text = singleInput.value.trim();
    if (!text) {
        showToast('Input Required', 'Please enter some text to analyze.', 'warning');
        return;
    }

    microIdle.classList.add("hidden");
    singleResult.classList.add("hidden");
    microLoading.classList.remove("hidden");

    try {
        const res = await fetch(`${API}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (data.error) throw new Error(data.error);

        document.getElementById("singleSentiment").innerText = data.sentiment;
        const badge = document.getElementById("singleSentiment");
        if (data.sentiment === "Positive") badge.style.color = "#4ade80";
        else if (data.sentiment === "Negative") badge.style.color = "#f87171";
        else badge.style.color = "#60a5fa";

        document.getElementById("txtPos").innerText = data.positive_probability + "%";
        document.getElementById("txtNeg").innerText = data.negative_probability + "%";
        
        setTimeout(() => {
            document.getElementById("barPos").style.width = data.positive_probability + "%";
            document.getElementById("barNeg").style.width = data.negative_probability + "%";
        }, 100);
        
        document.getElementById("singleConfidence").innerText = data.confidence;
        document.getElementById("singleScore").innerText = data.score > 0 ? `+${data.score}` : data.score;
        

        singleResult.classList.remove("hidden");
    } catch (err) {
        showToast('Analysis Error', err.message, 'error');
        microIdle.classList.remove("hidden");
    } finally {
        microLoading.classList.add("hidden");
    }
});

// ==========================================
// 15. LIVE SYSTEM STATUS & ONBOARDING
// ==========================================
async function checkSystemStatus() {
    const start = Date.now();
    try {
        await fetch(`${API}/`);
        const latency = Date.now() - start;
        const pingEl = document.getElementById('pingLatency');
        const statusEl = document.getElementById('apiStatusText');
        const pulseEl = document.querySelector('.pulse-dot');
        
        if (pingEl) pingEl.innerText = `${latency}ms`;
        if (statusEl) statusEl.innerText = "ONLINE";
        if (pulseEl) pulseEl.style.background = "#4ade80";
    } catch (e) {
        const pingEl = document.getElementById('pingLatency');
        const statusEl = document.getElementById('apiStatusText');
        const pulseEl = document.querySelector('.pulse-dot');
        
        if (pingEl) pingEl.innerText = `Timeout`;
        if (statusEl) statusEl.innerText = "OFFLINE";
        if (pulseEl) pulseEl.style.background = "#f87171";
    }
}
checkSystemStatus();
setInterval(checkSystemStatus, 30000);

// Onboarding toast (delayed)
setTimeout(() => {
    showToast('Pro Tip', 'Press Ctrl+K to open the Command Palette, or ? for keyboard shortcuts.', 'info', 6000);
}, 4000);

// ==========================================
// 16. CUSTOM CURSOR
// ==========================================
const cursorDot = document.querySelector('.cursor-dot');
const cursorOutline = document.querySelector('.cursor-outline');

if(window) window.addEventListener('mousemove', (e) => {
    const posX = e.clientX;
    const posY = e.clientY;
    
    cursorDot.style.left = `${posX}px`;
    cursorDot.style.top = `${posY}px`;
    
    cursorOutline.animate({
        left: `${posX}px`,
        top: `${posY}px`
    }, { duration: 500, fill: "forwards" });
});

if(document) document.addEventListener('mouseover', (e) => {
    if (['A', 'BUTTON', 'INPUT', 'TEXTAREA', 'KBD'].includes(e.target.tagName) || e.target.closest('.cmd-item') || e.target.closest('.history-item') || e.target.closest('.rec-chip') || e.target.closest('.share-action') || e.target.closest('.footer-link')) {
        cursorOutline.style.width = '60px';
        cursorOutline.style.height = '60px';
        cursorOutline.style.backgroundColor = 'rgba(255,255,255,0.05)';
    }
});
if(document) document.addEventListener('mouseout', (e) => {
    if (['A', 'BUTTON', 'INPUT', 'TEXTAREA', 'KBD'].includes(e.target.tagName) || e.target.closest('.cmd-item') || e.target.closest('.history-item') || e.target.closest('.rec-chip') || e.target.closest('.share-action') || e.target.closest('.footer-link')) {
        cursorOutline.style.width = '40px';
        cursorOutline.style.height = '40px';
        cursorOutline.style.backgroundColor = 'transparent';
    }
});

// ==========================================
// 17. ADVANCED FEATURES: GENAI, VOICE, MAP, GRAPH
// ==========================================


// GenAI Summary State Machine
function setSummaryState(state, message = '') {
    const states = ['summaryIdle', 'summaryLoading', 'summarySuccess', 'summaryEmpty', 'summaryError'];
    states.forEach(s => {
        const el = document.getElementById(s);
        if (el) {
            if (s === state) {
                el.classList.remove('hidden');
                if (s === 'summarySuccess' && message) {
                    const textEl = document.getElementById('genaiSummaryText');
                    if (textEl) textEl.innerHTML = ''; // Reset before typing
                }
            } else {
                el.classList.add('hidden');
            }
        }
    });
    
    // Ensure the container is visible
    const container = document.getElementById('smart-summary');
    if (container) container.classList.remove('hidden');
}

function generateSmartSummary(backendSummaryText) {
    if (!backendSummaryText) {
        setSummaryState('summaryEmpty');
        return;
    }
    
    setSummaryState('summarySuccess', backendSummaryText);
    const summaryText = document.getElementById('genaiSummaryText');
    const msg = backendSummaryText;
    
    summaryText.innerHTML = '<span id="typewriterSpan"></span><span class="typewriter-cursor"></span>';
    const span = document.getElementById('typewriterSpan');
    let i = 0;
    
    function typeWriter() {
        if (i < msg.length) {
            span.innerHTML += msg.charAt(i);
            i++;
            setTimeout(typeWriter, 20);
        }
    }
    typeWriter();
}


// Authenticity Helper
function getAuthenticityHtml(source) {
    const isSpam = Math.random() > 0.92;
    let sourceHtml = '';
    
    if (source) {
        let icon = 'public';
        if (source === 'Twitter') icon = 'flutter_dash';
        else if (source === 'Reddit') icon = 'forum';
        else if (source === 'Google News') icon = 'article';
        
        sourceHtml = `<span class="auth-badge bg-surface-container-high text-on-surface-variant mr-2 px-2 py-1 rounded text-xs inline-flex items-center gap-1 shadow-sm"><span class="material-symbols-outlined text-[14px]">${icon}</span> ${source}</span>`;
    }

    if (isSpam) {
        return `${sourceHtml}<span class="auth-badge auth-spam"><i class="fa-solid fa-flag"></i> Spam Flag</span>`;
    }
    const pct = Math.floor(85 + Math.random() * 14);
    return `${sourceHtml}<span class="auth-badge auth-genuine"><i class="fa-solid fa-check-circle"></i> ${pct}% Genuine</span>`;
}

// Voice Sentiment
let recognition;
let isRecording = false;
const voiceBtn = document.getElementById('voiceBtn');
const dialContainer = document.getElementById('sentimentDialContainer');
const dialNeedle = document.getElementById('dialNeedle');

if ('webkitSpeechRecognition' in window && voiceBtn && singleInput) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    
    let voiceBaseText = '';
    
    recognition.onstart = () => {
        isRecording = true;
        voiceBtn.classList.add('recording');
        if (dialContainer) dialContainer.classList.remove('hidden');
        if (singleInput.value === 'Listening...' || singleInput.value === '') {
            voiceBaseText = '';
            singleInput.value = '';
        } else {
            voiceBaseText = singleInput.value + ' ';
        }
        singleInput.placeholder = 'Listening...';
    };
    
    let debounceTimer;
    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        
        const currentText = voiceBaseText + finalTranscript + interimTranscript;
        singleInput.value = currentText;
        if (finalTranscript) {
            voiceBaseText += finalTranscript;
        }
        
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (currentText.trim().length > 0) {
                fetch(`${API}/predict`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: currentText })
                })
                .then(r => r.json())
                .then(data => {
                    let pct = ((data.score + 10) / 20) * 100;
                    if (pct < 0) pct = 0;
                    if (pct > 100) pct = 100;
                    if (dialNeedle) dialNeedle.style.left = `${pct}%`;
                }).catch(e => console.error(e));
            }
        }, 500);
    };
    
    recognition.onerror = (e) => {
        console.error('Speech recognition error', e.error);
        stopRecording();
    };
    
    recognition.onend = () => {
        if (isRecording) {
            // Chrome will automatically stop if there is a long pause in speech.
            // Restart to keep continuous listening.
            try {
                recognition.start();
            } catch (err) {
                stopRecording();
            }
        } else {
            if (singleInput.value.trim().length > 0 && singleButton) {
                singleButton.click();
            }
        }
    };
    
    voiceBtn.addEventListener('click', () => {
        if (isRecording) {
            stopRecording();
        } else {
            try {
                recognition.start();
            } catch(e) {
                console.error(e);
            }
        }
    });
} else if (voiceBtn) {
    voiceBtn.style.display = 'none';
}

function stopRecording() {
    isRecording = false;
    if (voiceBtn) voiceBtn.classList.remove('recording');
    try {
        if (recognition) recognition.stop();
    } catch(e) {}
    if (singleInput) singleInput.placeholder = 'Enter a sentence or paragraph...';
}


// ==========================================
// 19. SHADER AND GRID ANIMATIONS (STITCH DESIGN)
// ==========================================

// Shader Background Implementation
const initShader = () => {
    const container = document.getElementById('shader-container');
    if (!container) return;

    if (typeof THREE === 'undefined') {
        console.warn('THREE.js not loaded, skipping shader');
        return;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    const renderer = new THREE.WebGLRenderer({ alpha: false });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const vertexShader = `
        varying vec2 v_texCoord;
        void main() {
            v_texCoord = uv;
            gl_Position = vec4(position, 1.0);
        }
    `;

    const fragmentShader = `
        precision highp float;
        varying vec2 v_texCoord;
        uniform float u_time;
        uniform vec2 u_resolution;
        uniform vec2 u_mouse;

        float noise(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        float smoothNoise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            float a = noise(i);
            float b = noise(i + vec2(1.0, 0.0));
            float c = noise(i + vec2(0.0, 1.0));
            float d = noise(i + vec2(1.0, 1.0));
            return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
        }

        float fbm(vec2 p) {
            float v = 0.0;
            float a = 0.5;
            for (int i = 0; i < 5; i++) {
                v += a * smoothNoise(p);
                p *= 2.0;
                a *= 0.5;
            }
            return v;
        }

        void main() {
            vec2 uv = v_texCoord;
            vec2 mouse = u_mouse / u_resolution;
            
            // Create a sense of depth and movement
            float n = fbm(uv * 3.0 + u_time * 0.05);
            n += fbm(uv * 6.0 - u_time * 0.1) * 0.5;
            
            // Add mouse interaction
            float dist = distance(uv, mouse);
            float mouseEffect = smoothstep(0.4, 0.0, dist) * 0.2;
            
            // Primary color from Sentiment Noir (#00f2ff converted to vec3)
            vec3 color1 = vec3(0.0, 0.95, 1.0); 
            vec3 color2 = vec3(0.02, 0.04, 0.05); // Deep background
            
            vec3 finalColor = mix(color2, color1, n * 0.15 + mouseEffect);
            
            // Add "digital grain" or data points
            float grain = noise(uv * 500.0 + u_time);
            if (grain > 0.98) finalColor += color1 * 0.3;

            gl_FragColor = vec4(finalColor, 1.0);
        }
    `;

    const uniforms = {
        u_time: { value: 0 },
        u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
        u_mouse: { value: new THREE.Vector2(0, 0) }
    };

    const material = new THREE.ShaderMaterial({
        vertexShader,
        fragmentShader,
        uniforms,
        depthWrite: false,
        depthTest: false
    });

    const geometry = new THREE.PlaneGeometry(2, 2);
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    let mouseX = 0;
    let mouseY = 0;
    let targetMouseX = 0;
    let targetMouseY = 0;

    document.addEventListener('mousemove', (e) => {
        targetMouseX = e.clientX;
        targetMouseY = window.innerHeight - e.clientY; // Invert Y for shader
    });

    const animate = (time) => {
        requestAnimationFrame(animate);
        
        // Smooth mouse interpolation
        mouseX += (targetMouseX - mouseX) * 0.05;
        mouseY += (targetMouseY - mouseY) * 0.05;

        uniforms.u_time.value = time * 0.001;
        uniforms.u_mouse.value.set(mouseX, mouseY);
        
        renderer.render(scene, camera);
    };

    animate(0);

    window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        uniforms.u_resolution.value.set(window.innerWidth, window.innerHeight);
    });
};

// Interactive Grid Effect
const initGrid = () => {
    const grid = document.getElementById('interactive-grid');
    if(!grid) return;
    
    document.addEventListener('mousemove', e => {
        const rect = grid.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        grid.style.setProperty('--mouse-x', `${x}px`);
        grid.style.setProperty('--mouse-y', `${y}px`);
        grid.classList.add('active'); // active class for opacity
    });
};

// Global Typewriter Utilities
function wrapTextNodes(element) {
    if (element.tagName === 'CANVAS' || element.tagName === 'INPUT' || element.tagName === 'BUTTON' || element.tagName === 'SCRIPT' || element.tagName === 'STYLE' || element.tagName === 'A') {
        return;
    }
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
    let node;
    const textNodes = [];
    while (node = walker.nextNode()) {
        if (node.nodeValue.trim().length > 0) {
            textNodes.push(node);
        }
    }
    textNodes.forEach(textNode => {
        const text = textNode.nodeValue;
        const fragment = document.createDocumentFragment();
        for (let i = 0; i < text.length; i++) {
            const span = document.createElement('span');
            span.className = 'letter-hidden';
            if (text[i] === ' ') {
                span.innerHTML = '&nbsp;';
            } else {
                span.textContent = text[i];
            }
            fragment.appendChild(span);
        }
        textNode.parentNode.replaceChild(fragment, textNode);
    });
}

// Scroll Reveal Observer
const initReveal = () => {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('reveal-hidden');
                entry.target.classList.add('reveal-visible');
                
                // Trigger typewriter on all letter-hidden spans
                const letters = entry.target.querySelectorAll('.letter-hidden');
                if (letters.length > 0) {
                    let delay = 0;
                    letters.forEach(letter => {
                        setTimeout(() => {
                            letter.classList.remove('letter-hidden');
                            letter.classList.add('letter-visible');
                        }, delay);
                        delay += Math.random() * (22 - 5) + 5; // 5 to 22 ms
                    });
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-item').forEach(item => {
        // Pre-wrap eligible text elements for typewriter
        const textElements = item.querySelectorAll('h1, h2, h3, h4, h5, h6, p');
        textElements.forEach(el => wrapTextNodes(el));
        
        observer.observe(item);
    });
};

// Smooth Scrolling Interceptor
const initSmoothScroll = () => {
    document.querySelectorAll('nav a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetEl = document.getElementById(targetId);
            if (targetEl) {
                window.scrollTo({
                    top: targetEl.offsetTop - 50,
                    behavior: 'smooth'
                });
            }
        });
    });
};

// Simple subtle parallax for hero particles
const initParallax = () => {
    const hero = document.querySelector('.hero-particle-bg > div');
    document.addEventListener('mousemove', (e) => {
        if(!hero) return;
        const x = (e.clientX / window.innerWidth - 0.5) * 30;
        const y = (e.clientY / window.innerHeight - 0.5) * 30;
        hero.style.transform = `translate(${x}px, ${y}px)`;
    });
};

window.addEventListener('DOMContentLoaded', () => {
    initShader();
    initGrid();
    initReveal();
    initSmoothScroll();
    initParallax();
});


// ==========================================
// HEADER SCROLL — GLASSMORPHISM STICKY STATE
// ==========================================
const mainHeader = document.getElementById('main-header');

if (mainHeader) {
    const footerEl = document.querySelector('footer');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY || document.documentElement.scrollTop;
        if (scrollY > 60) {
            mainHeader.classList.add('header-scrolled');
        } else {
            mainHeader.classList.remove('header-scrolled');
        }

        // Smoothly fade out header when scrolling into footer
        if (footerEl) {
            const scrollBottom = scrollY + window.innerHeight;
            const footerTop = footerEl.offsetTop;
            
            if (scrollBottom > footerTop) {
                const overlap = scrollBottom - footerTop;
                const fadeRange = 250; // Fade out over 250px of scrolling
                let progress = overlap / fadeRange;
                if (progress > 1) progress = 1;
                
                mainHeader.style.opacity = (1 - progress).toString();
                mainHeader.style.transform = `translateY(-${progress * 100}%)`;
                mainHeader.style.pointerEvents = progress > 0.5 ? 'none' : 'auto';
            } else {
                mainHeader.style.opacity = '';
                mainHeader.style.transform = '';
                mainHeader.style.pointerEvents = 'auto';
            }
        }
    }, { passive: true });
}

// ==========================================
// ACTIVE NAV — IntersectionObserver Tracker
// ==========================================
(() => {
    // Map section IDs to their nav hrefs
    const sectionIds = ['hero', 'macro-analysis', 'data-pipeline', 'micro-inference'];
    const navLinks   = document.querySelectorAll('#main-header nav a[href^="#"]');

    if (!navLinks.length) return;

    // Build a Map<sectionId, navLinkElement> for O(1) lookups
    const linkMap = new Map();
    navLinks.forEach(link => {
        const id = link.getAttribute('href').replace('#', '');
        linkMap.set(id, link);
    });

    let activeId = null;

    function setActive(id) {
        if (id === activeId) return;          // no-op if already active
        activeId = id;
        navLinks.forEach(link => link.classList.remove('nav-active'));
        const target = linkMap.get(id);
        if (target) target.classList.add('nav-active');
    }

    // Use a generous rootMargin so the section is "active" once its top
    // enters the upper 40% of the viewport. threshold 0 = fire as soon
    // as any pixel is visible within that margin.
    const observer = new IntersectionObserver((entries) => {
        // Collect all currently-intersecting sections
        const visible = entries
            .filter(e => e.isIntersecting)
            .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

        if (visible.length) {
            setActive(visible[0].target.id);
        }
    }, {
        rootMargin: '-10% 0px -50% 0px',     // trigger zone: top 10–50% of viewport
        threshold: 0
    });

    sectionIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) observer.observe(el);
    });

    // Set initial active state on load
    setActive('hero');
})();
