# Client Subscribe

This document describes the client's subscribe/listen API and examples.

## Example: subscribe/listen usage

```python
async for event in client.subscriptions.listen("demo_subscription"):
    print(event)
```

## Example payload (JSON)

```json
{
  "subscription": "demo_subscription",
  "params": {}
}
```

## Notes
- The client's `SubscriptionClient` centralizes streaming, cancellation, and retry logic.
- See `tests/client/test_subscribe.py` for usage examples.
