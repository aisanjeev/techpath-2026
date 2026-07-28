# Figma — Step-by-Step Design Projects

**Module 05 — Figma UI/UX | Hands-On Projects**

---

## Why This Matters

> Knowing Figma tools isn't enough. Every interview will ask "Show me something you designed." This chapter walks you through 3 complete projects — by the end, you'll have portfolio-worthy designs.

---

## Project 1: Mobile App Login Screen

### What You'll Build

A modern login screen for a food delivery app — the kind you see in Swiggy, Zomato, Uber Eats.

> 🖼️ **IMAGE:** Final result — a clean mobile login screen with app logo at top, "Welcome Back" heading, email and password input fields with icons, a gradient "Sign In" button, "Forgot Password?" link, social login buttons (Google, Apple), and "Don't have an account? Sign Up" at bottom — dark or light theme
> `figma-project1-login-final.png`

### Step-by-Step

**Step 1: Create the Frame**
1. Press **F** (Frame tool)
2. In right panel, select "iPhone 14 Pro" (393 × 852)
3. Set background color: `#FFFFFF` (white) or `#0F172A` (dark)

> 🖼️ **IMAGE:** Figma interface showing the right panel with Frame presets — "iPhone 14 Pro" highlighted, showing the blank frame on canvas
> `figma-frame-selection.png`

**Step 2: Add the App Logo**
1. Press **R** for rectangle → 80×80, corner radius: 20
2. Fill with gradient: `#6366F1` → `#8B5CF6` (purple gradient)
3. Add text "FD" inside (food delivery initials): White, Bold, 32px

**Step 3: Add Heading Text**
1. Press **T** (text tool)
2. Type "Welcome Back" — Font: Inter Bold, 28px, `#1E293B`
3. Below it: "Sign in to your account" — Inter Regular, 16px, `#64748B`

**Step 4: Create Input Fields**
1. Press **R** → 345×56, corner radius: 12
2. Fill: `#F1F5F9`, stroke: `#E2E8F0`, 1px
3. Add placeholder text inside: "Email address" — Inter Regular, 16px, `#94A3B8`
4. Add an email icon (from Figma community or draw with pen)
5. Duplicate for "Password" field
6. Add eye icon for password visibility toggle

> 🖼️ **IMAGE:** Close-up of the input field design in Figma — showing the rectangle with rounded corners, placeholder text with icon on the left, and the right panel showing the exact fill color, stroke, and corner radius values
> `figma-input-field-design.png`

**Step 5: Create the Sign In Button**
1. Press **R** → 345×56, corner radius: 12
2. Fill with gradient: `#6366F1` → `#4F46E5`
3. Add text "Sign In" — Inter SemiBold, 18px, White, centered
4. Add subtle drop shadow: X:0, Y:4, Blur:12, `#6366F1` at 30% opacity

**Step 6: Add Social Login**
1. Add "or continue with" divider line
2. Create two buttons: Google and Apple
3. Each button: 165×50, fill: `#F8FAFC`, stroke: `#E2E8F0`, corner radius: 10
4. Add Google "G" icon and Apple icon inside

**Step 7: Add Bottom Text**
"Don't have an account?" (gray) + "Sign Up" (purple, bold)

**Step 8: Final Touches**
1. Select all elements → Align center horizontally
2. Check spacing: 16-24px between elements
3. Add status bar at top (time, signal, battery)

---

## Project 2: Dashboard Card Components

### What You'll Build

Reusable dashboard cards like you see in analytics tools — stats cards, chart cards, user cards.

> 🖼️ **IMAGE:** Four card components arranged in a 2×2 grid — (1) Stats card with big number "12,847" and "+12.5%" in green with up arrow, (2) User profile card with avatar, name, role, (3) Chart card with a mini line graph, (4) Task/to-do card with checkboxes — all in a consistent design system with rounded corners and subtle shadows
> `figma-project2-dashboard-cards.png`

### Stats Card — Step by Step

1. Frame: 280×160, fill: `#FFFFFF`, corner radius: 16
2. Shadow: X:0, Y:2, Blur:8, `#000000` at 5%
3. Top: Label "Total Users" — Inter Medium, 14px, `#64748B`
4. Middle: Big number "12,847" — Inter Bold, 36px, `#0F172A`
5. Bottom: Trend badge "+12.5%" — green background `#DCFCE7`, text `#16A34A`, Inter Medium, 14px, corner radius: 6
6. Add small up-arrow icon ↑ before the percentage
7. Top-right corner: Icon representing the metric (users icon)

**Make it a Component:**
1. Select the entire card
2. Right-click → Create Component (Ctrl+Alt+K)
3. Now you can reuse it and just change the numbers!

> 🖼️ **IMAGE:** Figma showing a stats card selected as a Component (purple diamond icon), with the right panel showing component properties — text overrides for label, number, and percentage
> `figma-component-properties.png`

### User Profile Card

1. Frame: 280×200, same style as stats card
2. Add circle (press **O**): 64×64 for avatar placeholder
3. Fill avatar with gradient or placeholder image
4. Name: "Rahul Sharma" — Inter SemiBold, 18px
5. Role: "Frontend Developer" — Inter Regular, 14px, `#64748B`
6. Bottom: 3 small stats in a row (Projects: 24 | Reviews: 4.8 | Joined: 2024)

---

## Project 3: Full App — Food Delivery (5 Screens)

This is your **portfolio centerpiece**. Design 5 screens for a food delivery app.

### Screen 1: Home / Restaurant List

> 🖼️ **IMAGE:** Mobile app home screen mockup — top search bar with location, horizontal category pills (Pizza, Burger, Biryani, Chinese, South Indian), restaurant cards below (each with food image, restaurant name, rating stars, delivery time, and price range), bottom navigation bar with Home/Search/Cart/Profile icons
> `figma-food-app-home.png`

**Elements to build:**
- Status bar (system)
- Search bar with location pin + current area name
- Horizontal scrollable category pills
- Restaurant cards (image, name, cuisine, rating, time, distance)
- Bottom navigation (Home, Search, Cart, Orders, Profile)

### Screen 2: Restaurant Detail

**Elements:**
- Full-width restaurant image with back button overlay
- Restaurant name, rating, cuisine type, delivery time
- Tab bar: Menu | Reviews | Info
- Menu items grouped by category (Starters, Main Course, Desserts)
- Each menu item: name, description, price, Add to Cart button
- Floating "View Cart" bar at bottom

### Screen 3: Cart

**Elements:**
- Cart items list (item name, quantity +/- buttons, price)
- Coupon code input field
- Bill breakdown: Item total, Delivery fee, GST, Discount, Grand total
- Tip section (₹20, ₹30, ₹50, Custom)
- "Place Order — ₹547" button

### Screen 4: Order Tracking

**Elements:**
- Map placeholder showing delivery route
- Order status steps: Confirmed → Preparing → Out for delivery → Delivered
- Current step highlighted with animation indicator
- Delivery partner card (name, photo, phone icon, chat icon)
- Estimated time: "Arriving in 25 min"

### Screen 5: Profile

**Elements:**
- Profile picture + name + phone
- Menu list: My Orders, Addresses, Payments, Favorites, Settings, Help, Logout
- Each menu item with icon on left and arrow on right

---

## Figma Pro Techniques

### Auto Layout — The Most Important Feature

Auto Layout makes designs responsive and easy to update.

**Without Auto Layout:** Move everything manually when text changes.
**With Auto Layout:** Everything adjusts automatically.

**How to add:**
1. Select elements that should be in a row/column
2. Press **Shift + A** (Add Auto Layout)
3. Set direction: Horizontal or Vertical
4. Set gap between items (e.g., 12px)
5. Set padding (e.g., 16px all sides)

> 🖼️ **IMAGE:** Before and after Auto Layout — left shows a button where manually changing text "Buy" to "Buy Now & Save" breaks the layout, right shows the same button with Auto Layout where the button automatically resizes when text changes
> `figma-auto-layout-before-after.png`

### Components & Variants

**Components** = Reusable design elements (like functions in code)

1. Design a button
2. Right-click → Create Component
3. Now you can drag instances from the Assets panel
4. Edit the main component → all instances update!

**Variants** = Different states of the same component

| Component | Variants |
|-----------|----------|
| Button | Primary, Secondary, Outline, Disabled |
| Input | Default, Focused, Error, Disabled |
| Card | Regular, Featured, Compact |
| Toggle | On, Off |

> 🖼️ **IMAGE:** A Figma component set showing a Button component with 4 variants arranged in a row — Primary (filled purple), Secondary (filled gray), Outline (bordered), Disabled (grayed out) — with the variant property dropdown visible in the right panel
> `figma-variants-example.png`

### Prototyping — Make It Interactive

1. Switch to **Prototype** tab (right panel)
2. Click a button → drag the connection arrow to the target screen
3. Set interaction:
   - Trigger: "On Click"
   - Action: "Navigate To"
   - Animation: "Smart Animate"
   - Duration: 300ms

4. Press **Play** button (top right) to test

**Common prototype interactions:**
- Button → Navigate to next screen
- Back arrow → Navigate back
- Tab bar items → Switch screens
- Swipe → Carousel/scroll effect

---

## Design Handoff — What Developers Need From You

When you hand your design to a developer, they need:

| What | How to Provide |
|------|---------------|
| **Colors** | Use a color palette (list all hex codes) |
| **Fonts** | List: font name, weights, sizes used |
| **Spacing** | Consistent spacing (8px system: 8, 16, 24, 32, 48) |
| **Assets** | Export icons as SVG, images as PNG/WebP |
| **Specs** | Use Figma's Inspect mode (Dev Mode) |

**Export assets:**
1. Select icon/image
2. Bottom of right panel → Export
3. Choose format: SVG (icons), PNG 2x (images), WebP (web)

---

## Practice Exercises

### Exercise 1: Recreate a Real App Screen
Pick any popular Indian app (Paytm, PhonePe, Myntra, BookMyShow).
Screenshot one screen → recreate it pixel-perfect in Figma.
This teaches you to observe professional design patterns.

### Exercise 2: Design System
Create a mini design system with:
- Color palette (Primary, Secondary, Success, Warning, Error, Gray scale)
- Typography scale (H1-H6, Body, Caption)
- Button component with 3 variants (Primary, Secondary, Ghost)
- Input field with 3 states (Default, Focus, Error)
- Card component

### Exercise 3: Wireframe to Mockup
1. Sketch a wireframe on paper (or low-fi in Figma — gray boxes)
2. Convert it to a high-fidelity mockup (colors, images, real text)
3. Add prototype interactions between 3 screens
4. Present it in Figma's Prototype mode
