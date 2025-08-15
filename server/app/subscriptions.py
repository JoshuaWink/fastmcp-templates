# Define and register subscription topics/streams


import time
from typing import Dict, Any

def current_utc_timestamp() -> float:
    """
    Returns the current UTC timestamp as a float (seconds since epoch).
    This is used to annotate all subscription events for traceability.
    """
    return time.time()

def register_subscriptions(server):
    """
    Register all subscription handlers with the server.
    This demo registers a 'demo_subscription' that emits timestamped events.
    """
    @server.subscription(
        name="demo_subscription",
        description="Demo subscription that emits events with a server-side timestamp."
    )
    def demo_subscription_handler(payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Demo subscription event handler that emits an event with a server-side timestamp.
        Best practice: Always include a 'timestamp' field in subscription events so clients can annotate
        both the send and receive times for full event traceability.
        """
        event = {
            "event": "demo_event",
            "data": payload or {},
            "timestamp": current_utc_timestamp(),  # Server-side event time
        }
        return event
