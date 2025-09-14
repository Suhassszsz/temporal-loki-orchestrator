# starter.py (project root)
import asyncio
from temporalio.client import Client
from src.workflows.my_workflow import MyWorkflow
from src.workflows.another_workflow import AnotherWorkflow

async def main():
    client = await Client.connect("temporal:7233")

    # Start two workflows in parallel with distinct workflow IDs
    handle1 = await client.start_workflow(
        MyWorkflow.run,
        "Alice",
        id="wf-my-alice",
        task_queue="my-task-queue",
    )

    handle2 = await client.start_workflow(
        AnotherWorkflow.run,
        id="wf-another-bob",
        task_queue="my-task-queue",
    )

    print(f"started {handle1.id} / {handle2.id}")

    # Optionally wait for results:
    res1 = await handle1.result()
    res2 = await handle2.result()
    print("res1:", res1)
    print("res2:", res2)

if __name__ == "__main__":
    asyncio.run(main())
