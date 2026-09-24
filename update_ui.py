import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = """            <!-- VIEW 2.5: DATA PIPELINE -->
            <section id="view-pipeline" class="view scroll-reveal">
                <div class="view-header">
                    <h2 class="anim-text">Data Pipeline</h2>
                </div>
                <!-- Purely decorative pipeline flow -->
                <div class="pipeline-flow" style="margin-top: 2rem;">
                    <div class="pipeline-line"></div>
                    <div class="pipeline-node active-node">
                        <div class="pipeline-icon"><i class="fa-solid fa-microphone"></i></div>
                        <div class="pipeline-title">Raw Source</div>
                        <div class="pipeline-desc">Voice / Text Stream</div>
                    </div>
                    <i class="fa-solid fa-arrow-right pipeline-arrow"></i>
                    <div class="pipeline-node active-node">
                        <div class="pipeline-icon"><i class="fa-solid fa-microchip"></i></div>
                        <div class="pipeline-title">Inference Engine</div>
                        <div class="pipeline-desc">NLP Processing</div>
                    </div>
                    <i class="fa-solid fa-arrow-right pipeline-arrow"></i>
                    <div class="pipeline-node active-node">
                        <div class="pipeline-icon"><i class="fa-solid fa-chart-column"></i></div>
                        <div class="pipeline-title">Actionable Data</div>
                        <div class="pipeline-desc">Classification Stream</div>
                    </div>
                </div>
            </section>

            <!-- VIEW 3: MICRO INFERENCE -->
            <section id="view-micro" class="view scroll-reveal">
                <div class="view-header">
                    <h2 class="anim-text">Micro Inference</h2>
                </div>
                
                <div class="micro-layout dashboard-panel" style="display: flex; gap: 2rem; margin-top: 2rem; padding: 2rem; background: rgba(0,0,0,0.2);">
                    
                    <!-- LEFT COLUMN: INPUT -->
                    <div class="micro-input-col" style="flex: 1; display: flex; flex-direction: column; gap: 1rem;">
                        <h3 class="anim-text" style="font-size: 1.2rem; color: var(--text-color); margin-bottom: 0;">Input Stream</h3>
                        <textarea id="singleInput" class="minimal-input anim-text" placeholder="Enter text for neural classification..." style="flex: 1; min-height: 150px; resize: none; padding: 1rem; border-radius: 8px; background: rgba(0,0,0,0.2);"></textarea>
                        
                        <div style="display: flex; gap: 1rem; align-items: center; margin-top: auto;">
                            <button id="voiceBtn" class="btn-secondary hover-magnetic" title="Live Voice" style="padding: 1rem; min-width: 50px;"><i class="fa-solid fa-microphone"></i></button>
                            <button id="singleButton" class="btn-primary hover-magnetic" style="flex: 1; padding: 1rem; justify-content: center;">Initialize Inference</button>
                        </div>
                    </div>

                    <!-- RIGHT COLUMN: OUTPUT -->
                    <div class="micro-output-col" style="flex: 1; border-left: 1px solid var(--border-color); padding-left: 2rem; display: flex; flex-direction: column; gap: 1rem;">
                        <h3 class="anim-text" style="font-size: 1.2rem; color: var(--text-color); margin-bottom: 0;">Classification Result</h3>
                        
                        <div id="microIdle" class="empty-state anim-text" style="flex: 1; display: flex; align-items: center; justify-content: center; min-height: 150px;">
                            Awaiting input stream...
                        </div>
                        
                        <div id="microLoading" class="loader-overlay hidden" style="flex: 1; position: relative; background: transparent; min-height: 150px;">
                            <div class="cyber-spinner"></div>
                            <div class="loader-text anim-text typewriter" style="margin-top: 1rem;">Computing tensors...</div>
                        </div>

                        <div id="singleResult" class="result-card hidden" style="width: 100%; border: none; background: transparent; padding: 0; margin: 0; flex: 1; display: flex; flex-direction: column;">
                            <div class="result-top" style="margin-bottom: 1.5rem; justify-content: space-between;">
                                <span class="result-label anim-text">Primary Sentiment:</span>
                                <span id="singleSentiment" class="result-badge" style="font-size: 1.2rem; padding: 0.5rem 1.5rem;">Neu</span>
                            </div>
                            
                            <div class="confidence-meters" style="gap: 1rem; flex: 1;">
                                <div class="meter">
                                    <div class="meter-info anim-text"><span>Positive</span><span id="txtPos">0%</span></div>
                                    <div class="meter-bar" style="height: 12px;"><div id="barPos" class="meter-fill pos-fill"></div></div>
                                </div>
                                <div class="meter">
                                    <div class="meter-info anim-text"><span>Negative</span><span id="txtNeg">0%</span></div>
                                    <div class="meter-bar" style="height: 12px;"><div id="barNeg" class="meter-fill neg-fill"></div></div>
                                </div>
                            </div>
                            
                            <div class="dial-container hidden" id="sentimentDialContainer" style="margin-top: 2rem;">
                                <div class="dial-header anim-text">Live Voice Sentiment</div>
                                <div class="speedometer" style="height: 80px; margin-top: 1rem;">
                                    <div class="dial-needle" id="dialNeedle"></div>
                                </div>
                            </div>
                            
                            <div class="result-bottom anim-text" style="margin-top: auto; padding-top: 1rem; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between;">
                                <span>Confidence: <span id="singleConfidence" class="text-accent">0.0%</span></span>
                                <span>Aggregated Score: <span id="singleScore" class="text-accent">0.0</span></span>
                            </div>
                        </div>
                    </div>

                </div>
            </section>"""

# Find where the old view-micro started and ended
start_idx = content.find('            <!-- VIEW 3: MICRO INFERENCE -->')
end_idx = content.find('        </main>', start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_content + '\n\n' + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# We also need to add navigation for view-pipeline in the sidebar
nav_pipeline = """                    <a href="#view-pipeline" class="nav-btn">
                        <i class="fa-solid fa-arrow-progress"></i> <span class="anim-text">Data Pipeline</span>
                    </a>
                    <a href="#view-summary" class="nav-btn">"""
content = content.replace('                    <a href="#view-summary" class="nav-btn">', nav_pipeline)

# Wait, FontAwesome doesn't have fa-arrow-progress. Use fa-diagram-project or fa-network-wired
content = content.replace('fa-arrow-progress', 'fa-network-wired')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
