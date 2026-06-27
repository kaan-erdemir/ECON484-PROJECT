import os
import sys
import subprocess


def run_step(script_name, description):
    print(f"\n[RUNNING] {description} ({script_name})...")

    script_path = os.path.join("code", script_name)
    if not os.path.exists(script_path):
        print(f"[ERROR] {script_name} not found! Path: {script_path}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd="code",
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[SUCCESS] {script_name} completed successfully.")

        if result.stdout:
            lines = result.stdout.strip().split('\n')
            summary = "\n".join(lines[-5:]) if len(lines) > 5 else result.stdout
            print(f"--- Output Summary ---\n{summary}\n----------------------")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[CRITICAL ERROR] {script_name} crashed during execution!")
        print(f"Error Details:\n{e.stderr}")
        return False


def main():
    print("   GLOBAL SUPPLY CHAIN SYSTEMIC RISK INDEX PIPELINE     ")

    pipeline_steps = [
        # phase 1
        ("data_extraction.py", "IMF DOTS API Integration & Raw Data Fetching"),
        ("preprocessing.py", "Missing Value Handling & Log Transformation"),
        ("baseline_kmeans.py", "Baseline Model Execution & K-Means Assignment"),
        ("evaluate_kmeans.py", "Qualitative Assessment of K-Means Flaws"),
        ("distance_justification.py", "Hierarchical Distance Metric Justification"),

        # phase 2
        ("hierarchical.py", "Wide Matrix Pivot and Hierarchical Clustering"),
        ("tax_havens_parsing.py", "Dendrogram Parsing and Hub Isolation"),
        ("vulnerability_alignment.py", "Macroeconomic Vulnerability Integration"),
        ("structural_misalignment.py", "Structural Misalignment Score Calculation"),
        ("systemic_risk_index.py", "Final Systemic Risk Index (SRI) Matrix"),
        ("generate_splits.py", "Data Cutoffs for Concept Drift Analysis (Splits)")
    ]

    for script, desc in pipeline_steps:
        success = run_step(script, desc)
        if not success:
            print("\n[STOP] Pipeline halted due to an error. Please check the error details above.")
            sys.exit(1)

    print("\n==================================================================")
    print("The entire end-to-end pipeline executed successfully.")
    print("Final Output: '../cleaned_data/systemic_risk_index_matrix.csv'")
    print("Temporal Splits: Ready in the '../splits/' directory.")
    print("==================================================================")


if __name__ == "__main__":
    main()