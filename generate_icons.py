from PIL import Image, ImageDraw
import os

# Configuration
SIZE = (64, 64)
COLOR_NORMAL = "#666666"
COLOR_ACTIVE = "#0052d9"
BG_COLOR = (255, 255, 255, 0) # Transparent
STROKE_WIDTH = 4
PADDING = 12

OUTPUT_DIR = "/Users/simo/codes/python/api-center/frontend-miniprogram/assets/tabbar"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_base_image():
    return Image.new("RGBA", SIZE, BG_COLOR)

def draw_home(draw, color):
    # House body
    # Roof: (10, 24) -> (32, 6) -> (54, 24)
    # Body: (16, 24) -> (16, 54) -> (48, 54) -> (48, 24)
    
    # Points for roof
    roof_points = [
        (PADDING, SIZE[1] * 0.4),
        (SIZE[0] / 2, PADDING),
        (SIZE[0] - PADDING, SIZE[1] * 0.4)
    ]
    draw.line(roof_points, fill=color, width=STROKE_WIDTH, joint="curve")
    
    # Body
    body_rect = [
        SIZE[0] * 0.25, SIZE[1] * 0.4,
        SIZE[0] * 0.75, SIZE[1] - PADDING
    ]
    # Draw U shape for body
    draw.line([
        (body_rect[0], body_rect[1]),
        (body_rect[0], body_rect[3]),
        (body_rect[2], body_rect[3]),
        (body_rect[2], body_rect[1])
    ], fill=color, width=STROKE_WIDTH, joint="curve")

def draw_article(draw, color):
    # Document shape
    # Rect: (16, 10) -> (48, 10) -> (48, 54) -> (16, 54)
    
    x1, y1 = SIZE[0] * 0.25, SIZE[1] * 0.15
    x2, y2 = SIZE[0] * 0.75, SIZE[1] * 0.85
    
    # Outline
    draw.rectangle([x1, y1, x2, y2], outline=color, width=STROKE_WIDTH)
    
    # Lines inside
    line_x1 = x1 + 8
    line_x2 = x2 - 8
    line_y_start = y1 + 12
    line_gap = 10
    
    for i in range(3):
        y = line_y_start + i * line_gap
        draw.line([(line_x1, y), (line_x2, y)], fill=color, width=STROKE_WIDTH)

def draw_puzzle(draw, color):
    # 4-grid (like a window or puzzle pieces)
    # Gap between blocks
    gap = 4
    
    # Calculate sizes
    # Total width = SIZE - 2*PADDING
    # Block width = (Total width - gap) / 2
    
    w = SIZE[0] - 2 * PADDING
    h = SIZE[1] - 2 * PADDING
    block_w = (w - gap) / 2
    block_h = (h - gap) / 2
    
    x1 = PADDING
    y1 = PADDING
    
    # Top Left
    draw.rectangle([x1, y1, x1 + block_w, y1 + block_h], outline=color, width=STROKE_WIDTH)
    # Top Right
    draw.rectangle([x1 + block_w + gap, y1, x1 + w, y1 + block_h], outline=color, width=STROKE_WIDTH)
    # Bottom Left
    draw.rectangle([x1, y1 + block_h + gap, x1 + block_w, y1 + h], outline=color, width=STROKE_WIDTH)
    # Bottom Right
    # Fill one to make it look like "pintu" or just outline all?
    # Let's outline all for consistency
    draw.rectangle([x1 + block_w + gap, y1 + block_h + gap, x1 + w, y1 + h], outline=color, width=STROKE_WIDTH)

def generate_icon(name, draw_func):
    # Normal
    img_normal = create_base_image()
    draw_normal = ImageDraw.Draw(img_normal)
    draw_func(draw_normal, COLOR_NORMAL)
    img_normal.save(os.path.join(OUTPUT_DIR, f"{name}.png"))
    
    # Active
    img_active = create_base_image()
    draw_active = ImageDraw.Draw(img_active)
    draw_func(draw_active, COLOR_ACTIVE)
    img_active.save(os.path.join(OUTPUT_DIR, f"{name}-active.png"))
    print(f"Generated {name}.png and {name}-active.png")

# Generate all
generate_icon("home-new", draw_home)
generate_icon("article-new", draw_article)
generate_icon("pintu-new", draw_puzzle)

print("All icons generated successfully.")
