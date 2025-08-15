# client/notifications.py

**Purpose:**
Client for managing notifications with priority queues.

**Key Entities:**
- NotificationsClient: Manages a local priority queue for notifications.

**API:**
- add_notification(message, priority="low"): Adds a notification with priority.
- get_notifications(max_count=None): Returns sorted notifications.
- clear_notifications(priority=None): Clears notifications by priority or all.
