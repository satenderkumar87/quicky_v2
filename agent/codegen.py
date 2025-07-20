"""
Code generator for creating complete React applications from AI-generated components.
"""

import os
import json
from typing import List, Dict, Any
from jinja2 import Template

class CodeGenerator:
    def __init__(self, output_dir: str = "generated_project"):
        self.output_dir = output_dir
        self.components_dir = os.path.join(output_dir, "src", "components")
        self.pages_dir = os.path.join(output_dir, "src", "pages")
    
    def generate_project(self, components_data: List[Dict[str, Any]], project_description: str = ""):
        """Generate complete React project structure."""
        print("Generating React project structure...")
        
        # Create directory structure
        self._create_directory_structure()
        
        # Generate package.json
        self._generate_package_json()
        
        # Generate Vite config
        self._generate_vite_config()
        
        # Generate Tailwind config
        self._generate_tailwind_config()
        
        # Generate index.html
        self._generate_index_html()
        
        # Generate main.jsx
        self._generate_main_jsx()
        
        # Generate App.jsx with routing
        self._generate_app_jsx(components_data)
        
        # Generate individual components
        self._generate_components(components_data)
        
        # Generate CSS files
        self._generate_css_files()
        
        print(f"Project generated successfully in: {self.output_dir}")
    
    def _create_directory_structure(self):
        """Create the basic React project directory structure."""
        dirs = [
            self.output_dir,
            os.path.join(self.output_dir, "src"),
            os.path.join(self.output_dir, "src", "components"),
            os.path.join(self.output_dir, "src", "pages"),
            os.path.join(self.output_dir, "src", "assets"),
            os.path.join(self.output_dir, "public")
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def _generate_package_json(self):
        """Generate package.json for the React project."""
        package_json = {
            "name": "ai-generated-ui",
            "private": True,
            "version": "0.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.8.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.43",
                "@types/react-dom": "^18.2.17",
                "@vitejs/plugin-react": "^4.2.1",
                "autoprefixer": "^10.4.16",
                "eslint": "^8.55.0",
                "eslint-plugin-react": "^7.33.2",
                "eslint-plugin-react-hooks": "^4.6.0",
                "eslint-plugin-react-refresh": "^0.4.5",
                "postcss": "^8.4.32",
                "tailwindcss": "^3.3.6",
                "vite": "^5.0.8"
            }
        }
        
        with open(os.path.join(self.output_dir, "package.json"), "w") as f:
            json.dump(package_json, f, indent=2)
    
    def _generate_vite_config(self):
        """Generate vite.config.js."""
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
"""
        with open(os.path.join(self.output_dir, "vite.config.js"), "w") as f:
            f.write(vite_config)
    
    def _generate_tailwind_config(self):
        """Generate tailwind.config.js."""
        tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        with open(os.path.join(self.output_dir, "tailwind.config.js"), "w") as f:
            f.write(tailwind_config)
        
        # Generate postcss.config.js
        postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        with open(os.path.join(self.output_dir, "postcss.config.js"), "w") as f:
            f.write(postcss_config)
    
    def _generate_index_html(self):
        """Generate index.html."""
        index_html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Generated UI</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
        with open(os.path.join(self.output_dir, "index.html"), "w") as f:
            f.write(index_html)
    
    def _generate_main_jsx(self):
        """Generate main.jsx."""
        main_jsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        with open(os.path.join(self.output_dir, "src", "main.jsx"), "w") as f:
            f.write(main_jsx)
    
    def _generate_app_jsx(self, components_data: List[Dict[str, Any]]):
        """Generate App.jsx with routing - Fixed version with proper JSX."""
        imports = []
        routes = []
        nav_items = []
        
        for component in components_data:
            component_name = component['component_name']
            imports.append(f"import {component_name} from './pages/{component_name}';")
            
            route_path = f"/{component_name.lower().replace('component', '')}"
            routes.append(f'          <Route path="{route_path}" element={{<{component_name} />}} />')
            
            nav_items.append({
                'name': component_name.replace('Component', ''),
                'path': route_path
            })
        
        # Generate navigation links
        nav_links = []
        for item in nav_items:
            nav_links.append(f'                <Link to="{item["path"]}" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">{item["name"]}</Link>')
        
        # Generate home page cards
        home_cards = []
        for item in nav_items:
            home_cards.append(f'                <Link to="{item["path"]}" className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow">')
            home_cards.append(f'                  <h3 className="text-lg font-semibold text-gray-900">{item["name"]}</h3>')
            home_cards.append(f'                  <p className="text-gray-600">View the {item["name"].lower()} page</p>')
            home_cards.append(f'                </Link>')
        
        # Create the App component with proper JSX structure
        app_jsx = f"""import React from 'react';
import {{ BrowserRouter as Router, Routes, Route, Link }} from 'react-router-dom';
{chr(10).join(imports)}

function App() {{
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {{/* Navigation */}}
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-gray-900">AI Generated UI</h1>
              </div>
              <div className="flex items-center space-x-4">
{chr(10).join(nav_links)}
              </div>
            </div>
          </div>
        </nav>

        {{/* Routes */}}
        <Routes>
          <Route 
            path="/" 
            element={{
              <div className="max-w-4xl mx-auto py-12 px-4">
                <h1 className="text-4xl font-bold text-gray-900 mb-8">Welcome to AI Generated UI</h1>
                <p className="text-lg text-gray-600 mb-8">
                  This application was generated from UI screenshots using AI. Navigate through the pages to see the generated components.
                </p>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
{chr(10).join(home_cards)}
                </div>
              </div>
            }} 
          />
{chr(10).join(routes)}
        </Routes>
      </div>
    </Router>
  );
}}

export default App;"""
        
        with open(os.path.join(self.output_dir, "src", "App.jsx"), "w") as f:
            f.write(app_jsx)
    
    def _generate_components(self, components_data: List[Dict[str, Any]]):
        """Generate individual React components."""
        for component in components_data:
            component_name = component['component_name']
            component_code = component['component_code']
            
            # Clean up the component code if needed
            if not component_code.strip().startswith('import'):
                component_code = f"import React from 'react';\n\n{component_code}"
            
            # Write component file
            component_file = os.path.join(self.pages_dir, f"{component_name}.jsx")
            with open(component_file, "w") as f:
                f.write(component_code)
            
            print(f"Generated component: {component_name}")
    
    def _generate_css_files(self):
        """Generate CSS files."""
        index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
"""
        with open(os.path.join(self.output_dir, "src", "index.css"), "w") as f:
            f.write(index_css)
