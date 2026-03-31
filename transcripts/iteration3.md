# Iteration 3: Statute-Checklist Prompt

## Goal

Force the model to walk through the statute subsection by subsection and explicitly justify each Boolean or arithmetic condition.

## Prompt

Translate 26 U.S.C. §152(a)-(d) into SMT-LIB, but do it as a checklist:

1. State the exact rule from subsection (a), then encode it.
2. State each exception from subsection (b), then encode it.
3. State each requirement in subsection (c), then encode it.
4. State each requirement in subsection (d), then encode it.
5. For every clause, name the variable or helper formula that represents it.

## Typical LLM Output Summary

- Produced the cleanest mapping between legal text and formal variables.
- Helped detect that the qualifying-relative branch must explicitly exclude anyone who is already a qualifying child of any taxpayer.
- Made it easier to explain the final model in the report because every helper function could be tied back to one subsection.

## What I Changed After Reviewing It

- Kept the naming discipline from this iteration.
- Simplified some clauses into scenario-level flags when encoding the full statute would have required a larger universe of people than the assignment needed.
- Used this iteration as the basis for the final `base_152.smt2`.

## Takeaway

This was the best method for a solo project because it produced both a workable SMT model and a report-ready explanation of why each condition exists.
