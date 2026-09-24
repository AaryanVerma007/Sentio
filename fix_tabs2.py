import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the incorrectly placed End of tabContentBattle
content = content.replace("                </div> <!-- End of tabContentBattle -->\n\n            <!-- GenAI Summary Section (Now integrated as part of results view) -->", "            <!-- GenAI Summary Section (Now integrated as part of results view) -->")

# 2. Place it right before the closing tag of macro-analysis section
content = content.replace("""                    </div>
                </div>
            </section>""", """                    </div>
                </div>
                </div> <!-- End of tabContentBattle -->
            </section>""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
