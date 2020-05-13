import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
import io

# ------------------------------------------------------------------------
# Countries as a list, revoming countries that aren't in all the datasets
# ------------------------------------------------------------------------
def get_countries_choices(df):
    df1 = df.rename(columns={'Country/Region': 'Country'}) #Rename
    df1 = df1.groupby('Country').sum() #All the df is organized by the order of the abc of the countries.
    l = df1.index #Indexing in pandas means simply selecting particular rows and columns of data from a DataFrame. 
    m = list(zip(l , l)) #Turning into a list

    #now i'm removing all the countries that aren't present in all the 3 datasets.
    m.remove(('Angola', 'Angola'))
    m.remove(('Belize', 'Belize'))
    m.remove(('Comoros', 'Comoros'))
    m.remove(('Macedonia', 'Macedonia'))
    m.remove(('North Cyprus', 'North Cyprus'))
    m.remove(('Puerto Rico', 'Puerto Rico'))
    m.remove(('Somaliland Region', 'Somaliland Region'))    
    m.remove(('Sudan', 'Sudan'))
    m.remove(('Suriname', 'Suriname'))
    m.remove(('Trinidad and Tobago', 'Trinidad and Tobago'))
    
    return m #returning the list

# -------------------------------------------------------
# Measures as a list
# -------------------------------------------------------
def get_choices_choices():
    l = (["Score", "GDP per Capita", "Healthy life expectancy", "Freedom to make life choices", "Generosity"])
    m = list(zip(l , l))
    return m

# -------------------------------------------------------
# Graph to img form
# -------------------------------------------------------
def plot_to_img(fig): 
    pngImage = io.BytesIO() 
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

# -------------------------------------------------------
# Fixing the datasets. There are some countries that aren't present in all the datasets. this function is made to find them. 
# -------------------------------------------------------
def fix_dataset(df):
    df1 = df.rename(columns={'Country/Region': 'Country'})
    df1 = df1.groupby('Country').sum()
    l = df1.index
    m = list(zip(l , l))

    dff = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2018.csv'))
    dff1 = dff.groupby('Country').sum()
    ll = dff1.index
    mm = list(zip(ll , ll))

    count = 0;

    for x in m:
        for y in mm:
            if x == y:
                count = count + 1
        if count != 1:
            print(x)
        count = 0




