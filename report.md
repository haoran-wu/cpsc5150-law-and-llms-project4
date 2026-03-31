# Project 4 Report: Translating 26 U.S.C. §152 into SMT

## Author

Haoran Wu

## Project Summary

This project translates 26 U.S.C. §152(a)-(d) into SMT-LIB, generates scenarios about whether a person is a dependent, checks those scenarios with Z3, and analyzes a case where an LLM-style natural-language answer diverges from the SMT result.

## Files Included

- `references/26_USC_152_excerpt.md`
- `transcripts/iteration1.md`
- `transcripts/iteration2.md`
- `transcripts/iteration3.md`
- `smt/base_152.smt2`
- `smt/dependent_case.smt2`
- `smt/non_dependent_case.smt2`
- `smt/borderline_case.smt2`
- `smt/divergence_case.smt2`
- `scenarios/dependent.md`
- `scenarios/non_dependent.md`
- `scenarios/borderline.md`
- `part_b/divergence_case.md`
- `solver_outputs/dependent_case.txt`
- `solver_outputs/non_dependent_case.txt`
- `solver_outputs/borderline_case.txt`
- `solver_outputs/divergence_case.txt`

## Part 1: Legal Text to SMT Translation

### Modeling Strategy

I modeled one taxpayer and one candidate dependent at a time. This keeps each scenario small enough to debug while still preserving the structure of the statute. The final SMT file separates the statute into helper formulas that correspond to the major legal concepts:

- `qualifying_child`
- `qualifying_relative`
- `nationality_ok`
- `dependent`
- `can_candidate_claim_dependents`

The model includes:

- the top-level definition in §152(a)
- the joint-return and nationality exceptions in §152(b)
- relationship, residence, age, self-support, and tie-breaker logic for qualifying children in §152(c)
- relationship, gross-income, support, and multiple-support logic for qualifying relatives in §152(d)

### Iterative Development Process

I used three prompt styles while developing the model:

- a direct translation prompt
- a structured intermediate representation prompt
- a statute-checklist prompt

The most reliable method was the checklist prompt because it forced an explicit mapping from each statutory clause to a variable or helper function. The direct prompt was fast, but it tended to miss edge cases. The structured prompt improved the rule separation and made the later report easier to write.

### Important Modeling Choices

- I represented support as percentages rather than raw dollars.
- I represented residence using months of co-residence.
- I treated the exemption amount in §152(d)(1)(B) as a configurable constant, `exemption_amount`.
- I modeled the tie-breaker rules in §152(c)(4) with flags for competing claimants and comparative AGI.

### Correctness Discussion

The final model captures the main structure of the statute and is accepted by Z3. It is strongest on scenario-level classification for a single candidate dependent. It is less detailed than a full tax engine because it abstracts away from a larger family network and from year-specific tax parameters unless they are explicitly supplied in a scenario.

## Part 2: Scenario Generation

### Scenario A: Dependent

The first scenario uses a straightforward qualifying-child case: a 17-year-old son who lived with the taxpayer all year, did not file a joint return, and did not support himself. This scenario should clearly classify as a dependent.

### Scenario B: Non-Dependent

The second scenario uses a 26-year-old sister who did not live with the taxpayer for more than half the year, earned income above the exemption threshold used in the model, and did not receive over half of her support from the taxpayer. This scenario should classify as not a dependent.

### Scenario C: Borderline

The third scenario uses a 23-year-old niece who is a full-time student, lived with the taxpayer for seven months, and provided 49% of her own support. The scenario is borderline because the key facts sit close to the statutory cutoffs, but the model should still classify her as a dependent.

## Part 3: Compliance Verification with Z3

The scenario-specific SMT files were run through Z3. The solver outputs are saved in the `solver_outputs/` directory. The expected classification pattern is:

- dependent case: `dependent = true`
- non-dependent case: `dependent = false`
- borderline case: `dependent = true`

### Discussion of Solver Output

The solver outputs confirm that the model behaves consistently with the intended structure of §152 for these examples. The dependent scenario and the borderline scenario both satisfy the qualifying-child branch. The non-dependent scenario satisfies neither the qualifying-child nor the qualifying-relative branch. The main value of the solver is that it turns an informal legal question into a traceable Boolean result grounded in explicit facts. It also makes debugging easier: if a scenario gives an unexpected answer, the error usually comes from one missing fact or one incorrectly encoded statutory condition.

## Part 4: Refinement Process

The refinement process focused on four issues:

- making the qualifying-child and qualifying-relative branches mutually coherent
- separating the joint-return exception from the basic qualifying-child branch
- adding a clearer model for multiple-support agreements
- making the tie-breaker rules explicit enough to discuss in the report

The final version is more faithful to the statutory text than the first pass because each helper function has a direct legal motivation. The iterative prompt records in `transcripts/` document how the model improved over time.

## Part B: Divergence Between LLM and SMT

### Divergence Scenario

The Part B scenario involves an 18-year-old son who lives with and is mostly supported by his mother, which strongly suggests dependency at first glance. However, he also filed a joint return with his spouse.

### LLM Answer

A quick natural-language answer is likely to say that the son is a dependent because the family relationship, residence, and support facts are all favorable.

### Chain-of-Thought Style LLM Reasoning

A step-by-step LLM explanation for this scenario would likely look something like this:

1. Noah is Maya's son, so the relationship requirement looks satisfied.
2. Noah lived with Maya for the full year, so the residence requirement looks satisfied.
3. Maya provided most of Noah's support, so the support requirement looks satisfied.
4. Noah is 18, so he appears to fit the age-related intuition for dependency.
5. Therefore, Noah is a dependent.

This reasoning is plausible but incomplete because it can stop once it sees the familiar family-support pattern.

### SMT Answer

The SMT model returns that he is not a dependent because §152(b)(2) contains a joint-return exception that blocks dependency. In the current encoding, the person still satisfies the qualifying-relative branch, but the final `dependent` predicate remains false because the joint-return exception is applied as a hard gate on dependency status.

### Manual Legal Assessment

The SMT result is legally stronger under the statutory text. Section 152(b)(2) directly states that an individual who made a joint return with a spouse is not treated as a dependent under subsection (a). That statutory exception overrides the otherwise favorable child, residence, and support facts.

### Why the Reasoning Diverges

The divergence appears at the final screening stage. The LLM reasoning above focuses on the positive dependency indicators and may implicitly assume that satisfying the qualifying-child pattern is enough. The SMT model does not stop there. It computes the positive branch, then applies the exceptions in §152(b), especially the joint-return exception.

In other words, the two methods diverge here:

- LLM-style reasoning: relationship + residence + support + age are sufficient.
- SMT reasoning: those facts are not sufficient until the statutory exceptions are checked.

The discrepancy therefore comes primarily from the LLM's interpretation of the statute rather than from the scenario specification. The SMT encoding is doing exactly what it was designed to do: enforce the exception as a mandatory Boolean gate.

## Conclusion

This project shows that SMT is a useful way to formalize statutory dependency rules in a way that is testable and auditable. The LLM was valuable during development for producing candidate encodings and explanations, but the solver provided the final consistency check.
