import streamlit as st
import re

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}
.stApp { background-color: #0a0a0f; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}
            
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #6b7280;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.stTextInput > div > div > input {
    background-color: #13131f !important;
    border: 1px solid #2d2d45 !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 2px rgba(167,139,250,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 2rem !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }

.step-card {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.step-card.active {
    border-color: #a78bfa;
    box-shadow: 0 0 20px rgba(167,139,250,0.08);
}
.step-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.25rem;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #c4b5fd;
}
.step-content {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #9ca3af;
    line-height: 1.7;
    margin-top: 0.75rem;
    white-space: pre-wrap;
    word-break: break-word;
    padding-right: 0.5rem;
}
.badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    margin-left: 0.5rem;
    vertical-align: middle;
}
.badge-done   { background: #14532d; color: #4ade80; }
.badge-active { background: #2e1065; color: #c4b5fd; }

.report-card {
    background: linear-gradient(160deg, #0f0f1a, #13131f);
    border: 1px solid #2d2d45;
    border-radius: 14px;
    padding: 2rem;
    margin-top: 1rem;
}
.report-text {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    line-height: 1.85;
    color: #d1d5db;
    white-space: pre-wrap;
}
.feedback-card {
    background: #0d1117;
    border: 1px solid #1c2a1c;
    border-left: 3px solid #34d399;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
}
.feedback-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #6ee7b7;
    line-height: 1.75;
    white-space: pre-wrap;
}
.divider {
    border: none;
    border-top: 1px solid #1e1e30;
    margin: 1.5rem 0;
}
.step-content::-webkit-scrollbar { width: 4px; }
.step-content::-webkit-scrollbar-track { background: transparent; }
.step-content::-webkit-scrollbar-thumb { background: #2d2d45; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Research Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Multi-Stage AI Orchestration Pipeline</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="Enter a research topic — e.g. Quantum computing breakthroughs 2025",
    )
with col_btn:
    run = st.button("Run →")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Helper ─────────────────────────────────────────────────────────────────────
def extract_first_url(text):
    urls = re.findall(r'https?://\S+', text)
    return urls[0] if urls else None

def render_step(ph, num, title, content=None, done=False, active=False):
    badge = ""
    if done:
        badge = '<span class="badge badge-done">DONE</span>'
    elif active:
        badge = '<span class="badge badge-active">RUNNING</span>'
    content_html = f'<div class="step-content">{content}</div>' if content else ""
    card_class = "step-card active" if active else "step-card"
    ph.markdown(f"""
    <div class="{card_class}">
        <div class="step-label">Step {num}</div>
        <div class="step-title">{title}{badge}</div>
        {content_html}
    </div>
    """, unsafe_allow_html=True)

# ── Pipeline ───────────────────────────────────────────────────────────────────
if run and topic.strip():

    try:
        from tools import search_web, scrape_url
        from agents import writer_chain, critic_chain
    except Exception as e:
        st.error(f"Import error: {e}")
        st.stop()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("### Pipeline Stages")
        s1 = st.empty()
        s2 = st.empty()
        s3 = st.empty()
        s4 = st.empty()

        render_step(s1, 1, "Web Search")
        render_step(s2, 2, "Scrape Top URL")
        render_step(s3, 3, "Writer Agent")
        render_step(s4, 4, "Critic Agent")

    with right:
        st.markdown("### Output")
        report_ph   = st.empty()
        feedback_ph = st.empty()

    state = {}

    # Step 1
    render_step(s1, 1, "Web Search", active=True)
    search_result = search_web.invoke(topic)
    state["search_results"] = search_result
    render_step(s1, 1, "Web Search", content=search_result, done=True)

    # Step 2
    render_step(s2, 2, "Scrape Top URL", active=True)
    url = extract_first_url(state["search_results"])
    if url:
        scraped = scrape_url.invoke(url)
        state["scraped_content"] = scraped
        preview = f"URL: {url}\n\n{scraped}"
    else:
        state["scraped_content"] = "No URL found."
        preview = "No URL found."
    render_step(s2, 2, "Scrape Top URL", content=preview, done=True)

    # Step 3
    render_step(s3, 3, "Writer Agent", active=True)
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
    render_step(s3, 3, "Writer Agent", content="Report generated ✓", done=True)
    report_ph.markdown(f"""
    <div class="report-card">
        <div class="step-label" style="margin-bottom:0.75rem">Final Report</div>
        <div class="report-text">{state["report"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Step 4
    render_step(s4, 4, "Critic Agent", active=True)
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    render_step(s4, 4, "Critic Agent", content="Review complete ✓", done=True)
    feedback_ph.markdown(f"""
    <div class="feedback-card">
        <div class="step-label" style="color:#6b7280; margin-bottom:0.5rem">Critic Feedback</div>
        <div class="feedback-text">{state["feedback"]}</div>
    </div>
    """, unsafe_allow_html=True)

elif run and not topic.strip():
    st.warning("Please enter a research topic first.")

else:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: #374151;">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔬</div>
        <div style="font-family: 'Space Mono', monospace; font-size: 0.8rem; letter-spacing: 0.1em;">
            ENTER A TOPIC ABOVE AND PRESS RUN →
        </div>
    </div>
    """, unsafe_allow_html=True)