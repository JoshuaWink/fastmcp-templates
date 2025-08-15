# Server Types

This document sketches common type shapes used in MCP servers (pseudotype/TypeScript examples).

Example types:

```typescript
type ToolSpec = {
  name: string;
  description?: string;
  argsSchema?: object;
}
```

Use Python dataclasses or Pydantic models in production code where helpful.
