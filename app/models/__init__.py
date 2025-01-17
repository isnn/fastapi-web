import sys
import os
import importlib
from sqlmodel import SQLModel

# Add the parent directory of the models folder to the system path
models_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(models_dir, os.pardir))
if project_root not in sys.path:
    sys.path.append(project_root)

# Function to recursively import Python files from nested folders
def recursive_import(directory, parent_module="app.models"):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Build the module name dynamically
                relative_path = os.path.relpath(root, directory)
                if relative_path == ".":
                    module_name = f"{parent_module}.{file[:-3]}"
                else:
                    module_name = f"{parent_module}.{relative_path.replace(os.sep, '.')}.{file[:-3]}"
                
                # Dynamically import the module if not already imported
                if module_name not in sys.modules:
                    importlib.import_module(module_name)

recursive_import(models_dir)
# Export metadata
metadata = SQLModel.metadata 
