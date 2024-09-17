# Tagesaufgaben: Dash Apps
# -------------------------------------------------
#
# Heute drehen sich alle Tagesaufgaben um die Erstellung einer
# Dash App. Die Kommentare sind als Arbeitsschritte zu verstehen.
# Schreibe deinen Code unter die jeweiligen Kommentare und
# achte darauf, dass sich deine App am Ende fehlerlos ausführen lässt.


# VORBEREITUNG
# ------------
# 1. Lade unter diesem Kommentar alle für deine App
#    benötigten Module
# ---------------

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# 2. Lade den iris Datensatz aus plotly
iris = px.data.iris()

# 3. Erstelle dein App-Objekt
app = Dash()

server= app.server

# 4. KOMPONENTEN-ERSTELLUNG
# ------------
# 4.1. Erstelle ein Histogramm von petal_width und eines von petal_length.
#    Speichere sie jeweils in einer Variable.
#    Beschrifte die Histogramme und passe ihren Stil an.

# 1.Histogramm erstellen
histogramm_01 = px.histogram(iris, 
                          x = 'petal_width', 
                          color = 'species',
                          opacity=0.7,
                          nbins = 30,
                          barmode = 'overlay',
                          template='plotly_dark')

histogramm_01.update_layout(title="Blütenblattbreite je Iris-Spezies",
                    xaxis_title="Blütenblattbreite(cm)",
                    yaxis_title="Anzahl",
                    legend_title="Spezies")

# 2.Histogramm erstellen
histogramm_02 = px.histogram(iris, 
                          x = 'petal_length', 
                          color = 'species',
                          opacity=0.7,
                          nbins = 30,
                          barmode = 'overlay',
                          template='plotly_dark')

histogramm_02.update_layout(title="Blütenblattlänge je Iris-Spezies",
                    xaxis_title="Blütenblattlänge(cm)",
                    yaxis_title="Anzahl",
                    legend_title="Spezies")

# 4.2. Erstelle einen Scatterplot zwischen petal_width (x) und petal_length (y).
#    a) Verwende beschreibende Achsenbeschriftungen und einen Titel
#    b) Färbe die Punkte der drei Spezies in drei verschiedenen Lila-Tönen.

lila_toene = px.colors.sequential.Purples[2::3]

scatterplot = px.scatter(iris, 
                         x="petal_width",
                         y="petal_length",
                         color="species",
                         color_discrete_sequence=lila_toene,
                         template='plotly_dark')

scatterplot.update_layout(title="Verhältnis Blütenblattlänge zu Blütenblattbreite je Iris-Spezies",
                    xaxis_title="Blütenblattbreite(cm)",
                    yaxis_title="Blütenblattlänge(cm)",
                    legend_title="Spezies")

# 4.3. Erstelle eine Tabelle mit den Daten des iris-DataFrames.
#      Formatiere sie ansprechend.
columns = list(iris.columns)
data = iris.to_dict('list')

table_figure = go.Figure(data=[go.Table(
    header=dict(
        values=[f"<b>{col}</b>" for col in columns],  # Überschriften fett darstellen
        fill_color='skyblue',                        # Hintergrundfarbe der Kopfzeile
        align='center',                               # Überschriften zentrieren
        line_color='black'
    ),
    cells=dict(
        values=[data[col] for col in columns],       # Zellenwerte aus dem DataFrame
        fill_color='white',                          # Hintergrundfarbe der Zellen
        align=['right' if col != 'species' else 'center' for col in columns],  # Textausrichtung je nach Spalte
        line_color='black'
    )
)])

# Umformatierung des DataFrames in Dictionarys mit dash_table
table_dash = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in iris.columns],  # Spalten aus dem iris DataFrame
        data=iris.to_dict('records'),          # Daten des iris DataFrame umwandeln
        style_cell={'textAlign': 'right'},     # Ausrichtung Zellen
        style_table={
        'height': '300px',      # Maximale Höhe der Tabelle festlegen
        'overflowY': 'auto',    # Vertikales Scrollen aktivieren
        'width': '100%',        # Breite der Tabelle auf 100% des Containers setzen
        'minWidth': '100%'      # Minimale Breite der Tabelle
    },
        style_header={
            'fontWeight': 'bold',               # Fett formatierte Überschriften
            'backgroundColor': 'skyblue',       # Hintergrundfarbe der Kopfzeile
            'textAlign': 'center'               # Überschriften zentrieren
        },
        style_cell_conditional=[
            {'if': {'column_id': 'species'}, 'textAlign': 'center'}]  # Arten-Spalte zentrieren           
    )

# 5. KOMPONENTEN EINBINDEN
# ------------
# Füge nun die erstellten Plots, sowie einige
# zusätzliche Elemente in deine
# Dash App ein:
#   1. Die App soll als erstes einen großen
#      Titel bekommen, der "Iris-Dashboard" heißt.
#   2. Anschließend soll eine Überschrift
#      "Univariate Analyse" kommen.
#   3. Unter dieser Überschrift, füge die
#      Histogramme ein, die du vorbereitet hast. 
#   4. Anschließend soll eine zweite Überschrift
#      "Bivariate Analyse" kommen.
#   5. Unter dieser Überschrift, füge den
#      vorbereiteten Scatterplot ein.
#   6. Füge eine letzte Überschrift
#      "Zusatzinfos" ein, und binde darunter die
#                vorbereitete Tabelle ein.


app.layout = html.Div([
    html.H1("Iris-Dashboard"),
    html.Hr(), 

    html.H2("Univariate Analyse"),
    dcc.Graph(figure=histogramm_01),
    html.Br(),
    dcc.Graph(figure=histogramm_02),
    html.Br(),

    html.H2("Bivariate Analyse"),
    dcc.Graph(figure=scatterplot),
    html.Br(),

    html.H2("Zusatzinfos"),
    html.Br(),
    html.H4("mit dash_table.DataTable"),
    html.Div(table_dash), 
    html.Br(),
    html.Hr(),
    html.Br(),
    html.H4("mit plotly go"),
    dcc.Graph(figure=table_figure),             # Tabelle mit go.Table
    html.Br(),
    html.H5("Dashboard Ende")
])

# FÜHRE DIE APP AUS!
# ------------
# Wenn man das Skript ausführt, soll die App
# gestartet werden.

if __name__ == "__main__":
    app.run_server(debug=True)
