# 🚛 Pro Driver Payroll System

**Professional Accounting & Analytics System** for trucking companies – parse trip data, match with invoices, resolve conflicts, and generate insightful reports.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Table of Contents
- [✨ Features](#-features)
- [⚙️ Technology Stack](#️-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [🧪 Running Tests](#-running-tests)
- [📂 Input File Formats](#-input-file-formats)
- [🖥️ Usage](#️-usage)
- [📊 Output Reports](#-output-reports)
- [📄 License](#-license)

---

## ✨ Features

- **Automatic Parsing** – reads `.txt` files containing trip details and invoice data.
- **Conflict Resolution** – detects multi‑driver trips, paid trips without assigned drivers, and extra pay entries; lets you resolve them interactively.
- **Dynamic Analytics** – real‑time metrics (total paid, average RPM, top earners) with interactive charts (Plotly).
- **Detailed Driver Stats** – per‑driver breakdown: total earnings, trips, miles, RPM, completion rate.
- **Export Reports** – download **TXT** and **Excel** reports (with per‑driver sheets and summary).
- **Glass‑morphism UI** – modern, animated, and responsive design built with Streamlit.
- **RPM & Mileage Support** – automatically extracts revenue per mile and distance from trip files.

---

## ⚙️ Technology Stack

- **Frontend/UI** – [Streamlit](https://streamlit.io/)
- **Data Processing** – Pandas, NumPy
- **Visualization** – Plotly Express
- **Excel Export** – XlsxWriter
- **Testing** – Pytest
- **Language** – Python 3.9+

---

## 📁 Project Structure
```
ProDriverPayrollSystem/
├── app.py                     # Main Streamlit application
├── config.py                  # Configuration (patterns, columns)
├── core/
│   ├── __init__.py
│   ├── models.py              # Dataclasses: Trip, Invoice, InvoiceItem
│   ├── parsers.py             # TripsParser, InvoiceParser
│   ├── calculator.py          # DataFrame builder & driver stats
│   └── exporter.py            # TXT and Excel report generators
├── ui/
│   ├── __init__.py
│   ├── sidebar.py             # Sidebar with file uploads
│   ├── components.py          # Reusable UI components (glass cards, charts)
│   └── pages.py               # Analytics and Data tabs
├── utils/
│   ├── helpers.py             # Currency parsing, formatting, normalization
├── tests/
│   ├── conftest.py            # Fixtures for testing
│   ├── test_parsers.py
│   ├── test_calculator.py
│   ├── test_exporter.py
│   └── test_helpers.py
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ProDriverPayrollSystem.git
   cd ProDriverPayrollSystem
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not provided, install manually:
   ```bash
   pip install streamlit pandas plotly xlsxwriter pytest
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```
   The app will open in your default browser at `http://localhost:8501`.

---

## 🧪 Running Tests

Execute the test suite using **pytest**:
```bash
pytest tests/
```
All tests are located in the `tests/` folder and cover parsing, calculation, export, and helpers.

---

## 📂 Input File Formats

The system expects **two plain text (`.txt`)** files:

### 1. Trips File
Contains detailed trip data. The parser recognises:
- Trip IDs (e.g., `T-114BSKL1H`)
- Driver names (e.g., `D. Hodjaev, N. Ohai`)
- Expected pay (lines starting with `$`, e.g., `$1,096.15`)
- **RPM** (lines like `$2.72/mi`)
- **Miles** (lines like `404 mi`)
- Locations and timestamps
- Status indicators (`Rejected`, `Canceled`)

> **Example snippet:**
> ```
> T-114BSKL1H
> Spot
> ACY9 Swedesboro, NJ 08085
> Sat, Jan 17, 18:26 EST
> BOS7 Fall River, MA 02720
> Sun, Jan 18, 07:00 EST
> 404 mi
> $1,096.15
> $2.72/mi
> D. Hodjaev, N. Ohai
> 3/4 Loads
> ```

### 2. Invoice File
A **tab‑separated** (or custom delimiter) CSV‑like file containing invoice details.  
Columns (at minimum):
- `Block ID`, `Trip ID`, or `Load ID` – to match trips
- `Gross Pay` – paid amount
- `Route` (optional)
- `Distance (Mi)` or `Miles` – if available, it will be used for mileage stats

> The delimiter and column names for miles are configurable in `config.py`.

---

## 🖥️ Usage

1. **Upload files** via the sidebar:
   - Click **“Trips File (.txt)”** and select your trips file.
   - Click **“Invoice File (.txt)”** and select your invoice file.

2. **Resolve conflicts** (if any):
   - The system will automatically detect multi‑driver trips, paid trips without drivers, and extra invoices.
   - You will see a **“Diqqat Talab”** section where you can assign drivers using dropdowns and the **“Assign”** button.

3. **Explore Analytics**:
   - The **“Smart Analytics”** tab shows:
     - Summary metrics (total paid, total invoice, difference, number of loads, average RPM).
     - **Top 15 earners** bar chart.
     - **Top 15 RPM** bar chart (if RPM data exists).

4. **View Data & Export**:
   - The **“Data & Export”** tab displays a full data table.
   - Filter by driver using the dropdown.
   - Driver statistics (earnings, trips, miles, RPM, completion rate) are shown in mini‑cards.
   - Download reports:
     - **TXT** – plain text report with per‑driver breakdowns.
     - **Excel** – multi‑sheet workbook with summary and individual driver sheets.

5. **Refresh** – use the **“Yangilash”** (Refresh) button in the sidebar to clear session state and start fresh.

---

## 📊 Output Reports

### TXT Report
- A human‑readable report with section per driver.
- Shows total paid, pending amounts, miles, RPM, and a detailed table of each trip.
- Ends with grand totals.

### Excel Report
- **Summary sheet** – overview of all drivers with total paid, pending, trips, miles, and average RPM.
- **Per‑driver sheets** – detailed trip list with all fields; includes a **TOTAL GROSS** row at the bottom.
- All numeric values are properly formatted (currency, numbers, decimals).

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 💬 Contact

For questions or suggestions, please open an issue or reach out to the maintainer.

---

**Happy trucking!** 🚛💨