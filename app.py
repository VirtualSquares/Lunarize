from flask import Flask, render_template
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/submit")
def submit():
    return generate_plot()

def downsample_data(latitudes, longitudes, heights, factor=10):
    """
    Downsample data by a factor to improve performance.
    """
    downsampled_latitudes = latitudes[::factor, ::factor]
    downsampled_longitudes = longitudes[::factor, ::factor]
    downsampled_heights = heights[::factor, ::factor]
    return downsampled_latitudes, downsampled_longitudes, downsampled_heights

def generate_plot():
    latitudes_df = pd.read_csv('data/latitude.csv', header=None)
    longitudes_df = pd.read_csv('data/longitude.csv', header=None)
    heights_df = pd.read_csv('data/height.csv', header=None)

    latitudes = latitudes_df.to_numpy()
    longitudes = longitudes_df.to_numpy()
    heights = heights_df.to_numpy()

    latitudes, longitudes, heights = downsample_data(latitudes, longitudes, heights, factor=10)

    longitude_grid, latitude_grid = np.meshgrid(longitudes[0], latitudes[:, 0])

    surface = go.Surface(z=heights, x=longitude_grid, y=latitude_grid, colorscale='Viridis', showscale=False)
    layout = go.Layout(
        title='3D Visualization of Shackleton Terrain',
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Elevation'
        ),
        autosize=True
    )
    fig = go.Figure(data=[surface], layout=layout)

    plot_html = pio.to_html(fig, full_html=False)

    return plot_html

if __name__ == '__main__':
    app.run(debug=True)
