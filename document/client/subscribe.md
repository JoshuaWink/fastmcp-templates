
# client/subscribe.py

**Purpose:**
Client for subscribing to and listening for streamed updates (e.g., progress, logs, events, notifications) via FastMCP or other sources.

**Core Model:**
- `SubscriptionClient` (core): subscribes to any topic (progress, logs, notifications, etc.)
- `SubscriptionHandle`: returned by subscribe(), allows polling or stopping the subscription.
- **Notifications**: are a schema/extension of the subscription model (not a standalone category).

**Pseudocode Inheritance/Extension:**
```python
class SubscriptionClient:
		# ... core subscribe/unsubscribe logic ...

class NotificationsClient(SubscriptionClient):
		# (Conceptual) Extends SubscriptionClient for notification-specific logic/schema
		# e.g., subscribe('notifications', callback=...)
```

**Notification Schema Example:**
```json
{
	"type": "notification",
	"priority": "high",  // or "low", "critical", etc.
	"message": "...",
	"timestamp": "..."
}
```


**API:**
- subscribe(topic, callback=None): Subscribes to a topic and listens for updates. Optionally calls a callback for each message.
- unsubscribe(topic): Stops listening to a topic.
- SubscriptionHandle.get(): Polls for the next message.
- SubscriptionHandle.stop(): Stops the subscription thread.

**Best Practice: Timestamp Incoming Messages**
- Whenever a message is received from a subscription, immediately annotate it with a local receive timestamp (e.g., `received_at = time.time()`).
- This enables full traceability, latency measurement, and context-aware reasoning for downstream consumers (LLMs, UIs, logs).

**Example:**
```python
import time

def on_subscription_message(msg):
		received_at = time.time()  # Local receive time (UTC seconds since epoch)
		msg["received_at"] = received_at
		# Now msg contains both the server's 'timestamp' and the local 'received_at'
		# Use both for context, logging, or prompt construction
		print(f"Event sent at {msg.get('timestamp')}, received at {received_at}, latency: {received_at - msg.get('timestamp', received_at):.3f} seconds")
```

**Architectural Note:**
	- Always document and use both the server's `timestamp` and the local `received_at` for robust, debuggable, and LLM-friendly event handling.

**Architectural Note:**
- The subscription model is the core for all streaming/event-driven context (progress, logs, notifications, etc.).
- Notifications are an extension/schema of subscription, adding context as needed but not required for all workflows.
