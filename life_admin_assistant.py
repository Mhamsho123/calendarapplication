#!/usr/bin/env python3
"""AI Life Admin Assistant MVP.

Generates proactive, high-value life-maintenance insights from simple structured signals.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any


@dataclass
class Insight:
    score: float
    insight: str
    why_it_matters: str
    suggested_action: str
    optional_assist: str

    def render(self) -> str:
        return (
            f"[INSIGHT]\n{self.insight}\n\n"
            f"[WHY IT MATTERS]\n{self.why_it_matters}\n\n"
            f"[SUGGESTED ACTION]\n{self.suggested_action}\n\n"
            f"[OPTIONAL ASSIST]\n{self.optional_assist}\n"
        )


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def build_insights(payload: dict[str, Any]) -> list[Insight]:
    today = parse_date(payload.get("today", date.today().isoformat()))
    signals = payload.get("signals", {})
    generated: list[Insight] = []

    for sub in signals.get("subscriptions", []):
        if sub.get("kind") == "free_trial" and sub.get("expires_on"):
            expires_on = parse_date(sub["expires_on"])
            days_left = (expires_on - today).days
            if days_left <= 2:
                cost = sub.get("monthly_cost", 0)
                generated.append(
                    Insight(
                        score=95 - max(days_left, 0) * 10,
                        insight=(
                            f"Your {sub['name']} free trial expires in {days_left} day(s) on "
                            f"{expires_on.isoformat()}."
                        ),
                        why_it_matters=(
                            f"If not canceled, you could be charged about ${cost:.2f} starting this cycle."
                        ),
                        suggested_action=(
                            "Decide today whether to keep it; cancel now if you are not actively using it."
                        ),
                        optional_assist=(
                            "I can provide a 2-minute cancellation checklist or suggest lower-cost alternatives."
                        ),
                    )
                )

        if sub.get("price_increased"):
            old_price = float(sub.get("old_price", 0))
            new_price = float(sub.get("new_price", 0))
            increase = max(0, new_price - old_price)
            yearly_impact = increase * 12
            generated.append(
                Insight(
                    score=70 + min(increase * 3, 15),
                    insight=(
                        f"{sub['name']} increased from ${old_price:.2f} to ${new_price:.2f} this billing cycle."
                    ),
                    why_it_matters=(
                        f"That is about ${yearly_impact:.2f} extra per year if unchanged."
                    ),
                    suggested_action="Compare alternatives or downgrade within the next 48 hours.",
                    optional_assist=(
                        "I can draft a cancellation/downgrade message and shortlist comparable options."
                    ),
                )
            )

    for bill in signals.get("bills", []):
        prev = float(bill.get("previous_amount", 0))
        cur = float(bill.get("current_amount", 0))
        delta = cur - prev
        if delta >= 10:
            generated.append(
                Insight(
                    score=80 + min(delta / 2, 15),
                    insight=(
                        f"Your {bill['name']} bill rose by ${delta:.2f} in {bill.get('month', 'the latest month')}."
                    ),
                    why_it_matters=f"That trend can cost about ${delta * 12:.2f} more per year.",
                    suggested_action="Request a retention discount or shop competing providers this week.",
                    optional_assist=(
                        "I can draft a negotiation script you can copy-paste into chat or phone notes."
                    ),
                )
            )

    for habit in signals.get("habits", []):
        if habit.get("name") == "gym" and int(habit.get("days_since_last_activity", 0)) >= 10:
            days = int(habit.get("days_since_last_activity", 0))
            monthly_cost = float(habit.get("monthly_cost", 0))
            generated.append(
                Insight(
                    score=62 + min(days, 20) / 2,
                    insight=(
                        f"You have not logged a gym session in {days} days against a "
                        f"{habit.get('goal_per_week', 3)}x/week goal."
                    ),
                    why_it_matters=(
                        f"You are paying ${monthly_cost:.2f}/month for a service you are not using consistently."
                    ),
                    suggested_action=(
                        "Schedule one lighter workout this week or pause membership until your routine stabilizes."
                    ),
                    optional_assist=(
                        "I can create a minimal 2-session plan or draft a membership pause request."
                    ),
                )
            )

    for task in signals.get("pending_tasks", []):
        overdue_days = int(task.get("days_overdue", 0))
        severity = task.get("severity", "low")
        if overdue_days >= 3 and severity in {"high", "medium"}:
            severity_boost = 18 if severity == "high" else 8
            generated.append(
                Insight(
                    score=75 + severity_boost + min(overdue_days, 14),
                    insight=f"'{task['title']}' has been pending for {overdue_days} days.",
                    why_it_matters=(
                        "Delaying admin tasks can increase stress and make the issue harder or more expensive later."
                    ),
                    suggested_action="Send a short update message today to unblock next steps.",
                    optional_assist="I can draft a concise message you can send in under 60 seconds.",
                )
            )

    return sorted(generated, key=lambda i: i.score, reverse=True)[:3]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate proactive life-admin insights.")
    parser.add_argument("--input", required=True, help="Path to JSON input file")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    insights = build_insights(payload)

    if not insights:
        print("No high-value life-admin risks found right now.")
        return

    for idx, item in enumerate(insights, start=1):
        print(f"=== Insight {idx} ===")
        print(item.render())


if __name__ == "__main__":
    main()
