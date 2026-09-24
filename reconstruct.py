import sys

original_part1 = []
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    original_part1 = lines[:296]
    
    # Find micro inference
    micro_idx = -1
    for i, line in enumerate(lines):
        if '<!-- Micro Inference -->' in line:
            micro_idx = i
            break
    
    original_part2 = lines[micro_idx:]

missing_content = """                <div class="absolute right-[10%] top-1/2 -translate-y-1/2 w-64 h-64 md:w-96 md:h-96 rounded-full border border-outline-variant/10 flex items-center justify-center opacity-30 pointer-events-none hidden lg:flex">
                    <div class="w-full h-full border border-dashed border-primary/20 rounded-full animate-[spin_60s_linear_infinite]"></div>
                    <div class="absolute w-3/4 h-3/4 border border-dashed border-secondary/20 rounded-full animate-[spin_40s_linear_infinite_reverse]"></div>
                </div>
            </section>

            <!-- Macro Analysis Section -->
            <section class="px-margin-mobile md:px-margin-desktop py-24 border-t border-outline-variant/10 relative scroll-mt-32" id="macro-analysis">
                <div class="absolute inset-0 bg-surface-container-low/50 backdrop-blur-sm -z-10"></div>
                <div class="mb-12 reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">Macro Analysis</h3>
                    <p class="font-label-mono text-label-mono text-primary uppercase tracking-widest">Global Sentiment Data</p>
                </div>

                <h4 class="font-bold text-2xl mb-4 text-primary reveal-item reveal-hidden">Single Analysis</h4>
                <!-- Search Input: Single -->
                <div id="searchSingle" class="flex flex-col sm:flex-row gap-4 max-w-4xl mb-12 reveal-item reveal-hidden" style="transition-delay: 0.2s;">
                    <input type="text" id="topicInput" class="flex-1 bg-surface-container/50 border border-outline-variant/30 rounded-lg p-6 text-xl placeholder:text-xl text-on-surface focus:border-primary focus:outline-none transition-colors" placeholder="Enter topic to analyze (e.g. latest tech)...">
                    <button id="topicButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)] hover:shadow-[0_0_25px_rgba(0,219,231,0.5)]">Analyze</button>
                </div>

                <!-- Macro Results Grid -->
                <div id="topicResults" class="hidden">
                    <div class="flex items-center justify-between mb-6">
                        <div class="flex items-center gap-3 font-label-mono text-lg text-on-surface-variant reveal-item reveal-hidden font-bold">
                            <div id="singleLiveDot" class="w-3 h-3 rounded-full bg-secondary-fixed animate-pulse"></div>
                            <span id="singleLiveStatus">Tracking...</span>
                            <span id="singleLiveStats" class="ml-4 text-primary">0 Mentions</span>
                        </div>
                        <button id="exportMacroBtn" class="hidden px-8 py-4 bg-primary/10 text-primary font-bold uppercase text-sm tracking-wider hover:bg-primary hover:text-on-primary transition-all rounded-lg shadow-[0_0_10px_rgba(0,219,231,0.2)] border border-primary/30 flex items-center gap-2">
                            <span class="material-symbols-outlined text-xl">download</span> Export PDF
                        </button>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Score -->
                        <div class="data-card p-10 rounded-lg flex flex-col gap-4 glow-border h-full reveal-item reveal-hidden" style="transition-delay: 0.1s;">
                            <span class="material-symbols-outlined text-primary text-3xl mb-2 animate-pulse drop-shadow-[0_0_8px_rgba(0,219,231,0.8)]">bolt</span>
                            <h4 class="font-bold text-2xl">Aggregated Score</h4>
                            <div class="flex-1 flex flex-col justify-center items-center">
                                <div id="finalScore" class="text-5xl font-extrabold text-primary">0.0</div>
                                <div class="text-[10px] font-label-mono text-outline mt-2">SCALE -10 TO +10</div>
                            </div>
                        </div>

                        <!-- Chart 1: Distribution -->
                        <div class="data-card p-10 rounded-lg flex flex-col gap-4 glow-border h-full md:col-span-1 reveal-item reveal-hidden" style="transition-delay: 0.2s;">
                            <span class="material-symbols-outlined text-primary text-3xl mb-2">pie_chart</span>
                            <h4 class="font-bold text-2xl">Distribution</h4>
                            
                            <div class="flex justify-between text-xl font-bold font-label-mono mb-2">
                                <span class="text-secondary-fixed">POS: <span id="posPercent" class="text-xl">0%</span></span>
                                <span class="text-outline">NEU: <span id="neuPercent">0%</span></span>
                                <span class="text-error">NEG: <span id="negPercent" class="text-xl">0%</span></span>
                            </div>

                            <div class="flex-1 relative min-h-[150px]">
                                <canvas id="sentimentChart" class="relative z-10"></canvas>
                                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center justify-center pointer-events-none z-0 mt-2">
                                    <div class="text-sm font-label-mono text-outline leading-tight tracking-widest uppercase">SENTIMENTS</div>
                                    <div id="totalCount" class="text-4xl font-extrabold text-primary leading-none mt-2">0</div>
                                </div>
                            </div>
                        </div>

                        <!-- Chart 2: Trend -->
                        <div class="data-card p-10 rounded-lg flex flex-col gap-4 glow-border h-full md:col-span-1 reveal-item reveal-hidden" style="transition-delay: 0.3s;">
                            <span class="material-symbols-outlined text-primary text-3xl mb-2">trending_up</span>
                            <h4 class="font-bold text-2xl">7-Day Trend</h4>
                            <div class="flex-1 relative min-h-[150px]">
                                <canvas id="trendChart"></canvas>
                            </div>
                        </div>

                        <!-- Signals -->
                        <div class="data-card p-10 rounded-lg flex flex-col gap-6 glow-border h-full md:col-span-3 reveal-item reveal-hidden" style="transition-delay: 0.4s;">
                            <div class="flex items-center gap-3 border-b border-outline-variant/10 pb-4">
                                <span class="material-symbols-outlined text-primary text-3xl">sensors</span>
                                <h4 class="font-bold text-2xl tracking-tight">Live Sentiments</h4>
                            </div>
                            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 w-full mt-2">
                                <!-- Positive -->
                                <div class="bg-secondary-fixed/5 rounded-xl p-6 border border-secondary-fixed/20 shadow-lg flex flex-col h-full hover:bg-secondary-fixed/10 transition-colors">
                                    <h5 class="text-[14px] font-label-mono text-secondary-fixed mb-4 uppercase flex items-center gap-2 font-bold"><span class="material-symbols-outlined text-lg">trending_up</span> Positive</h5>
                                    <div id="posSamples" class="sample-list flex flex-col gap-4 flex-1"></div>
                                </div>
                                <!-- Neutral -->
                                <div class="bg-outline-variant/5 rounded-xl p-6 border border-outline-variant/20 shadow-lg flex flex-col h-full hover:bg-outline-variant/10 transition-colors">
                                    <h5 class="text-[14px] font-label-mono text-outline mb-4 uppercase flex items-center gap-2 font-bold"><span class="material-symbols-outlined text-lg">trending_flat</span> Neutral</h5>
                                    <div id="neuSamples" class="sample-list flex flex-col gap-4 flex-1"></div>
                                </div>
                                <!-- Negative -->
                                <div class="bg-error/5 rounded-xl p-6 border border-error/20 shadow-lg flex flex-col h-full hover:bg-error/10 transition-colors">
                                    <h5 class="text-[14px] font-label-mono text-error mb-4 uppercase flex items-center gap-2 font-bold"><span class="material-symbols-outlined text-lg">trending_down</span> Negative</h5>
                                    <div id="negSamples" class="sample-list flex flex-col gap-4 flex-1"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="w-full h-px bg-outline-variant/20 my-16 reveal-item reveal-hidden"></div>

                <h4 class="font-bold text-2xl mb-4 text-primary reveal-item reveal-hidden">Battle Mode</h4>
                <!-- Search Input: Battle -->
                <div id="searchBattle" class="flex flex-col sm:flex-row gap-4 max-w-5xl mb-12 reveal-item reveal-hidden items-center" style="transition-delay: 0.2s;">
                    <input type="text" id="topicInputA" class="flex-1 bg-surface-container/50 border border-outline-variant/30 rounded-lg p-6 text-xl placeholder:text-xl text-on-surface focus:border-primary focus:outline-none transition-colors" placeholder="Topic A (e.g. Marvel)...">
                    
                    <button id="swapTopicsBtn" class="p-4 rounded-full bg-surface-container border border-outline-variant/30 hover:bg-primary/20 hover:border-primary/50 transition-all text-on-surface-variant hover:text-primary flex items-center justify-center group" title="Swap Topics">
                        <span class="material-symbols-outlined font-bold text-xl group-hover:rotate-180 transition-transform duration-300">swap_horiz</span>
                    </button>
                    
                    <input type="text" id="topicInputB" class="flex-1 bg-surface-container/50 border border-outline-variant/30 rounded-lg p-6 text-xl placeholder:text-xl text-on-surface focus:border-primary focus:outline-none transition-colors" placeholder="Topic B (e.g. DC)...">
                    
                    <button id="battleButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)] hover:shadow-[0_0_25px_rgba(0,219,231,0.5)]">Analyze Battle</button>
                </div>

                <!-- Battle Results Grid -->
                <div id="battleResults" class="hidden flex flex-col gap-6 w-full max-w-7xl mx-auto">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-3 font-label-mono text-lg text-on-surface-variant font-bold">
                            <div id="battleLiveDot" class="w-3 h-3 rounded-full bg-secondary-fixed animate-pulse"></div>
                            <span id="battleLiveStatus">Waiting to initiate battle...</span>
                        </div>
                        <button id="exportBattleBtn" class="hidden px-8 py-4 bg-primary/10 text-primary font-bold uppercase text-sm tracking-wider hover:bg-primary hover:text-on-primary transition-all rounded-lg shadow-[0_0_10px_rgba(0,219,231,0.2)] border border-primary/30 flex items-center gap-2">
                            <span class="material-symbols-outlined text-xl">download</span> Export PDF
                        </button>
                    </div>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
                        <!-- Topic A Panel -->
                        <div class="lg:col-span-2 flex flex-col gap-6">
                            <h4 id="battleTitleA" class="font-bold text-3xl uppercase text-primary border-b border-outline-variant/20 pb-2">Topic A</h4>
                            
                            <div class="data-card p-6 rounded-lg flex flex-col gap-4 glow-border bg-surface-container/30">
                                <div class="flex justify-between items-center">
                                    <h5 class="font-bold text-xl">Aggregated Score</h5>
                                    <div id="finalScoreA" class="text-4xl font-extrabold text-primary">0.0</div>
                                </div>
                            </div>
                            
                            <div class="data-card p-6 rounded-lg flex flex-col gap-4 glow-border bg-surface-container/30">
                                <div class="flex justify-between items-center mb-2">
                                    <h5 class="font-bold text-xl">Distribution</h5>
                                </div>
                                <div class="flex justify-between text-xl font-bold font-label-mono mb-2">
                                    <span class="text-secondary-fixed">POS: <span id="posPercentA">0%</span></span>
                                    <span class="text-error">NEG: <span id="negPercentA">0%</span></span>
                                </div>
                                <div class="relative min-h-[150px] flex-1">
                                    <canvas id="sentimentChartA" class="relative z-10"></canvas>
                                    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center justify-center pointer-events-none z-0 mt-2">
                                        <div class="text-sm font-label-mono text-outline leading-tight tracking-widest uppercase">SENTIMENTS</div>
                                        <div id="totalCountA" class="text-4xl font-extrabold text-primary leading-none mt-2">0</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="data-card p-6 rounded-lg glow-border flex-1 bg-surface-container/30 max-h-[500px] overflow-y-auto">
                                <h5 class="font-bold text-xl border-b border-outline-variant/10 pb-2 mb-4">Live Feed</h5>
                                <div id="feedA" class="sample-list flex flex-col gap-4"></div>
                            </div>
                        </div>
                        
                        <!-- Verdict Center -->
                        <div class="lg:col-span-1 flex flex-col items-center justify-start py-12 border-x border-outline-variant/10 px-4 sticky top-24 h-fit bg-surface-container-low/20 rounded-lg shadow-inner">
                            <h4 class="font-label-mono text-outline uppercase tracking-widest text-sm mb-6">Verdict</h4>
                            <div id="verdictIcon" class="material-symbols-outlined text-[80px] text-outline mb-6 drop-shadow-md">balance</div>
                            <div id="verdictTitle" class="text-3xl font-extrabold uppercase text-center mb-4 leading-tight tracking-tighter">Too Close<br/>To Call</div>
                            <div class="text-sm text-center text-on-surface-variant mt-4 p-4 border border-outline-variant/20 rounded bg-surface/50" id="verdictSubtext">Waiting for sufficient evidence...</div>
                        </div>

                        <!-- Topic B Panel -->
                        <div class="lg:col-span-2 flex flex-col gap-6">
                            <h4 id="battleTitleB" class="font-bold text-3xl uppercase text-primary border-b border-outline-variant/20 pb-2 text-right">Topic B</h4>
                            
                            <div class="data-card p-6 rounded-lg flex flex-col gap-4 glow-border bg-surface-container/30">
                                <div class="flex justify-between items-center flex-row-reverse">
                                    <h5 class="font-bold text-xl">Aggregated Score</h5>
                                    <div id="finalScoreB" class="text-4xl font-extrabold text-primary">0.0</div>
                                </div>
                            </div>
                            
                            <div class="data-card p-6 rounded-lg flex flex-col gap-4 glow-border bg-surface-container/30">
                                <div class="flex justify-between items-center mb-2 flex-row-reverse">
                                    <h5 class="font-bold text-xl">Distribution</h5>
                                </div>
                                <div class="flex justify-between text-xl font-bold font-label-mono mb-2 flex-row-reverse">
                                    <span class="text-secondary-fixed">POS: <span id="posPercentB">0%</span></span>
                                    <span class="text-error">NEG: <span id="negPercentB">0%</span></span>
                                </div>
                                <div class="relative min-h-[150px] flex-1">
                                    <canvas id="sentimentChartB" class="relative z-10"></canvas>
                                    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center justify-center pointer-events-none z-0 mt-2">
                                        <div class="text-sm font-label-mono text-outline leading-tight tracking-widest uppercase">SENTIMENTS</div>
                                        <div id="totalCountB" class="text-4xl font-extrabold text-primary leading-none mt-2">0</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="data-card p-6 rounded-lg glow-border flex-1 bg-surface-container/30 max-h-[500px] overflow-y-auto">
                                <h5 class="font-bold text-xl text-right border-b border-outline-variant/10 pb-2 mb-4">Live Feed</h5>
                                <div id="feedB" class="sample-list flex flex-col gap-4"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- GenAI Summary Section -->
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
            </section>

            <!-- Data Pipeline Flow -->
            <section class="px-margin-mobile md:px-margin-desktop py-24 border-t border-outline-variant/10 relative scroll-mt-32" id="data-pipeline">
                <div class="absolute inset-0 bg-surface/30 backdrop-blur-sm -z-10"></div>
                <div class="mb-16 text-center reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">Data Pipeline</h3>
                    <p class="font-label-mono text-label-mono text-on-surface-variant uppercase tracking-widest">Ingest to Inference</p>
                </div>
                <div class="flex flex-col md:flex-row items-center justify-between gap-8 max-w-7xl mx-auto relative px-4">
                    <!-- Connecting line -->
                    <div class="hidden md:block absolute top-1/2 left-0 w-full h-[1px] bg-outline-variant/30 -z-10"></div>
                    <div class="flex flex-col items-center gap-6 bg-surface/80 p-10 rounded-lg border border-outline-variant/20 z-10 w-72 text-center glow-border reveal-item reveal-hidden" style="transition-delay: 0.1s;">
                        <div class="w-16 h-16 rounded bg-surface-container flex items-center justify-center text-on-surface">
                            <span class="material-symbols-outlined text-4xl">rss_feed</span>
                        </div>
                        <h5 class="font-bold text-xl uppercase tracking-wider">Raw Sources</h5>
                        <p class="text-base text-on-surface-variant font-label-mono">Voice / Text Stream</p>
                    </div>
                    <span class="material-symbols-outlined text-3xl text-outline-variant rotate-90 md:rotate-0 reveal-item reveal-hidden" style="transition-delay: 0.2s;">arrow_forward</span>
                    <div class="flex flex-col items-center gap-6 bg-surface-container-high/90 p-10 rounded-lg border border-primary/30 z-10 w-72 text-center shadow-[0_0_20px_rgba(0,219,231,0.1)] relative overflow-hidden reveal-item reveal-hidden hover:-translate-y-1 transition-transform" style="transition-delay: 0.3s;">
                        <div class="absolute inset-0 bg-gradient-to-b from-primary/10 to-transparent"></div>
                        <div class="w-16 h-16 rounded bg-primary/20 flex items-center justify-center text-primary relative z-10">
                            <span class="material-symbols-outlined text-4xl">hub</span>
                        </div>
                        <h5 class="font-bold text-xl uppercase tracking-wider text-primary relative z-10">Inference Engine</h5>
                        <p class="text-base text-on-surface-variant font-label-mono relative z-10">NLP Processing</p>
                    </div>
                    <span class="material-symbols-outlined text-3xl text-outline-variant rotate-90 md:rotate-0 reveal-item reveal-hidden" style="transition-delay: 0.4s;">arrow_forward</span>
                    <div class="flex flex-col items-center gap-6 bg-surface/80 p-10 rounded-lg border border-outline-variant/20 z-10 w-72 text-center glow-border reveal-item reveal-hidden" style="transition-delay: 0.5s;">
                        <div class="w-16 h-16 rounded bg-surface-container flex items-center justify-center text-on-surface">
                            <span class="material-symbols-outlined text-4xl">terminal</span>
                        </div>
                        <h5 class="font-bold text-xl uppercase tracking-wider">Actionable Data</h5>
                        <p class="text-base text-on-surface-variant font-label-mono">Classification Stream</p>
                    </div>
                </div>
            </section>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(original_part1)
    f.write(missing_content)
    f.writelines(original_part2)
