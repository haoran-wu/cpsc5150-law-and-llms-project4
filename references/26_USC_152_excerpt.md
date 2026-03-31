# 26 U.S.C. §152(a)-(d) Working Notes

Source used for this project:

- Official U.S. Code, Office of the Law Revision Counsel:
  https://uscode.house.gov/view.xhtml?req=%28title%3A26+section%3A152+edition%3Aprelim

This project models the following portions of the statute:

- §152(a): dependent means either a qualifying child or a qualifying relative.
- §152(b): exceptions, especially the joint-return rule and nationality/residency rule.
- §152(c): qualifying child rules: relationship, same abode for more than half the year, age, self-support, and tie-breaker logic.
- §152(d): qualifying relative rules: relationship, gross income below the exemption amount, taxpayer provides over half of support or satisfies the multiple-support rule, and the rule that the person cannot be a qualifying child of any taxpayer.

Modeling notes:

- The SMT model uses a configurable integer `exemption_amount` instead of hard-coding a tax-year-specific dollar figure.
- Support is represented as integer percentages from `0` to `100`.
- Residence is represented with months of co-residence.
- The tie-breaker rules in §152(c)(4) are represented with explicit flags for whether there is a competing claimant, whether the claimant is a parent, and comparative AGI or residency duration.
- The model is intentionally scoped to one taxpayer and one candidate dependent at a time so that each scenario can be checked independently.
