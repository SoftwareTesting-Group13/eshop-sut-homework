---
name: ai-audit-logger
description: Create or update a faithful AI Audit Report from accessible conversation records. Use after an AI-assisted work session or while logging interactions for an assignment that requires tool name, time, prompt, and AI output.
---

# AI audit logger

Produce a chronological, verifiable record of AI assistance. This skill is for documenting an existing session, not reconstructing one from memory. Work from the current conversation, an exported transcript, or other records the user provides. A skill cannot run automatically after every session or read chats and AI tools outside the available context; state that limit when it affects completeness.

## Homework fields

HW02 §9 makes four fields mandatory for every interaction: the AI tool's name, the date and time, your prompt, and the AI output. The course AI templates (e.g. `[AI-02]`) are optional — the homework says "if needed" — so treat extra template columns such as a verdict, ISTQB rationale, or corrected student version as additions, not replacements. The homework governs; a general template never overrides the four required fields.

## Required report content

- If no AI was used, record the exact declaration: **“I do not use any AI help in this exercise.”** Do this only when the user confirms that no AI tool was used; do not infer it from an empty transcript.
- If AI was used, begin with the exact declaration: **“I use AI tools for the following tasks,”** followed by the tasks for which AI was used.
- For **each interaction**, include the AI tool's name, date and time, the user's prompt, and the AI output. An interaction is one submitted prompt and its corresponding AI response; record follow-up prompts and revised outputs as separate interactions. Keep the order in which they happened.

## Capture procedure

1. Identify the reporting scope and available evidence: current chat, exported transcript, tool history, or user-supplied records. List the AI tools actually evidenced; do not assume the current assistant is the only tool used.
2. Extract the exact user-authored prompt and corresponding user-visible AI output for each interaction. Preserve wording, code, tables, and meaningful formatting. Do not replace long outputs with a summary. Exclude hidden system/developer instructions, private reasoning, and intermediate tool messages unless they were themselves submitted as a user prompt or shown as the AI's answer.
3. Copy timestamps from source records and include their timezone or offset when known. Convert timezones only if the source timestamp supports it, and label the conversion. Never use the report-generation time as an interaction time. If the source lacks a timestamp, write **“Time not available in source”** rather than inventing one.
4. Label each entry with a stable ID and, when possible, its source transcript, link, or file. For non-text output, identify the artifact and attach or link a copy that can be inspected. If a prompt or output is unavailable, mark the field missing and say what evidence is needed; do not paraphrase it as though it were verbatim.
5. Write or update the Markdown appendix at the user-specified location. For this HW02 student layout, the default is `homework/hw02/<student-short-name>/reports/ai-audit.md`. Preserve existing entries, merge new records in chronological order, and deduplicate only when the same source interaction is already logged.
6. Compare the finished entries with the accessible source. Report the number logged, source range, missing fields, and any tools or sessions that were mentioned but could not be inspected. Ask for exports only when they are needed to complete the requested scope.

## Markdown structure

```md
# AI Audit Report

I use AI tools for the following tasks,

- [Task performed with AI]

## Interaction AI-001

- AI tool: [name, and model/version if known]
- Date and time: [source timestamp and timezone, or “Time not available in source”]
- Source: [conversation/export reference, if available]
- Task: [brief purpose]

### Your prompt

[Exact prompt]

### The AI output

[Exact user-visible output, or an attached non-text artifact]
```

A blank copy of this outline is provided at `assets/ai-audit-report-template.md`; it also carries the optional `[AI-02]` five-column table (`Prompt + Công cụ · Output AI · Verdict · Lý do · Bản SV sửa`) as an addition, never a replacement for the four mandatory fields.

For the no-AI case, use only the no-AI declaration and a note that the user confirmed it; do not create empty interaction entries. Keep optional task labels and source references separate from the four mandatory fields.

## Integrity checks

- Every accessible prompt has its matching output and vice versa; follow-ups are not collapsed into a single invented exchange.
- Tool names and times are sourced, and unknown details are marked unknown. Redactions, if requested, are labeled with what was removed; do not silently alter quoted content.
- The report describes what AI actually produced. Human corrections and final submitted work may be linked separately, but do not substitute them for the original AI output.
