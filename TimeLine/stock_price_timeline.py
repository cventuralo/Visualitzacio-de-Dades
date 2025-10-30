import pandas as pd
import yfinance as yf
import plotly.express as px
import os

# -------------------------------------------------
# Aquí baixo les dades de l'acció que m'interessa
def getStockData(stock, start=None, end=None, interval=None):
    try:
        stockYF = yf.Ticker(stock)
        df = pd.DataFrame(columns=[stock])
        
        # Si especifico un interval, faig servir la funció download
        if interval:
            downloadDF = yf.download(stock, start=start, end=end, interval=interval, auto_adjust=False)
            df[stock] = downloadDF['Close']
        else:
            df[stock] = stockYF.history(start=start, end=end).Close
        
        # Treballo amb l'índex sense zona horària
        df.index = df.index.tz_localize(None)
    except Exception as e:
        print(f"No puc obtenir les dades per {stock}: {e}")
        return pd.DataFrame()  # Retorno un DataFrame buit si hi ha cap error
    
    return df


# -------------------------------------------------
# Aquí executo el meu script principal
if __name__ == "__main__":
    stock_symbol = "AAPL"   # Aquí trio l'acció que vull visualitzar
    start_date = "2025-01-01"
    end_date = "2026-10-01"

    # Descarrego les dades
    df_stock = getStockData(stock_symbol, start=start_date, end=end_date)

    if not df_stock.empty:
        # Creo la gràfica del preu de l'acció al llarg del temps
        fig = px.line(
            df_stock,
            x=df_stock.index,
            y=stock_symbol,
            title=f"{stock_symbol} Stock Timeline",
            markers=True
        )
        fig.update_traces(text=df_stock[stock_symbol], textposition="top center")

        # Guardo el fitxer HTML al mateix lloc on executo aquest script
        output_file = os.path.join(os.getcwd(), "stock_plot.html")
        fig.write_html(output_file)

        print(f"He guardat el gràfic correctament com a: {output_file}")
        print("Ara puc pujar aquest fitxer a GitHub i veure'l amb GitHub Pages.")
    else:
        print("No hi ha dades per mostrar.")

