# Text-to-Graph-Document Conversion Procedure

This prompt defines how to convert a given input text into a Graph Document (GD).

It assumes the companion document **"Graph Document Definition"** (node/link structure, the full list of relation types, and the relation selection rule) is provided together with this prompt. This document does not redefine relation types; it defines the **conversion procedure, output schema, granularity rules, and verification steps**.

---

## 1. Node granularity (segmentation)

- Each node must express exactly one proposition, entity, event, state, or action.
- A compound or complex sentence must be split into multiple nodes connected by an appropriate relation, rather than kept as a single node.

  Example: "It rained, so the river overflowed." must become two nodes connected by `[Causes]`, not a single node containing the whole sentence.

- Do not split a sentence into fragments smaller than a full proposition merely to create more links. A node must stand on its own as a meaningful statement even outside the graph.
- Do not merge two distinct propositions into a single node merely because they appear in the same sentence.
- As established in the companion document, do not encode a relation's meaning into a node's wording (e.g., "even if," "because," "if") merely to make it easier to attach a relation. Split the proposition and let the relation type carry that meaning instead.

---

## 2. Extraction vs. inference boundary

- Nodes must be extracted from content explicitly present in the input text. Do not invent facts, entities, or propositions that are not stated or strictly and necessarily entailed by the text.
- An intermediate node (per the companion document's relation selection rule) may only be introduced when:
  1. It is strictly entailed by the surrounding text (not merely plausible or likely), and
  2. It introduces no new factual content beyond what is already stated or logically necessary to connect two existing nodes with an existing relation type.
- If you are not sure whether a relation applies, prefer `[Uncertain]` or omit the link entirely, rather than guessing.
- Node text should preserve the original wording as closely as possible (extractive), only lightly normalized for grammatical completeness (e.g., resolving an omitted subject). Do not paraphrase into different vocabulary or add interpretive framing.

---

## 3. Conversion steps

Perform the conversion in this order:

1. **Segment**: Read the input text and identify candidate propositions according to the granularity rules in Section 1. Assign each a unique node id.
2. **Resolve coreference**: If the same entity or proposition is referred to multiple times with different surface forms (e.g., a pronoun, a repeated paraphrase), decide whether to represent it as a single reused node, or as separate nodes connected by `[Equal]`. Prefer a single reused node when the surface forms are trivially co-referential (pronouns); prefer `[Equal]` when both forms carry independent informational value (e.g., a name and a description).
3. **Propose candidate links**: For each pair of nodes with a plausible textual or logical connection (adjacency in the text, discourse markers, shared entities, causal or temporal cues, etc.), propose a candidate relation.
4. **Select relation type**: Apply the relation selection rule from the companion document — choose the relation type only when its definition precisely applies. Do not choose the nearest approximate type. Discard candidate links with no precise match.
5. **Enforce structural constraints**: For each accepted link, apply the correct structure — exactly one sourceNode and one targetNode for asymmetric relations, or a `sourceNodes` list of two or more for symmetric relations (no targetNode). See the companion document.
6. **Self-verify**: Run the checklist in Section 5 before finalizing output.
7. **Emit output**: Produce the result in the schema defined in Section 4.

---

## 4. Output schema

Emit the result as a single JSON object with this shape:

```json
{
  "nodes": [
    { "id": "n1", "text": "..." },
    { "id": "n2", "text": "..." }
  ],
  "links": [
    { "relation": "Causes", "source": "n1", "target": "n2" },
    { "relation": "Contrast", "sourceNodes": ["n3", "n4", "n5"] }
  ]
}
```

Rules:

- Every node referenced in `links` must have a corresponding entry in `nodes`.
- An asymmetric relation link uses `source` and `target` (each a single node id). It must not include `sourceNodes`.
- A symmetric relation link uses `sourceNodes` (an array of two or more node ids, order not meaningful). It must not include `source` or `target`.
- A node with no links is allowed (an isolated node is valid output, not an error).
- Do not include any text, explanation, or commentary outside the JSON object.

---

## 5. Self-verification checklist

Before emitting output, check every link against this list. Discard or fix any link that fails:

- [ ] Does the chosen relation's definition (from the companion document) precisely match this pair, not merely approximately?
- [ ] For an asymmetric relation, is the direction correct (which node is source, which is target)?
- [ ] Does either node's text contain a relation-indicating expression ("even if," "because," "if," "although," etc.) that duplicates the meaning already carried by the relation type itself? If so, rewrite the node to remove it.
- [ ] Is this relation confusable with a similar one (e.g., `[Causes]` vs. `[Conclusion]` vs. `[Triggers]`; `[Contrast]` vs. `[Conflict]`; `[Unconditional]` vs. `[Compromise]`; `[Purpose]` vs. `[Solution]`; `[Member]` vs. `[Example]`)? If so, re-check the distinction described in the companion document.
- [ ] Is every node's text extractive (traceable to the input text) rather than invented?
- [ ] Does any node link to itself? If so, remove the link.
- [ ] Are there duplicate nodes (same proposition, different id) that should be merged?

---

## 6. Additional rules

- A self-loop (a node linked to itself) is never valid.
- Two nodes may be connected by more than one relation only when each relation independently and precisely applies (e.g., the same pair may be simultaneously in `[Before]` and `[Causes]`). Do not add a second relation merely to hedge between two plausible interpretations — pick the one that precisely applies, or omit the link.
- Do not force every node to participate in at least one link. A sparse graph that omits weak or approximate connections is preferred over a dense graph with imprecise links.
- When the input text is long, process it in its entirety before emitting output; do not truncate or summarize away nodes to shorten the result.
