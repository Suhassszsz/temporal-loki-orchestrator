# src/interceptors/workflow_interceptor.py
from datetime import timedelta
from temporalio import workflow
from temporalio.worker import Interceptor, WorkflowInboundInterceptor

# Import the logging activity (safe to call from workflow)
from src.activities.logging_activity import log_workflow_event


class MyWorkflowInboundInterceptor(WorkflowInboundInterceptor):
    def __init__(self, next: WorkflowInboundInterceptor):
        super().__init__(next)

    async def execute_workflow(self, input):
        info = workflow.info()

        # Log START via activity
        await workflow.execute_activity(
            log_workflow_event,
            args=[info.workflow_id, info.run_id, info.workflow_type, "STARTED", "Workflow started"],
            schedule_to_close_timeout=timedelta(seconds=10),
        )

        try:
            result = await super().execute_workflow(input)

            # Log END via activity
            await workflow.execute_activity(
                log_workflow_event,
                args=[info.workflow_id, info.run_id, info.workflow_type, "COMPLETED", "Workflow finished"],
                schedule_to_close_timeout=timedelta(seconds=10),
            )

            return result

        except Exception as e:
            # Log ERROR via activity
            await workflow.execute_activity(
                log_workflow_event,
                args=[info.workflow_id, info.run_id, info.workflow_type, "FAILED", str(e)],
                schedule_to_close_timeout=timedelta(seconds=10),
            )
            raise


class WorkflowLoggerInterceptor(Interceptor):
    def workflow_interceptor_class(self, input) -> type[WorkflowInboundInterceptor]:
        return MyWorkflowInboundInterceptor
