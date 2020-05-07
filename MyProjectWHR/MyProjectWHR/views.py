# -------------------------------------------------------
# Daniel Gonen
# World Happiness Report
# -------------------------------------------------------

"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from MyProjectWHR import app
from MyProjectWHR.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from MyProjectWHR.Models.QueryFormStructure     import QueryFormStructure 
from MyProjectWHR.Models.QueryFormStructure     import LoginFormStructure 
from MyProjectWHR.Models.QueryFormStructure     import UserRegistrationFormStructure 
from MyProjectWHR.Models.plot_service_functions import get_countries_choices
from MyProjectWHR.Models.plot_service_functions import get_choices_choices
from MyProjectWHR.Models.plot_service_functions import plot_to_img

db_Functions = create_LocalDatabaseServiceRoutines() 

# -------------------------------------------------------
# Home page
# -------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

# -------------------------------------------------------
# Contact page
# -------------------------------------------------------
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='My contact page.'
    )

# -------------------------------------------------------
# About page
# -------------------------------------------------------
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='My application description page.'
    )

# -------------------------------------------------------
# data analysing of the datasets 
# quary
# -------------------------------------------------------
@app.route('/Query', methods=['GET', 'POST'])
def Query():
    Years = ''
    chart = ''
    country_choices = ''
    choices_choices = ''
    
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2016.csv'))
    df = df.set_index('Country')

    form = QueryFormStructure(request.form)
    raw_data_table = ''

# puts the choices into select fields
    country_choices = get_countries_choices(df)
    form.country_mselect.choices = country_choices
    
    choices_choices = get_choices_choices()
    form.measures_mselect.choices = choices_choices

    if (request.method == 'POST' ):
        Years = form.year.data

# checking which year the user chose
        if (form.year.data == '2016'):
            df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2016.csv'))
        elif (form.year.data == '2018'):
            df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2018.csv'))
        elif (form.year.data == '2019'):
            df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2019.csv'))

# creating the base to the graph
        df = df.set_index('Country')  #Set the DataFrame index using existing columns
        df = df[(form.measures_mselect.data)]  #filter the selected dataset by the user choices
        df = df.loc[(form.country_mselect.data)] #filter the selected dataset by the user choices

# the graph as picture form
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'barh', figsize=(15, 5))
        chart = plot_to_img(fig)

    return render_template('Query.html', 
            form = form, 
            Years = Years,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input',
            chart = chart ,
            height = "300" ,
            width = "750"

        )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""
            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('Query') #move to query page
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Data Model Page
# -------------------------------------------------------
@app.route('/data')
def data():
    """Renders the about page."""
    return render_template(
        'data.html',
        title='World Happiness Report',
        year=datetime.now().year,
        message='Main Data Model'
    )

# -------------------------------------------------------
# Data sets:
# -------------------------------------------------------

@app.route('/WHR2019')
def WHR2019():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2019.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    """Renders the about page."""
    return render_template(
        'WHR2019.html',
        title='World Happiness Report 2019',
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        message='Happiness rank and scores by country, 2019.'
    )

@app.route('/WHR2018')
def WHR2018():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2018.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    """Renders the about page."""
    return render_template(
        'WHR2018.html',
        title='World Happiness Report 2018',
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        message='Happiness rank and scores by country, 2018.'
    )

@app.route('/WHR2016')
def WHR2016():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2016.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    """Renders the about page."""
    return render_template(
        'WHR2016.html',
        title='World Happiness Report 2016',
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        message='Happiness rank and scores by country, 2016.'
    )


