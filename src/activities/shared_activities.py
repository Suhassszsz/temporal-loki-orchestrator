# src/activities/shared_activities.py
from temporalio import activity
from src.logger import get_custom_logger
import asyncio

logger = get_custom_logger(__name__)

@activity.defn(name="shared_activity")
async def shared_activity(name: str) -> str:
    logger.info(f"shared_activity running for {name}")
    # simulate work
    await asyncio.sleep(1)
    logger.info(f"shared_activity completed for {name}")
    return f"Hello, {name} from shared_activity!"
