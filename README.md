# AI Life Admin Assistant (MVP)

A proactive assistant that surfaces high-value "life maintenance" tasks before they become expensive or stressful.

## What this MVP does

- Detects actionable signals from simple user data (subscriptions, bills, habits, reminders).
- Prioritizes tasks that save money, prevent issues, and reduce mental load.
- Outputs each recommendation in a strict, reusable structure:
  - `[INSIGHT]`
  - `[WHY IT MATTERS]`
  - `[SUGGESTED ACTION]`
  - `[OPTIONAL ASSIST]`
- Limits recommendations to the top 3 to avoid overwhelm.

## Quick start

```bash
python3 life_admin_assistant.py --input sample_signals.json
```

## Input shape

The script expects JSON in this format:

```json
{
  "today": "2026-03-26",
  "signals": {
    "subscriptions": [
      {
        "name": "HBO Max",
        "kind": "free_trial",
        "expires_on": "2026-03-27",
        "monthly_cost": 15.99
      }
    ],
    "bills": [
      {
        "name": "Comcast Internet",
        "previous_amount": 70,
        "current_amount": 90,
        "month": "2026-03"
      }
    ],
    "habits": [
      {
        "name": "gym",
        "goal_per_week": 3,
        "days_since_last_activity": 12,
        "monthly_cost": 49
      }
    ],
    "pending_tasks": [
      {
        "title": "Text landlord about kitchen leak",
        "days_overdue": 5,
        "severity": "high"
      }
    ]
  }
}
```

## Design choices

- **Proactive, not reactive:** insights are inferred from signals without waiting for explicit asks.
- **High-value only:** scoring heavily favors money risk, urgency, and neglected admin tasks.
- **Low friction:** each insight includes one immediate next step and an offer to assist.

## Notes

This is a lightweight MVP to demonstrate behavior and output style. It can be extended with:

- Gmail API ingestion
- Calendar synchronization
- Push notifications
- Action executors (drafting messages, cancellation playbooks, comparison shopping)
