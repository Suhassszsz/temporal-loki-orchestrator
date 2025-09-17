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

    # Cleaner: workflow_id is automatically added by logger
    msg = f"Workflow event: status={status} workflow_type={workflow_type} run_id={run_id} message={message}"
    logger.info(msg)

    return f"Logged {status} for {workflow_type} ({workflow_id})"
