from PIL import Image, ImageDraw, ImageFont
import os

# Ask the user the number of posts to generate
def numInput(): 
    number = input("How many posts do you want to generate? (The maximum is 20): ") 
    if number.isdigit():
        if int(number) > 20:
            print("Please choose a number less than or equal to 20") 
            return numInput() 
        else:
            return int(number) 
    else: 
        print("You must input a number") 
        return numInput()

# Ask the user for the Instagram handle
def getHandle(): 
    handle = input("Please write the Instagram account's handle or simply press enter to not include it: ") 
    if handle == "":
        handle = None 
    return handle

# Main logic to create the posts
def create_instagram_post():
    folder_path = "background_images"
    phrases_path = "phrases.txt"
    logo_path = "logo.png"
    post_count = numInput()
    handle = getHandle()

    # Resize and crop the logo in case it exists
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        max_logo_size = 70  
        aspect_ratio = logo.height / logo.width
        logo = logo.resize((max_logo_size, int(max_logo_size * aspect_ratio)))

        mask = Image.new("L", (max_logo_size, max_logo_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, max_logo_size, max_logo_size), fill=255)

        circular_logo = Image.new("RGBA", (max_logo_size, max_logo_size), (0, 0, 0, 0))
        circular_logo.paste(logo, (0, 0), mask)

    else:
        circular_logo = None

    # Create the number of posts that the user specified from phrases.txt
    for count in range(0, post_count):
        try:
            with open(phrases_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                text = lines[count].strip()  
        except FileNotFoundError:
            print("Error: The program stopped because phrases.txt could not be located.")
            return False
        
        # Load background image
        image_path = os.path.join(folder_path, f"{count + 1}.webp")
        if not os.path.exists(image_path):
            print(f"Error: Image {count + 1}.webp not found in {folder_path}.")
            return False
        
        image = Image.open(image_path).convert("RGBA")
        max_image_size = 1080 
        image = image.resize((max_image_size, max_image_size))
        draw = ImageDraw.Draw(image)
        
        # Load font for the text and the handle
        try:
            font_path = "fonts/Lato-Black.ttf"
            font = ImageFont.truetype(font_path, 40)  
            small_font = ImageFont.truetype(font_path, 20) 
        except IOError:
            print("Warning: 'Lato-Black' not found. Using default font.")
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Wrap text to fit within the max width
        max_width = 500
        words = text.split()
        wrapped_text = []
        current_line = ""
            
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                current_line = test_line
            else:
                wrapped_text.append(current_line)
                current_line = word
        
        wrapped_text.append(current_line)
        text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in wrapped_text)
        
        # Position the text in the center
        img_width, img_height = image.size
        y = (img_height - text_height) / 2
        
        # Define a semi-transparent ash gray background
        padding = 60
        background_color = (249, 246, 238, 150)
        text_bg_x0 = (img_width - max_width) / 2 - padding
        text_bg_y0 = y - padding
        text_bg_x1 = (img_width + max_width) / 2 + padding
        text_bg_y1 = y + text_height + padding + 30
        radius = 20  
        
        # Create an overlay
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle([(text_bg_x0, text_bg_y0), (text_bg_x1, text_bg_y1)], fill=background_color, radius=radius)
        
        # Blend the overlay with the original image
        image = Image.alpha_composite(image, overlay)
        draw = ImageDraw.Draw(image)
        line_y = y
        draw = ImageDraw.Draw(image)
        
        line_spacing = 5 
        ascent, descent = font.getmetrics()
        line_height = ascent + descent + line_spacing 

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
        
        # Add the handle at the bottom right of the text area in case it exists
        if handle:
            handle_text = f"@{handle}"
            handle_width, handle_height = draw.textbbox((0, 0), handle_text, font=small_font)[2:4]
            handle_x = text_bg_x1 - handle_width - 10 
            handle_y = text_bg_y1 - handle_height - 10 
            draw.text((handle_x, handle_y), handle_text, font=small_font, fill="black")

        # Add logo in case it exists
        if circular_logo:
            logo_x = text_bg_x0 + max_logo_size/2
            logo_y = text_bg_y0 - max_logo_size/2
            image.paste(circular_logo, (int(logo_x), int(logo_y)), circular_logo)

        # Save final image
        output_path = os.path.join("generated_posts", f"post{count + 1}.png")
        image.save(output_path)
    
    print(f"{post_count} posts were succesfully created :)")

if __name__ == "__main__":
    create_instagram_post()