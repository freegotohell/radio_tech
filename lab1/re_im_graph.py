import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import os
os.chdir(r'D:\PyCharm_ssau\radiotech\lab1')

data = pd.read_csv(r'D:\PyCharm_ssau\radiotech\lab1\samples_re_im_0.txt', sep=r'\s+', header=None)

data.columns = ['frequency_Hz', 're', 'im', 'P']

fig = make_subplots(rows=1, cols=2, subplot_titles=["Real on Frequency (Hz)", "Imaginary on Frequency (Hz)"])

fig.add_trace(go.Scatter(x=data['frequency_Hz'], y=data['re'],
                         mode='lines',
                         name='Real', showlegend=False),
              row=1, col=1)

fig.add_trace(go.Scatter(x=data['frequency_Hz'], y=data['im'],
                         mode='lines',
                         name='Imaginary', showlegend=False),
              row=1, col=2)

fig.update_xaxes(title_text="Frequency, Hz")
fig.update_yaxes(title_text="Part")

fig.update_layout(title_text="Dependency Graph real and imaginary parts for 0")

fig.write_image("output_re_im_0.png")

fig.show()
