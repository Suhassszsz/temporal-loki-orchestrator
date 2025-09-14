# src/activities/logging_activity.py
from temporalio import activity
from src.logger import get_custom_logger


@activity.defn
async def log_workflow_event(
    workflow_id: str,
    run_id: str,
    workflow_type: str,
    status: str,
    message: str,
):
    """
    Activity that logs workflow lifecycle events.
    Logs are structured JSON and flow to both console and Loki.
    """

    logger = get_custom_logger("workflow-event")

    log_record = {
        "workflow_id": workflow_id,
        "run_id": run_id,
        "workflow_type": workflow_type,
        "status": status,
        "message": message,
    }

    logger.info(log_record)

    return f"Logged {status} for {workflow_type} ({workflow_id})"
