import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import os
import plotly.io as pio

pio.renderers.default = "browser"
os.chdir(r'D:\PyCharm_ssau\radiotech\lab1')

data = pd.read_csv('samples_unipolar01.csv', sep=',', header=None)

data.columns = ['frequency_Hz', 'power_W', 'power_D']

data_clean = data[data['power_D'].isin([-np.inf, np.inf]) == False]

fig = make_subplots(rows=1, cols=2)

fig.add_trace(
    go.Scatter(x=data['frequency_Hz'], y=data['power_W'], mode='lines', showlegend=False),
    row=1, col=1)

fig.add_trace(
    go.Scatter(x=data['frequency_Hz'], y=data['power_D'], mode='lines', showlegend=False),
    row=1, col=2)

fig.update_xaxes(title_text="Frequency, Hz")
fig.update_yaxes(title_text="Power")

fig.update_layout(
    title_text="Dependency Graph unipolar 0.1",
    width=1200,
    height=800
)

fig.write_image("output_unipolar01.png")
fig.show()