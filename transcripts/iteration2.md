# Iteration 2: Structured Intermediate Representation

## Goal

Reduce ambiguity by first extracting the statute into structured rule buckets and then translating those buckets into SMT.

## Prompt

Read 26 U.S.C. §152(a)-(d) and produce a JSON-style intermediate representation with:

- rule name
- required facts
- disqualifiers
- numeric thresholds
- interactions with other rules

Then convert that intermediate representation into SMT-LIB.

## Typical LLM Output Summary

- Produced cleaner rule separation than iteration 1.
- Identified the qualifying-child and qualifying-relative branches more clearly.
- Explicitly surfaced thresholds such as more than half-year residence and support.
- Still struggled with how to encode the handicapped-dependent income exclusion and the tie-breaker logic compactly.

## What I Changed After Reviewing It

- Introduced a `countable_gross_income` helper term so sheltered-workshop income can be excluded when the statutory conditions hold.
- Collapsed the multiple-support agreement into a Boolean formula rather than a procedural explanation.
- Added scenario-friendly variables such as `months_same_abode`, `taxpayer_support_percent`, and `joint_return_only_for_refund`.

## Takeaway

The structured intermediate step produced a much better model skeleton and made it easier to justify the final encoding in the report.
