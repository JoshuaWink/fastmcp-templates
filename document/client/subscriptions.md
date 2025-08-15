# Client Subscriptions

This file documents subscription patterns for client-side code.

Example:

```python
# subscribe and process events
async for ev in client.subscriptions.listen("demo_subscription"):
    print(ev)
```

See `client/README.md` and `tests/client` for concrete examples.

# Client-Side Subscriptions: Timestamp Annotation Best Practice

## Overview

When consuming subscription (event stream) events from an MCP server, clients should annotate the time each event is received. This, combined with the server-provided `timestamp` field, enables full traceability, latency measurement, and context-aware reasoning for downstream consumers (e.g., LLMs, UIs, logs).

## Why Annotate Receive Time?
- **Latency Measurement:** Calculate the time between when the server emitted the event and when the client received it.
- **Debugging:** Identify network delays, dropped events, or out-of-order delivery.
- **Prompt Context:** LLMs and agents can reason about event freshness and delivery lag.
- **Auditing:** Enables robust event logging and replay with both send and receive times.

## Client-Side Pattern
- Upon receiving an event, immediately record the current time as the receive timestamp.
- Compare the server's `timestamp` (when the event was sent) to the local receive time.
- Example (Python):

```python
import time

def on_event(event):
    received_at = time.time()  # Local receive time (UTC seconds since epoch)
    sent_at = event.get("timestamp")  # Server send time
    print(f"Event sent at {sent_at}, received at {received_at}, latency: {received_at - sent_at:.3f} seconds")
```

## Best Practices
- Always check for the presence of the `timestamp` field in incoming events.
- Use UTC and a consistent format (e.g., seconds since epoch) for both send and receive times.
- Log or store both timestamps for auditing and debugging.
- If using the event in an LLM prompt, include both times for context-aware reasoning.

## Example Use Case
- **UI:** Display how recently an event was received (e.g., "Last update: 2.1 seconds ago").
- **LLM Prompt:** "The last sensor reading was sent at 1620000000.0 and received at 1620000000.2 (0.2s latency)."
- **Logs:** Record both send and receive times for each event.

## Summary
- **Always annotate the receive time for subscription events.**
- **Compare with the server's `timestamp` for full traceability.**
- **Document this pattern in your client code and API docs.**

This pattern ensures robust, debuggable, and LLM-friendly event handling in your MCP client.
