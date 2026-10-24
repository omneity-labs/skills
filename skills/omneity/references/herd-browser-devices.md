# Browser Devices

Use this for registering browser devices, listing devices, sending browser RPC,
and consuming events.

Common operations:

```bash
herd device list
herd device register
herd device events --device <device-id>
```

App pattern:

- Register devices per environment or user workspace.
- Keep device IDs server-side when possible.
- Stream events to internal logs or a backend event bus before showing them in
  the UI.
- Use direct device RPC for advanced control; prefer trails for repeatable
  product workflows.

Best practices:

- Display connection, permission, and last-seen states.
- Avoid exposing arbitrary browser RPC to end users.
- Keep device actions auditable.
