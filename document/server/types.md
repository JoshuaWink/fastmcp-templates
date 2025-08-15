# MCP Server Types & Interfaces (TypeScript-inspired)

This document defines the core types, interfaces, and schemas needed for a fully spec-compliant MCP server, using TypeScript-style notation for clarity.

---

```typescript
// === Core Types ===
interface ITool {
  name: string;
  description: string;
  parameters: Record<string, any>;
  handler: (...args: any[]) => any;
}

interface IResource {
  name: string;
  description: string;
  uri: string;
  fetch: () => any;
}

interface IPrompt {
  name: string;
  description: string;
  template: string;
  render: (args: Record<string, any>) => string;
}

interface ISubscription {
  topic: string;
  description: string;
  schema: Record<string, any>;
  subscribe: (callback: (msg: any) => void) => SubscriptionHandle;
}

interface INotification extends ISubscription {
  // Notification-specific schema fields
  priority: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  timestamp: string;
}

// === Auth & Session Types ===
interface IUserSession {
  userId: string;
  token: string;
  context: Record<string, any>;
  version: string;
}

interface IAuthProvider {
  authenticate: (credentials: any) => IUserSession;
  authorize: (session: IUserSession, action: string) => boolean;
}

// === Error Handling ===
interface IMCPError {
  code: string;
  message: string;
  details?: any;
}

// === Discovery ===
interface IDiscovery {
  listTools: () => ITool[];
  listResources: () => IResource[];
  listPrompts: () => IPrompt[];
  listSubscriptions: () => ISubscription[];
}

// === Versioning ===
interface IVersionInfo {
  protocol: string;
  serverVersion: string;
  supportedClients: string[];
}

// === Schema Exposure ===
interface ISchemaProvider {
  getToolSchema: (toolName: string) => any;
  getResourceSchema: (resourceName: string) => any;
  getPromptSchema: (promptName: string) => any;
  getSubscriptionSchema: (topic: string) => any;
}
```

---


**Notes:**
- These interfaces cover all required and recommended MCP server features: tools, resources, prompts, subscriptions, notifications, auth/session, error handling, discovery, versioning, and schema exposure.
- You can extend or specialize these interfaces as needed for your implementation.
- **Best Practice:** For subscriptions, always include a `timestamp` field in event payloads. See [subscriptions.md](./subscriptions.md) for rationale, code examples, and schema guidance.
