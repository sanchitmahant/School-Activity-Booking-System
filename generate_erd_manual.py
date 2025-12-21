"""
ERD Diagram Generation Script
Generates a professional Entity-Relationship Diagram (ERD) using PIL.
Matches the style of the user's reference (Table boxes with Type | Name | Key columns).
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Resolution - High Quality
width, height = 2400, 2400
img = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(img)

# Fonts
try:
    # Attempt to use standard Windows fonts for a professional look
    title_font = ImageFont.truetype("arialbd.ttf", 50)
    header_font = ImageFont.truetype("arialbd.ttf", 22) # For Table Headers
    text_font = ImageFont.truetype("arial.ttf", 20)     # For Items
    label_font = ImageFont.truetype("arial.ttf", 18)    # For Line Labels
except:
    # Fallback
    title_font = header_font = text_font = label_font = ImageFont.load_default()

# Colors
BORDER_COLOR = 'black'
HEADER_BG = '#ffffff' # White header as per screenshot
TEXT_COLOR = 'black'
LINE_COLOR = 'black'

# Title - Centered (REMOVED as per request)
# title_text = "Figure 3.1: Database Entity-Relationship Diagram"
# title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
# title_w = title_bbox[2] - title_bbox[0]
# draw.text(((width - title_w) // 2, 50), title_text, fill='black', font=title_font)

def draw_entity_table(x, y, table_name, fields):
    """
    Draws a database table box.
    """
    # Dimensions based on content - WIDENED
    col1_w = 150 # Type (was 120, increased for arrow/DATE/FLOAT fit)
    col2_w = 260 # Name (was 220)
    col3_w = 50  # Key
    row_h = 40
    total_w = col1_w + col2_w + col3_w
    
    # Calculate height
    header_h = 45
    total_h = header_h + (len(fields) * row_h)
    
    # Draw Background
    draw.rectangle([x, y, x+total_w, y+total_h], fill='white', outline=BORDER_COLOR, width=2)
    
    # Draw Header Separator
    draw.line([x, y+header_h, x+total_w, y+header_h], fill=BORDER_COLOR, width=2)
    
    # Header Text
    text_bbox = draw.textbbox((0, 0), table_name, font=header_font)
    text_w = text_bbox[2] - text_bbox[0]
    draw.text((x + (total_w - text_w)//2, y + 10), table_name, fill='black', font=header_font)
    
    # Draw Columns Lines
    draw.line([x+col1_w, y+header_h, x+col1_w, y+total_h], fill=BORDER_COLOR, width=2)
    draw.line([x+col1_w+col2_w, y+header_h, x+col1_w+col2_w, y+total_h], fill=BORDER_COLOR, width=2)
    
    # Draw Rows
    current_y = y + header_h
    for i, (dtype, name, key) in enumerate(fields):
        # Row Separator
        draw.line([x, current_y, x+total_w, current_y], fill=BORDER_COLOR, width=1)
        
        # Text with left padding
        draw.text((x + 15, current_y + 10), dtype, fill=TEXT_COLOR, font=text_font)
        draw.text((x + col1_w + 15, current_y + 10), name, fill=TEXT_COLOR, font=text_font)
        if key:
            draw.text((x + col1_w + col2_w + 10, current_y + 10), key, fill='black', font=header_font)
            
        current_y += row_h
        
    # Rect around everything
    draw.rectangle([x, y, x+total_w, y+total_h], outline=BORDER_COLOR, width=2)
    
    return (x, y, x+total_w, y+total_h)

def draw_crows_foot(x, y, orientation):
    """
    Draws Crow's Foot "Many" symbol.
    orientation: direction the line is COMING FROM.
    """
    size = 15
    if orientation == 'up': 
        draw.line([x, y, x-size, y-size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x+size, y-size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x, y-size], fill=LINE_COLOR, width=2)
        draw.line([x-size, y-size*1.5, x+size, y-size*1.5], fill=LINE_COLOR, width=2) 
        
    elif orientation == 'down': 
        draw.line([x, y, x-size, y+size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x+size, y+size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x, y+size], fill=LINE_COLOR, width=2)
        draw.line([x-size, y+size*1.5, x+size, y+size*1.5], fill=LINE_COLOR, width=2)

    elif orientation == 'left': 
        draw.line([x, y, x-size, y-size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x-size, y+size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x-size, y], fill=LINE_COLOR, width=2)
        draw.line([x-size*1.5, y-size, x-size*1.5, y+size], fill=LINE_COLOR, width=2)

    elif orientation == 'right': 
        draw.line([x, y, x+size, y-size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x+size, y+size], fill=LINE_COLOR, width=2)
        draw.line([x, y, x+size, y], fill=LINE_COLOR, width=2)
        draw.line([x+size*1.5, y-size, x+size*1.5, y+size], fill=LINE_COLOR, width=2)

def draw_one_bar(x, y, orientation):
    """Draws 'One' symbol (parallel lines)"""
    size = 12
    if orientation in ['up', 'down']:
        draw.line([x-size, y, x+size, y], fill=LINE_COLOR, width=2) 
        if orientation == 'down':
             draw.line([x-8, y+10, x+8, y+10], fill=LINE_COLOR, width=2)
             draw.line([x-8, y+20, x+8, y+20], fill=LINE_COLOR, width=2)
        else:
             draw.line([x-8, y-10, x+8, y-10], fill=LINE_COLOR, width=2)
             draw.line([x-8, y-20, x+8, y-20], fill=LINE_COLOR, width=2)
    elif orientation in ['left', 'right']:
        if orientation == 'right':
            draw.line([x+10, y-8, x+10, y+8], fill=LINE_COLOR, width=2)
            draw.line([x+20, y-8, x+20, y+8], fill=LINE_COLOR, width=2)
        else:
            draw.line([x-10, y-8, x-10, y+8], fill=LINE_COLOR, width=2)
            draw.line([x-20, y-8, x-20, y+8], fill=LINE_COLOR, width=2)

def draw_relationship(start_rect, end_rect, start_side, end_side, label_text="", start_offset=0, end_offset=0):
    """
    Draws orthogonal line between two boxes.
    start_offset: Move connection point along the edge (perpendicular to normal).
    """
    x1, y1, w1, h1 = start_rect[0], start_rect[1], start_rect[2]-start_rect[0], start_rect[3]-start_rect[1]
    x2, y2, w2, h2 = end_rect[0], end_rect[1], end_rect[2]-end_rect[0], end_rect[3]-end_rect[1]
    
    # Calculate start point
    if start_side == 'bottom': sx, sy = x1 + w1//2 + start_offset, y1 + h1
    elif start_side == 'top': sx, sy = x1 + w1//2 + start_offset, y1
    elif start_side == 'right': sx, sy = x1 + w1, y1 + h1//2 + start_offset
    elif start_side == 'left': sx, sy = x1, y1 + h1//2 + start_offset
    
    # Calculate end point
    if end_side == 'bottom': ex, ey = x2 + w2//2 + end_offset, y2 + h2
    elif end_side == 'top': ex, ey = x2 + w2//2 + end_offset, y2
    elif end_side == 'right': ex, ey = x2 + w2, y2 + h2//2 + end_offset
    elif end_side == 'left': ex, ey = x2, y2 + h2//2 + end_offset

    # Draw Line Routing
    points = []
    points.append((sx, sy))
    
    mid_x = (sx + ex) // 2
    mid_y = (sy + ey) // 2
    
    # Priority: ALWAYS exit perpendicular to the start side first.
    
    if start_side in ['bottom', 'top']:
        # Must move Vertically first.
        # If target is Left/Right, we can go straight to target Y (corner at sx, ey)
        if end_side in ['left', 'right']:
            # L-Shape: Vertical then Horizontal
            points.append((sx, ey))
            points.append((ex, ey))
        elif end_side in ['bottom', 'top']:
            # U-Shape or Z-Shape. 
            # Go to mid_y then across?
            points.append((sx, mid_y))
            points.append((ex, mid_y))
            points.append((ex, ey))
            
    elif start_side in ['left', 'right']:
        # Must move Horizontally first.
        if end_side in ['bottom', 'top']:
            # L-Shape: Horizontal then Vertical
            points.append((ex, sy))
            points.append((ex, ey))
        elif end_side in ['left', 'right']:
            # U-Shape
            points.append((mid_x, sy))
            points.append((mid_x, ey))
            points.append((ex, ey))
        
    # Draw Lines
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=LINE_COLOR, width=2)
        
    # Draw Symbols
    if end_side == 'top': draw_crows_foot(ex, ey, 'up')
    elif end_side == 'left': draw_crows_foot(ex, ey, 'left')
    elif end_side == 'right': draw_crows_foot(ex, ey, 'right')
    elif end_side == 'bottom': draw_crows_foot(ex, ey, 'bottom')
    
    draw_one_bar(sx, sy, start_side)

    # Draw Label
    if label_text:
        # Check last segment
        p1 = points[-2]
        p2 = points[-1]
        
        # If last segment is vertical (x same), we might want to put label on previous horizontal segment
        if p1[0] == p2[0] and len(points) > 2:
            p1 = points[-3]
            p2 = points[-2]
            
        lx = (p1[0] + p2[0]) // 2
        ly = (p1[1] + p2[1]) // 2
        
        # Padding
        pad = 8
        bbox = draw.textbbox((0, 0), label_text, font=label_font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        
        draw.rectangle([lx - lw//2 - pad, ly - lh//2 - pad, lx + lw//2 + pad, ly + lh//2 + pad], fill='white')
        draw.text((lx - lw//2, ly - lh//2), label_text, fill='black', font=label_font)


# ================= ENTITY DEFINITIONS & DATA =================

data_parent = [
    ('INT', 'id', 'PK'),
    ('VARCHAR', 'email', 'UQ'),
    ('VARCHAR', 'password', ''),
    ('VARCHAR', 'full_name', ''),
    ('VARCHAR', 'phone', ''),
    ('DATETIME', 'created_at', '')
]

data_child = [
    ('INT', 'id', 'PK'),
    ('INT', 'parent_id', 'FK'),
    ('VARCHAR', 'name', ''),
    ('INT', 'age', ''),
    ('VARCHAR', 'grade', ''),
    ('DATETIME', 'created_at', '')
]

data_activity = [
    ('INT', 'id', 'PK'),
    ('INT', 'tutor_id', 'FK'),
    ('VARCHAR', 'name', ''),
    ('FLOAT', 'price', ''),
    ('INT', 'max_capacity', ''),
    ('VARCHAR', 'day_of_week', ''),
    ('VARCHAR', 'start_time', ''),
    ('VARCHAR', 'end_time', '')
]

data_booking = [
    ('INT', 'id', 'PK'),
    ('INT', 'parent_id', 'FK'),
    ('INT', 'child_id', 'FK'),
    ('INT', 'activity_id', 'FK'),
    ('DATE', 'booking_date', ''),
    ('VARCHAR', 'status', ''),
    ('FLOAT', 'cost', '')
]

data_tutor = [
    ('INT', 'id', 'PK'),
    ('VARCHAR', 'email', 'UQ'),
    ('VARCHAR', 'full_name', ''),
    ('VARCHAR', 'specialization', ''),
    ('VARCHAR', 'status', ''),
]

data_waitlist = [
    ('INT', 'id', 'PK'),
    ('INT', 'parent_id', 'FK'),
    ('INT', 'activity_id', 'FK'),
    ('DATE', 'request_date', ''),
    ('VARCHAR', 'status', '')
]

# Positions
# Parent (Top Left)
rect_parent = draw_entity_table(200, 200, "parent", data_parent)
# Child (Top Right)
rect_child = draw_entity_table(1400, 200, "child", data_child)

# Booking (Center)
rect_booking = draw_entity_table(800, 800, "booking", data_booking)

# Activity (Bottom Right) - MOVED DOWN to clear Booking
rect_activity = draw_entity_table(1400, 1300, "activity", data_activity)

# Waitlist (Bottom Left) - MOVED DOWN to align
rect_waitlist = draw_entity_table(200, 1300, "waitlist", data_waitlist)

# Tutor (Way Bottom Right)
rect_tutor = draw_entity_table(1400, 1800, "tutor", data_tutor)


# ================= RELATIONSHIPS =================

# Parent -> Child (Direct)
draw_relationship(rect_parent, rect_child, 'right', 'left', 'parent_id', start_offset=-100, end_offset=-100)

# Parent -> Booking
# Parent(TL) -> Booking(Center)
# Bottom -> Left (Safe L shape)
draw_relationship(rect_parent, rect_booking, 'bottom', 'left', 'parent_id')

# Child -> Booking
# Child(TR) -> Booking(Center)
# Bottom -> Right (Safe L shape from Right side)
# Child Bottom Y ~450. Booking Right Y Center ~960. Safe to go down then left.
draw_relationship(rect_child, rect_booking, 'bottom', 'right', 'child_id', end_offset=-50)

# Activity -> Booking
# Activity(BR) -> Booking(Center)
# Now Activity(1300) is below Booking(1125).
# Top -> Bottom (Safe Vertical)
draw_relationship(rect_activity, rect_booking, 'top', 'bottom', 'activity_id', start_offset=-50, end_offset=50)

# Parent -> Waitlist
# Parent(TL) -> Waitlist(BL)
# Vertical down
draw_relationship(rect_parent, rect_waitlist, 'bottom', 'top', 'parent_id')

# Activity -> Waitlist
# Side by side - Activity Left -> Waitlist Right
draw_relationship(rect_activity, rect_waitlist, 'left', 'right', 'activity_id')

# Tutor -> Activity
# Tutor(1800) -> Activity(1300)
# Top -> Bottom
draw_relationship(rect_tutor, rect_activity, 'top', 'bottom', 'tutor_id')


# Output
output_path = r'C:\Users\Sanchit Kaushal\.gemini\antigravity\brain\4458f884-f7a8-4d56-98d5-c65f471419da\erd_diagram_final.png'
img.save(output_path)
print(f"Generated new ERD diagram at: {output_path}")
