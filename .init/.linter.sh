#!/bin/bash
cd /home/kavia/workspace/code-generation/support-ticket-manager-e2db4e87/ticket_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

