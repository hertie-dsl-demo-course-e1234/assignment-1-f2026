# Assignment 1 - linear regression from scratch (individual)

This assignment asks you to build ordinary least squares from first principles, using
nothing but the standard library, so that you understand exactly what a call to `fit()`
is doing before you rely on a modelling package for the rest of the course.

## Task

You are given a small tabular dataset and a `starter.py` with four functions to complete:
`fit_linear_regression`, `predict`, `r_squared` and `solve_linear_system`. The first three
build the familiar OLS workflow end to end; the fourth is the linear algebra underneath it,
since `fit_linear_regression` should call your own solver rather than a library routine.

Work through the normal equations by hand before you code them: write down the matrix
form, check the dimensions, and only then translate it into loops or list comprehensions.
A solver that works on a well-behaved toy example but breaks on a singular or
near-singular system is a common failure mode here, so test with more than one dataset
shape.

To get started:

- Read the starter and the docstrings before writing anything.
- Derive the normal equations on paper first.
- Implement `solve_linear_system`, then `fit_linear_regression`, then `predict` and `r_squared`.
- Test each function against a small worked example you can check by hand.
- Run the whole file top to bottom before you commit.

## What to submit

Upload your completed `starter.py` to Moodle. Nothing is collected from GitHub for this
assignment; this repository is where the starter and this brief live, not where work is
handed in.

## Grading

- Correctness of `solve_linear_system` on both well-conditioned and near-singular inputs.
- Correctness of `fit_linear_regression`, `predict` and `r_squared` against known worked examples.
- Code clarity: sensible names, no unnecessary repetition, and numerical guards where the
  docstrings ask for them.
- Whether the file runs cleanly from a fresh checkout.
