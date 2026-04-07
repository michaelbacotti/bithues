# SKILL.md — dashboard-builder

## What it does
Creates interactive web dashboards for Bacotti family enterprises using Python (Streamlit, Dash) or JavaScript (React, Chart.js).

## When to use
- User asks to build, create, or generate a dashboard
- KPI tracker or metrics visualization needed
- Data visualization for business or family entities

## When NOT to use
- For live data fetching from external APIs (dashboard would need manual refresh)
- For static reports (use business-manager or entity reports instead)
- For real-time trading dashboards (market data limitations)

## Inputs
- Data sources: CSV files, entity info markdown, family JSON
- Framework preference (Streamlit default, Dash/React for complexity)

## Outputs
- Python/JS dashboard code
- Run commands for local viewing

## Cost / Risk notes
No external calls. Writes code to workspace. Requires python3, node, npm for some frameworks.
