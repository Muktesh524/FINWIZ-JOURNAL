# 🚀 Approval Dashboard - Quick Start Card

## 30-Second Setup

```bash
# 1. Run the test suite
python test_approval_dashboard.py

# 2. Start the dashboard
streamlit run approval_dashboard.py

# 3. Open browser to http://localhost:8501
```

---

## Dashboard at a Glance

### 3 Main Tabs

| Tab | What You Do | Key Actions |
|-----|-------------|-------------|
| **📰 Pending News** | Review articles | ✅ Approve, ❌ Reject, ✏️ Edit, 🔗 View |
| **✅ Approved** | Verify approved | ↩️ Un-approve if needed |
| **📈 Market Data** | Review stocks | ✏️ Edit, ✅ Bulk approve |

---

## Quick Actions

### Approve an Article
1. Click **✅ Approve** button
2. Article moves to "Approved" tab
3. Pending count decreases

### Edit an Article
1. Click **✏️ Edit** button
2. Edit form appears
3. Modify headline or summary
4. Click **💾 Save Changes**

### Review Market Data
1. Go to **Market Data** tab
2. See Nifty 50 & Sensex
3. Green = Gainers
4. Red = Losers
5. Click **✅ Approve All** when ready

---

## Color Reference

| Color | Meaning |
|-------|---------|
| 🟣 Purple | Primary/Pending |
| 🟢 Green | Approved/Gainers |
| 🔴 Red | Rejected/Losers |
| 🟠 Orange | Pending status |

---

## Statistics

Always visible in top row:
- 📰 Pending News count
- ✅ Approved News count
- 📈 Pending Market data
- ✅ Approved Market data

---

## Workflow

```
Fetch Data → Review News → Edit if needed → Approve → 
Review Market → Approve Market → Check Approved → 
Generate Journal → Download HTML
```

---

## Common Tasks

### Bulk Approve All News
1. Go to **Pending News** tab
2. Scroll down (if needed)
3. All articles display
4. Approve individually OR use Market tab bulk approve

### View Approved Content
1. Go to **Approved Content** tab
2. See all approved articles
3. Can un-approve if needed

### Edit Market Data
1. Go to **Market Data** tab
2. Find stock in gainers/losers
3. Click **✏️** button
4. Edit price if needed

### Clear for Next Journal
1. Go to sidebar
2. Click **🗑️ Clear All Approved**
3. All approved content deleted
4. Ready for new data fetch

---

## Keyboard Shortcuts

| Action | Method |
|--------|--------|
| Refresh | F5 or Cmd+R |
| New Edit | Click ✏️ Edit |
| Save Edit | Click 💾 Save |
| Cancel Edit | Click ❌ Cancel |

---

## Helpful Tips

💡 **Use Edit for:**
- Fixing typos
- Clarifying headlines
- Improving summaries
- Removing inappropriate content

💡 **Market Data Tab:**
- Gainers shown in GREEN
- Losers shown in RED
- Full table available
- Edit individual prices

💡 **Bulk Operations:**
- Approve all market data at once
- Reject all if needed
- Faster than individual approval

💡 **Workflow Order:**
1. News review first
2. Market data review second
3. Check approved content
4. Then generate journal

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Changes don't save | Check browser console for errors |
| Counts don't update | Click "Refresh Stats" in sidebar |
| Edit form won't open | Ensure article ID is valid |
| Market data empty | Fetch data from main app first |

---

## File Locations

| File | Purpose |
|------|---------|
| `approval_dashboard.py` | Main dashboard app |
| `test_approval_dashboard.py` | Test suite |
| `APPROVAL_DASHBOARD_GUIDE.md` | Full documentation |
| `modules/database.py` | Database operations |

---

## Start Here

```
1. python test_approval_dashboard.py    ← Run tests
2. streamlit run approval_dashboard.py   ← Start dashboard
3. http://localhost:8501                 ← Open in browser
4. Review articles                       ← Approve/reject
5. Generate journal                      ← Create HTML
```

---

## Status Badges

| Badge | Meaning |
|-------|---------|
| ⏳ Pending | Waiting for approval |
| ✅ Approved | Ready for journal |
| 📄 Article | News item |
| 📈 Market | Stock/index data |

---

## Pro Tips

✨ **Fastest Workflow:**
1. Fetch data
2. Skim pending news (skip edit if fine)
3. Bulk approve market data
4. Approve news in bulk
5. Generate journal

✨ **Quality Control:**
1. Edit important articles
2. Verify market prices
3. Double-check approved content
4. Then generate

✨ **Time Saver:**
1. Use Edit only when needed
2. Bulk approve when possible
3. Clear and start fresh for next journal
4. Keep it simple

---

## Contact & Help

📖 **For Details:** Read APPROVAL_DASHBOARD_GUIDE.md
🧪 **For Testing:** Run test_approval_dashboard.py
❓ **For Issues:** Check troubleshooting section above

---

## Version Info

- **Version:** 1.0
- **Status:** Production Ready ✅
- **Last Update:** 2026-06-17

---

## Quick Links

- **Dashboard:** `streamlit run approval_dashboard.py`
- **Tests:** `python test_approval_dashboard.py`
- **Full Guide:** `APPROVAL_DASHBOARD_GUIDE.md`
- **Summary:** `APPROVAL_DASHBOARD_SUMMARY.md`

---

**Ready to start approving! ✅**

```
streamlit run approval_dashboard.py
```

Go to http://localhost:8501 and start reviewing content!

