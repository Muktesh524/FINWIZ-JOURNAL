# 📄 Journal Generation - Quick Start Card

## 30-Second Setup

```bash
# 1. Start the dashboard
streamlit run approval_dashboard.py

# 2. Go to "Generate Journal" tab

# 3. Configure (optional):
#    - Enter your organization name
#    - Toggle market data inclusion

# 4. Click "Generate Journal" button

# 5. Download HTML file

# 6. Open in browser
```

---

## Dashboard at a Glance

### 4 Main Tabs

| Tab | Purpose | Key Actions |
|-----|---------|-------------|
| **📰 Pending News** | Review articles | ✅ Approve, ❌ Reject, ✏️ Edit |
| **✅ Approved Content** | View approved | ↩️ Un-approve if needed |
| **📈 Market Data** | Review stocks | ✏️ Edit, ✅ Bulk approve |
| **📄 Generate Journal** | Create & download | 🚀 Generate, 💾 Download |

---

## Generate Journal Workflow

```
1️⃣  Approve Content
    ↓
2️⃣  Go to "Generate Journal" Tab
    ↓
3️⃣  Set Organization Name (optional)
    ↓
4️⃣  Click "Generate Journal"
    ↓
5️⃣  Click "Download HTML"
    ↓
6️⃣  Open in Browser or Print to PDF
```

---

## Quick Actions

### Generate a Journal
1. Go to **Generate Journal** tab
2. See stats: Approved News & Market Data
3. Enter organization name (e.g., "Finance Club")
4. Click **🚀 Generate Journal** button
5. Wait for success message

### Download Generated Journal
1. After generation, download section appears
2. See file size and creation time
3. Click **💾 Download HTML** button
4. Open file in browser

### View Recent Journals
1. Scroll to "📚 Recent Journals" section
2. See last 5 generated journals
3. Check file sizes and creation dates
4. Click to open any recent journal

### Clear & Generate New
1. After viewing journal
2. Click **✅ Clear & Generate New**
3. Approves content is removed
4. Ready to fetch and approve new data

---

## Journal Contents

### What's Included
✅ Organization name header  
✅ Generated date and time  
✅ News count and market count  
✅ Market data table (if included)  
✅ Financial news articles  
✅ Professional styling  
✅ Print-ready format  
✅ Legal disclaimer  

### What's Optional
- Include/exclude market data
- Organization name customization
- Article selection (all approved included)

---

## File Details

| Property | Details |
|----------|---------|
| **Format** | HTML (text-based) |
| **Size** | 30-200 KB depending on content |
| **Naming** | `journal_YYYYMMDD_HHMMSS.html` |
| **Location** | `data/` folder |
| **Browser Compatibility** | All modern browsers |
| **Print Support** | Full print-to-PDF support |

---

## Customization

### Organization Name
```
Default: "Finance Club"
Change: Enter in "Club/Organization Name" field
Where: Used in header and footer
```

### Market Data
```
Include: Toggle "Include Market Data" checkbox
Result: Market overview table shown/hidden
Default: ON (included)
```

### Download Name
```
Automatic: journal_20260617_103045.html
Keep current: No renaming in dashboard
Change after: Rename file in browser
```

---

## Viewing & Sharing

### View Generated Journal
1. Download HTML file
2. Open in any browser (Chrome, Firefox, Safari, Edge)
3. Scroll through content
4. Use Ctrl+F to search

### Print Journal
1. Open HTML in browser
2. Press Ctrl+P (Windows) or Cmd+P (Mac)
3. Select printer or "Save as PDF"
4. Choose settings
5. Print or save

### Share Journal
1. Download HTML file
2. Email to team members
3. Upload to cloud storage
4. Share via messaging apps
5. Post on internal portal

---

## Color Reference

| Element | Color | Meaning |
|---------|-------|---------|
| 🟣 Purple | #7c3aed | Primary color, headers |
| 🟢 Green | #10b981 | Approved items, gains |
| 🔴 Red | #ef4444 | Rejected items, losses |
| ⚫ Dark | #0f172a | Background |
| ⚪ Gray | #cbd5e1 | Secondary text |

---

## Statistics

### Dashboard Metrics
```
📰 Approved News       → Number of approved articles
📈 Approved Market     → Number of approved data points
📊 Total Items         → Combined count
✅ Ready              → Yes/No status
```

### Generated File
```
File Size             → KB display
Created               → Timestamp
File Name             → Exact filename
```

---

## Common Tasks

### Generate Daily Journal
1. Fetch data in morning
2. Review and approve content
3. Go to Generate Journal tab
4. Click Generate
5. Download and share

### Generate with Custom Name
1. Enter "My Company" in name field
2. Click Generate
3. Name appears in header/footer

### Bulk Operations
1. Approve all news (Pending News tab)
2. Approve all market data (Market Data tab)
3. Go to Generate Journal
4. All approved content auto-included

### Archive Old Journals
1. Download all journals
2. Rename with dates
3. Store in archive folder
4. Clear old data from system

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No approved content" | Go back and approve articles/market data |
| File won't download | Try different browser or check pop-ups |
| Journal looks blank | Ensure approved content exists |
| Download page not showing | Refresh browser (F5) after generation |
| Can't open HTML file | Use latest browser or try online HTML viewer |

---

## Pro Tips

💡 **Fastest Workflow:**
1. Fetch all data
2. Skim and approve quickly
3. Generate immediately
4. Download and share

💡 **Quality Journal:**
1. Edit important articles
2. Verify market prices
3. Check final preview
4. Then download

💡 **Batch Processing:**
1. Set up recurring schedule
2. Fetch data daily
3. Quick review
4. Auto-generate at same time

💡 **Sharing:**
1. Generate morning journal
2. Email to team by 9 AM
3. Post to Slack
4. Upload to shared drive

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Generate Journal | Click button (no shortcut) |
| Download File | Click download button |
| Print | Ctrl+P (Cmd+P on Mac) |
| Find in Page | Ctrl+F (Cmd+F on Mac) |
| Refresh Dashboard | F5 |

---

## File Management

### Where Files Are Saved
```
finwizjournal/
└── data/
    ├── finwiz.db              (Database)
    ├── index.html             (Dashboard)
    ├── journal_*.html         (Generated journals)
    └── ...
```

### How to Access
1. Navigate to `data/` folder
2. Look for `journal_*.html` files
3. Latest files appear first
4. Oldest files on bottom

### File Retention
- No automatic deletion
- Old files kept indefinitely
- Consider archiving after download
- Clear space as needed

---

## Security & Privacy

✅ **Safe to Use:**
- All HTML is local (no upload to cloud)
- Browser auto-escapes content
- No personal data exposed
- Self-contained files

✅ **File Sharing:**
- HTML files are self-contained
- No database access needed
- Safe to email
- Safe to share publicly

---

## Quick Reference

### Settings
```
Organization Name:  Text input (default: "Finance Club")
Include Market:     Checkbox (default: checked)
```

### Buttons
```
🚀 Generate Journal     → Creates HTML file
💾 Download HTML        → Downloads generated file
👁️ Preview in Browser   → Opens in new tab
✅ Clear & Generate New → Clears data, ready for new
```

### Info Display
```
File Size               → KB
Created                → Date and time
File Name              → journal_YYYYMMDD_*.html
```

---

## Next Steps After Generating

1. **View** - Download and open in browser
2. **Review** - Check styling and content
3. **Customize** - Edit organization name if needed
4. **Download** - Save to computer
5. **Print** - Use browser print feature
6. **Share** - Email or upload to cloud
7. **Archive** - Save with date for records
8. **Clear** - Click clear button to start fresh

---

## Template Information

### Templates Used
- `base.html` - Main styling template
- `journal.html` - Journal layout
- Dark theme design
- Professional styling

### Customization Files
- Edit CSS in `templates/base.html`
- Change colors in `:root` section
- Modify layout in templates
- Add custom fields

---

## Contact & Support

📖 **Full Guide:** Read `JOURNAL_GENERATION_GUIDE.md`  
🧪 **Testing:** Run `python test_journal_generation.py`  
❓ **Questions:** Check troubleshooting section  

---

## Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Success, ready |
| ❌ | Error, failed |
| 🚀 | Generate action |
| 💾 | Download action |
| 📄 | Journal file |
| 📚 | Recent list |

---

## Version Info

- **Version:** 1.0
- **Status:** Production Ready ✅
- **Last Update:** 2026-06-17

---

## Quick Links

- **Start Dashboard:** `streamlit run approval_dashboard.py`
- **Run Tests:** `python test_journal_generation.py`
- **Full Guide:** `JOURNAL_GENERATION_GUIDE.md`

---

**Ready to generate your journal! 🚀**

```
Go to "Generate Journal" tab → 
Click "Generate Journal" → 
Download HTML → 
Done! 📄
```

