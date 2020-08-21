# -*- coding: utf-8 -*-

from dash import Dash
from flask import Flask, redirect


url_base_pathname = '/catalog-dash'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)


@server.route('/')
def index():
    # redirect from `/` to `url_base_pathname`
    return redirect('{}'.format(url_base_pathname))


@server.route('/<bad_link>')
def redirect_to_index(bad_link):
    # if the user types an invalid link, then it redirects him to `url_base_pathname`
    return redirect('{}'.format(url_base_pathname))


app = Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    url_base_pathname='{}/'.format(url_base_pathname)
)
