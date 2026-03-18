---
sidebar_position: 11
title: WebhooksApi
---

# WebhooksApi

Register and manage webhooks for real-time notifications when documents change.

```python
wh_api = client.webhooks
```

**Base path:** `/api/v6/webhooks`

## Common Event Types

```python
WebhooksApi.EVENTS = [
    "onshape.model.lifecycle.changed",
    "onshape.model.translation.complete",
    "onshape.document.lifecycle.statechange",
    "onshape.workflow.transition",
    "onshape.comment.create",
    "onshape.revision.created",
]
```

## Methods

### list

List all webhooks owned by the current user.

```python
webhooks.list() -> list[Webhook]
```

```python
hooks = client.webhooks.list()
for h in hooks:
    print(f"{h.id}: {h.url} — events={h.events}")
```

---

### create

Register a new webhook.

```python
webhooks.create(
    url: str,
    events: list[str],
    filter: str | None = None,
    options: dict | None = None
) -> Webhook
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | Your callback endpoint URL |
| `events` | `list[str]` | Event types to subscribe to |
| `filter` | `str` | Optional JSON filter (e.g., `'{"documentId": "abc123"}'`) |
| `options` | `dict` | Optional config (e.g., `{"collapseEvents": True}`) |

```python
webhook = client.webhooks.create(
    url="https://my-server.com/onshape-webhook",
    events=["onshape.model.lifecycle.changed"],
    filter='{"documentId": "804d1a7a071db077dbad4e42"}',
)
print(f"Created webhook: {webhook.id}")
```

**Example response object:**

```json
{
  "id": "wh-abc123",
  "url": "https://my-server.com/onshape-webhook",
  "events": ["onshape.model.lifecycle.changed"],
  "options": {},
  "raw": { ... }
}
```

---

### get

Get details of a specific webhook.

```python
webhooks.get(webhook_id: str) -> Webhook
```

---

### update

Update an existing webhook.

```python
webhooks.update(
    webhook_id: str,
    url: str | None = None,
    events: list[str] | None = None,
    filter: str | None = None,
    options: dict | None = None
) -> Webhook
```

```python
client.webhooks.update(
    "wh-abc123",
    events=["onshape.model.lifecycle.changed", "onshape.comment.create"],
)
```

---

### delete

Delete a webhook.

```python
webhooks.delete(webhook_id: str) -> None
```

```python
client.webhooks.delete("wh-abc123")
```
