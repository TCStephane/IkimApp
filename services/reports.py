from database.db_connection import DB_CONNECTION, DB_CURSOR
from datetime import datetime

# --- REPORT 1: TOP SAVERS ---
def report_top_savers():
    """Identifies and displays the top 5 members with the highest cumulative savings."""
    print("\n--- [Report] Top 5 Savers ---")
    
    query = """
        SELECT m.member_name, SUM(t.amount) as total_savings
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        WHERE t.transaction_type = 'savings'
        GROUP BY m.member_id
        ORDER BY total_savings DESC
        LIMIT 5
    """
    
    try:
        # Using a dictionary cursor for readability (as seen in your template)
        cursor = DB_CONNECTION.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No savings data found.")
        else:
            print(f"{'Member Name':<25} | {'Total Savings':>15}")
            print("-" * 43)
            for row in results:
                print(f"{row['member_name']:<25} | {row['total_savings']:>15.2f}")
        
        cursor.close()
    except Exception as e:
        print(f"Error generating Top Savers report: {e}")

# --- REPORT 2: LOAN & INTEREST REVENUE ---
def report_loan_performance():
    """Summarizes loan_repayments vs. interest collected from members."""
    print("\n--- [Report] Loan & Interest Revenue ---")
    
    query = """
        SELECT m.member_name, 
               SUM(CASE WHEN t.transaction_type = 'loan_repayment' THEN t.amount ELSE 0 END) as loan_repayments,
               SUM(CASE WHEN t.transaction_type = 'interest' THEN t.amount ELSE 0 END) as interest
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        GROUP BY m.member_id
        HAVING loan_repayments > 0 OR interest > 0
        ORDER BY interest DESC
    """
    
    try:
        cursor = DB_CONNECTION.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No loan repayment history found.")
        else:
            print(f"{'Member Name':<20} | {'loan_repayments Paid':>15} | {'Interest Paid':>15}")
            print("-" * 56)
            for row in results:
                print(f"{row['member_name']:<20} | {row['loan_repayments']:>15.2f} | {row['interest']:>15.2f}")
        
        cursor.close()
    except Exception as e:
        print(f"Error generating Loan Performance report: {e}")

# --- REPORT 3: CYCLE DISBURSEMENT SUMMARY ---
def report_cycle_summary():
    """Provides a status update on funds disbursed for each cycle."""
    print("\n--- [Report] Cycle Disbursement Progress ---")
    
    query = """
        SELECT c.cycle_name, 
               COUNT(cb.cycle_benef_id) as total_spots,
               SUM(CASE WHEN cb.received_funds = 1 THEN 1 ELSE 0 END) as paid_spots,
               SUM(cb.amount) as total_to_disburse
        FROM cycles c
        LEFT JOIN cycle_beneficiaries cb ON c.cycle_id = cb.cycle_id
        GROUP BY c.cycle_id
    """
    
    try:
        cursor = DB_CONNECTION.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"{'Cycle Name':<20} | {'Progress':<10} | {'Total Commitment':>18}")
        print("-" * 54)
        for row in results:
            progress = f"{row['paid_spots'] or 0}/{row['total_spots'] or 0}"
            commitment = row['total_to_disburse'] or 0.00
            print(f"{row['cycle_name']:<20} | {progress:<10} | {commitment:>18.2f}")
            
        cursor.close()
    except Exception as e:
        print(f"Error generating Cycle Summary: {e}")

# --- REPORT 4: OVERALL CASH FLOW ---
def report_cash_flow():
    """High-level summary of all funds currently in the system by type."""
    print("\n--- [Report] General Cash Flow Summary ---")
    
    query = "SELECT transaction_type, SUM(amount) as total FROM transactions GROUP BY transaction_type"
    
    try:
        cursor = DB_CONNECTION.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        
        grand_total = 0
        for row in results:
            label = row['transaction_type'].replace('_', ' ').title()
            print(f"{label:<20}: {row['total']:>15.2f}")
            grand_total += row['total']
            
        print("-" * 38)
        print(f"{'NET SYSTEM FUNDS':<20}: {grand_total:>15.2f}")
        cursor.close()
    except Exception as e:
        print(f"Error calculating cash flow: {e}")

# --- MAIN MENU FOR REPORTS ---
def reports_menu():
    """ 
    Menu-driven interface for management to view various reports.
    This function should be imported and called from your main app file.
    """
    while True:
        print("\n--- Management Reporting System ---")
        print("1. Top 5 Savers")
        print("2. Loan & Interest Performance")
        print("3. Cycle Disbursement Status")
        print("4. General Cash Flow Summary")
        print("5. Return to Admin Menu")

        choice = input("Choose a report to generate: ").strip()

        if choice == "1":
            report_top_savers()
        elif choice == "2":
            report_loan_performance()
        elif choice == "3":
            report_cycle_summary()
        elif choice == "4":
            report_cash_flow()
        elif choice == "5":
            print("Returning to Admin Menu...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")