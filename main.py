import yfinance as yf
import pandas as pd
from datetime import datetime
import warnings

# Suppress yfinance warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# --------------------------
# CONFIGURATION
# --------------------------
STOCKS = [
    "HDFCBANK.NS",
    "RELIANCE.NS", 
    "ICICIBANK.NS",
    "BEL.NS",          # Bharat Electronics
    "HAL.NS",          # Hindustan Aeronautics
    "GOLDBEES.NS",     # Gold ETF (corrected from GOLDCHEM.NS)
    "SILVERBEES.NS",
    "TATAMOTORS.NS",
    "BHARTIARTL.NS"
]

INDEXES = ["^NSEI", "^BSESN"]  # Nifty 50 & BSE Sensex (corrected from ^BSE500)

OUTPUT_FILE = "Portfolio_Analysis.xlsx"

# --------------------------
# FUNCTION: Fetch PE ratios
# --------------------------
def get_pe_ratios(ticker):
    try:
        # Create Ticker object
        stock = yf.Ticker(ticker)
        
        # Get financial info
        info = stock.info
        
        # Extract PE ratios
        pe_ratio = info.get('trailingPE', None)
        industry_pe = info.get('industryPE', None)
        
        # Try alternative sources for industry PE
        if industry_pe is None:
            # Try sector PE or forward PE as alternatives
            industry_pe = info.get('sectorPE', info.get('forwardPE', None))
        
        # For ETFs and indexes, PE might not be available
        if ticker.endswith('.NS') and (pe_ratio is None or pe_ratio == 0):
            print(f"⚠️  PE data not available for {ticker}")
            return {"PE Ratio": None, "Industry PE": None}
        
        # Get additional fundamental metrics
        market_cap = info.get('marketCap', None)
        dividend_yield = info.get('dividendYield', None)
        beta = info.get('beta', None)
        
        return {
            "PE Ratio": pe_ratio,
            "Industry PE": industry_pe,
            "Market Cap (Cr)": market_cap / 10000000 if market_cap else None,  # Convert to Crores
            "Dividend Yield %": dividend_yield * 100 if dividend_yield else None,  # Convert to percentage
            "Beta": beta
        }
        
    except Exception as e:
        print(f"❌ Error fetching PE data for {ticker}: {str(e)}")
        return {"PE Ratio": None, "Industry PE": None}

# --------------------------
# FUNCTION: Fetch stock changes
# --------------------------
def get_price_changes(ticker):
    try:
        # Download single ticker to avoid MultiIndex issues
        data = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        
        if data.empty or len(data) < 30:  # Need at least 30 days of data
            print(f"⚠️  Insufficient data for {ticker}")
            return None

        # Get close data - handle MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            close_data = data[('Close', ticker)]
        else:
            close_data = data['Close']
        
        # Get the latest close price as a scalar
        last_close = float(close_data.iloc[-1])
        
        # Calculate changes for different periods
        changes = {}
        
        # Daily change (if we have at least 2 days of data)
        if len(close_data) >= 2:
            prev_close = float(close_data.iloc[-2])
            daily_change = ((last_close - prev_close) / prev_close) * 100
            changes["Daily Change %"] = daily_change
        else:
            changes["Daily Change %"] = None
            
        # Weekly change (5 trading days)
        if len(close_data) >= 5:
            week_ago_close = float(close_data.iloc[-5])
            weekly_change = ((last_close - week_ago_close) / week_ago_close) * 100
            changes["Weekly Change %"] = weekly_change
        else:
            changes["Weekly Change %"] = None
            
        # Monthly change (21 trading days)
        if len(close_data) >= 21:
            month_ago_close = float(close_data.iloc[-21])
            monthly_change = ((last_close - month_ago_close) / month_ago_close) * 100
            changes["Monthly Change %"] = monthly_change
        else:
            changes["Monthly Change %"] = None
            
        # YTD change (from start of year)
        current_year = datetime.now().year
        year_start_data = close_data[close_data.index.year == current_year]
        if not year_start_data.empty:
            year_start_close = float(year_start_data.iloc[0])
            ytd_change = ((last_close - year_start_close) / year_start_close) * 100
            changes["YTD Change %"] = ytd_change
        else:
            changes["YTD Change %"] = None
            
        # Yearly change (from 1 year ago)
        if len(close_data) >= 240:  # At least 240 trading days (roughly 11 months)
            # Use the first available data point (approximately 1 year ago)
            year_ago_close = float(close_data.iloc[0])
            yearly_change = ((last_close - year_ago_close) / year_ago_close) * 100
            changes["Yearly Change %"] = yearly_change
        else:
            changes["Yearly Change %"] = None

        return changes
        
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {str(e)}")
        return None

# --------------------------
# MAIN SCRIPT
# --------------------------
if __name__ == "__main__":
    print("📊 Starting Portfolio Analysis...")
    dashboard_data = []

    for stock in STOCKS + INDEXES:
        print(f"📈 Fetching data for {stock}...")
        changes = get_price_changes(stock)
        pe_data = get_pe_ratios(stock)
        
        if changes:
            # Combine price changes and PE data
            stock_data = {"Stock": stock, **changes, **pe_data}
            dashboard_data.append(stock_data)
            print(f"✅ Successfully fetched data for {stock}")
        else:
            dashboard_data.append({
                "Stock": stock, 
                "Daily Change %": None, 
                "Weekly Change %": None,
                "Monthly Change %": None, 
                "YTD Change %": None, 
                "Yearly Change %": None,
                "PE Ratio": pe_data.get("PE Ratio", None),
                "Industry PE": pe_data.get("Industry PE", None),
                "Market Cap (Cr)": pe_data.get("Market Cap (Cr)", None),
                "Dividend Yield %": pe_data.get("Dividend Yield %", None),
                "Beta": pe_data.get("Beta", None)
            })
            print(f"❌ Failed to fetch price data for {stock}")

    # Convert to DataFrame
    dashboard_df = pd.DataFrame(dashboard_data)
    
    # Round percentage columns to 2 decimal places
    percentage_columns = [col for col in dashboard_df.columns if "Change %" in col]
    for col in percentage_columns:
        # Convert to numeric, handling None values
        dashboard_df[col] = pd.to_numeric(dashboard_df[col], errors='coerce').round(2)
    
    # Round PE ratio columns to 2 decimal places
    pe_columns = ["PE Ratio", "Industry PE"]
    for col in pe_columns:
        if col in dashboard_df.columns:
            dashboard_df[col] = pd.to_numeric(dashboard_df[col], errors='coerce').round(2)
    
    # Round market cap to 2 decimal places
    if "Market Cap (Cr)" in dashboard_df.columns:
        dashboard_df["Market Cap (Cr)"] = pd.to_numeric(dashboard_df["Market Cap (Cr)"], errors='coerce').round(2)
    
    # Round dividend yield to 2 decimal places
    if "Dividend Yield %" in dashboard_df.columns:
        dashboard_df["Dividend Yield %"] = pd.to_numeric(dashboard_df["Dividend Yield %"], errors='coerce').round(2)
    
    # Round beta to 2 decimal places
    if "Beta" in dashboard_df.columns:
        dashboard_df["Beta"] = pd.to_numeric(dashboard_df["Beta"], errors='coerce').round(2)

    # Placeholder News Data
    news_df = pd.DataFrame([
        {"Stock": "HDFCBANK.NS", "Headline": "HDFC Bank sees growth in retail loans", "Source": "Economic Times",
         "Published At": "2025-01-10", "URL": "https://economictimes.indiatimes.com"},
        {"Stock": "RELIANCE.NS", "Headline": "Reliance Industries reports strong Q3 results", "Source": "Business Standard",
         "Published At": "2025-01-09", "URL": "https://business-standard.com"},
    ])

    # Save to Excel
    try:
        with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
            dashboard_df.to_excel(writer, sheet_name="Dashboard", index=False)
            news_df.to_excel(writer, sheet_name="News Feed", index=False)
        
        print(f"✅ Portfolio analysis saved to {OUTPUT_FILE}")
        print(f"📋 Processed {len(dashboard_data)} stocks/indexes")
        
        # Display summary
        print("\n📊 Summary:")
        successful_fetches = len([row for row in dashboard_data if any(row.get(col) is not None for col in percentage_columns)])
        print(f"   - Successfully fetched: {successful_fetches}/{len(dashboard_data)}")
        print(f"   - Failed fetches: {len(dashboard_data) - successful_fetches}/{len(dashboard_data)}")
        
    except Exception as e:
        print(f"❌ Error saving to Excel: {str(e)}")
        # Fallback to CSV if Excel fails
        dashboard_df.to_csv("Portfolio_Analysis.csv", index=False)
        news_df.to_csv("News_Feed.csv", index=False)
        print("✅ Saved as CSV files instead")
