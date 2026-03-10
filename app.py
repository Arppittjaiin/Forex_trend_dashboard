import streamlit as st
import streamlit.components.v1 as components
import json

# Page configuration
st.set_page_config(
    page_title="Forex Analysis Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the main shell
st.markdown("""
<style>
    /* Bloomberg Terminal Style */
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    
    .stApp { 
        background-color: #000000; 
        font-family: 'Roboto Mono', 'Courier New', monospace;
    }
    header, footer, #MainMenu { visibility: hidden; }
    
    /* Style for Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: #000000;
        justify-content: flex-start;
        border-bottom: 2px solid #333;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #111;
        border-radius: 0px;
        color: #888;
        font-family: 'Roboto Mono', monospace;
        font-weight: 700;
        padding: 5px 20px;
        border: 1px solid #333;
        border-bottom: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #000000 !important;
        color: #FFA500 !important;
        border: 1px solid #FFA500 !important;
        border-bottom: 2px solid #000 !important;
        margin-bottom: -2px;
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
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Roboto Mono', 'Courier New', monospace;
                background-color: #000000;
                color: #FFA500;
                margin: 0;
                padding: 10px 20px;
                overflow: hidden;
            }}

            .header-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                border-bottom: 1px solid #333;
                padding-bottom: 10px;
            }}

            .title-box {{
                background-color: #000;
                padding: 5px 15px;
                border: 1px solid #FFA500;
                color: #FFA500;
                font-size: 1.5rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .btn-group {{ display: flex; gap: 10px; }}

            .action-btn {{
                padding: 6px 15px;
                background-color: #000;
                border: 1px solid #555;
                color: #CCC;
                font-weight: 700;
                cursor: pointer;
                text-transform: uppercase;
                font-family: 'Roboto Mono', monospace;
                transition: all 0.2s;
                font-size: 0.8rem;
            }}

            .save-btn {{ border-color: #00FF00; color: #00FF00; }}
            .reset-btn {{ border-color: #FF0000; color: #FF0000; }}
            .save-btn:hover {{ background-color: #003300; }}
            .reset-btn:hover {{ background-color: #330000; }}

            /* Bench */
            .bench-label {{ color: #888; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; font-size: 0.8rem; }}
            .bench-container {{
                background: #050505;
                padding: 10px;
                border: 1px solid #333;
                min-height: 80px;
                margin-bottom: 20px;
            }}

            .currency-list {{ display: flex; flex-wrap: wrap; gap: 8px; min-height: 60px; }}

            /* Cards */
            .currency-card {{ width: 90px; background: #000; border: 1px solid #444; overflow: hidden; cursor: grab; display: flex; flex-direction: column; }}
            .card-header {{ background-color: #111; color: #FFA500; text-align: center; font-weight: 700; padding: 4px; font-size: 0.9rem; border-bottom: 1px solid #444; }}
            .card-body {{ height: 50px; display: flex; align-items: center; justify-content: center; background: #000; }}
            .card-body img {{ width: 100%; height: 100%; object-fit: cover; filter: grayscale(20%) contrast(120%); }}

            /* Dashboard */
            .board {{ display: flex; justify-content: space-between; gap: 4px; margin-bottom: 15px; }}
            .column-wrapper {{ flex: 1; display: flex; flex-direction: column; }}
            .drop-zone {{
                flex-grow: 1;
                min-height: 350px;
                display: flex;
                flex-direction: column-reverse; /* Bottom-up stacking */
                gap: 5px;
                padding: 8px;
                background: #050505;
                border: 1px solid #333;
            }}

            /* Scale Bar */
            .scale-bar {{ display: flex; width: 100%; height: 40px; border: 1px solid #555; background: #111; gap: 1px; }}
            .scale-item {{ flex: 1; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700; color: #000; background: #333; }}
            .n3 {{ background: #FF0000; color: #fff;}} .n2 {{ background: #CC0000; color: #fff; }} .n1 {{ background: #990000; color: #fff; }}
            .zero {{ background: #888888; color: #fff; }} .p1 {{ background: #006600; color: #fff; }} .p2 {{ background: #009900; color: #fff; }} .p3 {{ background: #00FF00; color: #000; }}

            .sortable-ghost {{ opacity: 0.4; outline: 1px dashed #FFA500; }}

            /* Modal & Toast */
            .overlay {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.9); display: none; align-items: center; justify-content: center; z-index: 1000;
            }}
            .confirm-box {{ background: #000; padding: 20px; border: 1px solid #FFA500; color: #FFA500; text-align: center; width: 300px; font-family: 'Roboto Mono', monospace; }}
            .confirm-actions {{ display: flex; gap: 10px; justify-content: center; margin-top: 15px; }}
            .confirm-btn {{ padding: 5px 15px; border: 1px solid #555; background: #111; color: #CCC; font-weight: 700; cursor: pointer; text-transform: uppercase; font-family: 'Roboto Mono', monospace; }}
            .yes-btn {{ border-color: #FFA500; color: #FFA500; }}
            .yes-btn:hover {{ background: #332000; }}
            .no-btn:hover {{ background: #333; }}
            .toast {{
                position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
                background: #000; color: #00FF00; padding: 10px 20px; border: 1px solid #00FF00;
                font-weight: 700; display: none; z-index: 2000; font-family: 'Roboto Mono', monospace;
                text-transform: uppercase; box-shadow: 0 0 10px rgba(0,255,0,0.2);
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
st.markdown('<div style="text-align: center; margin-bottom: 20px;"><h1 style="color: #FFA500; font-family: \'Roboto Mono\', monospace; font-weight: 700; font-size: 2.5rem; letter-spacing: 2px; text-transform: uppercase; border-bottom: 2px solid #333; padding-bottom: 10px;">TERMINAL FX // ANALYSIS</h1></div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_trend, tab_velocity = st.tabs(["[ TREND SCORE ]", "[ VELOCITY SCORE ]"])

with tab_trend:
    components.html(get_board_html("Trend Score", "forex_trend_placements"), height=900)

with tab_velocity:
    components.html(get_board_html("Velocity Score", "forex_velocity_placements"), height=900)
