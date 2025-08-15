import heapq
class NotificationsClient:
    """
    Client for managing notifications with priority queues.
    """
    PRIORITY_MAP = {"low": 3, "medium": 2, "high": 1, "critical": 0}

    def __init__(self, fastmcp_client):
        self._client = fastmcp_client
        self._queue = []  # (priority, count, message)
        self._counter = 0

    def add_notification(self, message, priority="low"):
        prio = self.PRIORITY_MAP.get(priority, 3)
        heapq.heappush(self._queue, (prio, self._counter, message))
        self._counter += 1

    def get_notifications(self, max_count=None):
        notifications = sorted(self._queue)
        if max_count:
            notifications = notifications[:max_count]
        return [msg for _, _, msg in notifications]

    def clear_notifications(self, priority=None):
        if priority is None:
            self._queue = []
        else:
            prio = self.PRIORITY_MAP.get(priority, 3)
            self._queue = [n for n in self._queue if n[0] != prio]
