# 📊 Portfolio Dashboard

A comprehensive Python-based portfolio analysis tool that fetches real-time stock data and generates detailed Excel reports with technical and fundamental analysis for Indian stocks and indices.

## 🚀 Features

### 📈 Technical Analysis
- **Price Changes**: Daily, Weekly, Monthly, YTD, and Yearly percentage changes
- **Real-time Data**: Live stock prices and historical data from Yahoo Finance
- **Multi-timeframe Analysis**: Track performance across different periods

### 💼 Fundamental Analysis
- **PE Ratio**: Price-to-Earnings ratio for valuation analysis
- **Industry PE**: Industry average PE for comparison
- **Market Cap**: Company size in Crores (₹)
- **Dividend Yield**: Income generation potential
- **Beta**: Risk/volatility coefficient

### 📊 Output
- **Excel Reports**: Comprehensive dashboard with multiple sheets
- **News Feed**: Placeholder for market news integration
- **Formatted Data**: Clean, readable tables with proper formatting

## 🛠️ Installation

### Prerequisites
- Python 3.13 or higher
- UV package manager (recommended) or pip

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/udayakiranss/portfolio-dashboard.git
   cd portfolio-dashboard
   ```

2. **Install dependencies using UV (recommended)**
   ```bash
   uv sync
   ```

   **Or using pip**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Basic Usage
```bash
# Using UV (recommended)
uv run main.py

# Using Python directly
python main.py
```

### Configuration
Edit the `STOCKS` and `INDEXES` lists in `main.py` to customize your portfolio:

```python
STOCKS = [
    "HDFCBANK.NS",
    "RELIANCE.NS", 
    "ICICIBANK.NS",
    "BEL.NS",          # Bharat Electronics
    "HAL.NS",          # Hindustan Aeronautics
    "GOLDBEES.NS",     # Gold ETF
    "SILVERBEES.NS",
    "TATAMOTORS.NS",
    "BHARTIARTL.NS"
]

INDEXES = ["^NSEI", "^BSESN"]  # Nifty 50 & BSE Sensex
```

## 📋 Output

The script generates `Portfolio_Analysis.xlsx` with two sheets:

### 📊 Dashboard Sheet
| Column | Description |
|--------|-------------|
| Stock | Stock/Index symbol |
| Daily Change % | Previous day's price change |
| Weekly Change % | 5-day price change |
| Monthly Change % | 21-day price change |
| YTD Change % | Year-to-date performance |
| Yearly Change % | 1-year performance |
| PE Ratio | Price-to-Earnings ratio |
| Industry PE | Industry average PE |
| Market Cap (Cr) | Market capitalization in Crores |
| Dividend Yield % | Annual dividend yield |
| Beta | Volatility relative to market |

### 📰 News Feed Sheet
Placeholder for market news and updates (currently contains sample data).

## 📊 Sample Output

```
📊 Starting Portfolio Analysis...
📈 Fetching data for HDFCBANK.NS...
✅ Successfully fetched data for HDFCBANK.NS
📈 Fetching data for RELIANCE.NS...
✅ Successfully fetched data for RELIANCE.NS
...
✅ Portfolio analysis saved to Portfolio_Analysis.xlsx
📋 Processed 11 stocks/indexes

📊 Summary:
   - Successfully fetched: 11/11
   - Failed fetches: 0/11
```

## 🔧 Dependencies

- **yfinance**: Yahoo Finance data fetching
- **pandas**: Data manipulation and analysis
- **xlsxwriter**: Excel file generation
- **openpyxl**: Excel file reading/writing
- **requests**: HTTP requests

## 📁 Project Structure

```
portfolio-dashboard/
├── main.py              # Main application script
├── pyproject.toml       # Project configuration and dependencies
├── uv.lock             # Dependency lock file
├── README.md           # This file
├── .gitignore          # Git ignore rules
├── .python-version     # Python version specification
└── Portfolio_Analysis.xlsx  # Generated output (not tracked)
```

## 🎯 Use Cases

### 📈 Portfolio Monitoring
- Track daily performance of your stock portfolio
- Monitor YTD and yearly returns
- Compare performance across different timeframes

### 💼 Investment Analysis
- Identify undervalued stocks (low PE ratios)
- Compare stock valuations with industry averages
- Assess risk through beta coefficients
- Evaluate dividend income potential

### 📊 Market Research
- Analyze sector performance through indices
- Track market trends and volatility
- Generate reports for investment decisions

## 🔍 Data Sources

- **Yahoo Finance**: Real-time stock data and fundamental metrics
- **NSE/BSE**: Indian stock market data
- **ETF Data**: Gold and Silver ETF performance

## ⚠️ Limitations

- **Market Hours**: Data accuracy depends on market trading hours
- **API Limits**: Yahoo Finance may have rate limits
- **Data Availability**: Some fundamental metrics may not be available for all stocks
- **ETFs**: PE ratios and some fundamental metrics are not available for ETFs

## 🚀 Future Enhancements

- [ ] Real-time news integration
- [ ] Technical indicators (RSI, MACD, etc.)
- [ ] Portfolio optimization suggestions
- [ ] Risk assessment tools
- [ ] Export to PDF reports
- [ ] Web dashboard interface
- [ ] Email alerts for significant changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Udaya Kiran S S**
- GitHub: [@udayakiranss](https://github.com/udayakiranss)
- Repository: [portfolio-dashboard](https://github.com/udayakiranss/portfolio-dashboard)

## 🙏 Acknowledgments

- Yahoo Finance for providing free financial data
- The Python community for excellent libraries
- Contributors and users of this project

---

⭐ **Star this repository if you find it useful!**
