# src/workflows/my_workflow.py
from datetime import timedelta
from temporalio import workflow

# Use Temporal's workflow logger (deterministic, sandbox-safe)
logger = workflow.logger

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        logger.info("MyWorkflow started", extra={"workflow_id": workflow.info().workflow_id})
        result = await workflow.execute_activity(
            "shared_activity",   # string name registered by activity.defn
            name,
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        logger.info("MyWorkflow finished", extra={"workflow_id": workflow.info().workflow_id})
        return result
