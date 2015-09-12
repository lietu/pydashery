import logging
import settings
import pydashery.manager


if __name__ == "__main__":

    tornado = logging.getLogger("tornado")
    tornado.propagate = False

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    tornado.addHandler(ch)

    manager = pydashery.manager.Manager(settings, logger)
    manager.start()
