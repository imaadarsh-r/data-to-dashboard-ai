# Test Cases for The Instant Dashboard

This directory contains comprehensive test cases to validate the dashboard generation functionality.

## Available Test Cases

### 1. **Simple Office Spending** (Original Assessment Test Case)
- **File:** `../test_data.json`
- **Complexity:** ⭐ Simple
- **Data Points:** 4 expense items
- **Best For:** Quick validation, basic functionality testing

### 2. **Complex Sales Dashboard** 
- **File:** `complex_sales_dashboard.json`
- **Complexity:** ⭐⭐⭐⭐ Complex
- **Data Points:** 50+ data points across multiple dimensions
- **Includes:**
  - Summary metrics (revenue, orders, growth)
  - Regional performance (4 regions)
  - Top products (5 products)
  - Monthly breakdown (3 months)
  - Customer segments (3 segments)
  - Key business metrics
- **Best For:** Testing complex layouts, multiple charts, data organization

### 3. **E-Commerce Analytics**
- **File:** `ecommerce_analytics.json`
- **Complexity:** ⭐⭐⭐⭐⭐ Very Complex
- **Data Points:** 70+ data points
- **Includes:**
  - Daily sales breakdown (7 days)
  - Category performance (4 categories)
  - Top selling items (5 products)
  - Traffic sources (5 sources)
  - Customer demographics (age groups, locations)
- **Best For:** Testing time-series data, multi-dimensional analysis, detailed breakdowns

## How to Use

1. **Copy the JSON content** from any test case file
2. **Paste into the JSON input** area in the application
3. **Choose a prompt** from `test_prompts.md` or create your own
4. **Click "Generate Dashboard"**
5. **Verify the results** match the expected output

## Testing Checklist

### Functionality Tests
- [ ] All numbers from JSON appear in the dashboard
- [ ] No hallucinated or made-up data
- [ ] Dashboard renders without errors
- [ ] Layout is responsive
- [ ] All sections from JSON are displayed

### Style Tests
- [ ] Dashboard matches the prompt description
- [ ] Colors are appropriate and professional
- [ ] Typography is readable
- [ ] Spacing and alignment are correct
- [ ] Visual hierarchy is clear

### Error Handling Tests
- [ ] Invalid JSON shows clear error message
- [ ] Empty prompt is handled gracefully
- [ ] Missing fields in JSON don't crash the app
- [ ] Large datasets render correctly

## Recommended Test Sequence

1. **Start Simple:** Use `test_data.json` to verify basic functionality
2. **Go Medium:** Try `complex_sales_dashboard.json` with a simple prompt
3. **Get Complex:** Use `ecommerce_analytics.json` with detailed styling instructions
4. **Test Variations:** Try the same data with different prompts
5. **Test Edge Cases:** Invalid JSON, very long prompts, minimal prompts

## Expected Generation Time

- Simple test case: ~2-3 seconds
- Complex test case: ~3-5 seconds
- Very complex test case: ~4-6 seconds

*Thanks to Groq's ultra-fast inference!*

## Tips for Best Results

1. **Be Specific:** Detailed prompts produce better results
2. **Mention Colors:** Specify color schemes for consistent branding
3. **Request Charts:** Ask for specific visualizations (tables, charts, cards)
4. **Set the Mood:** Describe the overall style (modern, professional, minimalist)
5. **Think Layout:** Mention how you want data organized (sections, grids, columns)

## Example Workflow

```bash
# 1. Open the application
# Visit http://localhost:5173

# 2. Load a test case
# Copy JSON from complex_sales_dashboard.json

# 3. Use a prompt
# "Create a professional executive dashboard with blue accents, 
#  show metrics in cards, regional data in a table, and monthly 
#  trends as a line chart"

# 4. Generate and verify
# Click "Generate Dashboard" and check all data appears correctly
```

## Troubleshooting

**Dashboard looks different than expected:**
- Try being more specific in your prompt
- Mention exact colors, fonts, or layout preferences

**Some data is missing:**
- Check that your JSON is valid
- Verify all required fields are present

**Generation takes too long:**
- Check your internet connection
- Verify backend is running
- Check Groq API status

## Contributing Test Cases

Want to add more test cases? Follow this format:

```json
{
  "report_title": "Your Dashboard Title",
  "data_category": [
    {"field": "value"}
  ]
}
```

Save as `your_test_case.json` and add documentation to this README.
