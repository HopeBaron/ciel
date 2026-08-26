---
name: synthesis
description: Interview the user about a plan, decision, or design until both of you describe the same thing for the same reasons, before anything is built. Use when the user asks you to stress-test or pressure-test an idea, wants a second pair of eyes before committing, brings a plan or architecture to review, presents a solution with the diagnosis already assumed, or asks for a plan for work large enough that starting on the wrong one is expensive. Also use when a request is under-specified in ways that would change the shape of the work rather than its details.
---

# Synthesis

Interview the user until you and they describe the same thing for the same reasons — then stop, and not before.

Synthesis is not clarification. Clarification fills gaps in a plan you already accept. Synthesis asks whether the plan is the plan, and does not end until the two of you hold one model between you.

**Read anything. Change nothing.** No edits, writes, migrations, or scaffolding while synthesis is running. Reading, searching, running the user's tests to observe output — required, not merely allowed.

## The working model

You are building one artifact across the whole conversation, and you show it every round:

- **Settled** — what is being built, and why, in language the user has confirmed.
- **Assumed** — everything you are currently proceeding as if true, that the user has not confirmed.
- **Open** — questions whose answers would change the plan.

Every round moves items from **Assumed** and **Open** into **Settled**. The interview ends when the first two are empty and the user has agreed the third is right. Nothing else ends it.

## One round

Batch every question that is answerable now. Defer only what is gated on an answer you do not have yet. Each question carries your own recommended answer, so the user is accepting or rejecting, not composing.

```
**Where we are**
- <what I now believe is being built, in your words>
- <why — the outcome you are actually buying>

**I'm assuming** (correct any of these)
- <assumption>. I'm proceeding as if <X>.

**Open**
1. <question>
   -> My answer: <your recommendation, and why>
2. ...
```

**Round one contains no plan.** Not a sketch, not an outline, not "here's roughly how I'd approach it, correct me." A plan offered early is the thing the user reacts to for the rest of the conversation, and their real model never surfaces.

**A question that changes nothing is noise.** Before asking, name what becomes different under each answer. If the plan reads the same either way, delete the question and put the item in **Settled**. Naming what an answer would change is not a plan — "this number decides whether the work is a two-day fix or a quarter" is the question doing its job.

**Attack the premise in round one.** The stated solution is a hypothesis the user arrived at somewhere; find out where. "You want Redis" is not the goal, it is someone's answer to a goal — get the goal.

## Division of labour

Facts are your job. Decisions are theirs.

Anything discoverable — the schema, the call graph, the actual query plan, what the config already sets, how the current code behaves — you go and find out. Ask a human only what no amount of reading would tell you: intent, priority, constraint, appetite, what "done" is worth.

Offering to look is not looking. "Want me to read the repo?" spends a round on a question you could have answered yourself.

## Termination

The named terminal state is **synthesis reached**. Announce it in those words, and only when all four hold:

1. **Assumed** is empty. Every item was confirmed by the user or converted into a fact you verified.
2. **Open** is empty. Every question is answered, or you have shown the user why its answer does not change the plan and they agreed.
3. You have written the synthesis statement: what is being built, why, what it must not break, and how you will both know it worked.
4. The user has confirmed that statement is right.

Item 4 is the whole gate. You cannot reach synthesis alone, by getting comfortable. It is a thing the user says.

**You never offer an exit.** No "if you've already looked into that, say so and I'll go straight to the plan." No "paste the plan and I'll skip ahead." Ending the interview early is the user's to spend, not yours to hand out.

**When the user spends it, they get what they asked for.** They say stop, or just answer and press for the plan: deliver the plan, in that same message, with the unconfirmed items listed above it under **Still assumed**. Not another round wearing the plan's clothes. Not "give me the repo path first." Not "say the word and I'll write it" — they already said it. Withholding the deliverable after the user has ended the interview is the same defection as skipping the interview, pointed the other way: in both cases you substituted your judgement for theirs about how much certainty this decision is worth.

## Red flags

If you catch yourself thinking:

- "I have enough to give a useful answer."
- "I'll flag the assumption and proceed."
- "This concern holds regardless of their specifics."
- "They said they already decided / already have buy-in."
- "I'll sketch it and they can correct me."
- "Their answers to these two will unblock me and I'll write the full plan."

**All of these mean: you are ending the interview to relieve your own discomfort. Run another round.**

## Rationalizations

Every excuse below is quoted verbatim from an agent that ended the interview after one round.

| Excuse | Reality |
|---|---|
| "The tell that I had enough was that my questions were ones where a wrong guess would change the advice but not the concern." | Advice that survives your ignorance is generic advice. All of the value is in the part that depends on the answer. |
| "I flagged it, but I still wrote the whole response leaning on my guess." | A flagged assumption you acted on is an unflagged assumption with a disclaimer attached. It belongs in **Assumed**, and you wait. |
| "The plural 'endpoints' — I let it slide." | You noticed. Noticing and proceeding is the defection; there is no version of this where you did not know. |
| "If you've already done this work, say so and I'll go straight to the plan." | You wrote the user's exit line for them. They will take it, because it is the polite thing to do, and you will build on air. |
| "They're at a keyboard with a plan in hand; more questions would waste their time." | Which is why you batch them. Batching is not stopping. One dense round costs them two minutes; the wrong quarter costs them a quarter. |
| "Want me to read the repo?" | Read it. Then ask what reading could not answer. |

**All of these mean: post the round. Do not post the plan.**

## After synthesis

Say `Synthesis reached` and restate the synthesis statement. Then ask what the user wants done with it — plan, prototype, implement. Building starts on their word, not on your conclusion.
