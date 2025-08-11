import logging
from logging import Formatter, FileHandler
from fyyur import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

    if not app.debug:
      file_handler = FileHandler('error.log')
      file_handler.setFormatter(
          Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
      )
      app.logger.setLevel(logging.INFO)
      file_handler.setLevel(logging.INFO)
      app.logger.addHandler(file_handler)
      app.logger.info('errors')