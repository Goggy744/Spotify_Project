from cProfile import run
from distutils.log import debug
from doctest import debug_script
from webapp import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
