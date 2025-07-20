"""
Code validator to ensure generated React components are error-free and build-ready.
"""

import re
import subprocess
import tempfile
import os
from typing import Dict, List, Tuple, Optional

class CodeValidator:
    def __init__(self):
        self.common_errors = [
            # JSX syntax errors
            r'```\w*',  # Markdown code blocks
            r'### \w+',  # Markdown headers
            r'- \*\*.*?\*\*',  # Markdown bullet points
            r'^\s*\*\*.*?\*\*.*$',  # Bold text lines
        ]
        
        self.required_patterns = [
            r'import React from [\'"]react[\'"];?',
            r'const \w+Component = \(\) => \{',
            r'export default \w+Component;?'
        ]
    
    def validate_react_component(self, code: str, component_name: str) -> Dict[str, any]:
        """Comprehensive validation of React component code."""
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'cleaned_code': code
        }
        
        # 1. Check for markdown artifacts
        markdown_issues = self._check_markdown_artifacts(code)
        if markdown_issues:
            result['errors'].extend(markdown_issues)
            result['valid'] = False
        
        # 2. Check required React patterns
        missing_patterns = self._check_required_patterns(code)
        if missing_patterns:
            result['errors'].extend(missing_patterns)
            result['valid'] = False
        
        # 3. Check JSX syntax
        jsx_errors = self._check_jsx_syntax(code)
        if jsx_errors:
            result['errors'].extend(jsx_errors)
            result['valid'] = False
        
        # 4. Check for common template literal issues
        template_errors = self._check_template_literals(code)
        if template_errors:
            result['errors'].extend(template_errors)
            result['valid'] = False
        
        # 5. If there are errors, try to clean the code
        if not result['valid']:
            cleaned = self._attempt_cleanup(code, component_name)
            if cleaned != code:
                result['cleaned_code'] = cleaned
                # Re-validate cleaned code
                cleaned_result = self.validate_react_component(cleaned, component_name)
                if cleaned_result['valid']:
                    result['valid'] = True
                    result['errors'] = []
                    result['warnings'].append("Code was automatically cleaned")
        
        return result
    
    def _check_markdown_artifacts(self, code: str) -> List[str]:
        """Check for markdown artifacts in the code."""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for markdown code blocks
            if re.match(r'^\s*```', line):
                errors.append(f"Line {i}: Markdown code block found: {line.strip()}")
            
            # Check for markdown headers
            if re.match(r'^\s*#{1,6}\s+', line):
                errors.append(f"Line {i}: Markdown header found: {line.strip()}")
            
            # Check for markdown bullet points
            if re.match(r'^\s*[-*]\s+\*\*.*?\*\*', line):
                errors.append(f"Line {i}: Markdown bullet point found: {line.strip()}")
        
        return errors
    
    def _check_required_patterns(self, code: str) -> List[str]:
        """Check for required React component patterns."""
        errors = []
        
        # Check for React import
        if not re.search(r'import React from [\'"]react[\'"];?', code):
            errors.append("Missing React import statement")
        
        # Check for component declaration
        if not re.search(r'const \w+Component = \(\) => \{', code):
            errors.append("Missing functional component declaration")
        
        # Check for export statement
        if not re.search(r'export default \w+Component;?', code):
            errors.append("Missing export default statement")
        
        # Check for return statement
        if not re.search(r'return \(', code):
            errors.append("Missing return statement in component")
        
        return errors
    
    def _check_jsx_syntax(self, code: str) -> List[str]:
        """Check for common JSX syntax errors."""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for unescaped template literals in JSX
            if re.search(r'className=\{`[^`]*\$\{[^}]*\}[^`]*`\}', line):
                errors.append(f"Line {i}: Complex template literal in className may cause issues")
            
            # Check for unmatched braces
            open_braces = line.count('{')
            close_braces = line.count('}')
            if abs(open_braces - close_braces) > 2:  # Allow some flexibility
                errors.append(f"Line {i}: Potentially unmatched braces")
            
            # Check for invalid JSX attributes
            if re.search(r'\w+=[\'"][^\'\"]*\$\{', line):
                errors.append(f"Line {i}: Template literal in string attribute")
        
        return errors
    
    def _check_template_literals(self, code: str) -> List[str]:
        """Check for problematic template literal usage."""
        errors = []
        
        # Find complex template literals that might cause issues
        complex_templates = re.findall(r'`[^`]*\$\{[^}]*\?[^}]*:[^}]*\}[^`]*`', code)
        if complex_templates:
            errors.append(f"Found {len(complex_templates)} complex template literals that may cause parsing issues")
        
        return errors
    
    def _attempt_cleanup(self, code: str, component_name: str) -> str:
        """Attempt to clean up problematic code."""
        lines = code.split('\n')
        cleaned_lines = []
        in_component = False
        component_ended = False
        
        for line in lines:
            # Skip markdown artifacts
            if re.match(r'^\s*```', line) or re.match(r'^\s*#{1,6}\s+', line):
                continue
            
            # Skip documentation after component ends
            if component_ended and (re.match(r'^\s*[-*]\s+', line) or re.match(r'^\s*\*\*', line)):
                continue
            
            # Track component boundaries
            if re.search(r'export default \w+Component;?', line):
                cleaned_lines.append(line)
                component_ended = True
                break
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def validate_build_compatibility(self, code: str, component_name: str) -> bool:
        """Test if the code can be built successfully."""
        try:
            # Create a temporary React project structure
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create minimal package.json
                package_json = {
                    "name": "test-component",
                    "version": "1.0.0",
                    "type": "module",
                    "dependencies": {
                        "react": "^18.2.0",
                        "react-dom": "^18.2.0"
                    },
                    "devDependencies": {
                        "@vitejs/plugin-react": "^4.2.1",
                        "vite": "^5.0.8"
                    }
                }
                
                # Write test files
                with open(os.path.join(temp_dir, 'package.json'), 'w') as f:
                    import json
                    json.dump(package_json, f)
                
                # Create vite config
                vite_config = """
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
"""
                with open(os.path.join(temp_dir, 'vite.config.js'), 'w') as f:
                    f.write(vite_config)
                
                # Create component file
                os.makedirs(os.path.join(temp_dir, 'src'), exist_ok=True)
                with open(os.path.join(temp_dir, 'src', f'{component_name}.jsx'), 'w') as f:
                    f.write(code)
                
                # Try to parse with Node.js (basic syntax check)
                result = subprocess.run(
                    ['node', '-c', f'src/{component_name}.jsx'],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                return result.returncode == 0
                
        except Exception as e:
            print(f"Build compatibility test failed: {e}")
            return False

def validate_generated_code(code: str, component_name: str) -> Tuple[bool, str, List[str]]:
    """Main validation function for generated code."""
    validator = CodeValidator()
    result = validator.validate_react_component(code, component_name)
    
    return result['valid'], result['cleaned_code'], result['errors']

def create_safe_component(component_name: str, screen_name: str = None) -> str:
    """Create a guaranteed safe React component."""
    if not screen_name:
        screen_name = component_name.replace('Component', '')
    
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          {screen_name} Screen
        </h1>
        
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Generated Component
          </h2>
          <p className="text-gray-600 mb-6">
            This component was generated from your UI screenshot.
          </p>
          
          <div className="flex space-x-4">
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">
              Primary Action
            </button>
            <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg">
              Secondary Action
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};
"""
