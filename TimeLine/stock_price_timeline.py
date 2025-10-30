import pandas as pd
import yfinance as yf
import plotly.express as px
import os

# -----------------------------
# Funció per descarregar dades
def getStockData(stock, start=None, end=None, interval=None):
    try:
        stokYF = yf.Ticker(stock)
        df = pd.DataFrame(columns=[stock])
        if interval:
            downloadDF = yf.download(stock, start=start, end=end, interval=interval, auto_adjust=False)
            df[stock] = downloadDF['Close']
        else:
            df[stock] = stokYF.history(start=start, end=end).Close
        df.index = df.index.tz_localize(None)
    except:
        print("CAN'T FIND THE STOCK\n")
        return pd.DataFrame()  # Retornem DataFrame buit si hi ha error
    return df

# -----------------------------
# Exemple d'ús
if __name__ == "__main__":
    stock_symbol = "AAPL"  # Acció a mostrar
    start_date = "2025-01-01"
    end_date = "2025-10-01"

    # Obtenim dades
    df_stock = getStockData(stock_symbol, start=start_date, end=end_date)

    if not df_stock.empty:
        # Creem gràfica timeline
        fig = px.line(df_stock, x=df_stock.index, y=stock_symbol,
                      title=f"{stock_symbol} Stock Timeline", markers=True)
        fig.update_traces(text=df_stock[stock_symbol], textposition="top center")
        
        # Crear carpeta de sortida si no existeix
        output_dir = "PAC 2/TimeLine"
        os.makedirs(output_dir, exist_ok=True)
        
        # Guardem el gràfic com a fitxer HTML
        output_file = os.path.join(output_dir, "stock_plot.html")
        fig.write_html(output_file)
        
        print(f"Gràfic guardat correctament com a {output_file}")
        print("Puja aquest fitxer a GitHub i podràs veure'l amb GitHub Pages.")
    else:
        print("No hi ha dades per mostrar.")
