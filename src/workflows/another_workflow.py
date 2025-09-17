from temporalio import workflow

logger = workflow.logger

@workflow.defn
class AnotherWorkflow:
    @workflow.run
    async def run(self) -> str:
        info = workflow.info()
        # Put workflow_id inside the message instead of as an "extra" tag
        logger.info(f"AnotherWorkflow started with {info.workflow_id}")
        # simple workflow body (you can add activities here if needed)
        logger.info(f"AnotherWorkflow finished with {info.workflow_id}")
        return "another workflow done"
