# SKILL.md — quality-scorer

## What it does
Evaluates any output (text, article, code, decision) on a 0-100 scale before publishing/sending, checking clarity, hallucination risk, style adherence, and completeness.

## When to use
- Before sending important messages, emails, or social posts
- Before publishing articles, website content, or documents
- After generating code, summaries, or reports
- When user asks "score this", "is this ready to send", or "review this quality"

## When NOT to use
- For trivial one-liner responses
- When output is clearly草稿 and will be heavily edited anyway
- For real-time conversational responses (too slow)

## Inputs
- The output to evaluate (text, article, code, decision)
- Optional: brand/format guidelines, tone expectations

## Outputs
- Overall score (0-100)
- Breakdown by dimension: Clarity, Hallucination Risk, Style Adherence, Completeness
- One-line improvement suggestion

## Scoring Dimensions

| Dimension | What it checks | Weight |
|-----------|---------------|--------|
| **Clarity** | Is it clear and jargon-free? Can a non-expert understand it? | 25% |
| **Hallucination Risk** | Are facts verifiable? Are claims supported? | 30% |
| **Style Adherence** | Does it match brand/format/voice guidelines? | 20% |
| **Completeness** | Is anything critical missing? | 25% |

## Cost / Risk notes
No external calls. Read-only evaluation of provided text.
