# Mohd Sharjeel - What I Built for This Project
**My Role**: UI/UX Designer  
**Project**: School Activity Booking System

---

## Quick Summary - What I Did

**In Simple Words**: I made the website look beautiful and easy to use.

**Think of it like this**: 
- The others built the engine and wheels (Code)
- I painted the car, put in comfortable seats, and designed the dashboard (Design)
- I made sure it looks good on your phone AND your laptop

**My Main Jobs**:
✅ Choosing colors and fonts (The Theme)  
✅ Designing the dashboard (The Look)  
✅ Making it work on mobile (Responsiveness)  
✅ Creating cool effects (Glassmorphism)  

---

## Part 1: The Design System (The Theme)

### What I Did (Simple Summary)
- Picked the "School Uniform" for the website
- Made sure everything matches
- Professional colors: Navy Blue, Teal, and Gold

### How Does It Work? (Easy Explanation)

**Imagine decorating a room**:
- You don't just throw random paint on walls
- You pick a palette: "Blue walls, white furniture, gold lamps"
- Everything must match!

**My Color Palette**:
- 🔵 **Navy Blue**: Serious, professional, trustworthy (Like a school blazer)
- 🟢 **Teal**: Fresh, energetic, fun (Like sports activities)
- 🟡 **Gold**: Excellence, winning, stars (Like a gold star)

**Why these colors?**
- If I used Neon Pink and Green, it would look like a toy store.
- Navy Blue makes parents trust us with their money and kids.

### The Code (With Simple Explanation)

```css
:root {
    /* I defined these once, used them everywhere */
    --primary-color: #002E5D;  /* Navy */
    --accent-color: #0DA49F;   /* Teal */
    --gold-color: #FFB91D;     /* Gold */
}

button {
    background-color: var(--primary-color); /* Use Navy */
}
```

**Real Example**:
```
Every button, header, and link uses these exact variables.
If I want to change Navy to Purple, I change it in ONE place, 
and the WHOLE website changes instantly!
```

---

## Part 2: The Parent Dashboard

### What I Did (Simple Summary)
- Designed the main screen parents see
- Made it easy to understand at a glance
- "How much money spent?", "How many bookings?"

### How Does It Work? (Easy Explanation)

**Imagine a car dashboard**:
- You need to see Speed and Fuel immediately.
- You don't want to search for them.

**My Dashboard Design**:
1. **Top Cards**: Big numbers!
   - "3 Children"
   - "5 Bookings"
   - "£125 Spent"
2. **Activity Cards**: Look like playing cards
   - Picture of activity
   - Price tag
   - "Book Now" button

**Glassmorphism (My Special Effect)**:
- I made the cards look like **frosted glass**.
- It looks modern and expensive (like Apple/Windows 11 design).
- It sits on top of the background image.

### The Code (With Simple Explanation)

```css
.glass-card {
    /* The Frosted Glass Effect */
    background: rgba(255, 255, 255, 0.7); /* See-through white */
    backdrop-filter: blur(10px);          /* Blur what's behind */
    border: 1px solid white;              /* Shiny edge */
    box-shadow: 0 10px 20px rgba(0,0,0,0.1); /* Shadow for depth */
}
```

**Real Example**:
```
When you look at the dashboard:
- The cards look like they are floating.
- You can slightly see the background through them.
- It feels 3D and high-tech.
```

---

## Part 3: Mobile Responsiveness

### What I Did (Simple Summary)
- Made the website shape-shift!
- Looks great on big computer screens
- Looks great on small phone screens
- It automatically adjusts (squeezes or expands)

### How Does It Work? (Easy Explanation)

**Imagine water in a container**:
- Pour water in a wide tray -> It spreads out wide.
- Pour water in a tall glass -> It becomes tall and thin.
- The water (content) is the same, but the shape changes.

**My "Breakpoints" (Shape-shifting rules)**:
1. **Big Screen (Laptop)**:
   - Show 3 cards in a row.
   - [Card] [Card] [Card]

2. **Medium Screen (Tablet)**:
   - Show 2 cards in a row.
   - [Card] [Card]
   - [Card]

3. **Small Screen (Phone)**:
   - Show 1 card in a row.
   - [Card]
   - [Card]
   - [Card]

### The Code (With Simple Explanation)

```css
/* Default: Mobile Phone (1 column) */
.grid {
    grid-template-columns: 1fr; 
}

/* If screen is bigger than tablet (768px) */
@media (min-width: 768px) {
    .grid {
        grid-template-columns: 1fr 1fr; /* 2 columns */
    }
}

/* If screen is bigger than laptop (1024px) */
@media (min-width: 1024px) {
    .grid {
        grid-template-columns: 1fr 1fr 1fr; /* 3 columns */
    }
}
```

**Real Example**:
```
Try this:
1. Open website on laptop -> 3 columns.
2. Shrink the window -> Snap! Becomes 2 columns.
3. Shrink more -> Snap! Becomes 1 column.
It never looks broken!
```

---

## Part 4: Availability Indicators

### What I Did (Simple Summary)
- Visual clues to show if class is full
- Green = Good, Red = Bad
- Progress bars showing how full it is

### How Does It Work? (Easy Explanation)

**Imagine a traffic light**:
- 🟢 Green Light = "Available" (Lots of space)
- 🟡 Yellow Light = "Filling Fast" (Hurry up!)
- 🔴 Red Light = "Full" (Stop!)

**My Logic**:
- If > 5 spots left -> Show Green Badge
- If 1-5 spots left -> Show Orange Badge
- If 0 spots left -> Show Red Badge "FULL"

**Progress Bar**:
- Like a battery meter on your phone.
- 50% full = Bar is half filled.
- 100% full = Bar is totally filled.

### The Code (With Simple Explanation)

```html
<!-- If lots of space -->
{% if spots > 5 %}
    <span class="badge green">Available</span>

<!-- If almost full -->
{% elif spots > 0 %}
    <span class="badge orange">Hurry!</span>

<!-- If full -->
{% else %}
    <span class="badge red">FULL</span>
{% endif %}
```

**Real Example**:
```
Parent looks at "Swimming":
- Sees Orange badge "Filling Fast"
- Sees progress bar is 90% full
- Thinks: "Oh no! I better book now!"
- Clicks Book immediately.
(Good design drives action!)
```

---

## My Contribution Summary

**Files I Created/Modified**:
1. `style.css` - The styling file (700+ lines)
2. `dashboard.html` - The layout of the main page
3. `base.html` - The master template (header/footer)

**What Each Part Does (Simple)**:

| Part | What It Does | Like... |
|------|--------------|---------|
| Color Palette | Sets the mood | Interior Decorating |
| Glassmorphism | Cool visual effect | Frosted Glass |
| Responsive Grid | Adapts to screen size | Water changing shape |
| Badges | Shows status | Traffic Lights |
| Typography | Fonts text | Handwriting style |

---

## Why This Matters

**Without my work**:
- ❌ Website would look like a boring Word document (Black text, white background)
- ❌ Impossible to use on a phone (Tiny text, scrolling sideways)
- ❌ Parents wouldn't trust it (Looks unprofessional/fake)
- ❌ Hard to see what is booked or full

**With my work**:
- ✅ Looks professional and expensive
- ✅ Works on any device (Phone/Tablet/Laptop)
- ✅ Easy to read and understand
- ✅ Fun to use!

---

**Mohd Sharjeel**  
UI/UX Design Specialist  
University of East London  
December 2025
