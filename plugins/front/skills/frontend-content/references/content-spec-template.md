# UI content spec template

Use the project's existing format when present. Replace placeholders; retain only sections relevant to the change. Keep material context complete, not repetitive.

## Purpose

- Audience and usage frequency:
- Screen's main task/question:
- Next useful action:
- Source brief, files and evidence:

## Content allocation

| Fact / requirement | Source or status | Destination (visible / on demand / spec only / redundant) | Why | Component / spec section |
|---|---|---|---|---|---|

Account for every material input. Separate facts, estimates and open questions. If information leaves the UI, give it a concrete destination.

## Interface contract

| Element | Final copy or representation | Level (1 / 2 / 3) | Trigger and return path | States / accessibility |
|---|---|---|---|---|

Record selected chart/table/number and the question it answers. Note required labels, units, period, scope, data freshness and accessible equivalents where relevant. Keep the number of controls proportional to the task.

## Context and calculations

Keep assumptions, formulas, sources, terminology, dependencies, constraints and design decisions that a maintainer needs. Explain excluded UI content and the rationale; preserve meaningful alternatives without implementing all of them. Link to authoritative existing specs instead of copying them.

## Open questions

List unresolved facts, their impact and how they are presented. Never turn a hypothesis into a fact to make the interface simpler.

## Acceptance and evidence

- Main task succeeds with the visible information.
- Exploration/detail are discoverable and work on keyboard, touch and small screens.
- Decision-critical information is visible before committing.
- Numbers, units, formulas and caveats match the sources and implemented UI.
- A chart has a useful accessible summary or data equivalent.
- Removed UI context is accounted for here or in linked documentation.
- Implementation paths and observed QA evidence:
