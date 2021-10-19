from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

# auth = Blueprint('auth', __name__, url_prefix='/auth')
lazuli = Blueprint('lazuli', __name__, url_prefix='/tlantisitl')


# Registros (BLUEPRINTS)
@lazuli.route("/prueba")
def prueba():
    return '¡Hello, World!'


@lazuli.route('/')
def index():
    return '🥵'


# /tlantisitl/register


@lazuli.route("/register")
def register():
    return render_template('auth/signUP.html')


# /tlantisitl/login


@lazuli.route("/login")
def login():
    return render_template('auth/login.html')

# /tlantisitl/servicios

@lazuli.route("/servicios")
def servicios():
    return render_template('auth/servicios.html')

