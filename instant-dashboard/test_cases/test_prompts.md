# Test Case Prompts for The Instant Dashboard

## Test Case 1: Complex Sales Dashboard
**File:** `complex_sales_dashboard.json`

### Prompt Options:

**Option A - Executive Summary Style:**
```
Create a professional executive dashboard with a modern corporate design. Use a clean white background with blue and green accents. Show the summary metrics in large cards at the top, followed by a regional performance comparison table. Include the monthly breakdown as a trend visualization. Use professional fonts and subtle shadows.
```

**Option B - Dark Analytics Style:**
```
Design a sleek analytics dashboard with a dark theme (dark blue/black background). Display key metrics as glowing cards with gradient borders. Create a vibrant bar chart for regional performance using different colors for each region. Show top products in a ranked list with progress bars. Make it look like a high-tech analytics platform.
```

**Option C - Colorful Modern Style:**
```
Build a vibrant, modern dashboard with a gradient background (purple to blue). Use colorful cards for each metric with icons. Display regional data as an interactive-looking table with alternating row colors. Show monthly trends with a line graph visualization. Add rounded corners and smooth shadows throughout.
```

---

## Test Case 2: E-Commerce Analytics
**File:** `ecommerce_analytics.json`

### Prompt Options:

**Option A - Retail Focus:**
```
Create a retail-focused dashboard with a light grey background. Show daily sales as a bar chart with different colors for weekdays vs weekends. Display category performance in a grid layout with percentage indicators. Include top selling items with product images placeholders. Use warm colors (orange, coral) for accents.
```

**Option B - Minimalist Clean:**
```
Design a minimalist e-commerce dashboard with lots of white space. Use a simple color palette (black, white, one accent color). Show overview metrics in a horizontal row at the top. Display daily sales as a clean line graph. Present categories in a simple table with subtle hover effects. Keep it clean and scannable.
```

**Option C - Data-Dense Professional:**
```
Build a comprehensive analytics dashboard that shows all data points. Use a professional layout with multiple sections. Include small charts for daily trends, pie charts for category breakdown, and detailed tables for traffic sources. Use a blue and grey color scheme. Make it information-rich but organized.
```

---

## Test Case 3: Original Simple Example
**File:** `test_data.json` (in root directory)

### Prompt:
```
Create a clean business dashboard. Show a total spending summary at the top and a simple table below for the items. Use a professional font and light grey background.
```

---

## Tips for Testing:

1. **Test Data Accuracy**: After generating, verify that all numbers match the JSON exactly
2. **Test Different Styles**: Try different prompts with the same data to see variety
3. **Test Complexity**: Start with the simple example, then try the complex ones
4. **Test Edge Cases**: Try very short prompts vs very detailed prompts
5. **Test Invalid JSON**: Try removing a comma to test error handling

---

## Expected Results:

✅ All numbers from JSON appear correctly in the dashboard  
✅ Dashboard matches the style described in the prompt  
✅ Layout is responsive and looks good  
✅ No hallucinated data (AI doesn't make up numbers)  
✅ Professional appearance with proper formatting  
✅ Colors and styling match the prompt description  

---

## Quick Test Commands:

Copy and paste these into your application:

### Quick Test 1 (Simple):
**JSON:** Copy from `test_data.json`  
**Prompt:** "Make it modern with blue colors and a card layout"

### Quick Test 2 (Medium):
**JSON:** Copy from `ecommerce_analytics.json`  
**Prompt:** "Create a dark theme dashboard with neon accents and charts"

### Quick Test 3 (Complex):
**JSON:** Copy from `complex_sales_dashboard.json`  
**Prompt:** "Build an executive summary dashboard with professional styling, charts, and tables"
