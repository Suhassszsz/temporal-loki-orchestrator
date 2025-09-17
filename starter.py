import asyncio
from temporalio.client import Client
from src.workflows.my_workflow import MyWorkflow
from src.workflows.another_workflow import AnotherWorkflow

async def main():
    client = await Client.connect("temporal:7233")

    handles = []

    # Start multiple instances of the same workflow type (homogeneous) to simulate concurrency
    for i, name in enumerate(["Alice", "Bob", "Carol"], start=1):
        wf_id = f"wf-my-{i}"
        handle = await client.start_workflow(
            MyWorkflow.run,
            name,
            id=wf_id,
            task_queue="my-task-queue",
        )
        handles.append(handle)
        print(f"started {wf_id}")

    # Start a couple of AnotherWorkflow instances too
    for i in range(1, 3):
        wf_id = f"wf-another-{i}"
        handle = await client.start_workflow(
            AnotherWorkflow.run,
            id=wf_id,
            task_queue="my-task-queue",
        )
        handles.append(handle)
        print(f"started {wf_id}")

    # Wait for all workflows to complete concurrently
    results = await asyncio.gather(*(h.result() for h in handles), return_exceptions=True)

    for h, res in zip(handles, results):
        print(f"{h.id} -> {res}")

if __name__ == "__main__":
    asyncio.run(main())
