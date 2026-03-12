IkimApp — Community Savings Group Manager

A Python CLI application to digitise and automate the management of community savings groups (ikimina) in Rwanda.


📌 Overview
Informal savings groups — known locally as ikimina — are a vital financial tool for millions of Rwandans, especially women and low-income earners who lack access to formal banking. These groups operate on a simple principle: members make regular equal contributions each cycle, and one member collects the pooled total. Today, most of these groups still rely on pen and paper, which leads to errors, disputes, and lost records.
IkimApp solves this by bringing the entire process to the command line. It gives group administrators a simple, offline tool to manage members, record contributions, track cycles, and generate reports — no internet connection required.

🎯 Project Context
FieldDetailsInstitutionAfrican Leadership University (ALU), Kigali, RwandaProgrammeBSc Software Engineering — Year 1, Trimester 2Project TypePeer Learning Project 1 (PLP-1)GCGO AlignmentEconomic Opportunity · Financial Inclusion · Women's EmpowermentTarget DeadlineApril 1, 2026

✨ Features
#FeatureDescription0Password AuthenticationAdmin password required on startup to protect financial data1Manage MembersAdd, view, and remove savings group members2Record ContributionLog member payments per cycle; flags missed contributions3View Cycle StatusShows current cycle recipient and payment status of all members4Generate ReportPrints a formatted summary of contributions, balances, and cycle activity5Transaction HistoryChronological per-member log of all contributions and activity

🗂️ Project Structure
ikimapp/
├── main.py                  # Entry point — displays the main menu
├── database.py              # Sets up SQLite database and all tables
├── members.py               # Feature 1: member management logic
├── contributions.py         # Feature 2: contribution recording logic
├── cycle_status.py          # Feature 3: cycle tracking logic
├── reports.py               # Feature 4: report generation logic
├── transaction_history.py   # Feature 5: transaction history logic
└── ikimapp.db               # SQLite database file (auto-created on first run)

🏛️ Architecture
IkimApp follows a three-layer architecture:
┌─────────────────────────────────┐
│         CLI Layer (main.py)     │  ← User interaction via menu prompts
├─────────────────────────────────┤
│      Business Logic Layer       │  ← Feature modules (members, contributions, etc.)
├─────────────────────────────────┤
│    Data Layer (database.py)     │  ← SQLite persistent storage
└─────────────────────────────────┘
Database Schema
members
member_id | name | phone | join_date | is_active
contributions
contrib_id | member_id | amount | date_paid | cycle_number
cycles
cycle_id | cycle_number | start_date | end_date | recipient_member_id | expected_amount

⚙️ Requirements

Python 3.8 or higher
No external libraries required — uses Python's built-in sqlite3 module only
No internet connection required
Compatible with Windows, macOS, and Linux


🚀 Getting Started
1. Clone the repository
bashgit clone https://github.com/<your-team-repo>/ikimapp.git
cd ikimapp
2. Run the application
bashpython main.py
3. On first launch, the database file ikimapp.db will be created automatically. You will be prompted to enter the admin password to access the main menu.

🧭 Usage
When the application starts, you will see:
Welcome to IkimApp — Community Savings Group Manager
Enter your admin password to continue:
After authentication, the main menu is displayed:
========= MAIN MENU =========
1. Manage Members
2. Record Contribution
3. View Cycle Status
4. Generate Report
5. Transaction History
6. Exit
Navigate using number keys and press Enter to confirm. Every screen includes a Back option to return to the previous menu.

👥 Team
NameFeature Assigned(Member 1)Feature 1 — Manage Members(Member 2)Feature 2 — Record Contribution(Member 3)Feature 3 — View Cycle Status(Member 4)Feature 4 — Generate Report(Member 5)Feature 5 — Transaction History

BSE Year 1 · Cohort 2 · Group 4 · African Leadership University


📚 References

The New Times (2023). How Equity Ikimina Account is formalising collective saving for inclusive growth.
allAfrica.com (2025). Informal savings systems such as ikimina have supported households for decades.
Republic of Rwanda, Ministry of Finance (2024). Rwanda FinScope Survey 2024.
ForAfrika (2025). Digitalising Hope: How Digitalising VSLA Groups is Promoting Financial Inclusion in Rwanda.
