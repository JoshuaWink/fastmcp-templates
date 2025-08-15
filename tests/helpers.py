class DummyServer:
    """Shared test double for server-side tests.

    Provides simple decorator methods that register functions into internal
    registries so tests can assert on registrations.
    """
    def __init__(self):
        self._tools = {}
        self._resources = {}
        self._prompts = {}
        self._subscriptions = {}
        self._schemas = {}
        self._error_handlers = {}
        self._auths = {}
        self._auth_providers = {}

    def tool(self, name, description=""):
        def decorator(fn):
            self._tools[name] = fn
            return fn
        return decorator

    def prompt(self, name, description=""):
        def decorator(fn):
            self._prompts[name] = fn
            return fn
        return decorator

    def resource(self, uri, name=None, description=""):
        def decorator(fn):
            self._resources[uri] = fn
            return fn
        return decorator

    def subscription(self, name, description=""):
        def decorator(fn):
            self._subscriptions[name] = fn
            return fn
        return decorator

    def error_handler(self, name, description=""):
        def decorator(fn):
            self._error_handlers[name] = fn
            return fn
        return decorator

    def schema(self, name, description=""):
        def decorator(fn):
            self._schemas[name] = fn
            return fn
        return decorator

    # Provide both auth and auth_provider for compatibility with tests
    def auth(self, name, description=""):
        def decorator(fn):
            self._auths[name] = fn
            return fn
        return decorator

    def auth_provider(self, name, description=""):
        def decorator(fn):
            self._auth_providers[name] = fn
            return fn
        return decorator
