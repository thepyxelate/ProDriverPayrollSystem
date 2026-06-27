# 🚛 Pro Driver Payroll System

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Pro Driver Payroll System** is a premium, Streamlit-based web application designed for trucking companies and fleet managers. It automates the reconciliation of driver trip records with invoice data, providing real-time financial analytics, conflict resolution, and automated report generation (TXT & Excel). 

Featuring an advanced **Glassmorphism UI** with animated gradient backgrounds, the system is as beautiful as it is powerful.

---

## ✨ Key Features

* **🧠 Smart Data Parsing**: Custom Regex-powered engines (`TripsParser` and `InvoiceParser`) automatically extract IDs, driver names, locations, dates, and expected/gross pay from raw `.txt` files.
* **⚠️ Interactive Conflict Resolution**: Automatically detects and flags discrepancies such as multi-driver loads, paid loads with missing drivers, and extra payments. Users can manually assign drivers via the UI.
* **📊 Advanced Visual Analytics**:
    * **Top Earners**: Interactive horizontal bar charts of the top 15 drivers.
    * **Average & Trip Counts**: Dual-column metrics showing average earnings and highest trip volumes.
    * **Top Routes**: Profitability analysis of start-to-end routing.
* **👤 Driver-Specific Dashboards**: Deep-dive into individual driver metrics, including status distribution (Pie Chart), earnings histograms, and payment completion rate progress bars.
* **📥 Comprehensive Exports**: One-click generation of detailed summary reports in both **.txt** and cleanly formatted **.xlsx** (Excel) files.
* **🎨 Premium UI/UX**: Built with custom CSS to provide a modern "glass" effect, smooth transitions, and responsive data containers.

---

## 🚀 Installation & Setup

### 1. Prerequisites
Make sure you have Python 3.8+ installed on your machine.

### 2. Clone the Repository
```bash
git clone [https://github.com/yourusername/pro-driver-payroll.git](https://github.com/yourusername/pro-driver-payroll.git)
cd pro-driver-payroll