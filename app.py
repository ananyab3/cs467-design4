from shiny import App, ui, render
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib as plt
import seaborn as sns
import numpy as np
import random
from shinywidgets import output_widget, render_widget

df = pd.read_csv("data/dataset.csv")
# Create a list of random colors
colors = ['#'+''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(1000)]


app_ui = ui.page_fluid(
    ui.panel_title("Spotify Song Analysis"),
    ui.navset_pill(
        ui.nav_panel("Speechiness vs. Emotional Impact",
                     ui.input_slider("speechiness_range", "Speechiness Range", 
                    min=df['speechiness'].min(), max=df['speechiness'].max(),
                    value=[df['speechiness'].min(), df['speechiness'].max()]),
                    ui.input_select("colorscale_selector", "Choose Color Scale",
                    choices=["Plotly3", "Viridis", "Tropic", "Greys", "Magma"],
                    selected="Plotly3"),
                    output_widget("emotional_impact_plot")),
        ui.nav_panel("Song Energy vs. Song Loudness", output_widget("energy_vs_loudness")),
        ui.nav_panel("Song Valence vs. Song Loudness", output_widget("valence_vs_loudness")),
        ui.nav_panel("Song Energy vs. Song Popularity", output_widget("energy_vs_popularity")),
        ui.nav_panel("Song Tempo vs. Song Popularity", output_widget("tempo_vs_popularity")),
        ui.nav_panel("Song Genre vs. Song Valence", 
                     ui.input_selectize(  
                    "chosen_genres",  
                    "Select options below:",  
                    df['track_genre'].unique().tolist(), 
                    multiple=True,  
                    ),
                    output_widget("genre_vs_valence")),
        
    ),
)

def server(input, output, session):
    @render_widget
    def emotional_impact_plot():
        speechiness_range = input.speechiness_range()
        selected_colorscale = input.colorscale_selector()

        filtered_df = df[
            (df['speechiness'] >= speechiness_range[0]) & 
            (df['speechiness'] <= speechiness_range[1])
        ]

        filtered_df.fillna(0, inplace=True)  # This fills NaNs with zeros

        fig = go.Figure(data=go.Scatter3d(
            x=filtered_df['danceability'],
            y=filtered_df['energy'],
            z=filtered_df['valence'],
            mode='markers',
            marker=dict(
                size=3,
                color=filtered_df['speechiness'], 
                cmin=df['speechiness'].min(),  
                cmax=df['speechiness'].max(), 
                colorscale=selected_colorscale,  # Dynamically set colorscale
                opacity=0.5,  # Lowered opacity to help see overlapping points
                colorbar=dict(title='Speechiness'),
                line=dict(width=0)
            )
        ))

        fig.update_layout(
            title="",
            scene=dict(
                xaxis=dict(title='Danceability'),
                yaxis=dict(title='Energy'),
                zaxis=dict(title='Valence'),
            ),
            margin=dict(l=0, r=0, b=0, t=0)  
        )

        return fig
    
    @render_widget
    def energy_vs_loudness():
        # Fit a trendline
        z = np.polyfit(df['energy'], df['loudness'], 1)
        p = np.poly1d(z)

        fig = go.Figure()

        # Add the scatter plot
        fig.add_trace(go.Scatter(
            x=df['energy'],
            y=df['loudness'],
            mode='markers',
            text=df[['track_name', 'artists']].apply(lambda x: f'{x[0]}, {x[1]}', axis=1),  # hover text
            marker=dict(
                size=2,
                color='red',
                line=dict(width=2, color='DarkSlateGrey')
            ),
            name='Data'
        ))

        # Add the trendline
        fig.add_trace(go.Scatter(
            x=df['energy'],
            y=p(df['energy']),
            mode='lines',
            marker=dict(color='blue'),
            name='Trendline'
        ))

        fig.update_layout(
            xaxis_title='Song Energy',
            yaxis_title='Song Loudness',
        )

        return fig
    
    @render_widget
    def valence_vs_loudness():
        # Fit a trendline
        z = np.polyfit(df['valence'], df['loudness'], 1)
        p = np.poly1d(z)

        fig = go.Figure()

        # Add the scatter plot
        fig.add_trace(go.Scatter(
            x=df['valence'],
            y=df['loudness'],
            mode='markers',
            text=df[['track_name', 'artists']].apply(lambda x: f'{x[0]}, {x[1]}', axis=1),  # hover text
            marker=dict(
                size=2,
                color='',
                line=dict(width=2, color='DarkSlateGrey')
            ),
            name='Data'
        ))

        # Add the trendline
        fig.add_trace(go.Scatter(
            x=df['valence'],
            y=p(df['valence']),
            mode='lines',
            marker=dict(color='blue'),
            name='Trendline'
        ))

        fig.update_layout(
            xaxis_title='Song Valence',
            yaxis_title='Song Loudness',
        )

        return fig
    
    @render_widget
    def energy_vs_popularity():
        # Fit a trendline
        z = np.polyfit(df['energy'], df['popularity'], 1)
        p = np.poly1d(z)

        fig = go.Figure()

        # Add the scatter plot
        fig.add_trace(go.Scatter(
            x=df['energy'],
            y=df['popularity'],
            mode='markers',
            text=df[['track_name', 'artists']].apply(lambda x: f'{x[0]}, {x[1]}', axis=1),  # hover text
            marker=dict(
                size=2,
                color='purple',
                line=dict(width=2, color='DarkSlateGrey')
            ),
            name='Data'
        ))

        # Add the trendline
        fig.add_trace(go.Scatter(
            x=df['energy'],
            y=p(df['energy']),
            mode='lines',
            marker=dict(color='blue'),
            name='Trendline'
        ))

        fig.update_layout(
            xaxis_title='Song Energy',
            yaxis_title='Song Popularity',
        )

        return fig
    
    @render_widget
    def tempo_vs_popularity():
        # Fit a trendline
        z = np.polyfit(df['tempo'], df['popularity'], 1)
        p = np.poly1d(z)

        fig = go.Figure()

        # Add the scatter plot
        fig.add_trace(go.Scatter(
            x=df['tempo'],
            y=df['popularity'],
            mode='markers',
            text=df[['track_name', 'artists']].apply(lambda x: f'{x[0]}, {x[1]}', axis=1),  # hover text
            marker=dict(
                size=2,
                color='purple',
                line=dict(width=2, color='DarkSlateGrey')
            ),
            name='Data'
        ))

        # Add the trendline
        fig.add_trace(go.Scatter(
            x=df['tempo'],
            y=p(df['tempo']),
            mode='lines',
            marker=dict(color='blue'),
            name='Trendline'
        ))

        fig.update_layout(
            xaxis_title='Song Tempo',
            yaxis_title='Song Popularity',
        )

        return fig
    
    @render_widget
    def genre_vs_valence():
        # Filter the DataFrame based on the genres chosen
        chosen_genres = list(input.chosen_genres())
        df_filtered = df[df['track_genre'].isin(chosen_genres)]

        # Group by genre and calculate the mean valence
        df_grouped = df_filtered.groupby('track_genre')['valence'].mean().reset_index()

        # Create the bar chart
        fig = go.Figure(data=go.Bar(
            x=df_grouped['track_genre'],
            y=df_grouped['valence'],
            marker_color=colors  # assign colors to each bar
        ))

        fig.update_layout(
            title_text='Genre vs Emotional Valence', # title of plot
            xaxis_title_text='Genre', # xaxis label
            yaxis_title_text='Emotional Valence', # yaxis label
        )

        return fig

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()