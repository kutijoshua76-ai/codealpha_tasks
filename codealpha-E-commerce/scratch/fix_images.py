from PIL import Image, ImageDraw, ImageFont
import os

def gen(text, fn):
    img = Image.new('RGB', (800, 800), (15, 23, 42))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    d.text((100, 400), text, fill=(241, 245, 249), font=font)
    
    # Add LUXE badge
    d.text((20, 20), "LUXÉ — PREMIUM", fill=(124, 58, 237))
    
    img.save(fn)
    print(f"Generated {fn}")

if __name__ == "__main__":
    bp = r"media/products/2026/05/05"
    if not os.path.exists(bp):
        os.makedirs(bp)
    gen("LG WASHING MACHINE", os.path.join(bp, "washing_machine.jpg"))
    gen("STEAM IRON", os.path.join(bp, "steam_iron.jpg"))
