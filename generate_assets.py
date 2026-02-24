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

def create_border():
    # A simple border pattern.
    # Let's make a 100x100 tileable pattern or a large frame.
    # Since window size is dynamic, a large image or resizing is needed.
    # I'll make a 4K abstract background.

    width, height = 3840, 2160
    img = Image.new('RGB', (width, height), "#2b2b2b")
    draw = ImageDraw.Draw(img)

    # Draw some geometric lines/border
    border_width = 20
    draw.rectangle((0, 0, width, height), outline="#1f6aa5", width=border_width)

    # Some diagonal lines
    for i in range(0, width + height, 50):
        draw.line([(i, 0), (0, i)], fill="#343638", width=2)

    if not os.path.exists("assets"):
        os.makedirs("assets")

    img.save("assets/border_bg.png")
    print("Created assets/border_bg.png")

if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")
    create_icon()
    create_border()
