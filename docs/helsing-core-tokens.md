# Helsing Core Tokens

Helsing is not just a light palette. It is a daylight design system built around a simple idea:

> use a small number of colours with clear jobs, and let those jobs stay stable everywhere.

This document explains the **16 core tokens** that define Helsing, why they exist, and how to think with them.

## The internal logic of Helsing

Helsing aims for two things at the same time:

- **aesthetic beauty**
- **maximum usability**

Those goals often fight each other.

- A beautiful palette can become too decorative.
- A purely functional palette can become dry, harsh, or forgettable.

Helsing resolves that tension by dividing colour into two systems:

1. **neutral structure**
2. **semantic accents**

The neutrals create calm, legibility, and physicality. They make the interface feel like paper, graphite, and annotation.

The accents create meaning. They tell the reader what kind of thing they are looking at.

That is the core idea:

- **neutrals shape the page**
- **accents shape meaning**

## Why 16 tokens

Sixteen is enough to express a complete daylight system without becoming arbitrary.

It gives Helsing:

- enough neutral separation for a refined light interface
- enough accent distinction for code and UI semantics
- enough consistency to port across editors, terminals, CSS, and documentation

The 16 tokens break down into:

- **7 structural tokens**
- **9 semantic accent tokens**

## The 16 core tokens

### Structural tokens

These make Helsing feel calm, readable, and grounded.

| Token | Hex | Example | Job | Think of it as |
| --- | --- | --- | --- | --- |
| `bg` | `#F4F1EA` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#F4F1EA;vertical-align:middle;"></span> | Main background | warm paper |
| `bg_alt` | `#EAE5DC` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#EAE5DC;vertical-align:middle;"></span> | Alternate surface | panel paper, margin, current plane |
| `fg` | `#2A2A2A` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#2A2A2A;vertical-align:middle;"></span> | Primary text | soft charcoal ink |
| `muted` | `#6B6B6B` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#6B6B6B;vertical-align:middle;"></span> | Secondary text | pencil annotation |
| `subtle` | `#A8A29E` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#A8A29E;vertical-align:middle;"></span> | Low-emphasis chrome | faint layout guidance |
| `border` | `#D6D0C4` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#D6D0C4;vertical-align:middle;"></span> | Dividers and boundaries | paper fold, rule line |
| `selection` | `#E6DCC8` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#E6DCC8;vertical-align:middle;"></span> | Active emphasis surface | warm marker wash |

### Semantic accent tokens

These create meaning without shouting.

| Token | Hex | Example | Job | Think of it as |
| --- | --- | --- | --- | --- |
| `purple` | `#7C6EE6` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#7C6EE6;vertical-align:middle;"></span> | keywords, logic, declarations | disciplined intellect |
| `blue` | `#3A7BD5` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#3A7BD5;vertical-align:middle;"></span> | functions, links, action | confidence and direction |
| `green` | `#4C9A5F` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#4C9A5F;vertical-align:middle;"></span> | strings, success, safe values | natural stability |
| `orange` | `#C47A2C` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#C47A2C;vertical-align:middle;"></span> | numbers, metrics, measured emphasis | warm precision |
| `cyan` | `#2F8F8B` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#2F8F8B;vertical-align:middle;"></span> | types, structure, interfaces | technical clarity |
| `pink` | `#C05A8C` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#C05A8C;vertical-align:middle;"></span> | constants, specials, rare emphasis | deliberate ornament |
| `red` | `#C23B3B` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#C23B3B;vertical-align:middle;"></span> | errors, invalid states, danger | restrained alarm |
| `yellow` | `#B58900` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#B58900;vertical-align:middle;"></span> | warnings, caution, pending attention | thoughtful caution |
| `info` | `#4A90E2` | <span style="display:inline-block;width:1.5em;height:1.5em;border:1px solid #999;background:#4A90E2;vertical-align:middle;"></span> | hints, info, neutral notices | calm signal |

## How to read Helsing

The fastest way to understand Helsing is to stop asking, "what colour should this be?" and instead ask:

- what role does this element play?
- is it structure or meaning?
- does it need emphasis, or just clarity?

That leads to a simple decision tree.

## The decision tree

### Step 1: Is this structural or semantic?

If the thing is part of layout, surface, spacing, separation, or readability, start with a structural token.

Examples:

- editor background -> `bg`
- sidebar background -> `bg_alt`
- inactive text -> `muted`
- divider line -> `border`
- faint punctuation or gutter aid -> `subtle`

If the thing carries meaning, use an accent token.

Examples:

- keyword -> `purple`
- function name -> `blue`
- string literal -> `green`
- type -> `cyan`
- error state -> `red`

### Step 2: If structural, how strong should it be?

Helsing has four levels of structural emphasis:

- `bg` for the main field of reading
- `bg_alt` for secondary surfaces
- `border` for explicit separation
- `subtle` for guidance without visual weight

This is what keeps the theme elegant. Not every difference deserves a stronger colour.

### Step 3: If semantic, what kind of meaning is it?

Helsing accents are not interchangeable. Each one has a mental category.

- `purple` = language logic
- `blue` = callable or active
- `green` = literal and safe
- `orange` = numeric and measured
- `cyan` = type and structure
- `pink` = constant and special
- `red` = error and failure
- `yellow` = warning and caution
- `info` = hint and informational status

When those jobs stay stable, the theme becomes teachable and memorable.

## Why the structural tokens matter so much

Many themes spend too much energy on accent colours and too little on the surfaces those accents sit on.

Helsing does the opposite.

The beauty of a light theme depends more on its neutrals than its highlights.

If the neutrals are wrong:

- white feels glaring
- grey feels muddy
- borders feel dirty
- text feels brittle
- accents feel louder than intended

If the neutrals are right:

- the page feels calm
- text feels anchored
- accents feel precise
- long sessions feel sustainable

That is why Helsing has **7 structural tokens**. They are not extras. They are the foundation.

## Why the accent tokens are restrained

Helsing is not trying to be pale, but it is trying to avoid spectacle.

The accents are designed to be:

- distinct enough to scan quickly
- soft enough to live on a bright surface
- memorable enough to build pattern recognition

The rule is simple:

> colour should clarify the code, not perform over it.

## Token-by-token guidance

### `bg`

Use `bg` for the main reading field.

Good uses:

- editor canvas
- main content area
- document body

Avoid using `bg` for highlighted or active regions. It is the resting state.

### `bg_alt`

Use `bg_alt` when you need a second plane without drawing too much attention.

Good uses:

- sidebars
- floating panels
- active line surface
- code block background inside a document

`bg_alt` should feel like the same paper under slightly different light.

### `fg`

Use `fg` for the majority of readable text.

Good uses:

- body text
- identifiers
- labels that matter

`fg` should never feel as harsh as pure black. It must read clearly but remain humane.

### `muted`

Use `muted` for content that should remain legible without competing.

Good uses:

- comments
- placeholder text
- inactive labels
- line metadata

If comments disappear, `muted` is too weak. If comments dominate, `muted` is too strong.

### `subtle`

Use `subtle` for hints, scaffolding, and low-priority marks.

Good uses:

- gutter guides
- punctuation with reduced emphasis
- disabled UI details

`subtle` exists so you do not overuse `muted` or `border`.

### `border`

Use `border` only when an explicit edge or division is useful.

Good uses:

- window separators
- card borders
- popup outlines
- table rules

In Helsing, borders should guide structure, not box everything in.

### `selection`

Use `selection` for active reading emphasis on a surface.

Good uses:

- selected text background
- active item row
- current search region if no stronger token exists

It should feel warmer and more intentional than `bg_alt`, but never loud.

### `purple`

Use `purple` for logic and language control.

Good uses:

- keywords
- declarations
- control flow

Purple gives Helsing its intellectual center of gravity.

### `blue`

Use `blue` for callability, navigation, and trust.

Good uses:

- function names
- links
- primary active affordances

Blue should feel useful, not flashy.

### `green`

Use `green` for values that feel stable, literal, or affirmative.

Good uses:

- strings
- success states
- valid output

Green should feel natural and readable, especially in long quoted text.

### `orange`

Use `orange` for quantities, measurements, and warm attention.

Good uses:

- numbers
- ports
- version literals
- highlighted metrics

Orange should stand out without stealing focus from errors.

### `cyan`

Use `cyan` for types, interfaces, and structural abstractions.

Good uses:

- class or type names
- schema keys when type-like
- interface markers

Cyan is Helsing’s technical skeleton.

### `pink`

Use `pink` for constants and special tokens that deserve distinct identity.

Good uses:

- constants
- enum variants in some languages
- macros
- special builtins

Pink should be rare enough to feel intentional.

### `red`

Use `red` for broken, dangerous, or invalid states.

Good uses:

- errors
- deleted items
- invalid syntax markers
- destructive actions

Helsing red is muted on purpose. It warns without becoming aggressive.

### `yellow`

Use `yellow` for caution and unresolved attention.

Good uses:

- warnings
- deprecations
- pending tasks
- caution badges

Yellow should feel alert, not alarming.

### `info`

Use `info` for informational feedback that matters but does not imply danger.

Good uses:

- hints
- neutral status labels
- informational notices
- system guidance

`info` exists so that not every non-error state collapses into `blue`.

## Examples

### Example 1: a code snippet

```text
if retry_count > 3 then
  logger.warn("retrying connection")
end
```

Suggested Helsing reading:

- `if`, `then`, `end` -> `purple`
- `retry_count` -> `fg`
- `3` -> `orange`
- `logger.warn` -> `blue`
- `"retrying connection"` -> `green`

Why it works:

- logic is separated from values
- call sites are easy to spot
- literals read naturally

### Example 2: a UI panel

Imagine a search results pane.

- panel surface -> `bg_alt`
- title text -> `fg`
- inactive metadata -> `muted`
- thin separators -> `border`
- matched item highlight -> `selection`
- clickable result title -> `blue`
- warning badge -> `yellow`

Why it works:

- the panel is clearly distinct from the main canvas
- interaction is legible without overdecorating the interface

### Example 3: diagnostics

For status messaging:

- success -> `green`
- info -> `info`
- warning -> `yellow`
- error -> `red`

Why it works:

- each state gets its own mental lane
- the reader learns the system quickly

### Example 4: documentation styling

In prose or docs pages:

- page background -> `bg`
- callout background -> `bg_alt`
- body text -> `fg`
- aside text -> `muted`
- inline code border -> `border`
- links -> `blue`
- warning callout title -> `yellow`
- destructive note -> `red`

This shows that Helsing is not only for code. It is a general reading system.

## Rules for using the 16 tokens well

### 1. Use neutrals first

If a problem can be solved with `bg_alt`, `muted`, `subtle`, or `border`, solve it there before reaching for an accent.

### 2. Use accents for meaning, not decoration

Do not colour an element just to make the interface feel more lively. Helsing should feel composed.

### 3. Keep semantic jobs stable

If `purple` means keywords in one target, it should not become warnings in another.

### 4. Preserve visual hierarchy

The reader should feel this order:

1. content
2. structure
3. meaning
4. exceptions

### 5. Let rare colours stay rare

`pink`, `red`, and `yellow` become weaker if used everywhere.

### 6. Resist pure extremes

Do not replace Helsing neutrals with pure white or pure black. The warmth and restraint are part of the identity.

## A simple memory model

If you want to remember Helsing quickly, remember this:

- `bg` and `bg_alt` are paper
- `fg`, `muted`, and `subtle` are ink pressure
- `border` is the rule line
- `selection` is the marker wash
- `purple`, `blue`, `green`, `orange`, `cyan`, `pink` are code meaning
- `red`, `yellow`, `info` are status meaning

That is Helsing’s internal logic.

It is a theme that wants to be read for hours.

It should feel calm first, precise second, and beautiful throughout.
