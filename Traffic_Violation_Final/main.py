import streamlit as st
from pathlib import Path
import pandas as pd
from utils import apply_theme

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Traffic Violation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"   # ✅ FORCE SIDEBAR VISIBLE
)

#-------------------------------------------------
# LOAD DATA ONCE
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Indian_Traffic_Violations_cleaned.csv")

df = load_data()

# Apply premium purple theme
apply_theme()

# Bootstrap Icons
st.markdown("""
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
""", unsafe_allow_html=True)

# Inject custom stylesheet (if present) so `styles/main.css` is applied
try:
    with open("styles/main.css", "r", encoding="utf-8") as _css_file:
        _css = _css_file.read()
        st.markdown(f"<style>{_css}</style>", unsafe_allow_html=True)
except Exception:
    # If loading fails, continue without breaking the app
    pass

# Add a persistent JS toggle button in case Streamlit's toggle becomes hidden
_sidebar_toggle_js = r'''
<script>
(function(){
    const SIDEBAR_SELECTOR = 'aside[data-testid="stSidebar"]';
    function ensureButton(){
        if(document.getElementById('custom-sidebar-toggle')) return;
        const btn = document.createElement('button');
        btn.id='custom-sidebar-toggle';
        btn.title = 'Toggle sidebar';
        btn.innerHTML='&#187;';
        Object.assign(btn.style,{
                position:'fixed',
                left:'8px',
                top:'12px',
                zIndex:2147483647,
                width:'34px',
                height:'34px',
                borderRadius:'6px',
                border:'none',
                background:'#0f172a',
                color:'#ffffff',
                cursor:'pointer',
                boxShadow:'0 2px 8px rgba(2,6,23,0.3)'
        });
        btn.onclick = function(){
            const aside = document.querySelector(SIDEBAR_SELECTOR);
            const container = document.querySelector('.main .block-container');
            if(!aside || !container) return;
            const left = getComputedStyle(aside).left;
            const isHidden = left && (left.indexOf('-') === 0 || left === 'auto');
            if(isHidden){
                aside.style.left = '0px';
                container.style.marginLeft = '300px';
                localStorage.setItem('mySidebarCollapsed','false');
            } else {
                aside.style.left = '-340px';
                container.style.marginLeft = '0px';
                localStorage.setItem('mySidebarCollapsed','true');
            }
        };
        document.body.appendChild(btn);
        // initialize from saved state
        setTimeout(()=>{
            const aside = document.querySelector(SIDEBAR_SELECTOR);
            const container = document.querySelector('.main .block-container');
            if(!aside || !container) return;
            const collapsed = localStorage.getItem('mySidebarCollapsed');
            if(collapsed === 'true'){
                aside.style.left = '-340px';
                container.style.marginLeft = '0px';
            } else {
                aside.style.left = '0px';
                container.style.marginLeft = '300px';
            }
        }, 200);
    }
    window.addEventListener('load', ensureButton);
    const obs = new MutationObserver(ensureButton);
    obs.observe(document.body, {childList:true, subtree:true});
})();
</script>
'''
st.markdown(_sidebar_toggle_js, unsafe_allow_html=True)
# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------


page = st.sidebar.radio(
 " Navigation",
    [
        "Home",
        "Dashboard",
        "Time Trend Analysis",
        "Environment Analysis",
        "Vehicle Analysis",
        "Driver Behaviour Analysis",
        "Payment Analysis",
        "Map Visualisation",
        "Report",
        "About"
    ],

)

st.sidebar.markdown("---")


st.sidebar.caption("Smart Traffic Violation Pattern Detector")

# --------------------------------------------------
# ROUTING (MATCHES YOUR FILES)
# --------------------------------------------------
if page == "Home":
    from views._1_Home import app
    app(df)

elif page == "Dashboard":
    from views._2_Dashboard import app
    app(df)

elif page == "Time Trend Analysis":
    from views._3_Time_Trend_Analysis import app
    app(df)

elif page == "Environment Analysis":
    from views._4_Environment_Analysis import app
    app(df)

elif page == "Vehicle Analysis":
    from views._5_Vehicle_Analysis import app
    app(df)

elif page == "Driver Behaviour Analysis":
    from views._6_Driver_Behaviour_Analysis import app
    app(df)

elif page == "Payment Analysis":
    from views._7_Payment_Analysis import app
    app(df)



elif page == "Map Visualisation":
    from views._8_Map_Visualisation import app
    app(df)

elif page == "Report":
    from views._9_Report import app
    app(df)

elif page == "About":
    from views._10_About import app
    app(df)


