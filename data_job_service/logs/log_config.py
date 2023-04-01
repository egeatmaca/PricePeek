import logging
import os


def config_logs():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=os.path.join('logs', 'data_job_service.log'))


