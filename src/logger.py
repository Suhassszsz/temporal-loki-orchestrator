import logging
import json
import time
import requests
from temporalio import workflow, activity

# ---------- FORMATTER ----------
class JSONFormatter(logging.Formatter):
    def format(self, record):
        # Prepare message text — handle dict messages cleanly
        raw_msg = record.getMessage()
        if isinstance(raw_msg, dict):
            try:
                message_text = json.dumps(raw_msg)
            except Exception:
                message_text = str(raw_msg)
        else:
            message_text = str(raw_msg)

        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": message_text,
        }

        # Add workflow_id as a structured field (not inside message text)
        workflow_id = getattr(record, "workflow_id", None)
        if workflow_id and workflow_id != "N/A":
            log_data["workflow_id"] = workflow_id

        return json.dumps(log_data)

# ---------- FILTERS ----------
class ActivityFilter(logging.Filter):
    def filter(self, record):
        try:
            info = activity.info()
            record.workflow_id = info.workflow_id
            return True
        except RuntimeError:
            # Not in an activity
            record.workflow_id = getattr(record, "workflow_id", "N/A")
            return True

class WorkflowFilter(logging.Filter):
    def filter(self, record):
        try:
            # workflow.in_workflow() can raise in non-workflow contexts
            if workflow.in_workflow():
                info = workflow.info()
                record.workflow_id = info.workflow_id
            else:
                record.workflow_id = getattr(record, "workflow_id", "N/A")
            return True
        except RuntimeError:
            record.workflow_id = getattr(record, "workflow_id", "N/A")
            return True

# ---------- LOKI HANDLER ----------
class LokiHTTPHandler(logging.Handler):
    def __init__(self, url, tags=None):
        super().__init__()
        self.url = url
        # Important: do NOT include workflow_id here — tags are static labels for Loki streams
        self.tags = tags or {"app": "temporal-worker"}

    def emit(self, record):
        try:
            # Base stream labels (no workflow_id label)
            stream_labels = {**self.tags, "level": record.levelname.lower()}

            log_entry = {
                "streams": [
                    {
                        "stream": stream_labels,
                        "values": [
                            [
                                str(time.time_ns()),  # nanosecond timestamp
                                self.format(record),
                            ]
                        ],
                    }
                ]
            }

            response = requests.post(
                self.url,
                data=json.dumps(log_entry),
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
            if response.status_code >= 400:
                # Print to console to help debugging inside container
                print(f"[Loki] error {response.status_code}: {response.text}", flush=True)

        except Exception as e:
            # Avoid raising inside logging
            print(f"[Loki] failed to send log: {e}", flush=True)

# ---------- LOGGER FACTORY ----------
def get_custom_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        activity_filter = ActivityFilter()
        workflow_filter = WorkflowFilter()

        class FilterGroup(logging.Filter):
            def filter(self, record):
                # Apply both filters (they each set record.workflow_id appropriately)
                return activity_filter.filter(record) and workflow_filter.filter(record)

        # Loki handler: note URL points to docker-compose service name "loki"
        loki_handler = LokiHTTPHandler(
            url="http://loki:3100/loki/api/v1/push",
            tags={"app": "temporal-worker"},  # default tags — no static workflow_id
        )
        loki_handler.addFilter(FilterGroup())
        loki_handler.setFormatter(JSONFormatter())

        # Console handler (stdout)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(JSONFormatter())
        console_handler.addFilter(FilterGroup())

        logger.addHandler(console_handler)
        logger.addHandler(loki_handler)

    return logger
