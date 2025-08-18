from PIL import Image, ImageDraw, ImageFont

def create_white_remote_image():
    """Create a sample white remote control image"""
    # Create a white background image
    width, height = 120, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw remote outline
    draw.rectangle([10, 10, width-10, height-10], outline='black', width=2)
    
    # Draw buttons
    button_width, button_height = 25, 15
    
    # Top buttons
    y_start = 30
    for i, label in enumerate(['PWR', '▲', '▼']):
        x = width // 2 - button_width // 2
        y = y_start + i * 25
        draw.rectangle([x, y, x + button_width, y + button_height], 
                      outline='gray', fill='lightgray')
        
        # Add text
        try:
            draw.text((x + 5, y + 2), label, fill='black')
        except:
            draw.text((x + 8, y + 2), label, fill='black')
    
    # Center circular button
    center_x, center_y = width // 2, height // 2
    radius = 20
    draw.ellipse([center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius], 
                outline='gray', fill='lightgray')
    draw.text((center_x - 5, center_y - 5), 'OK', fill='black')
    
    # Bottom buttons
    y_start = height - 80
    for i, label in enumerate(['□', '△']):
        x = width // 2 - button_width // 2
        y = y_start + i * 25
        draw.rectangle([x, y, x + button_width, y + button_height], 
                      outline='gray', fill='lightgray')
        draw.text((x + 8, y + 2), label, fill='black')
    
    # Add VirtuSense branding
    draw.text((15, height - 20), 'VirtuSense', fill='gray')
    
    return image

def create_black_remote_image():
    """Create a sample black remote control image"""
    # Create a black background image
    width, height = 120, 200
    image = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(image)
    
    # Draw remote outline
    draw.rectangle([10, 10, width-10, height-10], outline='white', width=2)
    
    # Draw buttons
    button_width, button_height = 25, 15
    
    # Top buttons
    y_start = 30
    for i, label in enumerate(['PWR', '▲', '▼']):
        x = width // 2 - button_width // 2
        y = y_start + i * 25
        draw.rectangle([x, y, x + button_width, y + button_height], 
                      outline='lightgray', fill='darkgray')
        draw.text((x + 5, y + 2), label, fill='white')
    
    # Center circular button
    center_x, center_y = width // 2, height // 2
    radius = 20
    draw.ellipse([center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius], 
                outline='lightgray', fill='darkgray')
    draw.text((center_x - 5, center_y - 5), 'OK', fill='white')
    
    # Bottom buttons
    y_start = height - 80
    for i, label in enumerate(['□', '△']):
        x = width // 2 - button_width // 2
        y = y_start + i * 25
        draw.rectangle([x, y, x + button_width, y + button_height], 
                      outline='lightgray', fill='darkgray')
        draw.text((x + 8, y + 2), label, fill='white')
    
    # Add VirtuSense branding
    draw.text((15, height - 20), 'VirtuSense', fill='lightgray')
    
    return image

if __name__ == "__main__":
    # Create and save the images
    white_remote = create_white_remote_image()
    white_remote.save("white_remote.png")
    print("Created white_remote.png")
    
    black_remote = create_black_remote_image()
    black_remote.save("black_remote.png")
    print("Created black_remote.png")
    
    print("Sample remote images created successfully!") 