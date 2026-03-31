# Iteration 1: Direct Translation Prompt

## Goal

Produce a first-pass SMT encoding of 26 U.S.C. §152(a)-(d) using a direct, natural-language prompt.

## Prompt

Translate 26 U.S.C. §152(a)-(d) into SMT-LIB. Model a taxpayer and one candidate dependent. Include qualifying child, qualifying relative, the joint-return exception, and the nationality rule.

## Typical LLM Output Summary

- Correctly identified the top-level rule that a dependent is either a qualifying child or a qualifying relative.
- Correctly included the same-abode and age tests for a qualifying child.
- Correctly included the gross-income and support tests for a qualifying relative.
- Omitted or under-specified the tie-breaker rules in §152(c)(4).
- Did not clearly separate the joint-return rule in §152(b)(2) from the more specific qualifying-child clause in §152(c)(1)(E).

## What I Changed After Reviewing It

- Added explicit variables for competing claimants and AGI comparisons.
- Made the nationality exception a separate gate on dependency status.
- Added a dedicated support rule for the multiple-support agreement in §152(d)(3).
- Added comments and domain constraints so the file is easier to audit and compile.

## Takeaway

The direct prompt was useful for getting a scaffold quickly, but it missed edge cases and made some of the statute look flatter than it actually is.
