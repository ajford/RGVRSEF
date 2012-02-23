
from . import app

if not app.debug:
    import logging
    from logging import FileHandler, Formatter
    try:
        from bundle_config import config
        file_handler = FileHandler("%s/RGVRSEF.log"%config['core']['data_directory'])
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(Formatter("""
            %(asctime)s %(levelname)s: %(message)s
            [in %(pathname)s:%(lineno)d]

            """))
        app.logger.addHandler(file_handler)
    except ImportError:
        pass


