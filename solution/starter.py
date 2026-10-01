"""Assignment 1 - linear regression from scratch.

Standard library only: no numpy, no pandas, no scikit-learn.

Fill in the four functions below. Keep the names and signatures exactly as they are - the
grading tests import them by name. See README.md for what is assessed.

Your two short answers go at the bottom of this file.
"""


def solve_linear_system(A, b):
    """Solve `A z = b` by Gaussian elimination with partial pivoting.

    Args:
        A: an n x n matrix, as a list of n rows (each a list of n floats).
        b: the right-hand side, a list of n floats.

    Returns:
        The solution vector `z`, a list of n floats.

    Raises:
        ValueError: if `A` is singular (no unique solution exists).

    Hint: work on a copy of the augmented matrix. For each column, find the row with the
    largest absolute value in that column (the pivot), swap it up, then eliminate the
    entries below it. Finish with back-substitution.
    """
    ### BEGIN SOLUTION
    n = len(A)
    # Work on a copy of the augmented matrix so the caller's data is untouched.
    M = [list(map(float, row)) + [float(rhs)] for row, rhs in zip(A, b)]

    for col in range(n):
        # Partial pivoting: the largest available |value| in this column becomes the pivot.
        # Without it, a small pivot divides the whole row and amplifies rounding error.
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-12:
            raise ValueError("matrix is singular - no unique solution")
        M[col], M[pivot] = M[pivot], M[col]

        for row in range(col + 1, n):
            factor = M[row][col] / M[col][col]
            if factor == 0.0:
                continue
            for k in range(col, n + 1):
                M[row][k] -= factor * M[col][k]

    # Back-substitution.
    z = [0.0] * n
    for row in reversed(range(n)):
        total = M[row][n] - sum(M[row][k] * z[k] for k in range(row + 1, n))
        z[row] = total / M[row][row]
    return z
    ### END SOLUTION


def fit_linear_regression(X, y):
    """Fit ordinary least squares, returning coefficients with the intercept FIRST.

    Args:
        X: a list of n rows, each a list of p feature values. No column of ones - this
           function adds the intercept itself.
        y: a list of n outcome values.

    Returns:
        A list of p + 1 coefficients: [intercept, b_1, ..., b_p].

    Build the normal equations X'X b = X'y (with the intercept column prepended to X) and
    hand them to `solve_linear_system`. Do NOT invert X'X.
    """
    ### BEGIN SOLUTION
    if not X or len(X) != len(y):
        raise ValueError("X and y must be non-empty and of equal length")

    design = [
        [1.0] + [float(v) for v in row] for row in X
    ]  # prepend the intercept column
    p = len(design[0])

    # X'X and X'y, accumulated directly - no inversion anywhere.
    xtx = [[sum(row[i] * row[j] for row in design) for j in range(p)] for i in range(p)]
    xty = [sum(row[i] * yi for row, yi in zip(design, y)) for i in range(p)]
    return solve_linear_system(xtx, xty)
    ### END SOLUTION


def predict(X, beta):
    """Fitted values for each row of `X`.

    Args:
        X: a list of n rows, each a list of p feature values (again, no column of ones).
        beta: a list of p + 1 coefficients as returned by `fit_linear_regression`.

    Returns:
        A list of n predictions.
    """
    ### BEGIN SOLUTION
    return [beta[0] + sum(b * v for b, v in zip(beta[1:], row)) for row in X]
    ### END SOLUTION


def r_squared(y_true, y_pred):
    """Coefficient of determination, 1 - RSS/TSS.

    Args:
        y_true: the observed outcomes.
        y_pred: the predicted outcomes, same length.

    Returns:
        A float. 1.0 for a perfect fit, 0.0 for predicting the mean of `y_true`, and
        negative for predictions worse than that mean.
    """
    ### BEGIN SOLUTION
    mean_y = sum(y_true) / len(y_true)
    rss = sum((a - p) ** 2 for a, p in zip(y_true, y_pred))
    tss = sum((a - mean_y) ** 2 for a in y_true)
    if tss == 0.0:
        raise ValueError("y_true has zero variance - R-squared is undefined")
    return 1.0 - rss / tss
    ### END SOLUTION


if __name__ == "__main__":
    # A place to try things out. Nothing here is graded, and nothing here runs on import.
    X = [[32], [45], [52], [60], [68], [75], [80], [95]]
    y = [540, 510, 640, 545, 720, 620, 770, 860]
    beta = fit_linear_regression(X, y)
    print("coefficients:", beta)
    print("R-squared:", r_squared(y, predict(X, beta)))


# ----------------------------------------------------------------------------------
# SHORT ANSWERS (3-5 sentences each - see README.md)
#
# 1. Why does partial pivoting matter numerically, and what goes wrong without it?
#
### BEGIN SOLUTION
#    Partial pivoting swaps the row with the largest absolute value in the current column
#    into the pivot position before eliminating. Elimination divides by the pivot, so a
#    pivot that is small relative to the other entries multiplies existing rounding error
#    by a large factor, and that error then propagates through every subsequent row and
#    through back-substitution. Without pivoting the algorithm also fails outright on a
#    perfectly solvable system whose leading entry happens to be exactly zero - the
#    division is by zero even though a unique solution exists. Pivoting costs one scan per
#    column and bounds the growth factor, which is why every production solver does it.
### END SOLUTION
#
# 2. Your fit fails on a design matrix containing both `area_in_sqm` and `area_in_sqft`.
#    Explain why in terms of X'X, and say what you would do about it.
#
### BEGIN SOLUTION
#    `area_in_sqft` is an exact multiple of `area_in_sqm`, so one column of the design
#    matrix is a linear combination of another and X has linearly dependent columns. Then
#    X'X is singular: its determinant is zero, no inverse exists, and infinitely many
#    coefficient vectors give exactly the same fitted values, so the estimator is not
#    identified. Numerically the elimination hits a pivot at machine-epsilon scale and
#    either raises or returns wild coefficients that are meaningless individually. The fix
#    is to drop one of the two columns - they carry identical information - or, if the
#    collinearity is approximate rather than exact, to regularise (ridge adds lambda*I to
#    X'X, which restores invertibility) and to report that the individual coefficients are
#    not separately interpretable.
### END SOLUTION
# ----------------------------------------------------------------------------------
