"""
Fixed template-based component generator that creates truly different pages.
"""

from jinja2 import Template, Environment, FileSystemLoader
import os
from typing import Dict, List, Any
from .component_namer import generate_smart_component_name

def create_login_page(component_name: str) -> str:
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

def create_dashboard_page(component_name: str) -> str:
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
                </div>
              </div>
            </div>
            
            <div className="mt-8 flex space-x-4">
              <button className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition duration-200">
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};"""

def create_error_free_component(layout_info: Dict[str, Any], component_name: str = None) -> str:
    """Create an error-free React component with TRULY DIFFERENT pages based on filename."""
    # Use provided component name or generate one
    if not component_name:
        component_name = generate_smart_component_name(
            filename=layout_info.get('filename', 'unknown'),
            elements=layout_info.get('basic_elements', [])
        )
    
    filename = layout_info.get('filename', 'unknown').lower()
    elements = layout_info.get('basic_elements', [])
    element_types = [elem.get('type', 'unknown') for elem in elements]
    
    print(f"🔍 Template generator processing: {filename}")
    print(f"🔍 Detected elements: {element_types}")
    print(f"🔍 Component name: {component_name}")
    
    # ENHANCED filename analysis - check component name too
    combined_analysis = f"{filename} {component_name.lower()}"
    
    # Primary filename-based detection
    if 'login' in combined_analysis or 'signin' in combined_analysis or 'auth' in combined_analysis:
        print("✅ Creating LOGIN page")
        return create_login_page(component_name)
    elif 'dashboard' in combined_analysis or 'admin' in combined_analysis:
        print("✅ Creating DASHBOARD page")
        return create_dashboard_page(component_name)
    elif 'profile' in combined_analysis or 'account' in combined_analysis or 'user' in combined_analysis:
        print("✅ Creating PROFILE page")
        return create_profile_page(component_name)
    elif 'home' in combined_analysis or 'landing' in combined_analysis or 'main' in combined_analysis:
        print("✅ Creating HOMEPAGE")
        return create_homepage(component_name)
    elif 'product' in combined_analysis or 'shop' in combined_analysis or 'store' in combined_analysis:
        print("✅ Creating E-COMMERCE page")
        return create_ecommerce_page(component_name)
    
    # Secondary element-based detection
    elif 'form' in element_types and 'button' in element_types:
        print("✅ Creating FORM page (based on elements)")
        return create_form_page(component_name, elements)
    elif 'table' in element_types:
        print("✅ Creating DATA TABLE page (based on elements)")
        return create_data_page(component_name, elements)
    elif 'navbar' in element_types and 'card' in element_types:
        print("✅ Creating DASHBOARD page (based on elements)")
        return create_dashboard_page(component_name)
    elif 'card' in element_types:
        print("✅ Creating CARD-BASED page (based on elements)")
        return create_card_page(component_name, elements)
    
    # For numeric filenames or unknown types, create varied pages based on component name
    else:
        print(f"⚠️  Unknown filename '{filename}', analyzing component name '{component_name}'")
        
        # Use component name to determine page type
        if 'dashboard' in component_name.lower():
            print("✅ Creating DASHBOARD (from component name)")
            return create_dashboard_page(component_name)
        elif 'login' in component_name.lower() or 'form' in component_name.lower():
            print("✅ Creating LOGIN FORM (from component name)")
            return create_login_page(component_name)
        elif 'profile' in component_name.lower() or 'user' in component_name.lower():
            print("✅ Creating PROFILE (from component name)")
            return create_profile_page(component_name)
        elif 'main' in component_name.lower() or 'home' in component_name.lower():
            print("✅ Creating HOMEPAGE (from component name)")
            return create_homepage(component_name)
        else:
            # Create different page types based on filename pattern
            print(f"✅ Creating UNIQUE page for '{filename}'")
            return create_varied_page_by_filename(component_name, filename, elements)

def create_homepage(component_name: str) -> str:
    """Create a homepage component."""
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
            </p>
            <button className="bg-white text-blue-600 px-8 py-3 rounded-md font-semibold hover:bg-gray-100">
              Start Free Trial
            </button>
          </div>
        </section>
      </main>
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
                className="px-4 py-2 border border-gray-300 rounded-md"
              />
              <button className="relative">
                <span className="text-2xl">🛒</span>
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">3</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
            <div className="h-48 bg-gray-200 rounded-t-lg flex items-center justify-center">
              <span className="text-gray-500">Product Image</span>
            </div>
            <div className="p-4">
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Product Name
              </h3>
              <div className="flex items-center justify-between">
                <span className="text-xl font-bold text-blue-600">$29.99</span>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                  Add to Cart
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

def create_unique_page(component_name: str, filename: str) -> str:
    """Create a unique page even for unknown filenames."""
    page_title = component_name.replace('Page', '').replace('Component', '')
    
    return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-white mb-12">
          <h1 className="text-4xl font-bold mb-4">{page_title}</h1>
          <p className="text-xl opacity-90">Specialized page generated from {filename}</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-lg p-6 text-white">
            <h3 className="text-xl font-semibold mb-4">Feature One</h3>
            <p className="opacity-90">This is a unique feature specific to this page type.</p>
          </div>
          
          <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-lg p-6 text-white">
            <h3 className="text-xl font-semibold mb-4">Feature Two</h3>
            <p className="opacity-90">Another distinctive element for this component.</p>
          </div>
          
          <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-lg p-6 text-white">
            <h3 className="text-xl font-semibold mb-4">Feature Three</h3>
            <p className="opacity-90">A third unique aspect of this page design.</p>
          </div>
        </div>
        
        <div className="text-center mt-12">
          <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition duration-200">
            Get Started with {page_title}
          </button>
        </div>
      </div>
    </div>
  );
}};

export default {component_name};"""
