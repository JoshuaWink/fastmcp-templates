# Areas of Responsibility: FastMCP Context, Client, and Server


This document clarifies the responsibilities of each layer in the FastMCP ecosystem—context providers (e.g., prompt engineers, LLM orchestrators), the client library, and the server. Clear separation of concerns ensures robust, extensible, and maintainable systems.

---

## Why Timestamps and Time Awareness Matter

Some workflows are highly time-sensitive. For example, if you are controlling a Mars rover, there may be an 8-minute delay between sending a command and receiving a response. In contrast, interacting with a local device may have sub-second or even millisecond latency. Knowing exactly when an event was generated (server `timestamp`) and when it was received (`received_at`) is critical for:
- **Decision Making:** Agents and humans can adjust actions based on event freshness or delay.
- **Debugging:** Identify network or system bottlenecks.
- **Transparency:** Users and LLMs can reason about the recency and reliability of information.

**Real-World Example:**
> If you are operating a Mars rover and receive a sensor reading, knowing that it was sent 8 minutes ago (due to the speed-of-light delay) is crucial for safe and effective control. In contrast, a 30-millisecond delay for a local robot may be negligible, but still worth tracking for high-precision tasks.


For these reasons, we recommend timestamping all events and making both send and receive times available in context, even if not all workflows require it.

---

## Annotating and Presenting Elapsed Time

Having both the server `timestamp` (when the event was sent) and the local `received_at` (when it was received) allows you to calculate the elapsed time (latency or age) for any event:

```python
elapsed = received_at - timestamp  # in seconds (float)
```

**Presentation Matters:**
- The way elapsed time is presented can affect both human and agent understanding.
- For agents or UIs, you may want to present elapsed time in a human-friendly format (e.g., "12.7 seconds" instead of "12700 milliseconds").
- You can also present it in milliseconds, deciseconds, or fractions of a second, depending on the use case.
- The choice of format should be driven by what is most useful for the agent or user in context.

**Example:**
> "Event sent at 1620000000.0, received at 1620000012.7 (elapsed: 12.7 seconds)"

**Note:**
- We provide both timestamps so you can compute and present elapsed time as needed. The responsibility for formatting and presentation lies with the context provider or application, allowing maximum flexibility for different workflows and audiences.

---

## 1. Context Providers (Prompt Engineers, LLM Orchestrators, Application Integrators)
- **Responsibility:**
  - Decide what information is included in the context for LLMs/agents (e.g., which events, how much history, what metadata).
  - Optionally annotate or transform incoming data (e.g., add `received_at` timestamps, filter or summarize events).
  - Construct prompts or agent inputs in the required format (e.g., JSON, Markdown, custom schemas).
  - Ensure that context is relevant, up-to-date, and formatted for optimal agent performance.
- **Example:**
  - Add a `received_at` field to each event before including it in the LLM prompt.
  - Filter out stale or irrelevant events.

---

## 2. Client Library (FastMCP Client)
- **Responsibility:**
  - Provide APIs for subscribing to topics, receiving events, and managing connections.
  - Optionally annotate incoming events with local metadata (e.g., `received_at` timestamp), but do not enforce this.
  - Expose all server-provided fields (e.g., `timestamp`) transparently to the user.
  - Offer utilities for context construction, but leave final context shaping to the application/integrator.
- **Example:**
  - Provide a callback mechanism where the user can add `received_at` if desired.
  - Do not force any particular context structure—allow flexibility for downstream consumers.

---

## 3. Server (FastMCP Server)
- **Responsibility:**
  - Emit events with all required metadata (e.g., `timestamp` for when the event was sent).
  - Document the schema and semantics of all event fields.
  - Ensure events are well-formed, timely, and discoverable by clients/agents.
  - Do not assume or require client-side context annotation.
- **Example:**
  - Every event includes a `timestamp` field (UTC, seconds since epoch or ISO8601).
  - Document the event schema in OpenAPI, JSON Schema, or Markdown docs.

---

## Summary Table

| Layer            | Responsibility Example                                 | Required? |
|------------------|-------------------------------------------------------|-----------|
| Context Provider | Add `received_at` to events for LLM prompt            | Optional  |
| Client Library   | Expose server fields, allow annotation, not enforce   | Optional  |
| Server          | Emit `timestamp` in all events, document schema        | Required  |

---

## Best Practice
- **Server:** Always provide a `timestamp` for traceability.
- **Client:** Allow, but do not require, local annotation (e.g., `received_at`).
- **Context Provider:** Shape and annotate context as needed for agent/LLM use.


---

## Opt-In, Composable Philosophy

The FastMCP architecture is designed for opt-in composability: each layer (server, client, context provider) can implement features like timestamping, elapsed time calculation, or context annotation as needed, without forcing requirements on others. If a feature is important for your workflow, you can enable and use it; if not, it remains as optional metadata.

This approach ensures:
- **Flexibility:** Only implement what you need, when you need it.
- **Extensibility:** New features and patterns can be layered in without breaking existing workflows.
- **Interoperability:** Different teams or agents can make independent choices about what context to use or ignore.

This opt-in, composable pattern applies not just to time awareness, but to all aspects of FastMCP context and event handling. It enables robust, future-proof systems that can adapt to new requirements and use cases as they arise.

This separation ensures each layer is clear, flexible, and easy to extend or adapt for new workflows.

AoR tl;dr
- Context Providers shape and annotate context for LLMs/agents.
- Client Libraries expose server fields and allow optional annotation.
- Servers emit required metadata (e.g., timestamps) and document schemas.