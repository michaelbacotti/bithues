#!/usr/bin/env python3
"""
Dependability Holding P/L Tracker
================================
Run: python3 pl_tracker.py <command> [args]

Commands:
  add "Month Year" amount    (e.g., add "Jan 2026" 15000)
  print year                 (e.g., print 2026)
  show                      (show all)
  init                      (create empty CSV)
"""

import csv
import os
import sys
import subprocess

# Use absolute path to the CSV
CSV_FILE = '/Users/mike/.openclaw/workspace/dependability-holding-llc/dependability_pl_tracker.csv'

def load_csv():
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    return rows

def save_csv(rows):
    if len(rows) == 0:
        fields = ['Month','Net_PL','Carryforward_In','Carryforward_Out','GP_Fee','Profit_Share','Bacotti_Total','YTD_Total']
    else:
        fields = list(rows[0].keys())
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def init():
    save_csv([])
    print("Initialized empty tracker.")

def add_entry(month, net_pl):
    rows = load_csv()
    
    # Get carryforward from last entry
    carry_in = float(rows[-1]['Carryforward_Out']) if rows else 0
    
    # Calculate per rules
    gp_fee = 1000
    net_after_carry = net_pl - carry_in
    profit_share = max(0, net_after_carry * 0.2)
    bacotti_total = gp_fee + profit_share
    
    # YTD - sum of all Bacotti_Total to date
    ytd = sum(float(r['Bacotti_Total']) for r in rows) + bacotti_total
    
    carry_out = max(0, carry_in - net_pl)
    
    new_row = {
        'Month': month,
        'Net_PL': net_pl,
        'Carryforward_In': carry_in,
        'Carryforward_Out': carry_out,
        'GP_Fee': gp_fee,
        'Profit_Share': round(profit_share, 2),
        'Bacotti_Total': round(bacotti_total, 2),
        'YTD_Total': round(ytd, 2)
    }
    
    rows.append(new_row)
    save_csv(rows)
    
    print(f"Updated {month}")
    print(f"Net P/L: ${net_pl:,.2f}")
    print(f"GP Fee: ${gp_fee}")
    print(f"Profit Share: ${profit_share:,.2f}")
    print(f"Bacotti Total: ${bacotti_total:,.2f}")
    print(f"YTD Total: ${ytd:,.2f}")
    print_table(rows[-6:])

def print_year(year):
    rows = load_csv()
    if not rows:
        print("No data.")
        return
    
    filtered = [r for r in rows if year in r['Month']]
    
    if not filtered:
        print(f"No data for {year}")
        return
    
    print(f"\n=== {year} ===\n")
    print_table(filtered)
    total = sum(float(r['Bacotti_Total']) for r in filtered)
    print(f"\nYTD Total: ${total:,.2f}")

def show():
    rows = load_csv()
    if not rows:
        print("No data. Use 'init' to create tracker.")
    else:
        print_table(rows)
        total = sum(float(r['Bacotti_Total']) for r in rows)
        print(f"\nAll-time Total: ${total:,.2f}")

def print_table(rows):
    if not rows:
        return
    # Simple table
    print(f"{'Month':<12} {'Net P/L':>10} {'Carry In':>10} {'GP Fee':>8} {'Share':>10} {'Total':>10} {'YTD':>10}")
    print("-" * 70)
    for r in rows:
        print(f"{r['Month']:<12} ${float(r['Net_PL']):>9,.0f} ${float(r['Carryforward_In']):>9,.0f} ${float(r['GP_Fee']):>7,.0f} ${float(r['Profit_Share']):>9,.0f} ${float(r['Bacotti_Total']):>9,.0f} ${float(r['YTD_Total']):>9,.0f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "init":
        init()
    elif cmd == "show":
        show()
    elif cmd == "add" and len(sys.argv) >= 4:
        month = sys.argv[2]
        try:
            amount = float(sys.argv[3])
            add_entry(month, amount)
        except ValueError:
            print("Invalid amount. Use: add 'Jan 2026' 15000")
    elif cmd == "print" and len(sys.argv) >= 3:
        year = sys.argv[2]
        print_year(year)
    else:
        print(__doc__)
