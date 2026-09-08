"""
UI helpers for FarmTech Solutions Streamlit app.

This module provides small reusable components and light CSS used
across the Streamlit pages to keep the UI consistent. Functions are
kept simple and intentionally do not contain business logic.
"""

import streamlit as st
from pathlib import Path
from PIL import Image


CSS = '''
<style>
body {background-color: #f6fbf7;}
.ft-hero{padding:24px;border-radius:12px;background:linear-gradient(90deg,#ffffffcc,#eaf7ee);box-shadow:0 4px 20px rgba(0,0,0,0.05);}
.ft-title{font-size:28px;color:#0b3d2e;margin:0}
.ft-sub{font-size:14px;color:#13505a;margin-top:4px}
.ft-card{padding:16px;border-radius:10px;background:#fff;border:1px solid #e6f0ea}
.ft-metric{padding:12px;border-radius:8px;background:linear-gradient(180deg,#ffffff,#f1fbf4);border:1px solid #e1efe2}
.ft-section{margin-top:28px;margin-bottom:18px}
.ft-flow{font-weight:600;color:#134b3d}
.ft-small{font-size:13px;color:#2b463f}
</style>
'''


def inject_css():
    """Inject the local CSS styles used by the app.

    This writes a small style block into the Streamlit page using
    `st.markdown(..., unsafe_allow_html=True)`. Kept minimal so it
    can be safely adjusted or replaced by a static asset later.
    """
    st.markdown(CSS, unsafe_allow_html=True)


def load_image_if_exists(path: str):
    """Load an image from disk if the path exists.

    Returns a PIL `Image` when the file exists and can be opened,
    otherwise returns `None`. The UI code should handle the `None`
    case and continue rendering without the image.
    """
    p = Path(path)
    if p.exists():
        try:
            return Image.open(p)
        except Exception:
            return None
    return None


def render_page_header(title: str, subtitle: str, icon: str = '🌱', banner: str = None):
    """Render a hero/header used on the landing page."""
    inject_css()
    img = load_image_if_exists(banner) if banner else None

    #st.markdown('<div class="ft-hero">', unsafe_allow_html=True)

    if img:
        st.image(img, use_container_width=True)

    st.markdown(
        f"""
        <div style="margin-top:18px">
            <div class="ft-title">{icon} {title}</div>
            <div class="ft-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)


def render_info_card(title: str, description: str, icon: str = ''):
    """Render a small info card used for feature summaries.

    This is a thin wrapper around `st.markdown` that outputs a small
    HTML block styled by the local CSS. Keep descriptions short.
    """
    st.markdown(f'<div class="ft-card"><strong>{icon} {title}</strong><div style="margin-top:6px" class="ft-small">{description}</div></div>', unsafe_allow_html=True)


def render_metric_card(label: str, value, delta=None, help_text: str = None):
    """Render a highlighted metric box using native Streamlit containers."""
    with st.container(border=True): # Cria a caixinha automaticamente
        if help_text:
            st.caption(help_text)
        st.metric(label, value, delta)


def render_section_divider(title: str = None):
    """Render a section title or a thin divider between UI blocks.

    Passing a `title` writes a small H4 styled header; otherwise a
    horizontal rule is emitted. This keeps page structure clear.
    """
    if title:
        st.markdown(f'<div style="margin-top:18px;margin-bottom:6px"><h4 style="color:#0b3d2e">{title}</h4></div>', unsafe_allow_html=True)
    else:
        st.markdown('<hr/>', unsafe_allow_html=True)
