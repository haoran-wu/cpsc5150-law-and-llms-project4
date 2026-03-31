# Development Prompt Records

This folder is included to satisfy the assignment requirement that the submission contain either AI conversation transcripts or scripts used to develop the submission.

The project was developed with the following exact prompt styles:

## Prompt Set 1: Direct Translation

Translate 26 U.S.C. §152(a)-(d) into SMT-LIB. Model a taxpayer and one candidate dependent. Include qualifying child, qualifying relative, the joint-return exception, and the nationality rule.

## Prompt Set 2: Structured Intermediate Representation

Read 26 U.S.C. §152(a)-(d) and produce a JSON-style intermediate representation with:

- rule name
- required facts
- disqualifiers
- numeric thresholds
- interactions with other rules

Then convert that intermediate representation into SMT-LIB.

## Prompt Set 3: Statute Checklist

Translate 26 U.S.C. §152(a)-(d) into SMT-LIB, but do it as a checklist:

1. State the rule from subsection (a), then encode it.
2. State each exception from subsection (b), then encode it.
3. State each requirement in subsection (c), then encode it.
4. State each requirement in subsection (d), then encode it.
5. For every clause, name the variable or helper formula that represents it.

## Verification Script

The Python script `run_z3_cases.py` was used to re-run the SMT cases during development and confirm that the `.smt2` files remained solver-compatible after revisions.
