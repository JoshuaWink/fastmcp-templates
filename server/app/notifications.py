
"""
Area of Responsibility: Notifications
- Register notification-specific subscriptions or schemas here.
- Notifications are a schema/extension of the subscription model.
- Document notification schemas for discoverability and LLM/agent use.
"""

def register_notifications(server):
    """
    Register notification-specific subscriptions or schemas with the FastMCP server instance.
    """
    @server.subscription(
        name="demo_notification",
        description="Demo notification that emits a message and priority."
    )
    def demo_notification_handler(message: str = "Test notification", priority: str = "low") -> dict:
        """
        Demo notification event handler that emits a notification with message and priority.
        Args:
            message (str): Notification message.
            priority (str): Notification priority (low, medium, high, critical).
        Returns:
            dict: Notification event.
        """
        return {
            "type": "notification",
            "message": message,
            "priority": priority,
        }
