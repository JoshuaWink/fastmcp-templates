
import threading
import queue

class SubscriptionClient:
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
        self._client = fastmcp_client
        self._subscriptions = {}

    def subscribe(self, topic, callback=None):
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
            for msg in self._client.listen(topic):
                if stop_event.is_set():
                    break
                q.put(msg)
                if callback:
                    callback(msg)
        thread = threading.Thread(target=listener, daemon=True)
        thread.start()
        handle = SubscriptionHandle(q, stop_event, thread)
        self._subscriptions[topic] = handle
        return handle

    def unsubscribe(self, topic):
        """
        Unsubscribe from a topic and stop receiving updates.
        """
        if topic in self._subscriptions:
            self._subscriptions[topic].stop()
            del self._subscriptions[topic]

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
