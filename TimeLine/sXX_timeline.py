import pandas as pd
import os
import plotly.graph_objects as go
import random

def carregar_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No s'ha trobat el fitxer: {file_path}")

    df = pd.read_csv(file_path)

    if 'Year' in df.columns:
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df['Year'] = pd.to_datetime(df['Year'], format='%Y', errors='coerce')
    else:
        raise ValueError("El CSV no conté la columna 'Year'.")

    return df

def filtrar_esdeveniments(df):
    # Filtra només els conflictes militars entre 1930 i 1950
    df_sXX = df[(df['Year'].dt.year >= 1930) & (df['Year'].dt.year <= 1950)]
    if 'Type of Event' in df_sXX.columns:
        df_sXX = df_sXX[df_sXX['Type of Event'] == 'Military Conflict']
    
    # Només un esdeveniment per any
    df_sXX = df_sXX.groupby(df_sXX['Year'].dt.year).first().reset_index(drop=True)
    
    df_sXX = df_sXX.sort_values('Year').reset_index(drop=True)
    return df_sXX

def crear_timeline_html(df, output_file="timeline_military_conflicts.html"):
    fig = go.Figure()

    y_base = 0
    max_y = 2  # altura màxima aleatòria de les línies

    # Línia base del timeline
    fig.add_trace(go.Scatter(
        x=[pd.to_datetime(1930, format='%Y'), pd.to_datetime(1950, format='%Y')],
        y=[y_base, y_base],
        mode='lines',
        line=dict(color='black', width=2)
    ))

    anys = list(range(1930, 1951))

    # Afegir cada esdeveniment amb línia vertical aleatòria
    for i, row in df.iterrows():
        y_random = random.uniform(0.8, max_y)
        fig.add_trace(go.Scatter(
            x=[row['Year'], row['Year']],
            y=[y_base, y_random],
            mode='lines+markers+text',
            marker=dict(size=8, color='#1f77b4'),
            line=dict(color='#1f77b4', width=3),
            text=[None, row['Name of Incident']],
            textposition='top center',
            hovertemplate=f"{row['Name of Incident']}<br>Año: {row['Year'].year}<extra></extra>"
        ))

    fig.update_layout(
        showlegend=False,
        title="Timeline de Conflictes Militars (1930-1950)",
        xaxis=dict(
            tickmode='array',
            tickvals=[pd.to_datetime(y, format='%Y') for y in anys],
            ticktext=[str(y) for y in anys],
            tickangle=45
        ),
        yaxis=dict(visible=False),
        plot_bgcolor='white',
        height=600,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    fig.write_html(output_file)
    print(f"✅ Fitxer HTML creat: {os.path.abspath(output_file)}")

def main():
    file_path = 'World_Important_Dates.csv'
    df = carregar_csv(file_path)
    df_filtrat = filtrar_esdeveniments(df)
    crear_timeline_html(df_filtrat)

if __name__ == "__main__":
    main()
