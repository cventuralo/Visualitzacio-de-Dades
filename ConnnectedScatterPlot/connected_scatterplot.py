import requests
import xml.etree.ElementTree as ET
import pandas as pd
import plotly.graph_objects as go

# URLs de les sèries de l'ECB per cada país
series_urls = {
    "Germany": "https://data-api.ecb.europa.eu/service/data/LFSI/M.DE.S.UNEHRT.TOTAL0.15_74.T",
    "France":  "https://data-api.ecb.europa.eu/service/data/LFSI/M.FR.S.UNEHRT.TOTAL0.15_74.T",
    "Italy":   "https://data-api.ecb.europa.eu/service/data/LFSI/M.IT.S.UNEHRT.TOTAL0.15_74.T",
    "Spain":   "https://data-api.ecb.europa.eu/service/data/LFSI/M.ES.S.UNEHRT.TOTAL0.15_74.T"
}

def fetch_monthly_data(url):
    resp = requests.get(url)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {'generic': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'}

    data = []
    for obs in root.findall('.//generic:Obs', ns):
        time_period = obs.find('generic:ObsDimension', ns).attrib['value']
        value = float(obs.find('generic:ObsValue', ns).attrib['value'])
        data.append((time_period, value))
    df = pd.DataFrame(data, columns=["Month", "Unemployment"])

    df["Month"] = pd.to_datetime(df["Month"], format="%Y-%m")
    df["Year"] = df["Month"].dt.year
    return df

def main():
    df_all = pd.DataFrame()
    for country, url in series_urls.items():
        try:
            df = fetch_monthly_data(url)
            df["Country"] = country
            df_all = pd.concat([df_all, df], ignore_index=True)
        except Exception as e:
            print(f"Error fetching {country}: {e}")

    # Agrupo per any i país, calcular mitjana anual
    df_yearly = df_all.groupby(["Country", "Year"])["Unemployment"].mean().reset_index()
    df_yearly["Year"] = pd.to_datetime(df_yearly["Year"].astype(str), format="%Y")

    # Anys >= 2000
    df_yearly = df_yearly[df_yearly["Year"].dt.year >= 2000]

    # Creo connected scatter plot
    fig = go.Figure()
    for country, g in df_yearly.groupby("Country"):
        fig.add_trace(go.Scatter(
            x=g["Year"],
            y=round(g["Unemployment"],2),
            mode="lines+markers",
            name=country
        ))

    fig.update_layout(
        title="Connected Scatterplot: Unemployment Rate (ECB)",
        xaxis_title="Year",
        yaxis_title="Unemployment (%)",
        xaxis=dict(tickformat="%Y"),
        template="plotly_white",
        height=600,
        width=1200
    )

    # Guardar com HTML
    output_path = "connected_scatter_plot.html"
    fig.write_html(output_path, include_plotlyjs='cdn', full_html=True)

if __name__ == "__main__":
    main()
