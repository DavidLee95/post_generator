from PIL import Image, ImageDraw, ImageFont
import os
import shelve

def create_instagram_post():
    folder_path = "background_images"
    phrases_path = "phrases.txt"
    logo_path = os.path.join(folder_path, "logo.png")

    # Resize logo
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

        # Resize the logo if needed (adjust size)
        max_logo_size = 70  # Adjust based on preference
        aspect_ratio = logo.height / logo.width
        logo = logo.resize((max_logo_size, int(max_logo_size * aspect_ratio)))

        # Create a circular mask
        mask = Image.new("L", (max_logo_size, max_logo_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, max_logo_size, max_logo_size), fill=255)

        # Apply circular crop
        circular_logo = Image.new("RGBA", (max_logo_size, max_logo_size), (0, 0, 0, 0))
        circular_logo.paste(logo, (0, 0), mask)

    else:
        print("Warning: 'logo.png' not found.")
        logo = None
    
    # Open a shelve file to keep track of which image and phrase to use
    with shelve.open('run_count_shelve') as db:
        count = db.get('count', 0)
        print(count)
        
        if count >= 20:
            print("You've reached the maximum number of runs (20) and count will be reset to 1")
            count = 1
        
        db['count'] = count + 1

    # Automatically get text from phrases.txt
    try:
        with open(phrases_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            text = lines[count].strip()  
    except FileNotFoundError:
        print("Error: phrases.txt not found.")
        text = "Default text"
    
    # Load image
    image_path = os.path.join(folder_path, f"{count}.png")
    if not os.path.exists(image_path):
        print(f"Error: Image '{image_map[count]}' not found in '{folder}'.")
        return
    
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    
    # Load font (ensure you have Arial or provide a TTF font path)
    try:
        font_path = "fonts/Lato-Black.ttf"
        font = ImageFont.truetype(font_path, 40)  # Adjust size as needed
        small_font = ImageFont.truetype(font_path, 20)  # Font for the watermark
    except IOError:
        print("Warning: 'lato-black' not found. Using default font.")
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Define text area width
    max_width = 500
    
    # Wrap text to fit within the max width
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        lines.append(current_line)
        return lines
    
    wrapped_text = wrap_text(text, font, max_width)
    text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in wrapped_text)
    
    # Position the text in the center
    img_width, img_height = image.size
    y = (img_height - text_height) / 2
    
    # Create an overlay for the semi-transparent rectangle
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Define semi-transparent ash gray background
    padding = 60
    background_color = (249, 246, 238, 150)
    text_bg_x0 = (img_width - max_width) / 2 - padding
    text_bg_y0 = y - padding
    text_bg_x1 = (img_width + max_width) / 2 + padding
    text_bg_y1 = y + text_height + padding + 30
    radius = 20  # Rounded corner radius
    
    # Draw rounded rectangle on the overlay
    overlay_draw.rounded_rectangle([(text_bg_x0, text_bg_y0), (text_bg_x1, text_bg_y1)], fill=background_color, radius=radius)
    
    # Blend the overlay with the original image
    image = Image.alpha_composite(image, overlay)
    
    # Add text on top of the background
    draw = ImageDraw.Draw(image)
    line_y = y
    # Add wrapped and justified text on top of the background
    draw = ImageDraw.Draw(image)
    
    line_spacing = 5  # Adjust this value to increase spacing
    ascent, descent = font.getmetrics()
    line_height = ascent + descent + line_spacing  # Ensures equal spacing for all lines

    line_y = y
    for i, line in enumerate(wrapped_text):
        words = line.split()
        if len(words) == 1 or i == len(wrapped_text) - 1:
            line_x = (img_width - max_width) / 2
            draw.text((line_x, line_y), line, font=font, fill="black")
        else:
            total_words_width = sum(draw.textbbox((0, 0), word, font=font)[2] for word in words)
            extra_space = (max_width - total_words_width) / (len(words) - 1)
            current_x = (img_width - max_width) / 2
            for word in words:
                draw.text((current_x, line_y), word, font=font, fill="black")
                word_width = draw.textbbox((0, 0), word, font=font)[2]
                current_x += word_width + extra_space  
                
        line_y += line_height
    
    # Add watermark text at the bottom right of the text area
    watermark_text = "@platicahoy"
    watermark_width, watermark_height = draw.textbbox((0, 0), watermark_text, font=small_font)[2:4]
    watermark_x = text_bg_x1 - watermark_width - 10  # 10px padding from right
    watermark_y = text_bg_y1 - watermark_height - 10  # 10px padding from bottom
    draw.text((watermark_x, watermark_y), watermark_text, font=small_font, fill="black")

    # Add logo
    if circular_logo:
        logo_x = text_bg_x0 + max_logo_size/2
        logo_y = text_bg_y0 - max_logo_size/2
        image.paste(circular_logo, (int(logo_x), int(logo_y)), circular_logo)


    # Save final image
    output_path = "post.png"
    image.save(output_path)

if __name__ == "__main__":
    create_instagram_post()