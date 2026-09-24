from PIL import Image

def remove_background(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    # Get the background color from the top-left pixel
    bg_color = data[0]
    
    # We'll calculate distance from bg_color
    def color_dist(c1, c2):
        return sum(abs(a - b) for a, b in zip(c1[:3], c2[:3]))

    for item in data:
        # If the pixel is very close to the background color, make it transparent
        dist = color_dist(item, bg_color)
        if dist < 40: # threshold
            # Fully transparent
            new_data.append((item[0], item[1], item[2], 0))
        elif dist < 120:
            # Semi-transparent blending to avoid jagged edges
            alpha = int(((dist - 40) / 80.0) * 255)
            new_data.append((item[0], item[1], item[2], alpha))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    
    # Let's also crop the image to remove unnecessary padding
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, "PNG")
    print(f"Saved transparent logo to {output_path}")

if __name__ == "__main__":
    remove_background("logo_dark.png", "logo_transparent.png")
