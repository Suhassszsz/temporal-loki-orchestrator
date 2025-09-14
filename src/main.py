# src/main.py
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from src.workflows.my_workflow import MyWorkflow
from src.workflows.another_workflow import AnotherWorkflow
from src.activities.shared_activities import shared_activity
from src.activities.logging_activity import log_workflow_event
from src.logger import get_custom_logger
from src.interceptors.workflow_interceptor import WorkflowLoggerInterceptor

async def main():
    # worker-level logger (optional)
    logger = get_custom_logger(__name__)
    logger.info("Worker starting up")

    client = await Client.connect("temporal:7233")

    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[MyWorkflow, AnotherWorkflow],
        activities=[shared_activity, log_workflow_event],
        interceptors=[WorkflowLoggerInterceptor()],  # this sets workflow inbound interceptor
    )

    logger.info("Worker run() entering (blocking)")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
