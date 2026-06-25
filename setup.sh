#!/usr/bin/bash
# Create main source folders
mkdir -p src/core src/services src/components src/utils
mkdir -p .streamlit
mkdir -p tests/unit tests/integration

# Create empty __init__.py files to make packages
touch src/__init__.py
touch src/core/__init__.py
touch src/services/__init__.py
touch src/components/__init__.py
touch src/utils/__init__.py