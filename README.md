Here is a streamlined, professional version of your `README.md`. It focuses on functionality and architecture while removing the verbose "field details" to make it more readable for developers and stakeholders.

---

# IkimApp: Community Savings Group Manager (Ikimina)

A robust Python CLI application designed to digitize and automate **Ikimina** (informal savings groups) in Rwanda. This tool replaces manual paper records with a structured database to manage member contributions, rotating payout schedules (Merry-Go-Round), and financial reporting.

## 🏛 Database Schema

The system runs on a relational SQLite/MySQL structure to ensure data integrity:

* **members**: `member_id`, `member_name`, `email_address`, `phone_number`, `physical_address`, `date_added`.
* **transactions**: `transaction_id`, `member_id`, `amount`, `transaction_type` (savings, loan_repayment, interest), `tx_datetime`.
* **cycles**: `cycle_id`, `cycle_name`, `start_date`, `end_date`.
* **cycle_beneficiaries**: `cycle_benef_id`, `cycle_id`, `member_id`, `amount`, `received_funds` (boolean), `received_date`.
* **users**: `user_id`, `username`, `password`, `role` (admin, treasurer, member).

---

## 🚀 Key Modules & Features

### 1. Member Management
Handles the lifecycle of group participants.
* **Add Member**: Register new participants with automated contact validation.
* **Auto-Sync**: Adding or removing a member automatically triggers a regeneration of the 12-month Ikimina rotation.
* **Member Directory**: View a formatted list of all active participants and their join dates.

### 2. Ikimina Cycle Management
Automates the "Merry-Go-Round" logic based on a 12-month fiscal calendar.
* **Smart Scheduler**: Auto-generates beneficiary slots. (e.g., 4 members = 3 turns each per year; 12 members = 1 turn each).
* **Payout Tracking**: Record when the "pot" is handed over to the designated beneficiary with unique ID tracking.
* **Schedule Transparency**: View the full yearly rotation to see who benefits in which month.

### 3. Transaction & History
The financial core of the application.
* **Multi-Type Logging**: Record savings, loan repayments, and interest earned.
* **Advanced Filtering**: Search history by Member ID or specific Date Ranges ($YYYY-MM-DD$).
* **Audit Trail**: View all beneficiary records to verify past payouts.

### 4. Management Reporting
Data-driven insights for group administrators.
* **Top Savers**: Identifies the top 5 contributing members.
* **Loan Performance**: Summary of principal collected vs. interest generated.
* **Disbursement Status**: A progress report on how many members have received their cycle funds vs. those pending.
* **Cash Flow Summary**: A high-level overview of total liquidity within the system.

---

## 📂 Project Structure

```text
IkimApp/
├── main.py                 # Application entry point & Main Menu
├── database/
│   ├── db_connection.py    # Database drivers and execution helpers
│   └── schema.sql          # Table definitions
├── services/
│   ├── member.py           # Member CRUD & Menu
│   ├── cycle.py            # Ikimina rotation logic & Payouts
│   ├── transactions.py     # History and filtering logic
│   └── reports.py          # Management report generators
└── requirements.txt        # Project dependencies
```

---

## ⚙️ Installation & Usage

1.  **Clone the Repo**: `git clone https://github.com/youruser/ikimapp.git`
2.  **Install Dependencies**: `pip install -r requirements.txt`
3.  **Launch**: `python main.py`

> **Note**: On first launch, the admin will be prompted to set up credentials. All Ikimina rotations are calculated from the current date forward for 12 months.

---
**BSE Year 1 · African Leadership University · Kigali, Rwanda**

Would you like me to add a specific "User Roles" section to define what the Admin vs. Treasurer can access?