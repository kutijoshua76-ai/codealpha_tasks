from PIL import Image, ImageDraw, ImageFont
import os

def generate_mixer_placeholder(filename):
    size = (800, 800)
    # KitchenAid Red theme
    bg_color = (153, 27, 27) # Deep red
    text_color = (241, 245, 249)
    
    img = Image.new('RGB', size, bg_color)
    d = ImageDraw.Draw(img)
    
    # Gradient overlay
    overlay = Image.new('RGB', size, (30, 41, 59))
    mask = Image.new('L', size)
    for y in range(size[1]):
        mask.putpixel((0, y), int(100 * (y / size[1])))
    img = Image.composite(img, overlay, mask)
    d = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        
    # Main Text
    d.text((100, 350), "KITCHENAID", fill=text_color, font=font)
    d.text((100, 420), "ARTISAN MIXER", fill=text_color, font=font)
    
    # Branding
    d.text((20, 20), "LUXÉ — PREMIUM HOME", fill=(245, 158, 11), font=small_font)
    
    img.save(filename)
    print(f"Generated {filename}")

if __name__ == "__main__":
    fn = r"media/products/2026/05/05/kitchenaid_mixer.jpg"
    generate_mixer_placeholder(fn)
