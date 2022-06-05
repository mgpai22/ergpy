# Install local project
python -m pip install -e .

# Check package presence
python -m pip freeze | grep ergpy
