📌 BarakahMail Development Roadmap
✅ Core System Setup
[x] Gmail Cleaner script functional

[x] OAuth credentials rotated and secured

[x] .gitignore updated to exclude sensitive files

[x] Git history cleaned with git filter-repo

[x] Force-push completed to GitHub

[x] Mirror repo (gmail_agent.git) marked for deletion

📤 Outreach Engine
[ ] Parse lead data from leads.csv or targets.json

[ ] Generate personalized emails using Jinja2 or f-strings

[ ] Schedule and send emails with opt-out footer

[ ] Log email status: sent, opened, replied, unsubscribed

🧠 Mistral Summarisation Layer
[ ] Summarize incoming replies using Mistral

[ ] Classify responses: interested, not now, unsubscribe, unclear

[ ] Store summaries in responses.json or a database

🧭 Ethical Filters
[ ] Scan outgoing messages for manipulative language

[ ] Auto-include opt-out line in all emails

[ ] Maintain do_not_contact list

[ ] Enforce barakah_protocol.md rules (Shariah, consent, privacy, transparency)

📊 Observability & Feedback Loop
[ ] Generate daily digest of outreach activity

[ ] Allow manual override for lead follow-ups or rephrasing

[ ] Log assistant decisions (why, what, when)

[ ] Reflect every 24h or on performance/ethical triggers

🧪 Optional Validation Mode
[ ] Add --validate flag to test emails on sandboxed leads

[ ] Log effectiveness of tone, structure, and CTA

🌟 Barakah Score System
[ ] Assign a “Barakah Score” to each outreach action

[ ] Use score to guide future decisions and ethical alignment

🧬 Training & Personalisation Logic
[ ] Implement training_config.yaml and training_engine.py

[ ] Adaptive learning pace based on user edits

[ ] Tone calibration with feedback prompts

[ ] Optional spiritual nudges (Du’as, prayer breaks, verses)

[ ] Human-AI co-creation mode with tone/style learning

[ ] Guardrails: no strategy changes without logging, no ethics override