This project shows how to run and monitor Python workflows using Temporal, Loki, and Grafana in a fully dockerized setup. It comes with multiple workflows that share activities, a custom interceptor that logs when workflows start and finish, and a custom logger that tags every log with the correct workflow_id before sending it to Loki. 

Once the system is up with docker-compose up --build -d, you can launch workflows in parallel (e.g., wf-my-alice and wf-another-bob) using docker-compose run --rm worker python starter.py.

Grafana is available at http://localhost:3000 (login: admin/admin); just add Loki as a datasource (http://loki:3100) and you’ll be able to query logs in the Explore tab, such as {app="temporal-worker"} to see everything or {app="temporal-worker", workflow_id="wf-my-alice"} to filter by workflow.

The result is an easy way to orchestrate workflows with Temporal and view rich, searchable logs in Grafana, making it simple to track and debug what’s happening inside your workflows.
