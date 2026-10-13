# Autograde tests: a worked example

These are the hidden tests for *Linear regression from scratch*. Copy this folder to start your
own. The toolkit's side of it:
[How autograding works](https://github.com/hertie-data-science-lab/dsl-teaching-toolkit/blob/main/docs/10-grade-and-return-assignments.md#autograding-optional).

## Where things live

```
solution branch (yours)                   main branch (what students get)
  grading_config.yml   autograde: true      starter.py   <- the student's code, at the root
  solution/starter.py  the model answer
  tests/               <- this folder, never handed out
```

`grading_config.yml` turns the tests on (`autograde: true`) and names this folder
(`tests: tests`). The folder exists only on the `solution` branch, so students never see it.

The student's code is `starter.py` at the root of their repo. The runner puts the submission on
`sys.path`, so a test imports it by name:

```python
from starter import fit_linear_regression, predict, r_squared, solve_linear_system
```

Tell students not to rename the file or the functions (this starter's docstring does): a missing
name is an import error, and every test fails.

## Writing a test

- **One behaviour per function, named for it.** The per-test detail lists each test by name
  with pass or fail, so `test_solve_rejects_singular` failing already says what is wrong.
- **A one-line docstring saying what it checks** - what you read when you open this file to see
  why a test failed.
- **Numbers with a tolerance:** `assert z == pytest.approx([2.0, 1.0], abs=1e-6)`, never `==`
  on floats.
- **Errors with `pytest.raises`:** `with pytest.raises(ValueError): ...` checks the student
  raises what the brief asks for.
- **Standard library and pytest only** - all you can count on the runner having. A test that
  imports numpy fails on every submission if the runner lacks it.
- **No bare file names.** Tests run from a folder outside the submission; build paths to data
  files yourself.

## How it is run and marked

1. At the late cutoff each submission is frozen at its last commit.
2. pytest runs this folder against it in a sandbox: the token stripped, resources capped, a
   5-minute limit.
3. The number passed, such as `7/10`, goes into `info.autograde` in the grading sheet and onto
   the Marks tab. Per-test detail goes to `semester-config/.system/autograde/<slug>/`.
4. The count is information for the marker. It is never a mark and students never see it; you
   enter the marks.

It runs once per assignment. To rerun after fixing a test, delete `.system/autograde/<slug>/` in
`semester-config`.

## What the ten tests show

| Group | Tests | Shows |
|---|---|---|
| `solve_linear_system` | 3 | a case you can check by hand; an edge case a naive answer misses (pivoting); the error the brief requires |
| exact recovery | 2 | noiseless data with a known answer - the clearest pass or fail |
| properties of OLS | 3 | checking what any correct answer must satisfy, not one expected output |
| `r_squared` | 2 | the boundaries (1 and 0) and the case students get wrong (negative values) |

Mix the kinds: known answers catch plain bugs; properties catch code that is right only for the
example.

## Reusing it for a new assignment

1. Copy `tests/` onto your template's `solution` branch and set `autograde: true`.
2. Change the `from starter import ...` line to your module and functions.
3. Keep the shape: shared data at the top, one section per function, one behaviour per test.
4. Check it against your model answer before the hand out, with the answer file on the path:
   `PYTHONPATH=solution python -m pytest tests` should pass every test.

## Notebooks and other languages

A submitted notebook is converted to a script first, so `analysis.ipynb` imports as `analysis`;
the completion check (`completion_check: true`) separately records whether it runs clean. For R
or anything else, put a `run.sh` here that writes JUnit XML -
[see the docs](https://github.com/hertie-data-science-lab/dsl-teaching-toolkit/blob/main/docs/10-grade-and-return-assignments.md#tests-in-another-language-testsrunsh).
