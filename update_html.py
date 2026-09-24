import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the Data Pipeline Title
content = content.replace(
    '<h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">Data Pipeline</h3>\n                    <p class="font-label-mono text-label-mono text-on-surface-variant uppercase tracking-widest">Ingest to Inference</p>',
    '<h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">How Sentio Works</h3>\n                    <p class="font-label-mono text-label-mono text-on-surface-variant uppercase tracking-widest">Educational Data Pipeline Overview</p>'
)

# 2. Restructure Macro Analysis
# We'll locate the start of Macro Analysis and the start of Smart Summary.
macro_start_str = """            <!-- Macro Analysis Section -->
            <section class="px-margin-mobile md:px-margin-desktop py-24 border-t border-outline-variant/10 relative scroll-mt-32" id="macro-analysis">
                <div class="absolute inset-0 bg-surface-container-low/50 backdrop-blur-sm -z-10"></div>
                <div class="mb-12 reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">Macro Analysis</h3>
                    <p class="font-label-mono text-label-mono text-primary uppercase tracking-widest">Global Sentiment Data</p>
                </div>"""

new_macro_start = """            <!-- Macro Analysis Section -->
            <section class="px-margin-mobile md:px-margin-desktop py-16 border-t border-outline-variant/10 relative scroll-mt-32" id="macro-analysis">
                <div class="absolute inset-0 bg-surface-container-low/50 backdrop-blur-sm -z-10"></div>
                
                <!-- PURPOSE / EXPLANATION -->
                <div class="mb-10 reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-4">Macro Analysis</h3>
                    <p class="font-body-lg text-on-surface-variant max-w-3xl leading-relaxed">
                        Analyze public sentiment around topics, compare subjects, and identify emerging trends across online conversations.
                    </p>
                    <div class="mt-6 flex items-center gap-2 text-sm text-outline font-label-mono uppercase tracking-widest">
                        <span>Need to classify one comment?</span>
                        <a href="#micro-inference" class="text-primary hover:underline font-bold flex items-center gap-1">Try Micro Inference <span class="material-symbols-outlined text-sm">arrow_forward</span></a>
                    </div>
                </div>

                <!-- PRIMARY ANALYSIS OPTIONS TABS -->
                <div class="flex gap-4 mb-8 border-b border-outline-variant/20 pb-4 reveal-item reveal-hidden">
                    <button id="tabBtnSingle" class="px-6 py-3 font-bold uppercase tracking-wider text-primary border-b-2 border-primary transition-all" onclick="switchMacroTab('single')">Single Analysis</button>
                    <button id="tabBtnBattle" class="px-6 py-3 font-bold uppercase tracking-wider text-outline hover:text-primary transition-all border-b-2 border-transparent" onclick="switchMacroTab('battle')">Battle Mode</button>
                </div>

                <!-- TAB CONTENT: SINGLE ANALYSIS -->
                <div id="tabContentSingle" class="block reveal-item reveal-hidden">"""
content = content.replace(macro_start_str, new_macro_start)

# Replace Single Analysis heading
content = content.replace(
    '<h4 class="font-bold text-2xl mb-4 text-primary reveal-item reveal-hidden">Single Analysis</h4>',
    ''
)

# Update single search inputs with labels and disable state
content = content.replace(
    '<div id="searchSingle" class="flex flex-col sm:flex-row gap-4 max-w-4xl mb-12 reveal-item reveal-hidden" style="transition-delay: 0.2s;">\n                    <input type="text" id="topicInput"',
    '<div id="searchSingle" class="flex flex-col sm:flex-row gap-4 max-w-4xl mb-12">\n                    <label for="topicInput" class="sr-only">Topic for Single Analysis</label>\n                    <input type="text" id="topicInput"'
)
content = content.replace(
    '<button id="topicButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)] hover:shadow-[0_0_25px_rgba(0,219,231,0.5)]">Analyze</button>',
    '<button id="topicButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed disabled:opacity-50 disabled:cursor-not-allowed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)]">Analyze</button>\n                </div>\n                <!-- TAB CONTENT: BATTLE MODE -->\n                <div id="tabContentBattle" class="hidden reveal-item reveal-hidden">'
)

# Replace Battle Mode heading
content = content.replace(
    '<h4 class="font-bold text-2xl mb-4 text-primary reveal-item reveal-hidden">Battle Mode</h4>',
    ''
)

# Replace Battle Mode Inputs
content = content.replace(
    '<div id="searchBattle" class="flex flex-col sm:flex-row gap-4 max-w-5xl mb-12 reveal-item reveal-hidden items-center" style="transition-delay: 0.2s;">\n                    <input type="text" id="topicInputA"',
    '<div id="searchBattle" class="flex flex-col sm:flex-row gap-4 max-w-5xl mb-12 items-center">\n                    <label for="topicInputA" class="sr-only">First Topic for Battle</label>\n                    <input type="text" id="topicInputA"'
)
content = content.replace(
    '<button id="swapTopicsBtn" class="p-4 rounded-full bg-surface-container border border-outline-variant/30 hover:bg-primary/20 hover:border-primary/50 transition-all text-on-surface-variant hover:text-primary flex items-center justify-center group" title="Swap Topics">',
    '<button id="swapTopicsBtn" class="p-4 rounded-full bg-surface-container border border-outline-variant/30 hover:bg-primary/20 hover:border-primary/50 transition-all text-on-surface-variant hover:text-primary flex items-center justify-center group" title="Swap Topics" aria-label="Swap Topics">'
)
content = content.replace(
    '<input type="text" id="topicInputB"',
    '<label for="topicInputB" class="sr-only">Second Topic for Battle</label>\n                    <input type="text" id="topicInputB"'
)
content = content.replace(
    '<button id="battleButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)] hover:shadow-[0_0_25px_rgba(0,219,231,0.5)]">Analyze Battle</button>',
    '<button id="battleButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed disabled:opacity-50 disabled:cursor-not-allowed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)]">Analyze Battle</button>\n                </div>'
)

# Update results grids
content = content.replace(
    '<!-- Macro Results Grid -->\n                <div id="topicResults" class="hidden">',
    '<!-- Single Results Grid -->\n                <div id="topicResults" class="hidden border-t border-outline-variant/10 pt-12 mt-8">'
)

content = content.replace(
    '<!-- Battle Results Grid -->\n                <div id="battleResults" class="hidden flex flex-col gap-6 w-full max-w-7xl mx-auto">',
    '<!-- Battle Results Grid -->\n                <div id="battleResults" class="hidden border-t border-outline-variant/10 pt-12 mt-8 flex flex-col gap-6 w-full max-w-7xl mx-auto">'
)

# Remove the line break separator between Single and Battle results (now handled by tabs)
content = content.replace(
    '<div class="w-full h-px bg-outline-variant/20 my-16 reveal-item reveal-hidden"></div>',
    ''
)

# Update GenAI Summary
genai_str = """            <!-- GenAI Summary Section -->
            <section class="px-margin-mobile md:px-margin-desktop py-12 border-t border-outline-variant/10 relative" id="smart-summary">
                <div class="absolute inset-0 bg-surface/30 backdrop-blur-sm -z-10"></div>
                <div class="mb-8 reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">AI Summary</h3>
                    <p class="font-label-mono text-label-mono text-primary uppercase tracking-widest">Sentiment Context</p>
                </div>
                <div class="max-w-4xl reveal-item reveal-hidden">
                    <div id="genaiSummaryText" class="font-body-md text-primary bg-surface-container/50 p-8 rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.1)] glow-border leading-relaxed text-xl min-h-[100px]">
                        <!-- Summary content injected via JS -->
                        <span class="text-outline">Waiting for analysis to complete...</span>
                    </div>
                </div>
            </section>"""

new_genai = """            <!-- GenAI Summary Section (Now integrated as part of results view) -->
            <section class="px-margin-mobile md:px-margin-desktop py-12 border-t border-outline-variant/10 relative hidden scroll-mt-32" id="smart-summary">
                <div class="absolute inset-0 bg-surface/30 backdrop-blur-sm -z-10"></div>
                <div class="mb-8">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">AI Summary</h3>
                    <p class="font-label-mono text-label-mono text-primary uppercase tracking-widest">Sentiment Context</p>
                </div>
                <div class="max-w-4xl">
                    <div id="genaiSummaryState" class="font-body-md text-on-surface bg-surface-container/50 p-8 rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.1)] glow-border leading-relaxed text-xl min-h-[100px] flex items-center" aria-live="polite">
                        <!-- IDLE STATE -->
                        <div id="summaryIdle" class="text-outline italic w-full text-center py-4">
                            Run an analysis to generate your AI summary.
                        </div>
                        
                        <!-- LOADING STATE -->
                        <div id="summaryLoading" class="hidden text-primary w-full flex flex-col items-center justify-center py-4">
                            <div class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
                            Generating AI summary...
                        </div>
                        
                        <!-- SUCCESS STATE -->
                        <div id="summarySuccess" class="hidden w-full">
                            <div id="genaiSummaryText" class="text-on-surface"></div>
                        </div>

                        <!-- EMPTY STATE -->
                        <div id="summaryEmpty" class="hidden text-outline w-full text-center py-4">
                            No sufficient analysis data is available for a summary.
                        </div>

                        <!-- ERROR STATE -->
                        <div id="summaryError" class="hidden text-error w-full text-center py-4 flex flex-col items-center gap-4">
                            <span class="material-symbols-outlined text-4xl">error</span>
                            We couldn't generate the summary.
                            <button id="retrySummaryBtn" class="px-6 py-2 border border-error/50 text-error rounded hover:bg-error/10">Retry</button>
                        </div>
                    </div>
                </div>
            </section>"""
content = content.replace(genai_str, new_genai)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
