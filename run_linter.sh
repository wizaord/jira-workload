#!/bin/zsh

function runPyLint() {
  echo "Running pylint..."
  pylint ${PYLINT_FILES:-$(find src -type f -name "*.py")}
}

function runISort() {
  echo "Running isort..."
  isort src
}

function runMyPy() {
  echo "Running mypy..."
  mypy ${PYLINT_FILES:-$(find src -type f -name "*.py")}
}


function runTests() {
  echo "Running tests..."
  pytest
}


runPyLint
runMyPy
runISort
runTests
