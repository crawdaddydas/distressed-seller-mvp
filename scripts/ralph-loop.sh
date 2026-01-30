#!/bin/bash
# Ralph Wiggum Loop for Distressed Seller MVP
# Usage: ./ralph-loop.sh "Your task prompt"

set -e

TASK="$1"
COMPLETION_Promise="<promise>COMPLETE</promise>"
MAX_ITERATIONS=50
ITERATION=1

if [ -z "$TASK" ]; then
    echo "Usage: ./ralph-loop.sh \"Your task prompt\""
    exit 1
fi

echo "=============================================="
echo "Ralph Wiggum Loop Started"
echo "Task: $TASK"
echo "Completion: $COMPLETION_Promise"
echo "Max Iterations: $MAX_ITERATIONS"
echo "=============================================="

while true; do
    echo ""
    echo "=============================================="
    echo "Iteration $ITERATION / $MAX_ITERATIONS"
    echo "=============================================="
    
    # Show what files exist
    echo "Current files:"
    find . -name "*.py" -type f | head -20
    
    echo ""
    echo "Running tests..."
    python -m pytest tests/ -v --tb=short 2>&1 | head -100 || true
    
    echo ""
    echo "Check for completion..."
    
    # In Claude Code, you would run:
    # /ralph-loop "Your task" --completion-promise "<promise>COMPLETE</promise>"
    # 
    # This creates a self-referential loop where Claude:
    # 1. Works on the task
    # 2. Runs tests
    # 3. If tests fail, fix code
    # 4. Repeat until tests pass
    # 5. Output <promise>COMPLETE</promise> when done
    
    echo "=============================================="
    echo "Ralph Wiggum loop complete!"
    echo "In Claude Code, run:"
    echo "/ralph-loop \"$TASK\" --completion-promise \"$COMPLETION_Promise\""
    echo "=============================================="
    
    break
done