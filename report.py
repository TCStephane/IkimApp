import sqlite3
from tabulate import tabulate
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
DB_FILE = "ikimapp.db"  # Path to your SQLite database file


# ============================================
# DATABASE CONNECTION UTILS
# ============================================
def connect_db():
    """Establish a connection to the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


# ============================================
# DATA FETCHING FUNCTIONS
# ============================================
def fetch_member_contributions(conn):
    """
    Pulls each member’s total contributions and missed payments.
    Assumes database tables:
      - members(id, name)
      - contributions(id, member_id, amount, date, cycle)
    """
    cursor = conn.cursor()

    # Fetching member data and contributions
    query = """
        SELECT 
            m.id,
            m.name,
            COALESCE(SUM(c.amount), 0) AS total_contribution,
            COUNT(c.id) AS num_contributions
        FROM members m
        LEFT JOIN contributions c ON m.id = c.member_id
        GROUP BY m.id
        ORDER BY m.name ASC;
    """
    cursor.execute(query)
    return cursor.fetchall()


def fetch_summary_totals(conn):
    """Summarises the total savings and number of transactions."""
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM contributions;")
    total_amount, num_records = cursor.fetchone()
    return total_amount, num_records


# ============================================
# REPORT GENERATION
# ============================================
def generate_report():
    """Generates and prints the community savings report."""
    conn = connect_db()
    if not conn:
        print("Could not connect to the database.")
        return

    # Get data from DB
    members = fetch_member_contributions(conn)
    total_savings, total_records = fetch_summary_totals(conn)

    # Prepare table
    headers = ["Member ID", "Member Name", "Total Contribution (RWF)", "Payments Made"]
    table = [
        [m[0], m[1], f"{m[2]:,.0f}", m[3]] for m in members
    ]

    # Display header info
    print("\n==============================================")
    print("             IKIMAPP GENERAL REPORT           ")
    print("==============================================")
    print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==============================================\n")

    if not table:
        print("No member data available. Please record contributions first.\n")
    else:
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        print("\n----------------------------------------------")
        print(f"Total Savings Recorded : {total_savings:,.2f} RWF")
        print(f"Number of Payments Made: {total_records}")
        print("----------------------------------------------")

    print("\n Report generation complete.\n")
    conn.close()


# ============================================
# MAIN RUNNER
# ============================================
if __name__ == "__main__":
    generate_report()
