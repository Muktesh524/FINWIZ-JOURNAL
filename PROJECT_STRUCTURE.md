# 📁 Project Structure - FinWiz Journal

## Organized Architecture (Frontend/Backend Separation)

```
finwizjournal/
│
├── 🎨 FRONTEND (Streamlit UI Layer)
│   ├── frontend/
│   │   ├── approval_dashboard.py      ← Main Streamlit dashboard app
│   │   │                               • 4 tabs: Pending News, Approved, Market Data, Generate Journal
│   │   │                               • Session state management
│   │   │                               • Professional dark theme UI
│   │   │
│   │   └── templates/                  ← Jinja2 HTML templates
│   │       ├── base.html               • Base template with CSS styling
│   │       ├── journal.html            • Main journal template
│   │       ├── index.html              • Landing page template
│   │       ├── news_section.html       • News section rendering
│   │       └── market_section.html     • Market data section rendering
│
├── 🔧 BACKEND (Business Logic Layer)
│   ├── backend/
│   │   ├── app.py                      ← Main Streamlit entry point
│   │   │                                • Dashboard startup configuration
│   │   │
│   │   ├── modules/                    ← Core business logic modules
│   │   │   ├── database.py             • SQLite CRUD operations
│   │   │   │                            - news_articles table
│   │   │   │                            - market_data table
│   │   │   │                            - generated_journals table
│   │   │   │
│   │   │   ├── news_fetcher.py         • RSS feed aggregation
│   │   │   │                            - Reuters Business
│   │   │   │                            - Economic Times
│   │   │   │                            - Moneycontrol Business
│   │   │   │                            - CNBC
│   │   │   │                            - MD5 duplicate detection
│   │   │   │
│   │   │   ├── market_data.py          • Yahoo Finance integration
│   │   │   │                            - Nifty 50 stocks
│   │   │   │                            - Top 5 gainers/losers
│   │   │   │                            - Sensex index
│   │   │   │
│   │   │   └── journal_generator.py    • Jinja2 HTML generation
│   │   │                                - generate_journal()
│   │   │                                - generate_journal_bytes()
│   │   │                                - get_journal_info()
│   │   │                                - get_generated_journals_list()
│   │   │
│   │   ├── data/                       ← Data storage
│   │   │   ├── finwiz.db               • SQLite database
│   │   │   └── journal_*.html          • Generated journal files
│   │   │
│   │   ├── test_data_fetching.py       ← Data fetching tests
│   │   ├── test_approval_dashboard.py  ← Dashboard workflow tests
│   │   ├── test_journal_generation.py  ← Journal generation tests
│   │   └── requirements.txt            ← Python dependencies
│
├── 🏃 Entry Points
│   ├── run.bat                         ← Windows startup script
│   └── run.sh                          ← Linux/Mac startup script
│
├── 📖 Documentation
│   └── README.md                       ← Project overview (ONLY markdown file)
│
└── ⚙️ Configuration
    ├── .gitignore                      ← Git configuration
    └── STRUCTURE.txt                   ← Legacy structure file
```

---

## 📊 Layer Breakdown

### Frontend Layer (`frontend/`)
**Purpose:** User interface and presentation

**Components:**
- `approval_dashboard.py` - Streamlit web application
  - 4 main tabs for workflow
  - Real-time data visualization
  - Professional dark theme
  - Color-coded status badges
  - Download functionality

- `templates/` - HTML/Jinja2 templates
  - Responsive layouts
  - Print-friendly styling
  - Professional design system
  - Dark theme (#0f172a)
  - Purple accents (#7c3aed)

**Responsibilities:**
- Display data to users
- Capture user input
- Handle downloads
- Manage UI state
- Render approval workflow

---

### Backend Layer (`backend/`)
**Purpose:** Business logic and data management

**Components:**

1. **app.py** - Main entry point
   - Streamlit configuration
   - Session state management
   - Dashboard startup

2. **modules/database.py** - Data persistence
   - SQLite database operations
   - CRUD operations
   - Statistics queries
   - Transaction handling

3. **modules/news_fetcher.py** - Data aggregation
   - RSS feed parsing (4 sources)
   - HTML tag removal
   - Duplicate detection via MD5
   - Data cleaning

4. **modules/market_data.py** - Market integration
   - Yahoo Finance API
   - Nifty 50 stocks
   - Index tracking
   - Top movers calculation

5. **modules/journal_generator.py** - Content generation
   - Jinja2 template rendering
   - HTML journal creation
   - File management
   - Metadata tracking

6. **data/** - Storage
   - SQLite database
   - Generated journals
   - Persistent data

7. **Tests** - Quality assurance
   - test_data_fetching.py
   - test_approval_dashboard.py
   - test_journal_generation.py

**Responsibilities:**
- Fetch data from external sources
- Manage database operations
- Generate content
- Handle business logic
- Provide data to frontend

---

## 🔄 Data Flow

```
External Sources
    ├─ Reuters RSS
    ├─ ET RSS
    ├─ Moneycontrol RSS
    ├─ CNBC RSS
    └─ Yahoo Finance API
         ↓
    news_fetcher.py (fetch)
    market_data.py (fetch)
         ↓
    database.py (store)
         ↓
    backend/data/finwiz.db
         ↓
    approval_dashboard.py (display)
         ↓
    User Reviews & Approves
         ↓
    journal_generator.py (render)
         ↓
    frontend/templates/ (template)
         ↓
    HTML Journal Generated
         ↓
    User Downloads
```

---

## 🎯 File Organization Strategy

### Why This Structure?

**Frontend Separation**
- ✅ Streamlit app in one place
- ✅ Templates organized together
- ✅ Easy to update UI
- ✅ Clear presentation layer

**Backend Separation**
- ✅ All business logic together
- ✅ Modules well-organized
- ✅ Tests co-located
- ✅ Data persistence separate
- ✅ Easy to maintain and extend

**Benefits**
1. **Clear Separation of Concerns** - UI vs Logic
2. **Easy Scaling** - Add more modules without cluttering root
3. **Better Testing** - Backend tests independent of UI
4. **Maintainability** - Related files grouped together
5. **Deployment Friendly** - Can deploy frontend/backend separately if needed

---

## 🚀 Running the Application

### Windows
```bash
run.bat
```

### Linux/Mac
```bash
bash run.sh
```

### Manual
```bash
cd backend
streamlit run app.py
```

---

## 📦 File Count Summary

| Component | Type | Count |
|-----------|------|-------|
| **Frontend** | Files | 2 |
| | Templates | 5 |
| **Backend** | Modules | 4 |
| | Tests | 3 |
| | Config | 1 |
| **Total** | | 18 |

---

## ✅ Organization Checklist

- [x] Removed all .md files (kept only README.md)
- [x] Created frontend/ directory
- [x] Moved UI files to frontend/
- [x] Created backend/ directory
- [x] Moved business logic to backend/
- [x] Organized templates
- [x] Organized modules
- [x] Organized tests
- [x] Created clean README.md
- [x] Verified structure

---

## 🔍 Key Files by Function

### Starting Point
→ `run.bat` or `run.sh` or `backend/app.py`

### Dashboard UI
→ `frontend/approval_dashboard.py`

### Data Management
→ `backend/modules/database.py`

### Data Fetching
→ `backend/modules/news_fetcher.py`
→ `backend/modules/market_data.py`

### Journal Creation
→ `backend/modules/journal_generator.py`

### HTML Templates
→ `frontend/templates/` (5 files)

### Testing
→ `backend/test_*.py` (3 files)

---

## 📊 Module Dependencies

```
approval_dashboard.py
├── → modules/database.py
├── → modules/journal_generator.py
├── → modules/market_data.py
└── → templates/

app.py
└── → approval_dashboard.py

journal_generator.py
├── → Jinja2
└── → templates/

news_fetcher.py
├── → database.py
└── → feedparser

market_data.py
├── → database.py
└── → yfinance

database.py
└── → sqlite3
```

---

## 🎓 Usage Examples

### As a Developer
```
1. Read README.md for overview
2. Check backend/modules/ for business logic
3. Check frontend/approval_dashboard.py for UI
4. Check frontend/templates/ for styling
5. Review backend/test_*.py for usage examples
```

### As an End User
```
1. Run: run.bat (Windows) or run.sh (Linux/Mac)
2. Dashboard opens in browser
3. Use 4 tabs: Pending News, Approved, Market Data, Generate Journal
4. Download generated HTML journals
```

### As Deployment
```
Frontend: Deploy frontend/approval_dashboard.py + frontend/templates/
Backend: Deploy backend/ + backend/requirements.txt
Database: backend/data/finwiz.db persists across runs
```

---

## 🔐 Access Patterns

**Frontend Access Backend Via:**
- Database queries through `backend/modules/database.py`
- Market data through `backend/modules/market_data.py`
- Journal generation through `backend/modules/journal_generator.py`

**Backend Access Patterns:**
- News fetcher → Database (persist)
- Market fetcher → Database (persist)
- Dashboard → Database (read/write)
- Generator → Database (read) + Templates (render)

---

## 📈 Future Scaling

This structure supports:
- Adding more frontend apps (e.g., API endpoint)
- Adding more backend modules (e.g., email, scheduling)
- Separating into microservices
- Adding Docker containerization
- Adding CI/CD pipelines

---

**Status:** ✅ Production Ready  
**Organization:** Optimized  
**Maintainability:** High
