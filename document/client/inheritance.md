# Client Inheritance & Interface Relationships (TypeScript-inspired)

This document shows the relationships and inheritance structure of all major client entities, using TypeScript-style interfaces and class extension for clarity.

---

```typescript
// === Core Interfaces ===
interface ISubscription {
  subscribe(topic: string, callback?: (msg: any) => void): SubscriptionHandle;
  unsubscribe(topic: string): void;
}

interface IToolCall {
  call(toolName: string, ...args: any[]): any;
}

interface IResource {
  get(resourceName: string): any;
}

// === Core Classes ===
class SubscriptionClient implements ISubscription {
  // ...
}

class ToolsClient implements IToolCall {
  // ...
}

class PromptsClient extends ToolsClient {
  // Always returns string
}

class ResourcesClient implements IResource {
  // ...
}

// === Extensions & Specializations ===
class NotificationsClient extends SubscriptionClient {
  // Handles notification schema/messages
}

// === Meta/Support ===
class DiscoveryClient {
  // Lists tools, resources, prompts
}

class ElicitationClient {
  // Handles structured input requests
}

class LoggingClient {
  // Handles logging (could be a subscription or tool call)
}

class LLMRouter {
  // Routes LLM JSON tool/resource calls
}

class MCPClient {
  // Orchestrates all subclients
}
```

---

**Notes:**
- `PromptsClient` is a subtype of `ToolsClient` (always returns string).
- `NotificationsClient` is an extension of `SubscriptionClient` (special schema for notifications).
- All core clients can be reasoned about as implementing one of: `ISubscription`, `IToolCall`, or `IResource`.
- Meta/support classes (discovery, elicitation, logging, router, orchestrator) do not fit the main inheritance tree but are essential for full client functionality.

# Client Inheritance Notes

This document illustrates patterns for composing client subcomponents and extending behavior.

Example (TypeScript-like pseudocode):

```typescript
class BaseClient {
  constructor(config) { this.config = config }
}

class ToolsClient extends BaseClient {
  call(name, args) { /* ... */ }
}
```

In Python, prefer composition over inheritance for clarity: `MCPClient` composes `ToolsClient`, `ResourcesClient`, etc.
