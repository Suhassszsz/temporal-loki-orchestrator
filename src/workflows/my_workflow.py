from datetime import timedelta
from temporalio import workflow

# Use Temporal's workflow logger (deterministic, sandbox-safe)
logger = workflow.logger

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        info = workflow.info()
        logger.info(f"MyWorkflow started with {info.workflow_id}")
        result = await workflow.execute_activity(
            "shared_activity",   # string name registered by activity.defn
            name,
            schedule_to_close_timeout=timedelta(seconds=20),
        )
        logger.info(f"MyWorkflow finished with {info.workflow_id}")
        return result
