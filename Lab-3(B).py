```python
import random

def generate_k_sat(k, m, n):
    """
    Generate a uniform random k-SAT formula.

    Parameters:
        k (int): Clause length
        m (int): Number of clauses
        n (int): Number of variables

    Returns:
        list of list of int: The SAT formula, each clause is a list of integers.
                             Positive integer = variable
                             Negative integer = negated variable
    """
    formula = []

    for _ in range(m):
        # Select k distinct variables from 1..n
        variables = random.sample(range(1, n + 1), k)
        
        # Randomly negate each variable
        clause = [var if random.choice([True, False]) else -var for var in variables]
        formula.append(clause)

    return formula


def print_formula(formula):
    """Pretty print the k-SAT formula in CNF."""
    result = []
    for clause in formula:
        result.append("(" + " ∨ ".join([f"x{abs(lit)}" if lit > 0 else f"¬x{abs(lit)}" for lit in clause]) + ")")
    return " ∧ ".join(result)


# Example usage
if __name__ == "__main__":
    k = 3   # Clause length
    m = 5   # Number of clauses
    n = 6   # Number of variables

    formula = generate_k_sat(k, m, n)
    print("Generated Formula (internal representation):", formula)
    print("Pretty Printed Formula (CNF):")
    print(print_formula(formula))
```
