"""
Class Diagram - FINAL CORRECTED VERSION
Fixes hidden "1" label by ensuring all coordinates are OUTSIDE class boxes.
"""
from PIL import Image, ImageDraw, ImageFont

# HD Resolution
width, height = 1800, 2200
img = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(img)

try:
    title_font = ImageFont.truetype("arial.ttf", 40)
    heading_font = ImageFont.truetype("arialbd.ttf", 22)
    italic_font = ImageFont.truetype("ariali.ttf", 18)
    text_font = ImageFont.truetype("arial.ttf", 18)
except:
    title_font = heading_font = text_font = ImageFont.load_default()
    italic_font = text_font

# Title
draw.text((width//2 - 200, 40), "System Class Diagram", fill='black', font=title_font)

# Helper to draw text with white background
def draw_label_with_bg(x, y, text, font=text_font, bg_color='white', text_color='#2c3e50'):
    bbox = draw.textbbox((x, y), text, font=font)
    padding = 4
    rect = [bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding]
    draw.rectangle(rect, fill=bg_color)
    draw.text((x, y), text, fill=text_color, font=font)

# ===== BOX COORDINATES (Calculated) =====
# Parent:   x=300, y=160.  Height=408 -> Bottom=568. Width=400.
# Child:    x=1100, y=160. Height=220 -> Bottom=380. Width=400.
# Booking:  x=600, y=800.  Height=408 -> Bottom=1208. Width=400.
# Activity: x=300, y=1600. Height=436 -> Bottom=2036. Width=400.

# ===== STEP 1: Draw ALL lines FIRST =====

# Parent to Child (Right of Parent to Left of Child)
# Parent Right: 700, 280 (approx mid)
# Child Left: 1100, 280
draw.line([700, 280, 1100, 280], fill='#2c3e50', width=3)
draw.polygon([(1100, 280), (1080, 273), (1080, 287)], fill='#2c3e50')

# Child to Booking (Bottom of Child to Top-Right of Booking)
# Child Bottom (mid-ish x): 1300, 380
# Booking Top (right-ish x): 1000, 800
draw.line([1300, 380, 1000, 800], fill='#2c3e50', width=3)
draw.polygon([(1000, 800), (1010, 785), (1020, 795)], fill='#2c3e50')

# Parent to Booking (Bottom of Parent to Top-Left of Booking)
# Parent Bottom (mid-ish x): 500, 568
# Booking Top (left-ish x): 600, 800
draw.line([500, 568, 600, 800], fill='#2c3e50', width=3)
draw.polygon([(600, 800), (590, 785), (605, 780)], fill='#2c3e50')

# Booking to Activity (Bottom of Booking to Top of Activity)
# Booking Bottom: 700, 1208
# Activity Top: 500, 1600
draw.line([700, 1208, 500, 1600], fill='#2c3e50', width=3)
draw.polygon([(500, 1600), (500, 1580), (520, 1585)], fill='#2c3e50')


# ===== STEP 2: Draw Labels with Backgrounds =====

# Parent -> Child
draw_label_with_bg(710, 255, "1")          # Outside Parent (x>700)
draw_label_with_bg(880, 255, "has")
draw_label_with_bg(1040, 255, "many")

# Child -> Booking
draw_label_with_bg(1280, 400, "1")        # Outside Child (y>380)
draw_label_with_bg(1110, 570, "included in")
draw_label_with_bg(1020, 750, "many")     # Outside Booking (y<800)

# Parent -> Booking
draw_label_with_bg(480, 580, "1")         # Outside Parent (y>568) - FIXED POSITION
draw_label_with_bg(540, 680, "books")
draw_label_with_bg(570, 750, "many")      # Outside Booking (y<800)

# Booking -> Activity
draw_label_with_bg(670, 1230, "many")     # Outside Booking (y>1208)
draw_label_with_bg(540, 1400, "scheduled for")
draw_label_with_bg(470, 1560, "1")        # Outside Activity (y<1600)


# ===== STEP 3: Draw class boxes =====

def draw_class(x, y, name, attrs, methods=None):
    w = 400
    h_attr = len(attrs) * 28 + 20
    h_meth = len(methods) * 28 + 20 if methods else 0
    h_total = 60 + h_attr + h_meth
    
    # White fill
    draw.rectangle([x, y, x+w, y+h_total], fill='white', outline='#2c3e50', width=3)
    
    # Header
    draw.rectangle([x, y, x+w, y+56], fill='#ecf0f1', outline='#2c3e50', width=3)
    draw.text((x+w//2-len(name)*6, y+18), name, fill='black', font=heading_font)
    draw.line([x, y+56, x+w, y+56], fill='#2c3e50', width=3)
    
    yp = y + 70
    for a in attrs:
        draw.text((x+12, yp), a, fill='black', font=text_font)
        yp += 28
    
    if methods:
        draw.line([x, y+60+h_attr, x+w, y+60+h_attr], fill='#2c3e50', width=3)
        yp = y + 74 + h_attr
        for m in methods:
            draw.text((x+12, yp), m, fill='black', font=text_font)
            yp += 28

# Draw classes
draw_class(300, 160, "Parent",
          ["- full_name: String", "- phone: String", "- created_at: DateTime", "--",
           "- id: Integer(PK)", "- email: String(Unique)", "- password: String(Hashed)"],
          ["+ set_password()", "+ check_password()", "+ get_bookings()", "+ get_children()"])

draw_class(1100, 160, "Child",
          ["- id: Integer", "- parent_id: Integer", "- name: String", 
           "- age: Integer", "- grade: String"])

draw_class(600, 800, "Booking",
          ["- booking_date: Date", "- status: String", "- cost: Float", "--",
           "- id: Integer(PK)", "- parent_id: Integer(FK)", 
           "- child_id: Integer(FK)", "- activity_id: Integer(FK)"],
          ["+ cancel()", "+ generate_invoice()", "+ get_cost()"])

draw_class(300, 1600, "Activity",
          ["- name: String", "- description: Text", "- price: Float",
           "- max_capacity: Integer", "- day_of_week: String", "--",
           "- id: Integer(PK)", "- start_time: String", "- end_time: String"],
          ["+ get_available_slots()", "+ is_full()", "+ get_price()"])


# Source Footer
draw.text((width-400, height-40), "(Source: SQLAlchemy Models)", fill='#999', font=text_font)

output = r'C:\Users\Sanchit Kaushal\.gemini\antigravity\brain\c550873f-467f-4d45-bd1d-2de222823472\class_diagram.png'
img.save(output, 'PNG', quality=95, optimize=True)
print("✅ FIXED: '1' label now visible below Parent box")
