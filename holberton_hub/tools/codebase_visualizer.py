#!/usr/bin/env python3
"""
Codebase Visualizer - Create a diagram of file relationships
"""

import os
import ast
import re
import sys
from pathlib import Path
import importlib.util

# Check if graphviz is installed
graphviz_available = importlib.util.find_spec("graphviz") is not None
if graphviz_available:
    try:
        import graphviz
    except ImportError:
        graphviz_available = False

class CodebaseVisualizer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.relationships = {}
        self.modules = set()

        if graphviz_available:
            self.graph = graphviz.Digraph('Codebase Structure',
                                         comment='Holberton Hub Codebase',
                                         format='png')
            self.graph.attr(rankdir='LR', size='12,8', ratio='fill')
            self.graph.attr('node', shape='box', style='filled', fillcolor='lightblue')

    def parse_python_file(self, file_path):
        """Extract imports from a Python file"""
        rel_path = file_path.relative_to(self.root_dir)
        module_path = str(rel_path).replace('/', '.').replace('.py', '')

        with open(file_path, 'r') as file:
            try:
                content = file.read()
                tree = ast.parse(content)

                # Add this module to our known modules
                self.modules.add(module_path)

                # Find imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            if module_path not in self.relationships:
                                self.relationships[module_path] = set()
                            self.relationships[module_path].add(name.name)

                    elif isinstance(node, ast.ImportFrom):
                        if node.module is not None:
                            if module_path not in self.relationships:
                                self.relationships[module_path] = set()
                            self.relationships[module_path].add(node.module)

                # Look for class definitions to track inheritance
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for base in node.bases:
                            if isinstance(base, ast.Name):
                                # This is a simplified approach and might need refinement
                                pass  # Inheritance is complex to track without full context

            except Exception as e:
                print(f"Error parsing {file_path}: {e}")

    def scan_directory(self):
        """Scan the directory structure for Python files"""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(os.path.join(root, file))
                    self.parse_python_file(file_path)

    def simplify_relationships(self):
        """Clean up relationships to focus on project modules"""
        project_prefix = self.root_dir.name
        simplified = {}

        for source, targets in self.relationships.items():
            if source not in simplified:
                simplified[source] = set()

            for target in targets:
                # Only include project-specific modules or direct imports from project
                if any(m for m in self.modules if target.startswith(m.split('.')[0])):
                    simplified[source].add(target)

        return simplified

    def generate_graph(self):
        """Create the graph visualization"""
        simplified = self.simplify_relationships()

        if not graphviz_available:
            return None

        # Add nodes for all modules
        for module in self.modules:
            short_name = module.split('.')[-1]
            self.graph.node(module, label=short_name, tooltip=module)

        # Add edges for relationships
        for source, targets in simplified.items():
            for target in targets:
                if target in self.modules:
                    self.graph.edge(source, target)

        return self.graph

    def generate_text_representation(self):
        """Generate a text-based representation of the code structure"""
        simplified = self.simplify_relationships()
        result = []

        result.append("Codebase Structure - Module Relationships")
        result.append("=" * 50)

        # Sort modules for consistent output
        sorted_modules = sorted(list(self.modules))

        for module in sorted_modules:
            result.append(f"\n{module}")
            result.append("-" * len(module))

            if module in simplified and simplified[module]:
                result.append("Imports:")
                for target in sorted(simplified[module]):
                    if target in self.modules:
                        result.append(f"  → {target}")
            else:
                result.append("No internal dependencies")

        return "\n".join(result)

    def visualize(self, output_file='codebase_diagram'):
        """Generate and save the visualization"""
        self.scan_directory()

        # Always generate text representation
        text_output = self.generate_text_representation()
        text_output_file = f"{output_file}.txt"

        with open(text_output_file, 'w') as f:
            f.write(text_output)

        print(f"Text representation saved to {text_output_file}")

        # Try to generate graphical representation
        if graphviz_available:
            graph = self.generate_graph()
            try:
                graph.render(output_file, cleanup=True)
                print(f"Diagram generated as {output_file}.png")
            except Exception as e:
                print("\nError generating graphical diagram:")
                print(f"  {str(e)}")
                print("\nTo fix this issue, install the Graphviz system package:")
                print("  Ubuntu/Debian: sudo apt-get install graphviz")
                print("  Fedora/RHEL:  sudo dnf install graphviz")
                print("  macOS:        brew install graphviz")
                print("\nThe text representation is still available in the .txt file.")
        else:
            print("\nGraphviz Python package not found.")
            print("To generate graphical diagrams, install the required packages:")
            print("  pip install graphviz")
            print("  sudo apt-get install graphviz  # Or equivalent for your system")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = '/home/scorpio/holberton-hub/holberton_hub'

    visualizer = CodebaseVisualizer(root_directory)
    visualizer.visualize()
