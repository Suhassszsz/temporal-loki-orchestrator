# src/workflows/another_workflow.py
from temporalio import workflow

logger = workflow.logger

@workflow.defn
class AnotherWorkflow:
    @workflow.run
    async def run(self) -> str:
        info = workflow.info()
        logger.info("AnotherWorkflow started", extra={"workflow_id": info.workflow_id})
        # simple workflow body
        logger.info("AnotherWorkflow finished", extra={"workflow_id": info.workflow_id})
        return "another workflow done"
