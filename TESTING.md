# FinWiz Journal - Testing Guide

## 🧪 Testing the System

Follow this guide to thoroughly test your FinWiz Journal system.

---

## ✅ Pre-Test Checklist

Before testing, ensure:

- [ ] Virtual environment is created
- [ ] Dependencies are installed (`pip install -r requirements.txt`)
- [ ] Internet connection is available
- [ ] `data/` directory exists
- [ ] All module files are present

---

## 🚀 Test 1: Application Startup

### Steps:

1. Run: `streamlit run app.py`
2. Wait for message: "You can now view your Streamlit app in your browser"
3. Browser opens automatically to `http://localhost:8501`

### Expected Results:

✅ App starts without errors
✅ Browser opens automatically
✅ Dashboard tab is visible
✅ Sidebar shows "Settings" and "Help"
✅ All 4 tabs visible (Dashboard, Fetch Data, Approve Content, Generate Journal)

### Troubleshooting:

- If browser doesn't open, manually navigate to `http://localhost:8501`
- If app crashes, check the terminal for error messages
- If modules not found, check virtual environment is activated

---

## 🧪 Test 2: Dashboard Tab Functionality

### Steps:

1. Navigate to "📈 Dashboard" tab
2. Observe the displayed metrics
3. Check the "Recent News" and "Recent Market Data" sections

### Expected Results:

✅ 4 metrics displayed (usually all zeros on first run)
✅ "Recent News" shows empty or "No pending news articles"
✅ "Recent Market Data" shows empty or "No pending market data"
✅ Refresh and Clear buttons are clickable

### Test Actions:

1. Click "🔄 Refresh Stats" button

   - ✅ Page refreshes without errors
   - ✅ Metrics update
2. Verify sidebar stats match dashboard metrics

   - ✅ Numbers match

---

## 🧪 Test 3: News Fetching

### Steps:

1. Navigate to "📥 Fetch Data" tab
2. Locate "📰 Fetch News" section on the left
3. Click "🔄 Fetch News from RSS Feeds" button
4. Wait for completion message

### Expected Results:

✅ Button becomes disabled during fetch
✅ Spinner shows "Fetching news from feeds..."
✅ Success message appears: "✅ Added X new articles"
✅ Available sources displayed:

- Financial Express
- Moneycontrol
- Economic Times
- Yahoo Finance

### Verify Data:

1. Check "Pending News Articles" section
2. See list of fetched articles
3. Click on expanders to view:
   - ✅ Article title
   - ✅ Source name
   - ✅ Category
   - ✅ Description preview
   - ✅ Article link

### Troubleshooting:

- If fetch fails, check internet connection
- Some feeds may be slow; wait up to 30 seconds
- If no articles added, the feed URLs may be unavailable
- Try again later or check feed URLs

---

## 🧪 Test 4: Market Data Fetching

### Steps:

1. Stay in "📥 Fetch Data" tab
2. Locate "📈 Fetch Market Data" section on the right
3. Click "🔄 Fetch Market Data" button
4. Wait for completion

### Expected Results:

✅ Spinner shows "Fetching market data..."
✅ Success message: "✅ Added X market data points"
✅ Available symbols displayed (Nifty 50, Sensex, etc.)

### Verify Data:

1. Check "Pending Market Data" table
2. Verify columns present:
   - ✅ symbol (ticker)
   - ✅ price (current price)
   - ✅ change_value (price change)
   - ✅ change_percent (percentage)

### Troubleshooting:

- If no data appears, yfinance may be rate-limited
- Wait a few minutes and try again
- Check internet connection
- Some symbols may not have data available

---

## 🧪 Test 5: Dashboard Updates

### Steps:

1. Go back to "📈 Dashboard" tab
2. Observe the metrics

### Expected Results:

✅ Metrics now show non-zero values
✅ Examples:

- "Pending News" = number fetched
- "Pending Market Data" = number fetched
  ✅ "Recent News" section shows articles
  ✅ "Recent Market Data" table shows prices

### Test Sidebar:

1. Check sidebar stats
2. Should match dashboard numbers

---

## 🧪 Test 6: Individual News Approval

### Steps:

1. Navigate to "✅ Approve Content" tab
2. Locate "📰 News Articles" section (left column)
3. Find first pending news article
4. Click "✅ Approve" button for one article

### Expected Results:

✅ Success message: "Approved!"
✅ Page refreshes automatically
✅ Article disappears from list
✅ Pending news count decreases
✅ Approved news count increases

### Verify:

1. Go to Dashboard and check metrics
2. "Approved News" count should increase by 1

---

## 🧪 Test 7: Bulk News Approval

### Steps:

1. Fetch more news (if needed)
2. Go to "Approve Content" tab
3. In "📰 News Articles" section, find "Approve All" button
4. Click it

### Expected Results:

✅ Success message: "Approved X articles!"
✅ Page refreshes
✅ All articles disappear from pending list
✅ Dashboard shows all as approved

### Verify:

1. Dashboard should show "Approved News" = all fetched news
2. "Pending News" should be 0

---

## 🧪 Test 8: Market Data Approval

### Steps:

1. In "✅ Approve Content" tab, find "📈 Market Data" section (right column)
2. Click "✅ Approve All" button

### Expected Results:

✅ Success message: "Approved X data points!"
✅ Market data disappears from list
✅ Pending market data count becomes 0
✅ Approved market data count increases

---

## 🧪 Test 9: Journal Generation

### Steps:

1. Navigate to "📄 Generate Journal" tab
2. Verify approved content counts are displayed
3. Click "📄 Generate HTML Journal" button
4. Wait for completion

### Expected Results:

✅ Spinner shows "Generating journal..."
✅ Success message appears
✅ File path displayed (e.g., `data/journal_20260617_120000.html`)
✅ "📥 Download HTML Journal" button appears
✅ Preview option checkbox appears

---

## 🧪 Test 10: Journal Download

### Steps:

1. In "Generate Journal" tab
2. Click "📥 Download HTML Journal" button
3. Save the file to your computer
4. Open the file in a web browser

### Expected Results:

✅ File downloads successfully
✅ File size is reasonable (> 50 KB)
✅ File name includes timestamp
✅ HTML opens in browser without errors

### Verify HTML Content:

✅ Header shows "FinWiz Journal"
✅ Generated date and time displayed
✅ Article count and market data count shown
✅ News articles section visible with titles
✅ Market data section with prices
✅ Professional dark theme applied
✅ All links are clickable
✅ Responsive layout (resize browser to test)

---

## 🧪 Test 11: Journal Preview

### Steps:

1. Go back to "Generate Journal" tab
2. Check "👀 Preview Journal (in new tab)" checkbox
3. Click the link that appears

### Expected Results:

✅ New browser tab opens with journal
✅ Journal displays correctly
✅ Same content as downloaded file

---

## 🧪 Test 12: Clear Approved Content

### Steps:

1. On Dashboard, click "🗑️ Clear All Approved" button (in Actions row)

### Expected Results:

✅ Success message: "Cleared all approved content!"
✅ Page refreshes
✅ "Approved News" count becomes 0
✅ "Approved Market Data" count becomes 0
✅ Pending counts unchanged

### Verify Database:

1. Refresh Dashboard
2. Approved content should still be 0

---

## 🧪 Test 13: Database Persistence

### Steps:

1. Fetch fresh news (should get new articles)
2. Go to Dashboard
3. Note the pending counts
4. Stop the app (Ctrl+C in terminal)
5. Wait 2 seconds
6. Start app again: `streamlit run app.py`
7. Check Dashboard

### Expected Results:

✅ Previously fetched articles still in database
✅ Pending counts match before restart
✅ All data persists across app restarts

---

## 🧪 Test 14: Error Handling

### Test 14a: Network Error

**Steps:**

1. Turn off internet
2. Try to fetch news
3. Wait for timeout

**Expected:** Error message appears, app doesn't crash

### Test 14b: Invalid Feed

**Steps:**

1. Edit RSS_FEEDS in news_fetcher.py with invalid URL
2. Fetch news

**Expected:** Error message for that feed, other feeds continue

### Test 14c: Database Corruption (Recovery)

**Steps:**

1. Delete `data/finwiz.db`
2. Restart app
3. Try to fetch and approve content

**Expected:**
✅ Database recreates automatically
✅ App works normally
✅ New data stored properly

---

## 🧪 Test 15: Performance Test

### Large Data Test:

1. Fetch news 3 times (should get ~30 articles)
2. Fetch market data 3 times
3. Go to Approve Content tab

### Expected Results:

✅ All articles load within 2 seconds
✅ Buttons remain responsive
✅ No lag when scrolling
✅ Approval actions complete quickly

### Database Size:

1. Check `data/finwiz.db` file size
2. Should be < 5 MB for 100+ articles

---

## 🧪 Test 16: Multiple Tab Navigation

### Steps:

1. Navigate rapidly between tabs
2. Fetch data in Tab 2
3. Go back to Tab 1
4. Verify data updated
5. Go to Tab 3
6. Verify pending content shown

### Expected Results:

✅ No data loss when switching tabs
✅ Metrics update correctly
✅ No lag or crashes

---

## 🧪 Test 17: HTML Template Rendering

### Verify Generated HTML:

1. Generate a journal (with news and market data)
2. Download the HTML
3. Open in browser
4. Right-click → "View Page Source"
5. Check for:
   - ✅ Proper HTML structure
   - ✅ CSS styling applied
   - ✅ All articles included
   - ✅ All market data included
   - ✅ Metadata (date, time, counts)

### Test Responsiveness:

1. Open HTML in browser
2. Press F12 (DevTools)
3. Click device toggle (mobile view)
4. Test different screen sizes
5. Verify layout adapts

---

## 🧪 Test 18: PDF Export (Browser Print)

### Steps:

1. Open generated journal in browser
2. Press Ctrl+P (or Cmd+P on Mac)
3. Select "Save as PDF"
4. Save the PDF
5. Open PDF in viewer

### Expected Results:

✅ PDF downloads successfully
✅ Content displays properly in PDF
✅ Layout is preserved
✅ Colors render correctly (or grayscale)

---

## 🧪 Test 19: Long Text Handling

### Steps:

1. Manually add a news article with very long title/description
2. Generate journal
3. Open in browser

### Expected Results:

✅ Long text wraps properly
✅ No horizontal scrolling
✅ Layout remains clean
✅ Readability maintained

---

## 🧪 Test 20: Session State Management

### Steps:

1. Select some news items (click checkboxes)
2. Navigate to another tab
3. Navigate back to Approve Content
4. Verify selections

### Expected Results:

✅ Selection state is preserved
✅ Selected items remain selected
✅ No data loss

---

## 📋 Regression Tests

Run these tests after making any code changes:

### Must Not Break:

- [ ] App startup
- [ ] Database initialization
- [ ] News fetching
- [ ] Market data fetching
- [ ] Dashboard metrics
- [ ] Approval workflows
- [ ] Journal generation
- [ ] HTML download
- [ ] Page navigation

---

## 🎯 Testing Checklist Summary

| Test                   | Status | Notes |
| ---------------------- | ------ | ----- |
| 1. Startup             | ✅/❌  |       |
| 2. Dashboard           | ✅/❌  |       |
| 3. News Fetch          | ✅/❌  |       |
| 4. Market Fetch        | ✅/❌  |       |
| 5. Dashboard Update    | ✅/❌  |       |
| 6. Individual Approval | ✅/❌  |       |
| 7. Bulk Approval       | ✅/❌  |       |
| 8. Market Approval     | ✅/❌  |       |
| 9. Journal Generation  | ✅/❌  |       |
| 10. Journal Download   | ✅/❌  |       |
| 11. Journal Preview    | ✅/❌  |       |
| 12. Clear Content      | ✅/❌  |       |
| 13. Persistence        | ✅/❌  |       |
| 14. Error Handling     | ✅/❌  |       |
| 15. Performance        | ✅/❌  |       |
| 16. Tab Navigation     | ✅/❌  |       |
| 17. HTML Rendering     | ✅/❌  |       |
| 18. PDF Export         | ✅/❌  |       |
| 19. Long Text          | ✅/❌  |       |
| 20. Session State      | ✅/❌  |       |

---

## 🐛 Bug Reporting Format

If you find an issue, report it with:

```
**Bug Title:** Brief description
**Severity:** Critical / High / Medium / Low
**Steps to Reproduce:**
1. Step 1
2. Step 2

**Expected Result:**
Description

**Actual Result:**
Description

**Environment:**
- OS: Windows/Mac/Linux
- Python Version: 3.x
- Browser: Chrome/Firefox/Safari
```

---

## ✅ Test Completion

Once all 20 tests pass:

1. System is ready for production
2. Document any failed tests
3. Report issues to development team
4. System is suitable for Finance Club use

---

**Happy Testing! 🚀**

For questions about testing, refer to:

- `README.md` - Feature overview
- `SETUP.md` - Setup issues
- `STRUCTURE.txt` - Project structure
