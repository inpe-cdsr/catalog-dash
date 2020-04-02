# -*- coding: utf-8 -*-

from catalog_dash import create_app
from catalog_dash.environment import DEBUG_MODE


if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=DEBUG_MODE)
