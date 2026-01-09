import time, logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task
def process_order(order_id: int):
    time.sleep(5)
    logger.info(f"Order {order_id} processed.")