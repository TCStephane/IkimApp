 Project Structure
IkimApp/
│
├── README.md                # Project overview, setup instructions, usage
├── requirements.txt         # Dependencies (if any, e.g., for database or formatting)
├── config.py                # Configuration variables (e.g., database file path, default settings)
│
├── main.py                  # Entry point for the application (runs the CLI menu)
│
├── database/
│   ├── db.py                # Functions to initiali.wze DB, connect, and run queries
│   └── schema.sql           # Optional: SQL schema for setting up SQLite tables
│
├── models/
│   ├── member.py            # Member class and related methods
│   ├── contribution.py      # Contribution class and methods
│   └── cycle.py             # Cycle management class
│
├── services/
│   ├── auth.py              # Password authentication and login handling
│   ├── reports.py           # Functions to generate reports and summaries
│   └── utils.py             # Helper functions (input validation, formatting, etc.)
│
├── tests/
│   ├── test_member.py       # Unit tests for member functionality
│   ├── test_contribution.py # Unit tests for contributions
│   └── test_cycle.py        # Unit tests for cycle tracking
│
└── data/
    └── ikimapp.db           # SQLite database file (generated when app runs) 