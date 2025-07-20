#!/usr/bin/env python3
"""
AI-Powered UI Generator - Main Entry Point

This script converts UI screenshots into production-ready React applications.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from agent.builder import UIBuilder

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY not found!")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='AI-Powered UI Generator')
    parser.add_argument('--input', '-i', default='input', help='Input directory containing images')
    parser.add_argument('--output', '-o', default='generated_project', help='Output directory for generated project')
    parser.add_argument('--setup-example', action='store_true', help='Setup example project structure')
    parser.add_argument('--status', action='store_true', help='Show project status')
    parser.add_argument('--no-host', action='store_true', help='Skip automatic hosting')
    parser.add_argument('--host-mode', choices=['development', 'production'], default='development', 
                       help='Hosting mode (development or production)')
    
    args = parser.parse_args()
    
    # Initialize builder
    builder = UIBuilder(input_dir=args.input, output_dir=args.output)
    
    if args.setup_example:
        builder.setup_example_project()
        return
    
    if args.status:
        status = builder.get_project_status()
        print("📊 Project Status:")
        print(f"   Input directory: {'✅' if status['input_dir_exists'] else '❌'} {args.input}")
        print(f"   Images found: {status['images_found']}")
        print(f"   Project description: {'✅' if status['project_description_exists'] else '❌'}")
        print(f"   Output directory: {'✅' if status['output_dir_exists'] else '❌'} {args.output}")
        
        if status['images_found'] == 0:
            print("\n💡 Tip: Add UI screenshots (.png, .jpg, .jpeg) to the input directory")
        
        return
    
    # Run the main UI generation workflow
    result = builder.build_ui_from_images(
        auto_host=not args.no_host,
        host_mode=args.host_mode
    )
    
    if result['success']:
        print(f"\n🎉 Success! Generated {result['components_generated']} components")
        if result['local_url']:
            print(f"🌐 Local URL: {result['local_url']}")
        if result['public_url']:
            print(f"🌍 Public URL: {result['public_url']}")
            print("   👆 Share this URL with anyone to preview your app!")
    else:
        print(f"\n❌ UI generation failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
