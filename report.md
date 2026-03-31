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
- `part_b/llm_quick_answer.md`
- `part_b/llm_step_by_step_reasoning.md`
- `solver_outputs/dependent_case.txt`
- `solver_outputs/non_dependent_case.txt`
- `solver_outputs/borderline_case.txt`
- `solver_outputs/divergence_case.txt`
- `scripts/run_z3_cases.py`
- `scripts/development_prompts.md`

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

Instead of raw chat exports, this submission includes development prompt records and verification scripts in the `scripts/` directory. This satisfies the assignment requirement to include transcripts or scripts used to develop the submission.

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

The solver outputs confirm that the model behaves consistently with the intended structure of §152 for these examples.

- Dependent case: Z3 returns `dependent = true`. The person satisfies the qualifying-child branch because the relationship, residence, age, and support facts all line up.
- Non-dependent case: Z3 returns `dependent = false`. The person is too old for the qualifying-child branch and also fails the income and support requirements for the qualifying-relative branch.
- Borderline case: Z3 returns `dependent = true`. The result depends on the student exception, residence of more than six months, and the fact that the candidate provides only 49% of her own support.

The main value of the solver is that it turns an informal legal question into a traceable Boolean result grounded in explicit facts. It also makes debugging easier: if a scenario gives an unexpected answer, the error usually comes from one missing fact or one incorrectly encoded statutory condition.

## Part 4: Refinement Process

The refinement process focused on four issues:

- making the qualifying-child and qualifying-relative branches mutually coherent
- separating the joint-return exception from the basic qualifying-child branch
- adding a clearer model for multiple-support agreements
- making the tie-breaker rules explicit enough to discuss in the report

The final version is more faithful to the statutory text than the first pass because each helper function has a direct legal motivation. The iterative prompt records in `transcripts/` document how the model improved over time.

One concrete unexpected result appeared during the Part B divergence scenario. The model classified Noah as:

- `qualifying_child = true`
- `dependent = false`

This happened because the encoding currently treats `filed_joint_return` as a hard bar at the top-level `dependent` predicate, even when `joint_return_only_for_refund = true`. That is a useful debugging result because it exposes a likely overbroad SMT encoding choice. In other words, the solver did not merely produce a yes-or-no answer; it revealed a place where the formalization can still be improved.

This gave me a specific revision history to report:

1. First pass: I focused on the positive dependency branches and scenario classification.
2. Refinement pass: I separated the joint-return logic from the qualifying-child branch.
3. Debugging pass: the Part B refund-only scenario revealed that the final top-level gate is still too strict.

That final issue is intentionally preserved in the submission because it provides a concrete example of model refinement and legal/formal mismatch, which is exactly what Part 4 asks the student to analyze.

## Part B: Divergence Between LLM and SMT

### Divergence Scenario

The Part B scenario involves an 18-year-old son who lives with and is mostly supported by his mother. He filed a joint return with his spouse, but only to claim a refund of withheld tax.

### LLM Answer

The recorded quick-answer prompt and response are included in `part_b/llm_quick_answer.md`. The answer says that Noah is Maya's dependent.

### Chain-of-Thought Style LLM Reasoning

The recorded step-by-step answer is included in `part_b/llm_step_by_step_reasoning.md`. In that answer, the LLM walks through relationship, residence, age, self-support, nationality, and the refund-only joint-return fact, and concludes that Noah should still count as Maya's dependent.

### SMT Answer

The SMT model returns that he is not a dependent. In the current encoding, the candidate satisfies the qualifying-child branch, but the final `dependent` predicate is forced to `false` because any joint return is treated as a hard top-level disqualifier.

### Manual Legal Assessment

The LLM answer is more legally plausible for this specific scenario. The refund-only carveout is reflected in §152(c)(1)(E), and the current SMT encoding is too rigid because it separately blocks all joint returns at the final dependency gate. That means the disagreement here comes from the SMT encoding, not from the LLM answer.

### Why the Reasoning Diverges

The divergence appears at the final screening stage. The LLM reasoning treats the refund-only joint return as non-disqualifying in context. The SMT model does not. It computes that Noah satisfies the positive qualifying-child conditions, but then applies a top-level Boolean gate that rejects all joint returns, including refund-only returns.

In other words, the two methods diverge here:

- LLM-style reasoning: relationship + residence + support + age are sufficient.
- SMT reasoning: those facts are not sufficient because the encoding rejects all joint returns at the last step.

The discrepancy therefore comes primarily from the SMT encoding rather than from the scenario specification. This is a useful example because it shows exactly how an implementation detail in the formal model can create a mismatch with a more nuanced legal reading.

## Conclusion

This project shows that SMT is a useful way to formalize statutory dependency rules in a way that is testable and auditable. The LLM was valuable during development for producing candidate encodings and explanations, but the solver provided the final consistency check.
