import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the messy structure
# 1. Remove the empty tabContentBattle
content = content.replace(
"""                <!-- TAB CONTENT: BATTLE MODE -->
                <div id="tabContentBattle" class="hidden reveal-item reveal-hidden">
                </div>""",
""
)

# 2. Add the closing div for tabContentSingle before searchBattle, and open tabContentBattle there
single_to_battle = """
                <!-- Search Input: Battle -->"""
new_single_to_battle = """
                </div> <!-- End of tabContentSingle -->

                <!-- TAB CONTENT: BATTLE MODE -->
                <div id="tabContentBattle" class="hidden reveal-item reveal-hidden">
                <!-- Search Input: Battle -->"""
content = content.replace(single_to_battle, new_single_to_battle)

# 3. Remove the rogue closing div that was after searchBattle (line 436)
# It looked like this:
#                 <button id="battleButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed disabled:opacity-50 disabled:cursor-not-allowed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)]">Analyze Battle</button>
#                 </div>
#                 </div>

rogue_div = """<button id="battleButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed disabled:opacity-50 disabled:cursor-not-allowed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)]">Analyze Battle</button>
                </div>
                </div>"""
fixed_div = """<button id="battleButton" class="px-10 py-6 text-lg bg-primary text-on-primary font-bold uppercase tracking-wider hover:bg-primary-fixed disabled:opacity-50 disabled:cursor-not-allowed transition-all rounded-lg shadow-[0_0_15px_rgba(0,219,231,0.3)]">Analyze Battle</button>
                </div>"""
content = content.replace(rogue_div, fixed_div)

# 4. We need to close tabContentBattle after battleResults.
# battleResults ends right before: <!-- GenAI Summary Section (Now integrated as part of results view) -->
# Let's find the closing of battleResults section
battle_results_end_marker = """            <!-- GenAI Summary Section (Now integrated as part of results view) -->"""
content = content.replace(
    battle_results_end_marker,
    "                </div> <!-- End of tabContentBattle -->\n\n" + battle_results_end_marker
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
