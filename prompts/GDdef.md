# Graph Document Definition

## Basic structure

- A graph document (GD) is a set of nodes and typed links.
- Each node contains a single sentence or phrase.
- Each link has exactly one relation type.
- Relation types are either **asymmetric (directed)** or **symmetric**.

**Asymmetric relations:**

- An asymmetric link connects exactly one sourceNode to exactly one targetNode.
- The meanings below always specify the meaning of:

  `sourceNode → [Relation] → targetNode`

**Symmetric relations:**

- A symmetric link does not have a sourceNode/targetNode distinction. Instead, it connects a **set of two or more sourceNodes**, all of which stand in the same relation to one another.
- A symmetric link has **no targetNode**.
- This allows a symmetric relation to naturally express more than two mutually related nodes (e.g., "A, B, and C are all in [Contrast] with one another") without forcing an arbitrary source/target split.

Nodes should express propositions, entities, events, states, actions, or other meaningful units.

**Do not encode the meaning of a relation into a node merely to express the relation.**

For example, do not use a node such as:

> "Even if it rains"

when the intended relation is `[Compromise]`.

Instead, use relation-neutral nodes such as:

```
sourceNode: "It rains."
relation: [Compromise]
targetNode: "I will go."
```

The relation itself should express the meaning of `[Compromise]`.

---

## Relation types

### Relation: [Equal]
**Symmetric:** Yes

**Definition:**
All sourceNodes are equal. Sometimes one node is a summary or a detail of another.

**Illustration:**
```
relation: [Equal]
sourceNodes:
  - "Barack Hussein Obama II"
  - "the 44th president of the USA"
```

**Japanese illustration:**
```
relation: [Equal]
sourceNodes:
  - "バラク・フセイン・オバマ2世"
  - "アメリカ合衆国第44代大統領"
```

---

### Relation: [Part]
**Symmetric:** No

**Definition:**
sourceNode is the whole, and targetNode is a part or component of it.

**Direction:** whole → [Part] → component

**Illustration:**
```
sourceNode: "a car"
relation: [Part]
targetNode: "the engine"
```

**Japanese illustration:**
```
sourceNode: "自動車"
relation: [Part]
targetNode: "エンジン"
```

---

### Relation: [Member]
**Symmetric:** No

**Definition:**
sourceNode is a set, and targetNode is an element of the set.

**Direction:** set → [Member] → element

**Illustration:**
```
sourceNode: "small countries"
relation: [Member]
targetNode: "Monaco"
```

**Japanese illustration:**
```
sourceNode: "小国"
relation: [Member]
targetNode: "モナコ"
```

---

### Relation: [Example]
**Symmetric:** No

**Definition:**
targetNode is an example of sourceNode.

**Direction:** general concept → [Example] → example

**Illustration:**
```
sourceNode: "small countries"
relation: [Example]
targetNode: "Monaco"
```

**Japanese illustration:**
```
sourceNode: "小国"
relation: [Example]
targetNode: "モナコ"
```

**Note:**
- `[Member]` means that targetNode belongs to a set represented by sourceNode.
- `[Example]` means that targetNode illustrates or exemplifies a concept represented by sourceNode.
- The same pair of nodes may sometimes support either relation depending on how sourceNode is interpreted.

---

### Relation: [Addition]
**Symmetric:** No

**Definition:**
targetNode is also true in relation to sourceNode.

**Direction:** statement → [Addition] → additional statement

**Illustration:**
```
sourceNode: "Tom was tired."
relation: [Addition]
targetNode: "He was also feverish."
```

**Japanese illustration:**
```
sourceNode: "トムは疲れていた。"
relation: [Addition]
targetNode: "彼は熱もあった。"
```

---

### Relation: [Specific]
**Symmetric:** No

**Definition:**
targetNode is a concretization of sourceNode.

**Direction:** general statement → [Specific] → more concrete statement

**Illustration:**
```
sourceNode: "My mother works at a hospital."
relation: [Specific]
targetNode: "She is a nurse."
```

**Japanese illustration:**
```
sourceNode: "私の母は病院で働いている。"
relation: [Specific]
targetNode: "母は看護師である。"
```

---

### Relation: [Content]
**Symmetric:** No

**Definition:**
sourceNode is thinking, speaking, believing, or the one who thinks, speaks, or believes, or a document or data representing thought, speech, or belief.
targetNode is the content of that thought, speech, belief, document, or data.

**Direction:**
thinker, speaker, believer, thought, speech, belief, document, or data → [Content] → content of the thought, speech, belief, document, or data

**Illustration:**
```
sourceNode: "René Descartes"
relation: [Content]
targetNode: "Cogito, ergo sum."
```

**Japanese illustration:**
```
sourceNode: "ルネ・デカルト"
relation: [Content]
targetNode: "我思う、ゆえに我あり。"
```

**Illustration:**
```
sourceNode: "I think"
relation: [Content]
targetNode: "She is wrong."
```

**Japanese illustration:**
```
sourceNode: "私は考えている。"
relation: [Content]
targetNode: "彼女は間違っている。"
```

**Illustration:**
```
sourceNode: "He believes"
relation: [Content]
targetNode: "The earth revolves around the sun."
```

**Japanese illustration:**
```
sourceNode: "彼は信じている。"
relation: [Content]
targetNode: "地球は太陽の周りを回っている。"
```

**Illustration:**
```
sourceNode: "a desire"
relation: [Content]
targetNode: "to get married."
```

**Japanese illustration:**
```
sourceNode: "願望"
relation: [Content]
targetNode: "結婚する"
```

**Illustration:**
```
sourceNode: "Tom:"
relation: [Content]
targetNode: "That's great!"
```

**Japanese illustration:**
```
sourceNode: "トムの発言"
relation: [Content]
targetNode: "それは素晴らしい！"
```

**Note:**
`[Content]` may connect a person, document, data, thought, speech, belief, desire, or other representation of mental or communicative content to the content represented, thought, spoken, believed, or intended.

The sourceNode does not need to contain an explicit expression such as "think," "say," or "believe." For example:

> "René Descartes" → [Content] → "Cogito, ergo sum."

is valid because the relation represents the content of a thought or proposition associated with René Descartes.

---

### Relation: [Contrast]
**Symmetric:** Yes

**Definition:**
All sourceNodes are in contrast with one another but do not conflict. Their co-occurrence is neither unlikely nor undesirable. They cannot naturally be connected using "even though" or "despite."

**Illustration:**
```
relation: [Contrast]
sourceNodes:
  - "The price is high."
  - "The quality is good."
```

**Japanese illustration:**
```
relation: [Contrast]
sourceNodes:
  - "価格が高い。"
  - "品質が良い。"
```

---

### Relation: [Disjunction]
**Symmetric:** Yes

**Definition:**
At least one of the sourceNodes exists, occurs, or is true.

**Illustration:**
```
relation: [Disjunction]
sourceNodes:
  - "Publish."
  - "Perish."
```

**Japanese illustration:**
```
relation: [Disjunction]
sourceNodes:
  - "論文を発表する。"
  - "研究を中止する。"
```

---

### Relation: [Dissimilar]
**Symmetric:** Yes

**Definition:**
All sourceNodes are dissimilar to one another.

**Illustration:**
```
relation: [Dissimilar]
sourceNodes:
  - "Tom is rich."
  - "Sue is rich."
```

**Japanese illustration:**
```
relation: [Dissimilar]
sourceNodes:
  - "トムは裕福である。"
  - "スーは裕福である。"
```

---

### Relation: [Causes]
**Symmetric:** No

**Definition:**
sourceNode is a cause, and targetNode is a result.

**Direction:** cause → [Causes] → result

**Illustration:**
```
sourceNode: "Heavy rainfall continued for several days."
relation: [Causes]
targetNode: "The river overflowed."
```

**Japanese illustration:**
```
sourceNode: "数日間にわたって大雨が続いた。"
relation: [Causes]
targetNode: "川が氾濫した。"
```

---

### Relation: [Conclusion]
**Symmetric:** No

**Definition:**
targetNode is inferred from sourceNode. In other words: targetNode because sourceNode.

**Direction:** evidence or premise → [Conclusion] → inferred conclusion

**Illustration:**
```
sourceNode: "People are putting up umbrellas."
relation: [Conclusion]
targetNode: "It's raining."
```

**Japanese illustration:**
```
sourceNode: "人々が傘をさしている。"
relation: [Conclusion]
targetNode: "雨が降っている。"
```

**Distinction from [Causes]:**
- `[Causes]`: sourceNode itself explains why targetNode occurred.
- `[Conclusion]`: sourceNode provides evidence or a premise from which targetNode is inferred.

---

### Relation: [Triggers]
**Symmetric:** No

**Definition:**
targetNode arises or becomes known due to sourceNode. sourceNode contains no information about the cause or reason for targetNode.

**Direction:** event or observation → [Triggers] → subsequent event or awareness

**Illustration:**
```
sourceNode: "We tasted the food."
relation: [Triggers]
targetNode: "We found that it was quite delicious."
```

**Japanese illustration:**
```
sourceNode: "私たちは料理を味わった。"
relation: [Triggers]
targetNode: "私たちはそれがとてもおいしいと分かった。"
```

**Distinction from [Causes]:**
Use `[Causes]` when sourceNode is a cause of targetNode. Use `[Triggers]` when sourceNode triggers the occurrence or discovery of targetNode without itself explaining why targetNode is true.

**Distinction from [Conclusion]:**
Use `[Conclusion]` when targetNode is inferred from sourceNode. Use `[Triggers]` when sourceNode triggers an event or discovery but does not provide the logical basis for an inference.

---

### Relation: [Purpose]
**Symmetric:** No

**Definition:**
sourceNode is the means or method. targetNode is the purpose of that means or method. The purpose may already have been achieved.

**Direction:** means → [Purpose] → purpose

**Illustration:**
```
sourceNode: "Tom studied hard."
relation: [Purpose]
targetNode: "Tom passed the exam."
```

**Japanese illustration:**
```
sourceNode: "トムは一生懸命勉強した。"
relation: [Purpose]
targetNode: "トムは試験に合格した。"
```

**Illustration:**
```
sourceNode: "The experiment compares models with and without resampling."
relation: [Purpose]
targetNode: "Determine whether resampling improves prediction performance."
```

**Japanese illustration:**
```
sourceNode: "リサンプリングありとなしのモデルを比較する実験を行う。"
relation: [Purpose]
targetNode: "リサンプリングが予測性能を改善するかどうかを明らかにする。"
```

**Incorrect direction:**
```
sourceNode: "Determine whether resampling improves prediction performance."
relation: [Purpose]
targetNode: "The experiment compares models with and without resampling."
```

**Japanese incorrect direction:**
```
sourceNode: "リサンプリングが予測性能を改善するかどうかを明らかにする。"
relation: [Purpose]
targetNode: "リサンプリングありとなしのモデルを比較する実験を行う。"
```

---

### Relation: [Conditional]
**Symmetric:** No

**Definition:**
If sourceNode, then targetNode. It is uncertain whether sourceNode and targetNode are true.

**Direction:** condition → [Conditional] → consequence

**Illustration:**
```
sourceNode: "Tom comes here."
relation: [Conditional]
targetNode: "He will be surprised."
```

**Japanese illustration:**
```
sourceNode: "トムがここに来る。"
relation: [Conditional]
targetNode: "トムは驚くだろう。"
```

---

### Relation: [Foreground]
**Symmetric:** No

**Definition:**
sourceNode provides a background explanation of targetNode, or provides a context in which to understand targetNode. The relationship is not a cause or reason.

**Direction:** background or context → [Foreground] → statement understood in that context

**Illustration:**
```
sourceNode: "John commutes to Manhattan."
relation: [Foreground]
targetNode: "Today he stopped off at Crestwood."
```

**Japanese illustration:**
```
sourceNode: "ジョンはマンハッタンに通勤している。"
relation: [Foreground]
targetNode: "今日はクレストウッドに立ち寄った。"
```

**Distinction from [Causes]:**
`[Foreground]` provides context for understanding targetNode. `[Causes]` explains why targetNode occurred or is true.

**Note: Definitions and explanations of terms**
When a node defines or explains a term used in node A, that definition/explanation node should point to A using `[Foreground]`. The definition provides background context that helps the reader understand A, making it the sourceNode with A as the targetNode.

**Illustration:**
```
sourceNode: "Apoptosis is a form of programmed cell death in which a cell actively triggers its own destruction."
relation: [Foreground]
targetNode: "Apoptosis is essential for normal development and tissue homeostasis."
```

**Japanese illustration:**
```
sourceNode: "アポトーシスとは、細胞が自らの死を能動的に引き起こすプログラムされた細胞死の一形態である。"
relation: [Foreground]
targetNode: "アポトーシスは正常な発生と組織の恒常性に不可欠である。"
```

---

### Relation: [Conflict]
**Symmetric:** Yes

**Definition:**
All sourceNodes are not very compatible with one another. Their co-occurrence is unlikely or undesirable.

**Illustration:**
```
relation: [Conflict]
sourceNodes:
  - "Tom studied hard."
  - "He failed the exam."
```

**Japanese illustration:**
```
relation: [Conflict]
sourceNodes:
  - "トムは一生懸命勉強した"
  - "トムは試験に落ちた"
```

**Distinction from [Contrast]:**
`[Contrast]` expresses a difference or opposition without incompatibility. `[Conflict]` expresses incompatibility, unexpected co-occurrence, or an undesirable combination.

---

### Relation: [Unconditional]
**Symmetric:** No

**Definition:**
Regardless of sourceNode, targetNode is true. Use `[Compromise]` instead if sourceNode makes targetNode unlikely or difficult to be true.

**Direction:** regardless of X → [Unconditional] → Y

**Illustration:**
```
sourceNode: "It rains."
relation: [Unconditional]
targetNode: "I'll go."
```
Natural-language interpretation: "I'll go whether or not it rains."

**Japanese illustration:**
```
sourceNode: "雨が降る"
relation: [Unconditional]
targetNode: "私は出かける
```
Natural-language interpretation: 「雨が降るかどうかにかかわらず、私は出かける。」

---

### Relation: [Compromise]
**Symmetric:** No

**Definition:**
Even if sourceNode, targetNode is still true. Use `[Compromise]` when sourceNode makes targetNode unlikely or difficult to occur or be true.

**Direction:** obstacle or difficulty → [Compromise] → outcome

**Illustration:**
```
sourceNode: "It rains."
relation: [Compromise]
targetNode: "I'll go."
```
Natural-language interpretation: "I'll go even if it rains."

**Japanese illustration:**
```
sourceNode: "雨が降る"
relation: [Compromise]
targetNode: "私は出かける"
```
Natural-language interpretation: 「雨が降っていても、私は出かける。」

**Distinction from [Unconditional]:**
`[Unconditional]` means that targetNode is true regardless of sourceNode. `[Compromise]` means that sourceNode makes targetNode difficult or unlikely, but targetNode is nevertheless true. The node itself must not contain the relation expression "even if" or "regardless of."

---

### Relation: [Response]
**Symmetric:** No

**Definition:**
targetNode is a response to sourceNode.

**Direction:** question, request, or action → [Response] → response

**Illustration:**
```
sourceNode: "Is this the right way to go?"
relation: [Response]
targetNode: "Probably not."
```

**Japanese illustration:**
```
sourceNode: "こちらの道で正しいですか。"
relation: [Response]
targetNode: "たぶん違います。"
```

---

### Relation: [Approval]
**Symmetric:** No

**Definition:**
targetNode is an affirmative response to sourceNode.

**Direction:** proposal, question, request, or statement → [Approval] → affirmative response

**Illustration:**
```
sourceNode: "Do you know this?"
relation: [Approval]
targetNode: "Sure."
```

**Japanese illustration:**
```
sourceNode: "これを知っていますか。"
relation: [Approval]
targetNode: "はい、知っています。"
```

---

### Relation: [Disapproval]
**Symmetric:** No

**Definition:**
targetNode is a negative response to sourceNode.

**Direction:** proposal, request, or statement → [Disapproval] → negative response

**Illustration:**
```
sourceNode: "Give me some money."
relation: [Disapproval]
targetNode: "I'm too poor."
```

**Japanese illustration:**
```
sourceNode: "お金をください。"
relation: [Disapproval]
targetNode: "私にはお金がありません。"
```

**Distinction from [Response]:**
`[Response]` is a general response. `[Approval]` is specifically an affirmative response. `[Disapproval]` is specifically a negative response.

---

### Relation: [Solution]
**Symmetric:** No

**Definition:**
sourceNode is a problem. targetNode is a proposed solution.

**Direction:** problem → [Solution] → proposed solution

**Illustration:**
```
sourceNode: "We might be caught in a traffic jam."
relation: [Solution]
targetNode: "Let's go around downtown."
```

**Japanese illustration:**
```
sourceNode: "交通渋滞に巻き込まれるかもしれない。"
relation: [Solution]
targetNode: "都心を迂回して行こう。"
```

**Distinction from [Purpose]:**
`[Purpose]`: sourceNode is a means and targetNode is its purpose. `[Solution]`: sourceNode is a problem and targetNode is a proposed solution.

---

### Relation: [Before]
**Symmetric:** No

**Definition:**
targetNode temporally follows sourceNode.

**Direction:** earlier event → [Before] → later event

**Illustration:**
```
sourceNode: "I arrived."
relation: [Before]
targetNode: "You came."
```

**Japanese illustration:**
```
sourceNode: "私が到着した。"
relation: [Before]
targetNode: "あなたが来た。"
```

---

### Relation: [Sametime]
**Symmetric:** Yes

**Definition:**
All sourceNodes are true simultaneously.

**Illustration:**
```
relation: [Sametime]
sourceNodes:
  - "Tom finished eating."
  - "Mary arrived."
```

**Japanese illustration:**
```
relation: [Sametime]
sourceNodes:
  - "トムが食事を終えた。"
  - "メアリーが到着した。"
```

---

### Relation: [Situation]
**Symmetric:** No

**Definition:**
targetNode is the time, place, or situation in which sourceNode exists, occurs, or is true.

**Direction:** event, entity, or statement → [Situation] → time, place, or situation

**Illustration:**
```
sourceNode: "the earthquake"
relation: [Situation]
targetNode: "2011"
```

**Japanese illustration:**
```
sourceNode: "地震"
relation: [Situation]
targetNode: "2011年"
```

**Illustration:**
```
sourceNode: "my house"
relation: [Situation]
targetNode: "Tokyo"
```

**Japanese illustration:**
```
sourceNode: "私の家"
relation: [Situation]
targetNode: "東京"
```

---

### Relation: [Object]
**Symmetric:** No

**Definition:**
sourceNode is a predication or represents a state, action, or operation. targetNode is the object, target, or entity involved in that predication, state, action, or operation.

**Direction:** predication, state, or action → [Object] → object or target

**Illustration:**
```
sourceNode: "find"
relation: [Object]
targetNode: "him"
```

**Japanese illustration:**
```
sourceNode: "探す"
relation: [Object]
targetNode: "彼"
```

---

### Relation: [Uncertain]
**Symmetric:** Yes

**Definition:**
The relationship among the sourceNodes is unclear.

**Illustration:**
```
relation: [Uncertain]
sourceNodes:
  - "The observed change"
  - "The preceding event"
```

**Japanese illustration:**
```
relation: [Uncertain]
sourceNodes:
  - "観察された変化"
  - "その前に起きた出来事"
```

---

## Symmetric relations

The following relations are symmetric:

- [Equal]
- [Contrast]
- [Disjunction]
- [Dissimilar]
- [Conflict]
- [Sametime]
- [Uncertain]

A symmetric relation link has **no sourceNode/targetNode distinction** and **no targetNode**. It instead holds a `sourceNodes` list containing two or more nodes, all of which stand in the same relation to one another. The order of nodes in `sourceNodes` carries no meaning:

```
relation: [Relation]
sourceNodes:
  - A
  - B
```

is equivalent to:

```
relation: [Relation]
sourceNodes:
  - B
  - A
```

All other (asymmetric) relations use exactly one `sourceNode` and exactly one `targetNode`, and are directed.

---

## Relation selection rule

- Use a relation only when the meaning of the relation precisely applies to the sourceNode and targetNode.
- Do not select the nearest or approximately similar relation.
- Do not reverse a relation merely to connect two nodes.
- Do not encode the meaning of a relation into a node to make the relation easier to express.

For example, do not include expressions such as:

- "even if"
- "regardless of"
- "because"
- "if"

in a node merely to represent `[Compromise]`, `[Unconditional]`, `[Conclusion]`, or `[Conditional]`. Instead, express the relevant propositions independently in the nodes and express the relationship using the relation type.

If no existing relation precisely represents the relationship:

- Do not create a link, or
- Introduce an intermediate node that makes an existing relation applicable.

The meaning of every relation must always be interpreted according to the definitions, directions, distinctions, and illustrations above.
