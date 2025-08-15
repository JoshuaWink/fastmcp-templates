# LLMRouter Call Flow Mapping

## 1. Entry Points

### a. `route(message)`
- **Input:** Python dict (e.g., `{"tool": ..., "args": ...}` or `{"prompt": ...}` or `{"resource": ...}`)
- **Logic:**
  - If `"tool"` in message: calls `self.client.tools.call(...)`
  - If `"prompt"` in message: calls `self.client.prompts.render(...)`
  - If `"resource"` in message: calls `self.client.resources.get(...)`
  - Else: raises `ValueError`
- **Output:** Result from the appropriate client section (tool, prompt, or resource).

### b. `route_batch(messages, parallel=False)`
- **Input:** List of message dicts (see above), optional `parallel` flag.
- **Logic:**
  - If `parallel=True`: uses `ThreadPoolExecutor` to call `route` on each message concurrently.
  - Else: sequentially calls `route` for each message.
- **Output:** List of results, one per message.

### c. `route(llm_json_str)`
- **Input:** JSON string (e.g., `'{"tool": "greet", "args": {"user": "Ford"}}'`)
- **Logic:**
  - Parses JSON to dict.
  - If `"resource"` in data: checks if resource exists, calls `self.client.resources.get(...)`
  - If `"tool"` in data: checks if tool exists, calls `self.client.tools.call(...)`
  - If `"prompt"` in data: checks if prompt exists, calls `self.client.prompts.render(...)`
  - Else: raises `ValueError`
- **Output:** Result from the appropriate client section.

---

## 2. Stub Methods (Not Used in Main Flow)

### a. `route_tool_call(tool_name, payload)`
- **Input:** Tool name and payload dict.
- **Logic:** Returns a stubbed dict: `{"tool": tool_name, "payload": payload, "result": "stubbed"}`
- **Output:** Stubbed response (not used by `route` or `route_batch`).

### b. `route_prompt(prompt_name, args)`
- **Input:** Prompt name and args dict.
- **Logic:** Returns a stubbed dict: `{"prompt": prompt_name, "args": args, "result": "stubbed"}`
- **Output:** Stubbed response (not used by `route` or `route_batch`).

---

## 3. Capabilities

### a. `get_llm_capabilities()`
- **Logic:** Returns a compact JSON string listing available tools, prompts, and resources from the client.

---

## 4. Data Flow Diagram

```
[LLM Output (JSON or dict)]
        |
        v
  [route or route_batch]
        |
        v
+-----------------------------+
|  if tool:    tools.call()   |
|  if prompt:  prompts.render()|
|  if resource: resources.get()|
+-----------------------------+
        |
        v
 [Result returned to caller]
```

---

## 5. Summary

- **Main routing is handled by `route` (dict or JSON) and `route_batch` (list of dicts).**
- **Stub methods are not used in the real workflow and can be removed or moved to a test/mock class.**
- **All real tool/prompt/resource calls go through the client’s actual methods.**
