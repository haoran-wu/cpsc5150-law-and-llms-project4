# Part B Divergence Scenario

Taxpayer: Maya Lopez, age 41.

Other person: Noah Lopez, age 18.

Facts:

- Noah is Maya's son.
- Noah lived with Maya for 12 months of the tax year.
- Noah is a U.S. citizen.
- Maya provided 90% of Noah's support.
- Noah provided only 5% of his own support.
- Noah married late in the year.
- Noah and his spouse filed a joint return only to claim a refund of withheld tax.

Why this scenario is useful:

- An LLM can reasonably read the refund-only joint-return fact as not disqualifying Noah from dependent status.
- The current SMT encoding treats any joint return as a hard bar at the top level, so it produces a different answer.

Planned comparison:

- Recorded LLM quick answer: dependent.
- SMT result: not a dependent because the current encoding blocks any joint return at the final dependency gate.
- Manual legal conclusion: the discrepancy most likely comes from the SMT encoding rather than from the LLM answer.
