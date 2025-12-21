# Waitlist Feature Testing Guide

## Prerequisites
- ✅ Application is running: `python app.py` (currently running)
- ✅ Dashboard URL: http://127.0.0.1:5000/dashboard
- ✅ Test Activity: **Swimming** (Tuesday, £30.00, Capacity: 10)

---

## Step-by-Step Testing Instructions

### Step 1: Login to Parent Dashboard
1. Open browser: http://127.0.0.1:5000/login
2. Login with your parent credentials
3. You should see your dashboard with available activities

---

### Step 2: Check Current Swimming Capacity
1. Scroll down to find **"Swimming"** activity card
2. Look for the capacity indicator (e.g., "1 / 10 enrolled")
3. Note: You need to fill it to **10/10** to trigger the waitlist

---

### Step 3: Fill Swimming to Capacity
**Important:** You need to make 9 MORE bookings to reach capacity (assuming 1/10 currently)

**For EACH booking:**
1. Select your child from dropdown: "Aryan Kaushal" (or your child's name)
2. Pick a future date (e.g., 2025-12-24, 2025-12-25, etc. - use different dates)
3. Click blue **"Book"** button
4. Complete payment form:
   - Email: your@email.com
   - Card: 4242 4242 4242 4242
   - Expiry: 12 / 25
   - CVV: 123
   - Name: Test User
   - Address: 123 Test St
   - City: London
   - Postcode: SW1A 1AA
5. Click **"Pay £30.00"**
6. You'll see booking confirmation
7. **Return to dashboard** (click "My Dashboard" in navbar)

**Repeat this process 9 times using different dates** until Swimming shows **10/10 enrolled**

---

### Step 4: Trigger Waitlist UI ✨
1. Once Swimming is at **10/10 capacity**
2. **Refresh the dashboard page** (press F5 or Ctrl+R)
3. Scroll to Swimming activity card
4. You should now see:
   - ❌ "FULL" badge (red badge at top)
   - ⚠️ **Yellow "Join Waitlist" button** instead of blue "Book" button
   - 🟡 Button text: "⏱ Join Waitlist"

---

### Step 5: Capture Screenshot 📸

**This is your Figure 7 screenshot!**

1. Make sure the Swimming card is fully visible on screen
2. Capture screenshot showing:
   - Activity name: "Swimming"
   - "FULL" badge visible
   - **Yellow "Join Waitlist" button** clearly visible
   - Tutor info (Dr. Sarah Jenkins)
   - Capacity indicator showing "10 / 10 enrolled"

**Screenshot Tools:**
- Windows: Press `Win + Shift + S` (Snipping Tool)
- Or: Press `PrtScn` then paste in Paint

**Save as:** `Figure_7_Waitlist_Screenshot.png`

---

### Step 6: Test Waitlist Functionality (Optional)
1. Select a child
2. Pick a date
3. Click yellow **"Join Waitlist"** button
4. Should see alert: "✓ Successfully added to waitlist! You will be notified if a spot becomes available."
5. Page will reload

---

## What You Should See (Expected Result)

### Before Capacity Reached (< 10 bookings):
```
┌─────────────────────────────┐
│ Swimming                    │
│ Tuesday    £30.00          │
│ ⏰ 16:00 - 17:00           │
│ 👤 Dr. Sarah Jenkins       │
│ ✅ 5 spots available        │
│ ─────────────────────────  │
│ [Select Child ▾] [Date]    │
│ [  Book  ] ← BLUE BUTTON   │
└─────────────────────────────┘
```

### After Capacity Reached (10/10):
```
┌─────────────────────────────┐
│ Swimming        🔴 FULL     │
│ Tuesday    £30.00          │
│ ⏰ 16:00 - 17:00           │
│ 👤 Dr. Sarah Jenkins       │
│ 10 / 10 enrolled           │
│ ─────────────────────────  │
│ [Select Child ▾] [Date]    │
│ [⏱ Join Waitlist] ← YELLOW │
└─────────────────────────────┘
```

---

## Troubleshooting

**Problem:** "Join Waitlist" button not appearing
- **Solution:** Refresh the page (F5) after reaching 10/10 capacity

**Problem:** Can't make 10 bookings (payment errors)
- **Solution:** All payment processing is simulated - any card works
- Use: 4242 4242 4242 4242 for testing

**Problem:** Running out of dates
- **Solution:** Use any future dates - they don't have to be Tuesdays
- System allows booking on any date for testing

**Problem:** Need to speed this up
- **Alternative:** I can create a script to automatically fill the Swimming activity to capacity
- Let me know if you want this option

---

## After Screenshot Captured

1. Insert screenshot into `FINAL_REPORT_DRAFT.md` at line 164
2. Replace: `[INSERT FIGURE 7: Booking System Flow HERE]`
3. With: Description of what screenshot shows

**Important:** Screenshot proves your report claim on line 162:
> "Waitlist: Activity Full -> System offers Waitlist option." ✅

---

## Ready to Proceed?

Let me know when you're ready to start, or if you'd like me to:
- Create an auto-fill script to speed up the booking process
- Help with any issues during testing
- Make any adjustments to the report
