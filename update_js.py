import sys
import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Hash Routing and Tabs
hash_routing = """
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
    const singleContent = document.getElementById('tabContentSingle');
    const battleContent = document.getElementById('tabContentBattle');
    const btnSingle = document.getElementById('tabBtnSingle');
    const btnBattle = document.getElementById('tabBtnBattle');
    
    if (tab === 'single') {
        singleContent.classList.remove('hidden');
        singleContent.classList.add('block');
        battleContent.classList.remove('block');
        battleContent.classList.add('hidden');
        
        btnSingle.classList.add('text-primary', 'border-primary');
        btnSingle.classList.remove('text-outline', 'border-transparent');
        btnBattle.classList.add('text-outline', 'border-transparent');
        btnBattle.classList.remove('text-primary', 'border-primary');
        
        // Update URL hash without jumping
        history.replaceState(null, null, '#macro-analysis?tab=single');
    } else {
        singleContent.classList.remove('block');
        singleContent.classList.add('hidden');
        battleContent.classList.remove('hidden');
        battleContent.classList.add('block');
        
        btnBattle.classList.add('text-primary', 'border-primary');
        btnBattle.classList.remove('text-outline', 'border-transparent');
        btnSingle.classList.add('text-outline', 'border-transparent');
        btnSingle.classList.remove('text-primary', 'border-primary');
        
        // Update URL hash without jumping
        history.replaceState(null, null, '#macro-analysis?tab=battle');
    }
};
"""

content = re.sub(
    r'// ==========================================\n// 1\. SPA ROUTING \(Feature 1\)\n// ==========================================.*?(?=// ==========================================\n// 2\. INTELLIGENT)',
    hash_routing.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

# 2. Update AI Summary State Machine
ai_summary_logic = """
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
"""

content = re.sub(
    r'// GenAI Summary\nfunction generateSmartSummary\(backendSummaryText\) \{.*?\}\n    typeWriter\(\);\n\}',
    ai_summary_logic.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

# 3. Add button disable states for Topic Button
content = content.replace(
    'document.getElementById("topicButton").click();',
    'if (!document.getElementById("topicButton").disabled) document.getElementById("topicButton").click();'
)

topic_click_orig = """(document.getElementById("topicButton") || {addEventListener:()=>{}}).addEventListener("click", () => {
    requestNotificationPermission();
    const topic = document.getElementById("topicInput").value.trim();
    if (!topic) {
        showToast('Input Required', 'Please enter a topic to analyze.', 'warning');
        return;
    }"""

topic_click_new = """(document.getElementById("topicButton") || {addEventListener:()=>{}}).addEventListener("click", () => {
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
"""
content = content.replace(topic_click_orig, topic_click_new)

# Re-enable on completion
single_completion_orig = """        if (exportBtnGlobal) exportBtnGlobal.classList.remove("hidden");
        if (shareBtnGlobal) shareBtnGlobal.classList.remove("hidden");
        showToast('Analysis Complete', `Finished analyzing "${topic}".`, 'success');
        document.getElementById('singleLiveDot').style.display = 'none';
        document.getElementById('singleLiveStatus').innerText = 'Analysis Complete';"""

single_completion_new = """        if (exportBtnGlobal) exportBtnGlobal.classList.remove("hidden");
        if (shareBtnGlobal) shareBtnGlobal.classList.remove("hidden");
        showToast('Analysis Complete', `Finished analyzing "${topic}".`, 'success');
        document.getElementById('singleLiveDot').style.display = 'none';
        document.getElementById('singleLiveStatus').innerText = 'Analysis Complete';
        
        // Re-enable inputs
        const topicInput = document.getElementById("topicInput");
        const topicBtn = document.getElementById("topicButton");
        if (topicInput) topicInput.disabled = false;
        if (topicBtn) {
            topicBtn.disabled = false;
            topicBtn.innerText = 'Analyze';
        }"""
content = content.replace(single_completion_orig, single_completion_new)

# Re-enable on error
single_error_orig = """    activeSingleStream.start();
});"""
single_error_new = """    activeSingleStream.start();
    
    // Safety timeout to re-enable button if something goes wrong
    setTimeout(() => {
        const topicBtn = document.getElementById("topicButton");
        if (topicBtn && topicBtn.disabled) {
            document.getElementById("topicInput").disabled = false;
            topicBtn.disabled = false;
            topicBtn.innerText = 'Analyze';
            setSummaryState('summaryError');
            showToast('Timeout', 'The analysis took too long. Please try again.', 'error');
            if (activeSingleStream) activeSingleStream.stop();
        }
    }, 45000);
});"""
content = content.replace(single_error_orig, single_error_new)


# 4. Update Battle Button
battle_click_orig = """(document.getElementById("battleButton") || {addEventListener:()=>{}}).addEventListener("click", () => {
    requestNotificationPermission();
    const topicA = document.getElementById("topicInputA").value.trim();
    const topicB = document.getElementById("topicInputB").value.trim();

    if (!topicA || !topicB) {
        showToast('Inputs Required', 'Please enter two topics to battle.', 'warning');
        return;
    }"""
    
battle_click_new = """(document.getElementById("battleButton") || {addEventListener:()=>{}}).addEventListener("click", () => {
    requestNotificationPermission();
    const inputA = document.getElementById("topicInputA");
    const inputB = document.getElementById("topicInputB");
    const battleBtn = document.getElementById("battleButton");
    const topicA = inputA.value.trim();
    const topicB = inputB.value.trim();

    if (!topicA || !topicB) {
        showToast('Inputs Required', 'Please enter two topics to battle.', 'warning');
        return;
    }
    
    if (topicA.toLowerCase() === topicB.toLowerCase()) {
        showToast('Invalid Battle', 'Topics must be different.', 'error');
        return;
    }

    inputA.disabled = true;
    inputB.disabled = true;
    battleBtn.disabled = true;
    battleBtn.innerHTML = '<div class="w-6 h-6 border-2 border-on-primary border-t-transparent rounded-full animate-spin"></div>';
    setSummaryState('summaryLoading');
"""
content = content.replace(battle_click_orig, battle_click_new)

battle_completion_orig = """            document.getElementById('battleLiveDot').style.display = 'none';
            document.getElementById('battleLiveStatus').innerText = 'Battle Complete';
            
            const exportBtnGlobal = document.getElementById("exportBattleBtn");"""

battle_completion_new = """            document.getElementById('battleLiveDot').style.display = 'none';
            document.getElementById('battleLiveStatus').innerText = 'Battle Complete';
            
            const inputA = document.getElementById("topicInputA");
            const inputB = document.getElementById("topicInputB");
            const battleBtn = document.getElementById("battleButton");
            if (inputA) inputA.disabled = false;
            if (inputB) inputB.disabled = false;
            if (battleBtn) {
                battleBtn.disabled = false;
                battleBtn.innerText = 'Analyze Battle';
            }
            
            const exportBtnGlobal = document.getElementById("exportBattleBtn");"""
content = content.replace(battle_completion_orig, battle_completion_new)


with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
