# gunicorn config

import logging
import os
import beeline

def post_worker_init(worker):
    logging.info(f'beeline initialization in process pid {os.getpid()}')
    api_key = os.environ.get('HONEYCOMB_API_KEY')
    beeline.init(writekey=api_key, dataset="trencher", debug=True)
