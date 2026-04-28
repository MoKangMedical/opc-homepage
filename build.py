#!/usr/bin/env python3
"""
MoKangMedical Homepage Builder
Reads data.json + github_stats.json -> generates index.html
Usage: python3 build.py
"""

import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "data.json")) as f:
    data = json.load(f)

stats = {}
stats_path = os.path.join(BASE, "github_stats.json")
if os.path.exists(stats_path):
    with open(stats_path) as f:
        stats = json.load(f)

total_projects = sum(len(s["projects"]) for s in data["segments"])
total_stars = sum(s.get("stars", 0) for s in stats.values())
live_count = sum(1 for s in data["segments"] for p in s["projects"] if p["status"] == "live")
dev_count = total_projects - live_count
today = datetime.date.today().strftime("%B %Y")


def tier_badge(tier):
    labels = {
        "cash-cow": "Cash Cow", "growth": "Growth", "pipeline": "Pipeline",
        "moat": "Open Source", "support": "Support", "niche": "Niche"
    }
    return labels.get(tier, tier.title())


def proj_card(p, seg_id):
    g = stats.get(p["repo"], {})
    stars = g.get("stars", 0)
    forks = g.get("forks", 0)
    lang = g.get("language", "")
    stars_html = '<span class="stat-badge" title="Stars">&#9733; %d</span>' % stars if stars > 0 else ''
    forks_html = '<span class="stat-badge" title="Forks">&#9906; %d</span>' % forks if forks > 0 else ''
    lang_html = '<span class="stat-badge">%s</span>' % lang if lang else ''
    impact = p.get("impact", "")
    impact_html = '<div class="proj-impact">%s</div>' % impact if impact else ''
    status_cls = "live" if p["status"] == "live" else "dev"
    status_txt = "Live" if p["status"] == "live" else "In Dev"
    pages_url = p.get("pages_url", "")
    pages_link = (' <a href="%s" class="proj-link proj-link-demo" target="_blank" rel="noopener">Live Demo &rarr;</a>' % pages_url) if pages_url else ''
    pages_attr = 'true' if pages_url else 'false'
    return (
        '<div class="proj-card" data-seg="%s" data-tier="%s" data-status="%s" data-name="%s" data-pages="%s">'
        '<div class="tier tier-%s">%s</div>'
        '<div class="proj-name">%s</div>'
        '<div class="proj-desc">%s</div>'
        '%s'
        '<div class="proj-meta">%s%s%s</div>'
        '<div class="proj-footer">'
        '<div class="proj-status status-%s"><span class="dot-sm"></span>%s</div>'
        '<div class="proj-links">'
        '<a href="https://github.com/MoKangMedical/%s" class="proj-link" target="_blank" rel="noopener">GitHub &rarr;</a>'
        '%s'
        '</div>'
        '</div></div>'
    ) % (seg_id, p["tier"], p["status"], p["name"].lower(), pages_attr,
         p["tier"], tier_badge(p["tier"]),
         p["name"], p["desc"],
         impact_html,
         stars_html, forks_html, lang_html,
         status_cls, status_txt, p["repo"],
         pages_link)


# Build segments HTML
segments_html = ""
nav_links = ""
for seg in data["segments"]:
    color = seg["color"]
    sid = seg["id"]
    cards = "".join(proj_card(p, sid) for p in seg["projects"])
    segments_html += (
        '<section class="segment" id="%s">'
        '<div class="seg-header reveal">'
        '<div class="seg-dot" style="background:%s"></div>'
        '<div class="seg-titles"><h2>%s</h2><span class="seg-zh">%s</span></div>'
        '<span class="seg-count">%d projects</span>'
        '</div>'
        '<p class="seg-tagline reveal">%s</p>'
        '<div class="projects-grid">%s</div>'
        '</section>'
    ) % (sid, color, seg["name"], seg["nameZh"], len(seg["projects"]), seg["tagline"], cards)
    short_name = seg["name"].split("&")[0].strip()
    nav_links += '<a href="#%s">%s</a>' % (sid, short_name)

# Featured Demos HTML — top live projects with pages_url
featured_projects = [p for seg in data["segments"] for p in seg["projects"]
                     if p.get("pages_url") and p["status"] == "live"]
# Prioritize cash-cow and growth tiers, then pipeline
tier_order = {"cash-cow": 0, "growth": 1, "pipeline": 2, "moat": 3, "niche": 4, "support": 5}
featured_projects.sort(key=lambda x: (tier_order.get(x.get("tier", ""), 9), x["name"]))
# Take top 6
featured_projects = featured_projects[:6]

featured_html = ""
fd_colors = ["#6366f1", "#ec4899", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4"]
fd_icons = ["&#9670;", "&#9670;", "&#9670;", "&#9670;", "&#9670;", "&#9670;"]
for i, p in enumerate(featured_projects):
    c = fd_colors[i % len(fd_colors)]
    seg_name = next((s["name"].split("&")[0].strip() for s in data["segments"]
                     if any(sp["repo"] == p["repo"] for sp in s["projects"])), "")
    featured_html += (
        '<div class="fd-card" style="--fd-accent:%s">'
        '<div class="fd-header">'
        '<div class="fd-dot" style="background:%s"></div>'
        '<span class="fd-segment">%s</span>'
        '</div>'
        '<div class="fd-name">%s</div>'
        '<div class="fd-desc">%s</div>'
        '<div class="fd-links">'
        '<a href="%s" class="fd-btn fd-btn-demo" target="_blank" rel="noopener">Live Demo</a>'
        '<a href="https://github.com/MoKangMedical/%s" class="fd-btn fd-btn-github" target="_blank" rel="noopener">GitHub</a>'
        '</div>'
        '</div>'
    ) % (c, c, seg_name, p["name"], p["desc"], p["pages_url"], p["repo"])

# Flywheels HTML
fw_html = ""
fw_icons = ["&#128300;", "&#129516;", "&#128131;", "&#127793;", "&#10024;"]
fw_colors = ["#6366f1", "#ec4899", "#10b981", "#06b6d4", "#f59e0b"]
for i, fw in enumerate(data["flywheels"]):
    fw_html += (
        '<div class="fw-card">'
        '<div class="fw-icon" style="background:%s22;color:%s">%s</div>'
        '<h3>%s</h3>'
        '<p class="fw-desc">%s</p>'
        '<div class="fw-tags"><span>%s</span><span>%d core projects</span></div>'
        '</div>'
    ) % (fw_colors[i], fw_colors[i], fw_icons[i],
         fw["name"], fw["description"], fw["arpu"], len(fw["projects"]))

# Team HTML
team_html = ""
for t in data["team_needs"]:
    p_cls = "urgent" if t["priority"] == "urgent" else "important"
    p_txt = "Urgent" if t["priority"] == "urgent" else "Important"
    team_html += (
        '<div class="team-card">'
        '<span class="team-badge %s">%s</span>'
        '<div><h4>%s</h4><p>%s</p><span class="team-type">%s</span></div>'
        '</div>'
    ) % (p_cls, p_txt, t["role"], t["desc"], t["type"])

# FAQ HTML
faq_items = [
    ("What is MoKangMedical?",
     "MoKangMedical is an AI-powered medical innovation ecosystem comprising %d+ open-source projects across drug discovery, clinical research, digital health, and solo entrepreneur empowerment." % total_projects),
    ("How can I use these projects?",
     "All projects are open-source on GitHub. You can use them directly, fork and customize, or contact us for enterprise deployment, custom development, and consulting services."),
    ("Do you offer enterprise support?",
     "Yes. We provide enterprise licenses, custom deployment, training, and dedicated support for research institutions, pharma companies, and healthcare organizations."),
    ("How do I collaborate or partner?",
     "We are actively seeking medical BD partners, knowledge monetization operators, overseas market BDs, full-stack engineers, and medical advisory board members."),
    ("How often are projects updated?",
     "Projects are actively maintained. New projects are added regularly. The homepage auto-syncs with GitHub for real-time stats."),
    ("Can I request a custom project?",
     "Absolutely. We build custom medical AI solutions leveraging our existing framework stack (Darwin, EvoX, Medical Harness)."),
]
faq_html = ""
for q, a in faq_items:
    faq_html += '<details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (q, a)

# Read template and replace placeholders
with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

html = template.replace("{{TOTAL_PROJECTS}}", str(total_projects))
html = html.replace("{{LIVE_COUNT}}", str(live_count))
html = html.replace("{{TOTAL_STARS}}", str(total_stars))
html = html.replace("{{TODAY}}", today)
html = html.replace("{{NAV_LINKS}}", nav_links)
html = html.replace("{{FEATURED_HTML}}", featured_html)
html = html.replace("{{FEATURED_COUNT}}", str(len(featured_projects)))
html = html.replace("{{FW_HTML}}", fw_html)
html = html.replace("{{SEGMENTS_HTML}}", segments_html)
html = html.replace("{{FAQ_HTML}}", faq_html)
html = html.replace("{{TEAM_HTML}}", team_html)

with open(os.path.join(BASE, "index.html"), "w") as f:
    f.write(html)

print("Built index.html: {:,} chars, {} projects, {} live, {} in dev".format(len(html), total_projects, live_count, dev_count))
