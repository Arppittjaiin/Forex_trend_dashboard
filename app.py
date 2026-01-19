import streamlit as st
import streamlit.components.v1 as components
import json

# Page configuration
st.set_page_config(
    page_title="Forex Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the main shell
st.markdown("""
<style>
    .stApp { background-color: #3D2B29; }
    header, footer, #MainMenu { visibility: hidden; }
    
    /* Style for Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(230, 196, 160, 0.1);
        border-radius: 10px 10px 0px 0px;
        color: #E6C4A0;
        font-weight: 700;
        padding: 10px 30px;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #E6C4A0 !important;
        color: #3D2B29 !important;
    }
</style>
""", unsafe_allow_html=True)

# Currency Data (major forex only)
CURRENCIES = {
    "CAD": {"flag": "https://flagcdn.com/w320/ca.png", "label": "CAD"},
    "EUR": {"flag": "https://flagcdn.com/w320/eu.png", "label": "EUR"},
    "CHF": {"flag": "https://flagcdn.com/w320/ch.png", "label": "CHF"},
    "JPY": {"flag": "https://flagcdn.com/w320/jp.png", "label": "JPY"},
    "NZD": {"flag": "https://flagcdn.com/w320/nz.png", "label": "NZD"},
    "USD": {"flag": "https://flagcdn.com/w320/us.png", "label": "USD"},
    "GBP": {"flag": "https://flagcdn.com/w320/gb.png", "label": "GBP"},
    "AUD": {"flag": "https://flagcdn.com/w320/au.png", "label": "AUD"},
}

def get_board_html(title, storage_key):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Outfit', sans-serif;
                background-color: #3D2B29;
                color: white;
                margin: 0;
                padding: 10px 20px;
                overflow: hidden;
            }}

            .header-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }}

            .title-box {{
                background-color: #E6C4A0;
                padding: 10px 40px;
                border-radius: 50px;
                color: #3D2B29;
                font-size: 1.8rem;
                font-weight: 800;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }}

            .btn-group {{ display: flex; gap: 12px; }}

            .action-btn {{
                padding: 8px 25px;
                border-radius: 30px;
                border: none;
                font-weight: 800;
                cursor: pointer;
                text-transform: uppercase;
                font-family: 'Outfit', sans-serif;
                transition: all 0.2s;
            }}

            .save-btn {{ background-color: #4CAF50; color: white; }}
            .reset-btn {{ background-color: #FF5252; color: white; }}
            .action-btn:hover {{ transform: translateY(-2px); filter: brightness(1.1); }}

            /* Bench */
            .bench-label {{ color: #E6C4A0; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; font-size: 0.9rem; }}
            .bench-container {{
                background: rgba(255, 255, 255, 0.04);
                padding: 15px;
                border-radius: 20px;
                border: 2px dashed rgba(230, 196, 160, 0.2);
                min-height: 90px;
                margin-bottom: 25px;
            }}

            .currency-list {{ display: flex; flex-wrap: wrap; gap: 12px; min-height: 70px; }}

            /* Cards */
            .currency-card {{ width: 105px; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: grab; }}
            .card-header {{ background-color: #E6C4A0; color: #3D2B29; text-align: center; font-weight: 800; padding: 4px; font-size: 0.9rem; }}
            .card-body {{ height: 65px; display: flex; align-items: center; justify-content: center; }}
            .card-body img {{ width: 100%; height: 100%; object-fit: cover; }}

            /* Dashboard */
            .board {{ display: flex; justify-content: space-between; gap: 10px; margin-bottom: 15px; }}
            .column-wrapper {{ flex: 1; display: flex; flex-direction: column; }}
            .drop-zone {{
                flex-grow: 1;
                min-height: 350px;
                display: flex;
                flex-direction: column-reverse; /* Bottom-up stacking */
                gap: 10px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.02);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.03);
            }}

            /* Scale Bar */
            .scale-bar {{ display: flex; width: 100%; height: 60px; border-radius: 15px; overflow: hidden; border: 3px solid #E6C4A0; }}
            .scale-item {{ flex: 1; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; }}
            .n3 {{ background: #D32F2F; }} .n2 {{ background: #F44336; }} .n1 {{ background: #FF8A80; }}
            .zero {{ background: #AFB42B; }} .p1 {{ background: #8BC34A; }} .p2 {{ background: #4CAF50; }} .p3 {{ background: #2E7D32; }}

            .sortable-ghost {{ opacity: 0.2; }}

            /* Modal & Toast */
            .overlay {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.8); display: none; align-items: center; justify-content: center; z-index: 1000;
            }}
            .confirm-box {{ background: #E6C4A0; padding: 25px; border-radius: 20px; color: #3D2B29; text-align: center; max-width: 350px; }}
            .confirm-actions {{ display: flex; gap: 10px; justify-content: center; margin-top: 15px; }}
            .confirm-btn {{ padding: 8px 20px; border-radius: 8px; border: none; font-weight: 700; cursor: pointer; }}
            .yes-btn {{ background: #3D2B29; color: white; }}
            .no-btn {{ background: rgba(0,0,0,0.1); color: #3D2B29; }}
            .toast {{
                position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
                background: #4CAF50; color: white; padding: 10px 30px; border-radius: 50px;
                font-weight: 800; display: none; z-index: 2000;
            }}
        </style>
    </head>
    <body>
        <div class="header-bar">
            <div class="title-box">{title}</div>
            <div class="btn-group">
                <button class="action-btn reset-btn" onclick="showConfirm('reset')">Reset</button>
                <button class="action-btn save-btn" onclick="showConfirm('save')">Save {title}</button>
            </div>
        </div>

        <div class="bench-label">Currency Bench</div>
        <div class="bench-container"><div id="bench" class="currency-list"></div></div>

        <div class="board">
            <div class="column-wrapper"><div id="col-n3" class="drop-zone"></div></div>
            <div class="column-wrapper"><div id="col-n2" class="drop-zone"></div></div>
            <div class="column-wrapper"><div id="col-n1" class="drop-zone"></div></div>
            <div class="column-wrapper"><div id="col-0" class="drop-zone"></div></div>
            <div class="column-wrapper"><div id="col-p1" class="drop-zone"></div></div>
            <div class="column-wrapper"><div id="col-p2" class="drop-zone"></div></div>
            <div class="column-wrapper"><div id="col-p3" class="drop-zone"></div></div>
        </div>

        <div class="scale-bar">
            <div class="scale-item n3">-3</div><div class="scale-item n2">-2</div><div class="scale-item n1">-1</div>
            <div class="scale-item zero">0</div><div class="scale-item p1">+1</div><div class="scale-item p2">+2</div><div class="scale-item p3">+3</div>
        </div>

        <div id="overlay" class="overlay">
            <div class="confirm-box">
                <h3 id="confirm-title">Confirm</h3>
                <p id="confirm-msg">Proceed?</p>
                <div class="confirm-actions">
                    <button class="confirm-btn yes-btn" onclick="proceed()">Yes</button>
                    <button class="confirm-btn no-btn" onclick="closeConfirm()">Cancel</button>
                </div>
            </div>
        </div>
        <div id="toast" class="toast">Saved!</div>

        <script>
            const currencies = {json.dumps(CURRENCIES)};
            const STORAGE_KEY = '{storage_key}';
            let pendingAction = null;

            const containers = {{
                'bench': document.getElementById('bench'),
                '-3': document.getElementById('col-n3'),
                '-2': document.getElementById('col-n2'),
                '-1': document.getElementById('col-n1'),
                '0': document.getElementById('col-0'),
                '1': document.getElementById('col-p1'),
                '2': document.getElementById('col-p2'),
                '3': document.getElementById('col-p3')
            }};

            function createCard(id) {{
                const data = currencies[id];
                const div = document.createElement('div');
                div.className = 'currency-card';
                div.dataset.id = id;
                div.innerHTML = `<div class="card-header">${{data.label}}</div><div class="card-body"><img src="${{data.flag}}"></div>`;
                return div;
            }}

            function init() {{
                const saved = localStorage.getItem(STORAGE_KEY);
                const state = saved ? JSON.parse(saved) : {{
                    "bench": ["CAD", "EUR", "CHF", "JPY", "NZD", "USD", "GBP", "AUD"],
                    "-3": [], "-2": [], "-1": [], "0": [], "1": [], "2": [], "3": []
                }};

                Object.keys(state).forEach(key => {{
                    const container = containers[key];
                    if (container) state[key].forEach(id => container.appendChild(createCard(id)));
                }});

                Object.values(containers).forEach(container => {{
                    new Sortable(container, {{ group: 'shared', animation: 150, ghostClass: 'sortable-ghost' }});
                }});
            }}

            function saveBoard() {{
                const state = {{}};
                Object.keys(containers).forEach(key => {{
                    state[key] = Array.from(containers[key].children).map(c => c.dataset.id);
                }});
                localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
                showToast("✅ {title} Saved!");
            }}

            function showConfirm(action) {{
                pendingAction = action;
                document.getElementById('confirm-title').innerText = action === 'save' ? 'Save {title}?' : 'Reset Board?';
                document.getElementById('confirm-msg').innerText = action === 'save' ? 'Save current positions?' : 'Clear all memory for this tab?';
                document.getElementById('overlay').style.display = 'flex';
            }}

            function closeConfirm() {{ document.getElementById('overlay').style.display = 'none'; }}
            function proceed() {{
                if (pendingAction === 'save') saveBoard();
                else if (pendingAction === 'reset') {{ localStorage.removeItem(STORAGE_KEY); location.reload(); }}
                closeConfirm();
            }}

            function showToast(msg) {{
                const t = document.getElementById('toast');
                t.innerText = msg; t.style.display = 'block';
                setTimeout(() => {{ t.style.display = 'none'; }}, 3000);
            }}

            init();
        </script>
    </body>
    </html>
    """

# App Header
st.markdown('<div style="text-align: center; margin-bottom: 20px;"><h1 style="color: #E6C4A0; font-family: Outfit; font-weight: 800; font-size: 3rem;">Forex Analysis Pro</h1></div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_trend, tab_velocity = st.tabs(["📊 Trend Score", "🚀 Velocity Score"])

with tab_trend:
    components.html(get_board_html("Trend Score", "forex_trend_placements"), height=900)

with tab_velocity:
    components.html(get_board_html("Velocity Score", "forex_velocity_placements"), height=900)
