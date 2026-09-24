import os

def create_index_html():
    content = """<!DOCTYPE html>
<html class="dark scroll-smooth" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>SentimentAI - Intelligence Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&family=Inter:wght@400;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Base CSS (for Chart.js, etc.) -->
    <link rel="stylesheet" href="style.css">

    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "inverse-primary": "#00696f",
                        "surface": "#0d1515",
                        "surface-container-low": "#151d1e",
                        "tertiary-fixed": "#ffe173",
                        "on-tertiary-fixed-variant": "#554500",
                        "background": "#0d1515",
                        "surface-tint": "#00dbe7",
                        "surface-bright": "#333b3b",
                        "surface-container": "#192122",
                        "outline": "#849495",
                        "on-tertiary": "#3b2f00",
                        "primary-fixed": "#74f5ff",
                        "on-surface": "#dce4e4",
                        "tertiary-container": "#fed83a",
                        "inverse-surface": "#dce4e4",
                        "on-primary-fixed": "#002022",
                        "secondary": "#ecffe3",
                        "primary-container": "#00f2ff",
                        "surface-container-lowest": "#080f10",
                        "on-secondary-fixed": "#002203",
                        "secondary-fixed": "#72ff70",
                        "secondary-container": "#13ff43",
                        "surface-container-highest": "#2e3637",
                        "surface-variant": "#2e3637",
                        "on-secondary-fixed-variant": "#00530e",
                        "error-container": "#93000a",
                        "outline-variant": "#3a494b",
                        "on-background": "#dce4e4",
                        "primary": "#e1fdff",
                        "inverse-on-surface": "#2a3232",
                        "error": "#ffb4ab",
                        "on-tertiary-fixed": "#221b00",
                        "on-surface-variant": "#b9cacb",
                        "tertiary": "#fff6e4",
                        "primary-fixed-dim": "#00dbe7",
                        "surface-container-high": "#232b2c",
                        "on-tertiary-container": "#725e00",
                        "on-error-container": "#ffdad6",
                        "on-primary": "#00363a",
                        "tertiary-fixed-dim": "#e8c423",
                        "secondary-fixed-dim": "#00e639",
                        "on-secondary": "#003907",
                        "on-primary-container": "#006a71",
                        "on-error": "#690005",
                        "on-primary-fixed-variant": "#004f54",
                        "on-secondary-container": "#007117",
                        "surface-dim": "#0d1515"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "unit": "4px",
                        "gutter": "24px",
                        "margin-mobile": "16px",
                        "container-max": "1440px",
                        "margin-desktop": "48px"
                    },
                    "fontFamily": {
                        "headline-lg-mobile": ["Montserrat"],
                        "body-md": ["Inter"],
                        "label-mono": ["JetBrains Mono"],
                        "display-lg": ["Montserrat"],
                        "headline-lg": ["Montserrat"],
                        "label-caps": ["Inter"]
                    },
                    "fontSize": {
                        "headline-lg-mobile": ["24px", { "lineHeight": "1.2", "fontWeight": "700" }],
                        "body-md": ["16px", { "lineHeight": "1.6", "letterSpacing": "0em", "fontWeight": "400" }],
                        "label-mono": ["12px", { "lineHeight": "1.4", "letterSpacing": "0.1em", "fontWeight": "500" }],
                        "display-lg": ["72px", { "lineHeight": "1.1", "letterSpacing": "-0.04em", "fontWeight": "800" }],
                        "headline-lg": ["32px", { "lineHeight": "1.2", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "label-caps": ["11px", { "lineHeight": "1.2", "letterSpacing": "0.2em", "fontWeight": "700" }]
                    },
                    "animation": {
                        "fade-in-up": "fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards"
                    },
                    "keyframes": {
                        "fadeInUp": {
                            "0%": { opacity: 0, transform: "translateY(20px)" },
                            "100%": { opacity: 1, transform: "translateY(0)" }
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: transparent; 
            color: #dce4e4;
        }
        
        .interactive-grid {
            position: fixed; /* Keep grid fixed to screen */
            inset: 0;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
            z-index: -1;
            pointer-events: none;
        }
        
        .interactive-grid::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(
                600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
                rgba(0, 219, 231, 0.15),
                transparent 40%
            );
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .interactive-grid.active::before {
            opacity: 1;
        }

        .hero-particle-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
            pointer-events: none;
        }
        
        .glow-border {
            border: 1px solid rgba(0, 219, 231, 0.2);
            box-shadow: 0 0 15px rgba(0, 219, 231, 0.05);
            transition: all 0.3s ease;
        }
        .glow-border:hover {
            border-color: rgba(0, 219, 231, 0.5);
            box-shadow: 0 0 20px rgba(0, 219, 231, 0.15);
            transform: translateY(-2px);
        }

        .data-card {
            background: rgba(46, 54, 55, 0.4); 
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
        }
        
        .reveal-hidden {
            opacity: 0;
            transform: translateY(30px);
        }
        
        .reveal-visible {
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: rgba(13, 21, 21, 0.5); }
        ::-webkit-scrollbar-thumb { background: rgba(0, 219, 231, 0.3); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0, 219, 231, 0.6); }

        .sample-list { max-height: 250px; overflow-y: auto; padding-right: 5px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="font-body-md text-body-md antialiased overflow-x-hidden">
    <!-- Shader Background -->
    <div class="fixed inset-0 w-full h-full -z-10 bg-surface" id="shader-container"></div>
    <div class="interactive-grid" id="interactive-grid"></div>

    <!-- UI Overlays (Toast, Share, Contact) -->
    <div id="toast-stack" class="fixed bottom-4 right-4 z-50 flex flex-col gap-2"></div>

    <!-- App Container -->
    <div class="flex h-screen w-full relative">
        <!-- SideNavBar -->
        <aside class="hidden md:flex flex-col p-gutter gap-4 h-full w-64 border-r border-outline-variant/20 bg-surface/80 dark:bg-surface/80 backdrop-blur-xl border-white/10 z-20 shrink-0">
            <div class="mb-8">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0"></div>
                    <div>
                        <h1 class="font-display-lg text-headline-lg tracking-tighter text-on-surface dark:text-primary">SENTIMENT.</h1>
                        <p class="font-label-mono text-label-mono text-on-surface-variant uppercase tracking-widest mt-1">AI Logic Engine</p>
                    </div>
                </div>
            </div>
            <nav class="flex-1 flex flex-col gap-2">
                <a class="flex items-center gap-3 p-3 bg-primary text-on-primary rounded-lg font-bold shadow-[0_0_15px_rgba(0,219,231,0.3)] scale-98 active:scale-95 transition-transform duration-200" href="#hero">
                    <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">visibility</span>
                    <span class="font-label-mono text-label-mono uppercase tracking-widest">Vision</span>
                </a>
                <a class="flex items-center gap-3 p-3 text-on-surface-variant hover:text-primary transition-colors duration-300 hover:bg-surface-variant/50 scale-98 active:scale-95" href="#macro-analysis">
                    <span class="material-symbols-outlined">analytics</span>
                    <span class="font-label-mono text-label-mono uppercase tracking-widest">Macro Analysis</span>
                </a>
                <a class="flex items-center gap-3 p-3 text-on-surface-variant hover:text-primary transition-colors duration-300 hover:bg-surface-variant/50 scale-98 active:scale-95" href="#data-pipeline">
                    <span class="material-symbols-outlined">network_wired</span>
                    <span class="font-label-mono text-label-mono uppercase tracking-widest">Data Pipeline</span>
                </a>
                <a class="flex items-center gap-3 p-3 text-on-surface-variant hover:text-primary transition-colors duration-300 hover:bg-surface-variant/50 scale-98 active:scale-95" href="#micro-inference">
                    <span class="material-symbols-outlined">insights</span>
                    <span class="font-label-mono text-label-mono uppercase tracking-widest">Micro Inference</span>
                </a>
            </nav>
            <div class="mt-auto flex flex-col gap-4 border-t border-outline-variant/20 pt-4">
                <div class="flex flex-col gap-2 text-xs text-on-surface-variant font-label-mono">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-[14px]">sensors</span>
                        <span>System Status: <span id="apiStatusText" class="text-secondary-fixed">ONLINE</span></span>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="flex-1 flex flex-col relative h-full overflow-y-auto" id="main-scroll">
            <!-- TopAppBar -->
            <header class="flex justify-between items-center px-margin-mobile md:px-margin-desktop py-4 w-full z-50 bg-surface/60 dark:bg-surface/60 backdrop-blur-md border-b border-outline-variant/10 sticky top-0 transition-all duration-300 ease-in-out">
                <div class="flex items-center gap-8">
                    <div class="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface tracking-tighter md:hidden">SENTIMENT.</div>
                </div>
                <div class="flex items-center gap-4">
                    <button class="text-on-surface-variant hover:text-primary transition-colors"><span class="material-symbols-outlined">share</span></button>
                    <button class="text-on-surface-variant hover:text-primary transition-colors"><span class="material-symbols-outlined">mail</span></button>
                    <button class="text-on-surface-variant hover:text-primary transition-colors"><span class="material-symbols-outlined">keyboard</span></button>
                </div>
            </header>

            <!-- Hero Section -->
            <section id="hero" class="relative flex-1 min-h-[600px] flex items-center px-margin-mobile md:px-margin-desktop py-24 overflow-hidden group">
                <div class="hero-particle-bg" id="particle-container">
                    <div class="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPjxyZWN0IHdpZHRoPSI0IiBoZWlnaHQ9IjQiIGZpbGw9IiMwZDE1MTUiPjwvcmVjdD48Y2lyY2xlIGN4PSIyIiBjeT0iMiIgcj0iMSIgZmlsbD0iI2RjZTRlNCI+PC9jaXJjbGU+PC9zdmc+')] mix-blend-screen transition-transform duration-1000 ease-out"></div>
                </div>
                <div class="relative z-10 max-w-4xl">
                    <h2 class="font-display-lg text-[48px] md:text-display-lg font-extrabold text-white leading-none mb-6 tracking-tighter opacity-0 animate-fade-in-up" style="animation-delay: 0s;">
                        MEASURE <br/>
                        <span class="text-surface-variant italic font-light">EMOTION</span> <br/>
                        AT SCALE.
                    </h2>
                    <p class="text-on-surface-variant text-lg md:text-xl max-w-2xl mb-10 leading-relaxed font-body-md border-l-2 border-primary/30 pl-4 opacity-0 animate-fade-in-up" style="animation-delay: 0.2s;">
                        The intelligence engine processing digital interactions into pure sentiment data, utilizing an 85% accuracy deep learning model.
                    </p>
                    <div class="flex flex-wrap gap-4 opacity-0 animate-fade-in-up" style="animation-delay: 0.4s;">
                        <a href="#macro-analysis" class="px-8 py-4 bg-white text-black font-bold uppercase tracking-wider hover:bg-primary transition-all duration-300 rounded-DEFAULT flex items-center gap-2 shadow-[0_0_0_rgba(0,219,231,0)] hover:shadow-[0_0_25px_rgba(0,219,231,0.5)] active:scale-95 group">
                            INITIATE SEQUENCE <span class="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward</span>
                        </a>
                    </div>
                </div>
                <div class="absolute right-[10%] top-1/2 -translate-y-1/2 w-64 h-64 md:w-96 md:h-96 rounded-full border border-outline-variant/10 flex items-center justify-center opacity-30 pointer-events-none hidden lg:flex">
                    <div class="w-full h-full border border-dashed border-primary/20 rounded-full animate-[spin_60s_linear_infinite]"></div>
                    <div class="absolute w-3/4 h-3/4 border border-dashed border-secondary/20 rounded-full animate-[spin_40s_linear_infinite_reverse]"></div>
                </div>
            </section>

            <!-- Macro Analysis Section -->
            <section class="px-margin-mobile md:px-margin-desktop py-24 border-t border-outline-variant/10 relative" id="macro-analysis">
                <div class="absolute inset-0 bg-surface-container-low/50 backdrop-blur-sm -z-10"></div>
                <div class="mb-12 reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">Macro Analysis</h3>
                    <p class="font-label-mono text-label-mono text-primary uppercase tracking-widest">Global Sentiment Data</p>
                </div>

                <!-- Search Input -->
                <div class="flex flex-col sm:flex-row gap-4 max-w-2xl mb-12 reveal-item reveal-hidden" style="transition-delay: 0.1s;">
                    <input type="text" id="topicInput" class="flex-1 bg-surface-container/50 border border-outline-variant/30 rounded p-4 text-on-surface focus:border-primary focus:outline-none transition-colors" placeholder="Enter topic to analyze (e.g. latest tech)...">
                    <button id="topicButton" class="px-8 py-4 bg-white text-black font-bold uppercase tracking-wider hover:bg-primary transition-all rounded shadow-[0_0_0_rgba(0,219,231,0)] hover:shadow-[0_0_15px_rgba(0,219,231,0.3)]">Analyze</button>
                </div>

                <!-- Macro Results Grid -->
                <div id="topicResults" class="hidden">
                    <div class="flex items-center gap-2 mb-6 font-label-mono text-[12px] text-on-surface-variant reveal-item reveal-hidden">
                        <div id="singleLiveDot" class="w-2 h-2 rounded-full bg-secondary-fixed animate-pulse"></div>
                        <span id="singleLiveStatus">Tracking...</span>
                        <span id="singleLiveStats" class="ml-auto text-primary">0 Mentions</span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Score -->
                        <div class="data-card p-8 rounded-lg flex flex-col gap-4 glow-border h-full reveal-item reveal-hidden" style="transition-delay: 0.1s;">
                            <span class="material-symbols-outlined text-primary text-3xl mb-2">bolt</span>
                            <h4 class="font-bold text-xl">Aggregated Score</h4>
                            <div class="flex-1 flex flex-col justify-center items-center">
                                <div id="finalScore" class="text-5xl font-extrabold text-primary">0.0</div>
                                <div class="text-[10px] font-label-mono text-outline mt-2">SCALE -10 TO +10</div>
                            </div>
                        </div>

                        <!-- Chart 1: Distribution -->
                        <div class="data-card p-8 rounded-lg flex flex-col gap-4 glow-border h-full md:col-span-1 reveal-item reveal-hidden" style="transition-delay: 0.2s;">
                            <span class="material-symbols-outlined text-primary text-3xl mb-2">pie_chart</span>
                            <h4 class="font-bold text-xl">Distribution</h4>
                            <div class="flex-1 relative min-h-[150px]">
                                <canvas id="sentimentChart"></canvas>
                            </div>
                            <div class="text-[10px] font-label-mono text-outline mt-2">SAMPLE: <span id="totalCount" class="text-primary">0</span></div>
                        </div>

                        <!-- Chart 2: Trend -->
                        <div class="data-card p-8 rounded-lg flex flex-col gap-4 glow-border h-full md:col-span-1 reveal-item reveal-hidden" style="transition-delay: 0.3s;">
                            <span class="material-symbols-outlined text-primary text-3xl mb-2">trending_up</span>
                            <h4 class="font-bold text-xl">7-Day Trend</h4>
                            <div class="flex-1 relative min-h-[150px]">
                                <canvas id="trendChart"></canvas>
                            </div>
                        </div>

                        <!-- Signals -->
                        <div class="data-card p-8 rounded-lg flex flex-col gap-4 glow-border h-full md:col-span-3 reveal-item reveal-hidden" style="transition-delay: 0.4s;">
                            <span class="material-symbols-outlined text-primary text-3xl mb-2">sensors</span>
                            <h4 class="font-bold text-xl">Live Signals</h4>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
                                <div>
                                    <h5 class="text-[12px] font-label-mono text-secondary-fixed mb-2 uppercase">Positive</h5>
                                    <div id="posSamples" class="sample-list flex flex-col gap-2"></div>
                                </div>
                                <div>
                                    <h5 class="text-[12px] font-label-mono text-outline mb-2 uppercase">Neutral</h5>
                                    <div id="neuSamples" class="sample-list flex flex-col gap-2"></div>
                                </div>
                                <div>
                                    <h5 class="text-[12px] font-label-mono text-error mb-2 uppercase">Negative</h5>
                                    <div id="negSamples" class="sample-list flex flex-col gap-2"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Data Pipeline Flow -->
            <section class="px-margin-mobile md:px-margin-desktop py-24 border-t border-outline-variant/10 relative" id="data-pipeline">
                <div class="absolute inset-0 bg-surface/30 backdrop-blur-sm -z-10"></div>
                <div class="mb-16 text-center reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">Data Pipeline</h3>
                    <p class="font-label-mono text-label-mono text-on-surface-variant uppercase tracking-widest">Ingest to Inference</p>
                </div>
                <div class="flex flex-col md:flex-row items-center justify-between gap-8 max-w-5xl mx-auto relative">
                    <!-- Connecting line -->
                    <div class="hidden md:block absolute top-1/2 left-0 w-full h-[1px] bg-outline-variant/30 -z-10"></div>
                    <div class="flex flex-col items-center gap-4 bg-surface/80 p-6 rounded-lg border border-outline-variant/20 z-10 w-48 text-center glow-border reveal-item reveal-hidden" style="transition-delay: 0.1s;">
                        <div class="w-12 h-12 rounded bg-surface-container flex items-center justify-center text-on-surface">
                            <span class="material-symbols-outlined">rss_feed</span>
                        </div>
                        <h5 class="font-bold text-sm uppercase tracking-wider">Raw Sources</h5>
                        <p class="text-xs text-on-surface-variant font-label-mono">Voice / Text Stream</p>
                    </div>
                    <span class="material-symbols-outlined text-outline-variant rotate-90 md:rotate-0 reveal-item reveal-hidden" style="transition-delay: 0.2s;">arrow_forward</span>
                    <div class="flex flex-col items-center gap-4 bg-surface-container-high/90 p-6 rounded-lg border border-primary/30 z-10 w-48 text-center shadow-[0_0_20px_rgba(0,219,231,0.1)] relative overflow-hidden reveal-item reveal-hidden hover:-translate-y-1 transition-transform" style="transition-delay: 0.3s;">
                        <div class="absolute inset-0 bg-gradient-to-b from-primary/10 to-transparent"></div>
                        <div class="w-12 h-12 rounded bg-primary/20 flex items-center justify-center text-primary relative z-10">
                            <span class="material-symbols-outlined">hub</span>
                        </div>
                        <h5 class="font-bold text-sm uppercase tracking-wider text-primary relative z-10">Inference Engine</h5>
                        <p class="text-xs text-on-surface-variant font-label-mono relative z-10">NLP Processing</p>
                    </div>
                    <span class="material-symbols-outlined text-outline-variant rotate-90 md:rotate-0 reveal-item reveal-hidden" style="transition-delay: 0.4s;">arrow_forward</span>
                    <div class="flex flex-col items-center gap-4 bg-surface/80 p-6 rounded-lg border border-outline-variant/20 z-10 w-48 text-center glow-border reveal-item reveal-hidden" style="transition-delay: 0.5s;">
                        <div class="w-12 h-12 rounded bg-surface-container flex items-center justify-center text-on-surface">
                            <span class="material-symbols-outlined">terminal</span>
                        </div>
                        <h5 class="font-bold text-sm uppercase tracking-wider">Actionable Data</h5>
                        <p class="text-xs text-on-surface-variant font-label-mono">Classification Stream</p>
                    </div>
                </div>
            </section>

            <!-- Micro Inference -->
            <section class="px-margin-mobile md:px-margin-desktop py-24 border-t border-outline-variant/10 relative" id="micro-inference">
                <div class="absolute inset-0 bg-surface-container-low/50 backdrop-blur-sm -z-10"></div>
                <div class="mb-12 reveal-item reveal-hidden">
                    <h3 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg tracking-tight mb-2">Micro Inference</h3>
                    <p class="font-label-mono text-label-mono text-primary uppercase tracking-widest">Direct Neural Classification</p>
                </div>
                
                <div class="data-card p-8 rounded-lg flex flex-col md:flex-row gap-8 glow-border reveal-item reveal-hidden" style="transition-delay: 0.2s;">
                    <!-- LEFT COLUMN: INPUT -->
                    <div class="flex-1 flex flex-col gap-4">
                        <h4 class="font-bold text-lg flex items-center gap-2"><span class="material-symbols-outlined text-primary">keyboard</span> Input Stream</h4>
                        <textarea id="singleInput" class="w-full h-40 bg-surface-container/50 border border-outline-variant/30 rounded p-4 text-on-surface focus:border-primary focus:outline-none bg-transparent resize-none transition-colors" placeholder="Enter text for direct neural classification..."></textarea>
                        
                        <div class="flex gap-4 items-center mt-2">
                            <button id="voiceBtn" class="flex items-center justify-center bg-surface-container hover:bg-primary/20 hover:text-primary border border-outline-variant/30 rounded transition-colors shadow-[0_0_10px_rgba(0,0,0,0.5)]" title="Live Voice" style="width: 64px; height: 64px; border-radius: 50%;">
                                <span class="material-symbols-outlined text-3xl">mic</span>
                            </button>
                            <button id="singleButton" class="py-4 px-8 bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed transition-all rounded shadow-[0_0_15px_rgba(0,219,231,0.3)] hover:shadow-[0_0_25px_rgba(0,219,231,0.5)]">Initialize Inference</button>
                        </div>
                    </div>
                    
                    <!-- RIGHT COLUMN: OUTPUT -->
                    <div class="flex-1 flex flex-col gap-4 md:border-l md:border-outline-variant/20 md:pl-8">
                        <h4 class="font-bold text-lg flex items-center gap-2"><span class="material-symbols-outlined text-primary">analytics</span> Classification Result</h4>
                        
                        <div id="microIdle" class="text-sm text-on-surface-variant py-8 flex flex-col items-center justify-center flex-1">
                            <span class="material-symbols-outlined text-4xl mb-4 opacity-50">hourglass_empty</span>
                            Awaiting input stream...
                        </div>
                        
                        <div id="microLoading" class="hidden text-sm text-primary py-8 flex flex-col items-center justify-center flex-1 animate-pulse">
                            <div class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
                            Computing tensors...
                        </div>
                        
                        <div id="singleResult" class="hidden flex-col gap-6 flex-1">
                            <div class="flex justify-between items-center bg-surface-container/50 p-4 rounded-lg">
                                <span class="text-sm font-label-mono text-outline">PRIMARY SENTIMENT</span>
                                <span id="singleSentiment" class="px-4 py-2 bg-surface-container rounded font-bold text-lg border border-outline-variant/20 shadow-[0_0_10px_rgba(255,255,255,0.05)]">Neu</span>
                            </div>
                            
                            <div class="flex flex-col gap-4 px-2">
                                <div class="flex flex-col gap-2">
                                    <div class="flex justify-between text-xs font-label-mono"><span class="text-secondary-fixed">POS</span><span id="txtPos" class="text-secondary-fixed">0%</span></div>
                                    <div class="w-full h-3 bg-surface-container rounded overflow-hidden shadow-inner"><div id="barPos" class="h-full bg-secondary-fixed rounded transition-all duration-500 ease-out" style="width:0%"></div></div>
                                </div>
                                
                                <div class="flex flex-col gap-2">
                                    <div class="flex justify-between text-xs font-label-mono"><span class="text-error">NEG</span><span id="txtNeg" class="text-error">0%</span></div>
                                    <div class="w-full h-3 bg-surface-container rounded overflow-hidden shadow-inner"><div id="barNeg" class="h-full bg-error rounded transition-all duration-500 ease-out" style="width:0%"></div></div>
                                </div>
                            </div>
                            
                            <div id="sentimentDialContainer" class="hidden mt-4 pt-4 border-t border-outline-variant/20">
                                <div class="text-[10px] font-label-mono text-outline text-center mb-2 uppercase tracking-widest">Live Voice Activity</div>
                                <div class="w-full h-[60px] bg-surface-container/30 rounded-t-full relative overflow-hidden border border-outline-variant/10 border-b-0">
                                    <div id="dialNeedle" class="absolute bottom-0 left-1/2 w-1 h-[50px] bg-primary origin-bottom shadow-[0_0_5px_#00dbe7]" style="transform: translate(-50%, 0) rotate(0deg); transition: transform 0.2s;"></div>
                                </div>
                            </div>
                            
                            <div class="mt-auto text-[10px] font-label-mono text-outline pt-4 border-t border-outline-variant/20 flex justify-between">
                                <span>CONF: <span id="singleConfidence" class="text-primary font-bold">0%</span></span>
                                <span>SCORE: <span id="singleScore" class="text-primary font-bold">0</span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Footer -->
            <footer class="flex justify-between items-center px-margin-desktop py-6 w-full bg-surface-container-lowest/80 dark:bg-surface-container-lowest/80 backdrop-blur-md border-t border-outline-variant/10 mt-auto">
                <div class="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface tracking-tighter">SENTIMENT.</div>
                <div class="hidden md:flex gap-6">
                    <a class="text-outline-variant hover:text-primary transition-colors font-label-mono text-label-mono" href="#">Privacy Policy</a>
                    <a class="text-outline-variant hover:text-primary transition-colors font-label-mono text-label-mono" href="#">Terms of Service</a>
                </div>
                <div class="font-label-mono text-label-mono text-secondary dark:text-secondary-fixed">
                    © 2026 SENTIMENT ANALYTICS
                </div>
            </footer>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    create_index_html()
