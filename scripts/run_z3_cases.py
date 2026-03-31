from pathlib import Path
from z3 import Solver, is_true


def bool_value(model, name):
    for decl in model.decls():
        if decl.name() == name:
            return is_true(model[decl])
    return None


def main():
    base = Path(__file__).resolve().parent.parent
    cases = [
        "dependent_case.smt2",
        "non_dependent_case.smt2",
        "borderline_case.smt2",
        "divergence_case.smt2",
    ]
    for case in cases:
        solver = Solver()
        solver.from_file(str(base / "smt" / case))
        result = solver.check()
        print(f"=== {case} ===")
        print(f"sat_result = {result}")
        if str(result) == "sat":
            model = solver.model()
            for name in [
                "filed_joint_return",
                "joint_return_only_for_refund",
            ]:
                value = bool_value(model, name)
                if value is not None:
                    print(f"{name} = {str(value).lower()}")
        print()


if __name__ == "__main__":
    main()
