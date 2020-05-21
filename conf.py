# gunicorn config

import logging
import os
import beeline

def post_worker_init(worker):
    logging.info(f'beeline initialization in process pid {os.getpid()}')
    api_key = os.environ.get('HONEYCOMB_API_KEY')
    dataset = os.environ.get('HONEYCOMB_DATASET')
    beeline.init(writekey=api_key, dataset=dataset, debug=True, presend_hook=presend)


def presend(fields):
    for key, value in os.environ.items():
        if key.startswith('HEROKU_'):
            fields[key.lower()] = value
