
import threading
import queue

class SubscriptionClient:

    def call_subscription(self, topic, payload=None):
        """
        Generator that yields events from the server for a given subscription topic.
        Delegates to the underlying FastMCP client if supported.
        """
        if hasattr(self._client, 'call_subscription'):
            return self._client.call_subscription(topic, payload=payload)
        elif hasattr(self._client, 'subscribe'):
            return self._client.subscribe(topic, payload=payload)
        else:
            raise NotImplementedError("Underlying FastMCP client does not support subscription streaming.")
    def listen(self, topic, payload=None):
        """
        Listen for events on a subscription topic using the FastMCP client's subscription API.
        Yields each event as it arrives.
        """
        # Always check the wrapper (MCPClient) first
        if hasattr(self._wrapper, 'call_subscription'):
            return self._wrapper.call_subscription(topic, payload=payload)
        if hasattr(self._wrapper, 'subscribe'):
            return self._wrapper.subscribe(topic, payload=payload)
        # Then check the underlying FastMCP client
        if hasattr(self._client, 'call_subscription'):
            return self._client.call_subscription(topic, payload=payload)
        if hasattr(self._client, 'subscribe'):
            return self._client.subscribe(topic, payload=payload)
        # Then check the inner client if present
        if hasattr(self._client, '_client'):
            inner = self._client._client
            if hasattr(inner, 'call_subscription'):
                return inner.call_subscription(topic, payload=payload)
            if hasattr(inner, 'subscribe'):
                return inner.subscribe(topic, payload=payload)
        raise NotImplementedError("FastMCP client does not support subscription streaming.")
    """
    Client for subscribing to and listening for streamed updates (e.g., progress, logs, events) via FastMCP or other sources.

    Areas of Responsibility:
    - Exposes server-provided fields (e.g., 'timestamp') transparently to the user.
    - Allows, but does not enforce, local annotation (e.g., 'received_at') for each message.
    - Provides a callback mechanism for context providers to shape, annotate, or format messages as needed.
    - Does not force any particular context structure—supports opt-in, composable workflows.
    """
    def __init__(self, fastmcp_client):
        """
        Initialize the SubscriptionClient with a FastMCP client instance.
        """
        self._wrapper = fastmcp_client
        self._client = fastmcp_client._client
        self._subscriptions = {}

    def subscribe(self, topic, callback=None, payload=None):
        """
        Subscribe to a topic (e.g., 'progress', 'logs') and listen for updates.

        If a callback is provided, it will be called with each new message.
        The callback can optionally annotate messages (e.g., add 'received_at') or compute elapsed time.
        Returns a SubscriptionHandle for manual polling or management.

        Example usage:
            def on_msg(msg):
                import time
                msg['received_at'] = time.time()
                # Optionally compute elapsed = msg['received_at'] - msg.get('timestamp', msg['received_at'])
            handle = client.subscribe('progress', callback=on_msg)
        """
        q = queue.Queue()
        stop_event = threading.Event()
        def listener():
            for msg in self.listen(topic, payload=payload):
                if stop_event.is_set():
                    break
                q.put(msg)
                if callback:
                    callback(msg)
        thread = threading.Thread(target=listener, daemon=True)
        thread.start()
        return SubscriptionHandle(q, stop_event, thread)
    def listen(self, topic, payload=None):
        """
        Listen for events on a subscription topic using the FastMCP client's subscription API.
        Yields each event as it arrives.
        """
        # Always check the wrapper (MCPClient) first
        if hasattr(self._wrapper, 'call_subscription'):
            return self._wrapper.call_subscription(topic, payload=payload)
        if hasattr(self._wrapper, 'subscribe'):
            return self._wrapper.subscribe(topic, payload=payload)
        # Then check the underlying FastMCP client
        if hasattr(self._client, 'call_subscription'):
            return self._client.call_subscription(topic, payload=payload)
        if hasattr(self._client, 'subscribe'):
            return self._client.subscribe(topic, payload=payload)
        raise NotImplementedError("FastMCP client does not support subscription streaming.")

class SubscriptionHandle:
    """
    Handle for managing a subscription thread and polling for messages.

    - get(): Poll for the next message (blocking or non-blocking).
    - stop(): Stop the subscription thread.
    """
    def __init__(self, queue, stop_event, thread):
        """
        Initialize the SubscriptionHandle with a message queue, stop event, and thread.
        """
        self._queue = queue
        self._stop_event = stop_event
        self._thread = thread
    def get(self, block=True, timeout=None):
        """
        Retrieve the next message from the queue.
        """
        return self._queue.get(block=block, timeout=timeout)
    def stop(self):
        """
        Stop the subscription thread and clean up resources.
        """
        self._stop_event.set()
        self._thread.join()
