# -*- coding: utf-8 -*-
from app import create_webapp
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = None

if not app:
    app = create_webapp()

if __name__ == "__main__":
    # Start application
    app.run(host="127.0.0.1", port=5050, debug=True)
