# Ralph Wiggum Loop - Fix Distressed Seller Scorer

## Mission
Fix `src/scorer.py` until ALL tests in `tests/test_scorer.py` pass.

## Success Criteria
```
python -m pytest tests/test_scorer.py -v
# Result: ALL TESTS PASS
```

## The Loop
1. Run tests: `python -m pytest tests/test_scorer.py -v`
2. If tests FAIL:
   - Read the error messages
   - Fix the scorer.py code
   - Run tests again
3. If tests PASS:
   - Output: `<promise>COMPLETE</promise>`
   - Stop

## Current Test Results
Run tests to see current status.

## Rules
- Fix the ACTUAL bug, don't change tests
- If tests fail, debug and fix code
- Don't output anything except your progress and completion promise
- Keep iterating until all tests pass

## Command to Start Loop
In Claude Code:
```
/ralph-loop "Fix scorer.py until all tests pass. Output <promise>COMPLETE</promise> when done." --max-iterations 20
```