"""
Template-based component generator for error-free React components.
"""

from jinja2 import Template, Environment, FileSystemLoader
import os
from typing import Dict, List, Any
from .component_namer import generate_smart_component_name

class TemplateGenerator:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(templates_dir))
    
    def generate_component_from_template(self, layout_info: Dict[str, Any]) -> str:
        """Generate a React component using Jinja2 template."""
        try:
            template = self.env.get_template('react_component.jinja')
            
            # Prepare template data
            component_name = layout_info['filename'].replace('.', '').replace('-', '').replace('_', '').title() + 'Component'
            screen_name = component_name.replace('Component', '')
            
            # Process elements for template
            elements = []
            for i, element in enumerate(layout_info.get('basic_elements', [])[:6]):
                element_type = element.get('type', 'component')
                bbox = element.get('bbox', {})
                
                # Determine element properties
                if element_type == 'navbar':
                    elements.append({
                        'title': 'Navigation Bar',
                        'description': f"Width: {bbox.get('width', 'N/A')}px",
                        'color': 'blue',
                        'interactive': True,
                        'content': '''<div className="flex space-x-2">
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">Home</span>
                  <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm">About</span>
                  <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm">Contact</span>
                </div>'''
                    })
                elif element_type == 'button':
                    elements.append({
                        'title': 'Button Element',
                        'description': f"Size: {bbox.get('width', 'N/A')} x {bbox.get('height', 'N/A')}px",
                        'color': 'green',
                        'interactive': True,
                        'content': '<button className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">Sample Button</button>'
                    })
                elif element_type == 'container':
                    elements.append({
                        'title': 'Content Container',
                        'description': f"Area: {element.get('area', 'N/A')}px²",
                        'color': 'purple',
                        'interactive': True,
                        'content': '''<div className="bg-gray-50 p-4 rounded">
                  <p className="text-sm text-gray-700">This represents a content area detected in your UI.</p>
                </div>'''
                    })
                else:
                    elements.append({
                        'title': f'{element_type.title()} Component',
                        'description': f"Dimensions: {bbox.get('width', 'N/A')} x {bbox.get('height', 'N/A')}px",
                        'color': 'gray',
                        'interactive': True,
                        'content': '''<div className="bg-gray-100 h-16 rounded flex items-center justify-center">
                  <span className="text-gray-500 text-sm">UI Element</span>
                </div>'''
                    })
            
            # Render template
            return template.render(
                component_name=component_name,
                screen_name=screen_name,
                elements=elements
            )
            
        except Exception as e:
            print(f"Error generating component from template: {e}")
            return self._generate_simple_fallback(layout_info)
    
    def _generate_simple_fallback(self, layout_info: Dict[str, Any]) -> str:
        """Generate a simple fallback component without templates."""
        component_name = layout_info['filename'].replace('.', '').replace('-', '').replace('_', '').title() + 'Component'
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
          
          <div className="grid gap-4 md:grid-cols-2">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900">UI Elements</h3>
              <p className="text-sm text-gray-600">
                {len(layout_info.get('basic_elements', []))} elements detected
              </p>
            </div>
            
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900">Dimensions</h3>
              <p className="text-sm text-gray-600">
                {layout_info.get('dimensions', {}).get('width', 'N/A')} x {layout_info.get('dimensions', {}).get('height', 'N/A')}px
              </p>
            </div>
          </div>
          
          <div className="mt-6 text-center">
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">
              Interactive Button
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};"""

def create_error_free_component(layout_info: Dict[str, Any], component_name: str = None) -> str:
    """Create an error-free React component with proper JSX syntax and smart naming."""
    # Use provided component name or generate one
    if not component_name:
        component_name = generate_smart_component_name(
            filename=layout_info.get('filename', 'unknown'),
            elements=layout_info.get('basic_elements', [])
        )
    
    filename = layout_info.get('filename', 'unknown').lower()
    elements = layout_info.get('basic_elements', [])
    element_types = [elem.get('type', 'unknown') for elem in elements]
    
    # Create page-specific layouts based on filename and elements
    if 'login' in filename or 'signin' in filename:
        return create_login_page(component_name)
    elif 'dashboard' in filename or 'admin' in filename:
        return create_dashboard_page(component_name, elements)
    elif 'profile' in filename or 'account' in filename:
        return create_profile_page(component_name)
    elif 'home' in filename or 'landing' in filename:
        return create_homepage(component_name)
    elif 'product' in filename or 'shop' in filename:
        return create_ecommerce_page(component_name)
    elif 'form' in element_types:
        return create_form_page(component_name, elements)
    elif 'table' in element_types:
        return create_data_page(component_name, elements)
    else:
        return create_generic_page(component_name, elements)

    """Create a login page component."""
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Sign In</h1>
          <p className="text-gray-600 mt-2">Welcome back! Please sign in to your account.</p>
        </div>
        
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              type="email"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your email"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              type="password"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your password"
            />
          </div>
          
          <div className="flex items-center justify-between">
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" />
              <span className="text-sm text-gray-600">Remember me</span>
            </label>
            <a href="#" className="text-sm text-blue-600 hover:underline">
              Forgot password?
            </a>
          </div>
          
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200"
          >
            Sign In
          </button>
        </form>
        
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="#" className="text-blue-600 hover:underline">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};"""

def create_profile_page(component_name: str) -> str:
    """Create a user profile page component."""
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 h-32"></div>
          <div className="relative px-6 pb-6">
            <div className="flex items-center -mt-16">
              <div className="w-24 h-24 bg-white rounded-full border-4 border-white shadow-lg flex items-center justify-center">
                <span className="text-2xl font-bold text-gray-600">JD</span>
              </div>
              <div className="ml-6 mt-16">
                <h1 className="text-2xl font-bold text-gray-900">John Doe</h1>
                <p className="text-gray-600">Software Developer</p>
              </div>
            </div>
            
            <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Personal Information</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Full Name
                    </label>
                    <input
                      type="text"
                      value="John Doe"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email
                    </label>
                    <input
                      type="email"
                      value="john.doe@example.com"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Phone
                    </label>
                    <input
                      type="tel"
                      value="+1 (555) 123-4567"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Account Settings</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-700">Email Notifications</span>
                    <button className="bg-blue-600 w-12 h-6 rounded-full relative">
                      <div className="w-4 h-4 bg-white rounded-full absolute right-1 top-1"></div>
                    </button>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-700">SMS Notifications</span>
                    <button className="bg-gray-300 w-12 h-6 rounded-full relative">
                      <div className="w-4 h-4 bg-white rounded-full absolute left-1 top-1"></div>
                    </button>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-700">Two-Factor Auth</span>
                    <button className="bg-blue-600 w-12 h-6 rounded-full relative">
                      <div className="w-4 h-4 bg-white rounded-full absolute right-1 top-1"></div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="mt-8 flex space-x-4">
              <button className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition duration-200">
                Save Changes
              </button>
              <button className="bg-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-400 transition duration-200">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};"""

def create_ecommerce_page(component_name: str) -> str:
    """Create an e-commerce page component."""
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-blue-600">ShopApp</span>
            </div>
            <div className="flex items-center space-x-4">
              <input
                type="text"
                placeholder="Search products..."
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button className="relative">
                <span className="text-2xl">🛒</span>
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">3</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="flex">
          <aside className="w-64 mr-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Filters</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Category</h4>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input type="checkbox" className="mr-2" />
                      <span className="text-sm">Electronics</span>
                    </label>
                    <label className="flex items-center">
                      <input type="checkbox" className="mr-2" />
                      <span className="text-sm">Clothing</span>
                    </label>
                    <label className="flex items-center">
                      <input type="checkbox" className="mr-2" />
                      <span className="text-sm">Books</span>
                    </label>
                  </div>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Price Range</h4>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input type="radio" name="price" className="mr-2" />
                      <span className="text-sm">Under $25</span>
                    </label>
                    <label className="flex items-center">
                      <input type="radio" name="price" className="mr-2" />
                      <span className="text-sm">$25 - $50</span>
                    </label>
                    <label className="flex items-center">
                      <input type="radio" name="price" className="mr-2" />
                      <span className="text-sm">Over $50</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </aside>
          
          <div className="flex-1">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {{[1,2,3,4,5,6].map(i => (
                <div key={{i}} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
                  <div className="h-48 bg-gray-200 rounded-t-lg flex items-center justify-center">
                    <span className="text-gray-500">Product Image</span>
                  </div>
                  <div className="p-4">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      Product Name {{i}}
                    </h3>
                    <p className="text-gray-600 text-sm mb-3">
                      High-quality product with amazing features and great value.
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-xl font-bold text-blue-600">
                        ${{(Math.random() * 100 + 10).toFixed(2)}}
                      </span>
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition duration-200">
                        Add to Cart
                      </button>
                    </div>
                  </div>
                </div>
              ))}}
            </div>
            
            <div className="mt-8 flex justify-center">
              <div className="flex space-x-2">
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
                  Previous
                </button>
                <button className="px-3 py-2 bg-blue-600 text-white rounded-md">1</button>
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50">2</button>
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50">3</button>
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}};

export default {component_name};"""

def create_form_page(component_name: str, elements: List[Dict]) -> str:
    """Create a form page component."""
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-2xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Contact Form</h1>
            <p className="text-gray-600 mt-2">Get in touch with us. We'd love to hear from you.</p>
          </div>
          
          <form className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  First Name *
                </label>
                <input
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter your first name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Last Name *
                </label>
                <input
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter your last name"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your email address"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Subject
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option>General Inquiry</option>
                <option>Technical Support</option>
                <option>Business Partnership</option>
                <option>Other</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Message *
              </label>
              <textarea
                required
                rows="5"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your message here..."
              ></textarea>
            </div>
            
            <div className="flex items-center">
              <input type="checkbox" id="newsletter" className="mr-2" />
              <label htmlFor="newsletter" className="text-sm text-gray-600">
                Subscribe to our newsletter for updates
              </label>
            </div>
            
            <div className="flex space-x-4">
              <button
                type="submit"
                className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 transition duration-200 font-medium"
              >
                Send Message
              </button>
              <button
                type="reset"
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition duration-200"
              >
                Clear
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};"""

def create_data_page(component_name: str, elements: List[Dict]) -> str:
    """Create a data table page component."""
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900">Data Management</h1>
              <div className="flex space-x-3">
                <input
                  type="text"
                  placeholder="Search..."
                  className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                  Add New
                </button>
              </div>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {{[1,2,3,4,5,6,7,8].map(i => (
                  <tr key={{i}} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      #{{1000 + i}}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                          U{{i}}
                        </div>
                        <div className="ml-3">
                          <div className="text-sm font-medium text-gray-900">User {{i}}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      user{{i}}@example.com
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={{`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${{i % 2 === 0 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}}`}}>
                        {{i % 2 === 0 ? 'Active' : 'Pending'}}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      2024-01-{{10 + i}}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button className="text-blue-600 hover:text-blue-900">Edit</button>
                      <button className="text-red-600 hover:text-red-900">Delete</button>
                    </td>
                  </tr>
                ))}}
              </tbody>
            </table>
          </div>
          
          <div className="px-6 py-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-700">
                Showing 1 to 8 of 97 results
              </div>
              <div className="flex space-x-2">
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 text-sm">
                  Previous
                </button>
                <button className="px-3 py-2 bg-blue-600 text-white rounded-md text-sm">1</button>
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 text-sm">2</button>
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 text-sm">3</button>
                <button className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 text-sm">
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};"""

def create_generic_page(component_name: str, elements: List[Dict]) -> str:
    """Create a generic page component based on detected elements."""
    screen_name = component_name.replace('Page', '').replace('Component', '')
    if not screen_name:
        screen_name = 'Generated Screen'
    
    # Generate element cards with proper JSX
    element_jsx = []
    
    for i, element in enumerate(elements[:6]):
        element_type = element.get('type', 'component')
        bbox = element.get('bbox', {})
        width = bbox.get('width', 'N/A')
        height = bbox.get('height', 'N/A')
        
        element_jsx.append(f"""            <div key="{i}" className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {element_type.title()} Element
              </h3>
              <p className="text-gray-600">
                Size: {width} x {height}px
              </p>
              <div className="mt-4 bg-gray-100 h-12 rounded flex items-center justify-center">
                <span className="text-gray-500 text-sm">UI Component</span>
              </div>
            </div>""")
    
    # If no elements, add a default card
    if not element_jsx:
        element_jsx.append("""            <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-gray-500">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Generated Component
              </h3>
              <p className="text-gray-600">
                This component was generated from your UI screenshot.
              </p>
            </div>""")
    
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-600 text-white p-6">
        <h1 className="text-3xl font-bold">{screen_name}</h1>
        <p className="mt-2 text-blue-100">Generated from UI screenshot analysis</p>
      </header>
      
      <main className="p-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
{chr(10).join(element_jsx)}
          </div>
        </div>
      </main>
      
      <footer className="bg-gray-100 p-4 text-center text-gray-600 mt-8">
        <p>Generated by AI UI Generator</p>
      </footer>
    </div>
  );
}};

export default {component_name};"""
    """Create a homepage/landing page component."""
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-white">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-blue-600">YourApp</span>
            </div>
            <div className="flex items-center space-x-8">
              <a href="#" className="text-gray-700 hover:text-blue-600">Features</a>
              <a href="#" className="text-gray-700 hover:text-blue-600">Pricing</a>
              <a href="#" className="text-gray-700 hover:text-blue-600">About</a>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <main>
        <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl font-bold mb-6">
              Build Amazing Apps with Ease
            </h1>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              Transform your ideas into reality with our powerful platform. 
              Create, deploy, and scale your applications effortlessly.
            </p>
            <div className="space-x-4">
              <button className="bg-white text-blue-600 px-8 py-3 rounded-md font-semibold hover:bg-gray-100">
                Start Free Trial
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-md font-semibold hover:bg-white hover:text-blue-600">
                Watch Demo
              </button>
            </div>
          </div>
        </section>
        
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Why Choose Our Platform?
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                Discover the features that make us the preferred choice for developers worldwide.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-blue-600 text-2xl">⚡</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Lightning Fast</h3>
                <p className="text-gray-600">
                  Deploy your applications in seconds with our optimized infrastructure.
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-green-600 text-2xl">🔒</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Secure by Default</h3>
                <p className="text-gray-600">
                  Enterprise-grade security built into every layer of our platform.
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-purple-600 text-2xl">📈</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Auto Scaling</h3>
                <p className="text-gray-600">
                  Handle millions of users without worrying about infrastructure.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <span className="text-2xl font-bold text-blue-400">YourApp</span>
            <p className="mt-4 text-gray-400">
              © 2024 YourApp. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}};

export default {component_name};"""
    """Create a dashboard page component."""
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-500 hover:text-gray-700">
                Notifications
              </button>
              <div className="w-8 h-8 bg-blue-600 rounded-full"></div>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Total Users</h3>
              <p className="text-3xl font-bold text-blue-600 mt-2">12,345</p>
              <p className="text-sm text-green-600 mt-1">↗ +12% from last month</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Revenue</h3>
              <p className="text-3xl font-bold text-green-600 mt-2">$45,678</p>
              <p className="text-sm text-green-600 mt-1">↗ +8% from last month</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Orders</h3>
              <p className="text-3xl font-bold text-purple-600 mt-2">1,234</p>
              <p className="text-sm text-red-600 mt-1">↘ -3% from last month</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Conversion</h3>
              <p className="text-3xl font-bold text-orange-600 mt-2">3.2%</p>
              <p className="text-sm text-green-600 mt-1">↗ +0.5% from last month</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  <span className="text-sm text-gray-600">New user registered</span>
                  <span className="text-xs text-gray-400">2 min ago</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span className="text-sm text-gray-600">Order completed</span>
                  <span className="text-xs text-gray-400">5 min ago</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-yellow-600 rounded-full"></div>
                  <span className="text-sm text-gray-600">Payment pending</span>
                  <span className="text-xs text-gray-400">10 min ago</span>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Analytics Chart</h3>
              <div className="h-48 bg-gray-100 rounded flex items-center justify-center">
                <span className="text-gray-500">Chart Placeholder</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}};

export default {component_name};"""
    """Create an error-free React component with proper JSX syntax and smart naming."""
    # Use provided component name or generate one
    if not component_name:
        component_name = generate_smart_component_name(
            filename=layout_info.get('filename', 'unknown'),
            elements=layout_info.get('basic_elements', [])
        )
    
    filename = layout_info.get('filename', 'unknown').lower()
    elements = layout_info.get('basic_elements', [])
    element_types = [elem.get('type', 'unknown') for elem in elements]
    
    # Create page-specific layouts based on filename and elements
    if 'login' in filename or 'signin' in filename:
        return create_login_page(component_name)
    elif 'dashboard' in filename or 'admin' in filename:
        return create_dashboard_page(component_name, elements)
    elif 'profile' in filename or 'account' in filename:
        return create_profile_page(component_name)
    elif 'home' in filename or 'landing' in filename:
        return create_homepage(component_name)
    elif 'product' in filename or 'shop' in filename:
        return create_ecommerce_page(component_name)
    elif 'form' in element_types:
        return create_form_page(component_name, elements)
    elif 'table' in element_types:
        return create_data_page(component_name, elements)
    else:
        return create_generic_page(component_name, elements)
