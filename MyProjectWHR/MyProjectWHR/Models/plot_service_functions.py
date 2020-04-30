import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
import io


# -------------------------------------------------------
# countries as a list
# -------------------------------------------------------

def get_countries_choices(df):
    df1 = df.rename(columns={'Country/Region': 'Country'})
    df1 = df1.groupby('Country').sum()
    l = df1.index
    m = list(zip(l , l))
    m.remove(('Belize', 'Belize'))
    return m

# -------------------------------------------------------
# benchmarks as a list
# -------------------------------------------------------

def get_choices_choices():
    l = (["Score", "GDP per Capita", "Healthy life expectancy", "Freedom to make life choices", "Generosity"])
    m = list(zip(l , l))
    return m

# -------------------------------------------------------
# graph to img form
# -------------------------------------------------------

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

