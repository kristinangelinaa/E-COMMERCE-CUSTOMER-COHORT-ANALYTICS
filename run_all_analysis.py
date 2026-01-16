"""
Run All Analysis Scripts
Author: Analytics Team
Date: 2026-01-16

This script runs all analysis steps in sequence with progress tracking.
"""

import subprocess
import sys
import time
from datetime import datetime

def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_script(script_name, description):
    """Run a Python script and track time"""
    print(f"▶ Starting: {description}")
    print(f"  Script: {script_name}")
    print(f"  Time: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 70)

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=True,
            text=True
        )

        elapsed_time = time.time() - start_time

        print(result.stdout)
        print(f"✓ Completed in {elapsed_time:.2f} seconds")
        return True

    except subprocess.CalledProcessError as e:
        elapsed_time = time.time() - start_time
        print(f"✗ Error occurred after {elapsed_time:.2f} seconds")
        print(f"Error output:\n{e.stderr}")
        return False

def main():
    """Run all analysis scripts"""
    print_banner("E-COMMERCE CUSTOMER & COHORT ANALYTICS")
    print("Running complete analysis pipeline...")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    total_start = time.time()

    # Define all scripts to run
    scripts = [
        ("01_data_cleaning.py", "Data Cleaning & Preparation"),
        ("02_cohort_analysis.py", "Customer Acquisition Cohort Analysis"),
        ("03_repeat_vs_onetime_buyers.py", "Repeat vs One-Time Buyers Analysis")
    ]

    results = []

    # Run each script
    for i, (script, description) in enumerate(scripts, 1):
        print_banner(f"Step {i}/{len(scripts)}: {description}")
        success = run_script(script, description)
        results.append((script, success))

        if not success:
            print("\n⚠ Warning: Script failed. Check the error messages above.")
            user_input = input("\nDo you want to continue with the next script? (y/n): ")
            if user_input.lower() != 'y':
                print("\n❌ Analysis pipeline stopped by user.")
                break

    # Summary
    total_elapsed = time.time() - total_start

    print_banner("ANALYSIS PIPELINE SUMMARY")

    print("Results:")
    for script, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {status}  {script}")

    successful = sum(1 for _, success in results if success)
    print(f"\nTotal: {successful}/{len(scripts)} scripts completed successfully")
    print(f"Total time: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)")

    if successful == len(scripts):
        print("\n🎉 All analysis completed successfully!")
        print("\nNext steps:")
        print("  1. Review the generated CSV files")
        print("  2. Run the Streamlit dashboard:")
        print("     streamlit run 04_streamlit_dashboard.py")
        print("  3. Build Tableau dashboard using TABLEAU_DASHBOARD_GUIDE.md")
    else:
        print("\n⚠ Some scripts failed. Please review the error messages above.")

    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Analysis interrupted by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
