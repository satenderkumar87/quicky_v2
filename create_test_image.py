#!/usr/bin/env python3
"""
Create a simple test UI mockup image for testing the AI UI generator.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_dashboard_mockup():
    """Create a simple dashboard mockup image."""
    # Create a white canvas
    width, height = 1200, 800
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Convert to PIL for text rendering
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Colors
    blue = (59, 130, 246)
    gray = (107, 114, 128)
    light_gray = (243, 244, 246)
    dark_gray = (31, 41, 55)
    
    # Header/Navigation bar
    draw.rectangle([0, 0, width, 80], fill=blue)
    draw.text((20, 25), "E-commerce Dashboard", fill=(255, 255, 255), font=font_large)
    draw.text((width-200, 30), "Profile | Settings", fill=(255, 255, 255), font=font_medium)
    
    # Sidebar
    draw.rectangle([0, 80, 250, height], fill=light_gray)
    sidebar_items = ["Dashboard", "Products", "Orders", "Customers", "Analytics", "Settings"]
    for i, item in enumerate(sidebar_items):
        y_pos = 120 + i * 50
        if i == 0:  # Highlight first item
            draw.rectangle([10, y_pos-10, 240, y_pos+30], fill=blue)
            draw.text((20, y_pos), item, fill=(255, 255, 255), font=font_medium)
        else:
            draw.text((20, y_pos), item, fill=dark_gray, font=font_medium)
    
    # Main content area
    content_x = 270
    
    # Stats cards
    card_width = 200
    card_height = 100
    cards_data = [
        ("Total Products", "1,234"),
        ("Orders Today", "56"),
        ("Revenue", "$12,345"),
        ("Customers", "890")
    ]
    
    for i, (title, value) in enumerate(cards_data):
        x = content_x + i * (card_width + 20)
        y = 100
        
        # Card background
        draw.rectangle([x, y, x + card_width, y + card_height], fill=(255, 255, 255), outline=gray)
        
        # Card content
        draw.text((x + 15, y + 15), title, fill=gray, font=font_small)
        draw.text((x + 15, y + 40), value, fill=dark_gray, font=font_large)
    
    # Product table header
    table_y = 230
    draw.rectangle([content_x, table_y, width - 20, table_y + 40], fill=light_gray)
    draw.text((content_x + 15, table_y + 12), "Recent Products", fill=dark_gray, font=font_medium)
    
    # Table headers
    headers = ["Product Name", "Category", "Price", "Stock", "Status"]
    header_y = table_y + 50
    draw.rectangle([content_x, header_y, width - 20, header_y + 30], fill=gray)
    
    header_x_positions = [content_x + 15, content_x + 200, content_x + 350, content_x + 450, content_x + 550]
    for i, header in enumerate(headers):
        draw.text((header_x_positions[i], header_y + 8), header, fill=(255, 255, 255), font=font_small)
    
    # Table rows
    products = [
        ("Wireless Headphones", "Electronics", "$99.99", "45", "Active"),
        ("Running Shoes", "Sports", "$129.99", "23", "Active"),
        ("Coffee Maker", "Home", "$79.99", "12", "Low Stock"),
        ("Smartphone Case", "Electronics", "$24.99", "67", "Active"),
    ]
    
    for i, (name, category, price, stock, status) in enumerate(products):
        row_y = header_y + 40 + i * 35
        
        # Alternate row colors
        if i % 2 == 0:
            draw.rectangle([content_x, row_y, width - 20, row_y + 30], fill=(249, 250, 251))
        
        # Row data
        row_data = [name, category, price, stock, status]
        for j, data in enumerate(row_data):
            color = (220, 38, 38) if data == "Low Stock" else dark_gray
            draw.text((header_x_positions[j], row_y + 8), data, fill=color, font=font_small)
    
    # Action buttons
    button_y = header_y + 200
    draw.rectangle([content_x, button_y, content_x + 120, button_y + 35], fill=blue)
    draw.text((content_x + 25, button_y + 10), "Add Product", fill=(255, 255, 255), font=font_small)
    
    draw.rectangle([content_x + 140, button_y, content_x + 240, button_y + 35], fill=(255, 255, 255), outline=gray)
    draw.text((content_x + 165, button_y + 10), "Export Data", fill=dark_gray, font=font_small)
    
    # Convert back to numpy array
    return np.array(pil_img)

def create_login_mockup():
    """Create a simple login page mockup."""
    width, height = 800, 600
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Colors
    blue = (59, 130, 246)
    gray = (107, 114, 128)
    light_gray = (243, 244, 246)
    dark_gray = (31, 41, 55)
    
    # Center login form
    form_width = 400
    form_height = 350
    form_x = (width - form_width) // 2
    form_y = (height - form_height) // 2
    
    # Form background
    draw.rectangle([form_x, form_y, form_x + form_width, form_y + form_height], 
                  fill=(255, 255, 255), outline=gray, width=2)
    
    # Title
    draw.text((form_x + 150, form_y + 30), "Login", fill=dark_gray, font=font_large)
    
    # Email field
    draw.text((form_x + 30, form_y + 90), "Email", fill=dark_gray, font=font_medium)
    draw.rectangle([form_x + 30, form_y + 115, form_x + 370, form_y + 145], 
                  fill=(255, 255, 255), outline=gray)
    
    # Password field
    draw.text((form_x + 30, form_y + 170), "Password", fill=dark_gray, font=font_medium)
    draw.rectangle([form_x + 30, form_y + 195, form_x + 370, form_y + 225], 
                  fill=(255, 255, 255), outline=gray)
    
    # Login button
    draw.rectangle([form_x + 30, form_y + 260, form_x + 370, form_y + 295], fill=blue)
    draw.text((form_x + 180, form_y + 270), "Login", fill=(255, 255, 255), font=font_medium)
    
    # Footer text
    draw.text((form_x + 120, form_y + 320), "Don't have an account? Sign up", 
             fill=gray, font=font_medium)
    
    return np.array(pil_img)

def main():
    """Create test images for the AI UI generator."""
    input_dir = "input"
    os.makedirs(input_dir, exist_ok=True)
    
    print("Creating test UI mockups...")
    
    # Create dashboard mockup
    dashboard_img = create_dashboard_mockup()
    cv2.imwrite(os.path.join(input_dir, "dashboard.png"), dashboard_img)
    print("✅ Created dashboard.png")
    
    # Create login mockup
    login_img = create_login_mockup()
    cv2.imwrite(os.path.join(input_dir, "login.png"), login_img)
    print("✅ Created login.png")
    
    print(f"📁 Test images saved to: {input_dir}/")
    print("🚀 Now run: python main.py")

if __name__ == "__main__":
    main()
