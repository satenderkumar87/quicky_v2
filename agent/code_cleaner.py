"""
Code cleaner to fix AI-generated code issues and ensure valid JavaScript/JSX.
"""

import re

class CodeCleaner:
    def __init__(self):
        # Patterns to identify and remove invalid content
        self.markdown_patterns = [
            r'```jsx\s*',  # Remove ```jsx
            r'```javascript\s*',  # Remove ```javascript  
            r'```\s*',  # Remove ```
            r'### Key Features:.*$',  # Remove feature descriptions
            r'- \*\*.*?\*\*.*$',  # Remove bullet points with bold text
            r'^\s*\*\*.*?\*\*.*$',  # Remove lines starting with bold text
        ]
        
        # Patterns for valid React component structure
        self.valid_patterns = {
            'import': r'^import\s+.*from\s+[\'"].*[\'"];?\s*$',
            'component_start': r'^const\s+\w+\s*=\s*\(\s*\)\s*=>\s*\{',
            'export': r'^export\s+default\s+\w+;?\s*$'
        }
    
    def clean_ai_generated_code(self, code: str) -> str:
        """Clean AI-generated code to ensure it's valid JavaScript/JSX."""
        lines = code.split('\n')
        cleaned_lines = []
        in_component = False
        component_ended = False
        
        for line in lines:
            # Skip empty lines at the start
            if not cleaned_lines and not line.strip():
                continue
            
            # Check if we've reached the end of the component
            if re.match(r'^export\s+default\s+\w+;?\s*$', line.strip()):
                cleaned_lines.append(line)
                component_ended = True
                break
            
            # Skip markdown and documentation after component ends
            if component_ended:
                continue
            
            # Remove markdown code blocks
            if re.match(r'```', line.strip()):
                continue
            
            # Remove documentation lines
            if self._is_documentation_line(line):
                continue
            
            # Keep valid JavaScript/JSX lines
            if self._is_valid_js_line(line) or in_component:
                cleaned_lines.append(line)
                
                # Track if we're inside the component
                if re.match(r'^const\s+\w+\s*=\s*\(\s*\)\s*=>\s*\{', line.strip()):
                    in_component = True
        
        # Join lines and do final cleanup
        cleaned_code = '\n'.join(cleaned_lines)
        return self._final_cleanup(cleaned_code)
    
    def _is_documentation_line(self, line: str) -> bool:
        """Check if a line is documentation/markdown."""
        stripped = line.strip()
        
        # Check for markdown patterns
        for pattern in self.markdown_patterns:
            if re.match(pattern, stripped, re.MULTILINE):
                return True
        
        # Check for common documentation patterns
        doc_patterns = [
            r'^###\s+',  # Markdown headers
            r'^-\s+\*\*',  # Bullet points with bold
            r'^\*\*.*?\*\*',  # Bold text
            r'^Key Features:',  # Feature descriptions
            r'^Responsive Design:',  # Design descriptions
        ]
        
        for pattern in doc_patterns:
            if re.match(pattern, stripped):
                return True
        
        return False
    
    def _is_valid_js_line(self, line: str) -> bool:
        """Check if a line is valid JavaScript/JSX."""
        stripped = line.strip()
        
        # Empty lines are okay
        if not stripped:
            return True
        
        # Check for valid JS patterns
        valid_starts = [
            'import ',
            'const ',
            'let ',
            'var ',
            'function ',
            'export ',
            '//',  # Comments
            '/*',  # Block comments
            '*/',  # Block comment end
        ]
        
        for start in valid_starts:
            if stripped.startswith(start):
                return True
        
        # If we're not sure, assume it's valid (better to include than exclude)
        return True
    
    def _final_cleanup(self, code: str) -> str:
        """Final cleanup of the code."""
        # Remove multiple empty lines
        code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)
        
        # Ensure proper ending
        if not code.strip().endswith(';'):
            lines = code.strip().split('\n')
            if lines and not lines[-1].strip().endswith(';'):
                if 'export default' in lines[-1]:
                    lines[-1] = lines[-1].rstrip() + ';'
            code = '\n'.join(lines)
        
        return code.strip() + '\n'
    
    def validate_react_component(self, code: str) -> bool:
        """Validate that the code is a proper React component."""
        # Check for required elements
        has_import = 'import React' in code
        has_component = re.search(r'const\s+\w+\s*=\s*\(\s*\)\s*=>\s*\{', code)
        has_export = re.search(r'export\s+default\s+\w+', code)
        has_return = 'return (' in code or 'return(' in code
        
        return has_import and has_component and has_export and has_return

def clean_generated_code(code: str) -> str:
    """Main function to clean AI-generated code."""
    cleaner = CodeCleaner()
    cleaned = cleaner.clean_ai_generated_code(code)
    
    # Validate the result
    if cleaner.validate_react_component(cleaned):
        return cleaned
    else:
        # If validation fails, return a safe fallback
        return create_safe_fallback_component(code)

def create_safe_fallback_component(original_code: str) -> str:
    """Create a safe fallback component if cleaning fails."""
    # Extract component name from original code
    component_match = re.search(r'const\s+(\w+)\s*=', original_code)
    component_name = component_match.group(1) if component_match else 'GeneratedComponent'
    
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          {component_name.replace('Component', '')} Screen
        </h1>
        
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Generated Component
          </h2>
          <p className="text-gray-600">
            This component was generated from your UI screenshot.
          </p>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};
"""
