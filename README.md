# 💹 Forex Analysis Terminal

A premium, high-performance dashboard for currency trend and velocity analysis. This terminal provides a visual interface for traders to organize and score major currency pairs based on their market performance.

---

## ✨ Features

- **Dynamic Scoring**: Drag-and-drop currency cards across a -3 to +3 scale.
- **Dual Analysis Tabs**: Separate boards for **Trend Score** and **Velocity Score**.
- **State Persistence**: Your placements are automatically saved to your browser's local storage.
- **Premium Aesthetics**: Bloomberg-inspired dark mode with glassmorphism and smooth animations.
- **Micro-Animations**: Real-time hover effects and interactive modal confirmations.
- **Multi-Runtime Support**: Run via Python (Streamlit) or a blazingly fast Rust backend (Axum).

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS (Custom Gradients & Shadows), Javascript (SortableJS).
- **Backend (Rust)**: [Axum](https://github.com/tokio-rs/axum) & [Tokio](https://tokio.rs/).
- **Backend (Python)**: [Streamlit](https://streamlit.io/).

---

## 🚀 Quick Start

### Option 1: Rust Backend (Recommended for Performance)
This version serves a highly optimized, single-page application.

1. Ensure you have [Rust](https://www.rust-lang.org/tools/install) installed.
2. Run the application:
   ```bash
   cargo run --release
   ```
3. Open your browser at `http://127.0.0.1:8080`.

### Option 2: Python (Streamlit)
Ideal for rapid prototyping or if you prefer a Python environment.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

---

## 📁 Project Structure

- `src/main.rs`: Rust Axum server implementation.
- `app.py`: Streamlit dashboard implementation.
- `static/index.html`: The core dashboard UI (premium version).
- `Cargo.toml`: Rust package dependencies.
- `requirements.txt`: Python package dependencies.
- `run.bat`: Quick-start batch file for Windows users.

---

## 🔒 Security & Data
All data is stored **locally** in your browser's cache. No currency data is sent to external servers, ensuring your analysis remains private.

---

*Designed for serious traders who value speed and clarity.*
