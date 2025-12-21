"""
Use Case Diagram - FINAL VERSION with correct layer ordering
Layer 1: Actors and boundary
Layer 2: All connection lines  
Layer 3: Use cases with WHITE FILL (covers lines)
Layer 4: Text on top
"""
from PIL import Image, ImageDraw, ImageFont

# Create image
width, height = 1600, 1100
img = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(img)

# Fonts
try:
    title_font = ImageFont.truetype("arial.ttf", 28)
    text_font = ImageFont.truetype("arial.ttf", 13)
    small_font = ImageFont.truetype("arial.ttf", 11)
except:
    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# ===== LAYER 1: Title, Boundary, Actors =====
# Title
title = "System Use Case Diagram"
title_bbox = draw.textbbox((0, 0), title, font=title_font)
draw.text(((width - (title_bbox[2] - title_bbox[0])) // 2, 40), title, fill='black', font=title_font)

subtitle = "School Activity Booking System v1.0"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=small_font)
draw.text(((width - (subtitle_bbox[2] - subtitle_bbox[0])) // 2, 75), subtitle, fill='#666666', font=small_font)

# System boundary
boundary_left = 300
draw.rectangle([boundary_left, 150, boundary_left + 1000, 950], outline='#2c3e50', width=3)

# Actors
def draw_actor(draw, x, y, name, color='black'):
    head_r = 20
    draw.ellipse([x-head_r, y-head_r*2, x+head_r, y], outline=color, width=2)
    draw.line([x, y, x, y+50], fill=color, width=2)
    draw.line([x-35, y+15, x+35, y+15], fill=color, width=2)
    draw.line([x, y+50, x-25, y+95], fill=color, width=2)
    draw.line([x, y+50, x+25, y+95], fill=color, width=2)
    name_bbox = draw.textbbox((0, 0), name, font=text_font)
    draw.text((x - (name_bbox[2]-name_bbox[0])//2, y+100), name, fill=color, font=text_font)

actor_x = 180
parent_y = 320
admin_y = 550
tutor_y = 780

draw_actor(draw, actor_x, parent_y, "Parent", '#e74c3c')
draw_actor(draw, actor_x, admin_y, "Administrator", '#3498db')
draw_actor(draw, actor_x, tutor_y, "Tutor", '#27ae60')

# ===== LAYER 2: ALL CONNECTION LINES =====
# Use case positions
col1_x, col2_x, col3_x = 500, 750, 1000

use_case_positions = {
    'reg': (col1_x, 230),
    'child': (col1_x, 320),
    'browse': (col2_x, 230),
    'book': (col2_x, 320),
    'wait': (col2_x, 410),
    'invoice': (col3_x, 230),
    'cancel': (col3_x, 320),
    
    'act': (col1_x, 550),
    'approve': (col2_x, 550),
    'logs': (col3_x, 550),
    
    'apply': (col1_x, 780),
    'sched': (col2_x, 780),
    'stud': (col3_x, 780),
}

# Draw lines from actors to use cases
def draw_line(x1, y1, x2, y2, color, width=2):
    draw.line([x1, y1, x2, y2], fill=color, width=width)

# Parent lines (red)
for key in ['reg', 'child', 'browse', 'book', 'invoice', 'cancel']:
    x2, y2 = use_case_positions[key]
    draw_line(actor_x + 40, parent_y, x2, y2, '#e74c3c')

# Admin lines (blue)
for key in ['reg', 'act', 'approve', 'logs']:
    x2, y2 = use_case_positions[key]
    draw_line(actor_x + 40, admin_y, x2, y2, '#3498db')

# Tutor lines (green)
for key in ['reg', 'apply', 'sched', 'stud']:
    x2, y2 = use_case_positions[key]
    draw_line(actor_x + 40, tutor_y, x2, y2, '#27ae60')

# <<extend>> dashed line
x1, y1 = col2_x, 410  # waitlist
x2, y2 = col2_x, 360  # above book
for i in range(0, 50, 16):
    draw.line([x1, y1 - i, x2, y1 - i - 8], fill='#95a5a6', width=2)

# ===== LAYER 3: USE CASES WITH WHITE FILL (covers lines) =====
def draw_use_case_filled(x, y, text, w=140, h=60):
    """Draw use case with WHITE FILL to cover lines underneath"""
    # Draw filled ellipse
    draw.ellipse([x - w//2, y - h//2, x + w//2, y + h//2], 
                 fill='white', outline='#2c3e50', width=2)
    # Draw text on top
    text_bbox = draw.textbbox((0, 0), text, font=small_font)
    text_w = text_bbox[2] - text_bbox[0]  
    text_h = text_bbox[3] - text_bbox[1]
    draw.text((x - text_w//2, y - text_h//2), text, fill='black', font=small_font)

# Now draw all use cases ON TOP of the lines
draw_use_case_filled(col1_x, 230, "Register/Login", 140, 60)
draw_use_case_filled(col1_x, 320, "Manage Children", 150, 60)
draw_use_case_filled(col2_x, 230, "Browse Activities", 150, 60)
draw_use_case_filled(col2_x, 320, "Book Activity", 130, 60)
draw_use_case_filled(col2_x, 410, "Join Waitlist", 120, 60)
draw_use_case_filled(col3_x, 230, "Download Invoice", 150, 60)
draw_use_case_filled(col3_x, 320, "Cancel Booking", 140, 60)

draw_use_case_filled(col1_x, 550, "Manage Activities", 160, 60)
draw_use_case_filled(col2_x, 550, "Approve Tutors", 140, 60)
draw_use_case_filled(col3_x, 550, "View System Logs", 150, 60)

draw_use_case_filled(col1_x, 780, "Apply as Tutor", 140, 60)
draw_use_case_filled(col2_x, 780, "View Schedule", 130, 60)
draw_use_case_filled(col3_x, 780, "View Students", 130, 60)

# ===== LAYER 4: Labels on top =====
draw.text((col2_x + 15, 375), "<<extend>>", fill='#7f8c8d', font=small_font)

# Legend
legend_y = height - 80
x_pos = 200
draw.line([x_pos, legend_y, x_pos + 60, legend_y], fill='#e74c3c', width=3)
draw.text((x_pos + 70, legend_y - 8), "Parent", fill='black', font=small_font)

x_pos += 200
draw.line([x_pos, legend_y, x_pos + 60, legend_y], fill='#3498db', width=3)
draw.text((x_pos + 70, legend_y - 8), "Administrator", fill='black', font=small_font)

x_pos += 250
draw.line([x_pos, legend_y, x_pos + 60, legend_y], fill='#27ae60', width=3)
draw.text((x_pos + 70, legend_y - 8), "Tutor", fill='black', font=small_font)

# Source note
note = "Based on verified implementation in app.py"
note_bbox = draw.textbbox((0, 0), note, font=small_font)
draw.text((width - (note_bbox[2] - note_bbox[0]) - 30, height - 30), note, fill='#999999', font=small_font)

# Save
output_path = r'C:\Users\Sanchit Kaushal\.gemini\antigravity\brain\c550873f-467f-4d45-bd1d-2de222823472\use_case_diagram_final.png'
img.save(output_path, 'PNG', quality=100, optimize=True)
print(f"✅ FINAL Use Case Diagram created with correct layer ordering!")
print(f"✅ NO lines cutting through text - use cases drawn on top with white fill")
print(f"✅ Saved to: {output_path}")
