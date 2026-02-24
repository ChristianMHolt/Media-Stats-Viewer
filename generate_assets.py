from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0)) # Transparent
    draw = ImageDraw.Draw(img)

    # Draw a rounded rectangle or circle
    draw.ellipse((10, 10, 246, 246), fill="#1f6aa5", outline="white", width=5)

    # Add text "ML" (Media Library)
    # Since I don't have fonts, I'll draw simple shapes or use default font if available,
    # but default font might be tiny. I'll just draw a "play" triangle.
    draw.polygon([(80, 60), (80, 196), (200, 128)], fill="white")

    if not os.path.exists("assets"):
        os.makedirs("assets")

    img.save("assets/icon.png")
    print("Created assets/icon.png")

if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")
    create_icon()
