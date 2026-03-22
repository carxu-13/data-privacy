import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_FILE = "experiment_results.csv"

def generate_report():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: {RESULTS_FILE} not found. Run experiment.py first.")
        return

    df = pd.read_csv(RESULTS_FILE)

    # Ensure all required columns exist for older runs
    for col in ['asr', 'pcr', 'udr', 'tcr', 'completion_score', 'status']:
        if col not in df.columns:
            df[col] = 0.0 if col != 'status' else "Unknown"

    # Calculate metrics by defense mode and case type
    summary = df.groupby(['mode', 'case_type']).agg({
        'asr': 'mean',
        'pcr': 'mean',
        'udr': 'mean',
        'tcr': 'mean',
        'completion_score': 'mean'
    }).reset_index()

    print("\n" + "="*70)
    print("EXPERIMENT RESULTS SUMMARY")
    print("="*70)
    print(summary.to_string(index=False))
    print("="*70)

    # Specific look at adversarial cases
    adv_summary = summary[summary['case_type'] == 'adversarial']
    
    print("\nATTACK COMPLETION METRICS BY DEFENSE:")
    print(f"{'Mode':20} | {'ASR (Full)':>10} | {'Completion':>10}")
    print("-" * 45)
    for _, row in adv_summary.iterrows():
        print(f"{row['mode']:20} | {row['asr']*100:9.1f}% | {row['completion_score']*100:9.1f}%")

    # Show example status for each mode (adversarial)
    print("\nMOST RECENT STATUS (Adversarial):")
    for mode in df['mode'].unique():
        mode_adv = df[(df['mode'] == mode) & (df['case_type'] == 'adversarial')]
        if not mode_adv.empty:
            last_status = mode_adv.iloc[-1]['status']
            print(f"{mode:20}: {last_status}")

    print("\nBENIGN UTILITY METRICS BY DEFENSE:")
    print(f"{'Mode':20} | {'TCR (Utility)':>12}")
    print("-" * 35)
    benign_summary = summary[summary['case_type'] == 'benign']
    for _, row in benign_summary.iterrows():
        print(f"{row['mode']:20} | {row['tcr']*100:11.1f}%")

    # Generate a plot
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot 1: Attack Progress (ASR vs Completion Score)
        adv_summary.plot(x='mode', y=['asr', 'completion_score'], kind='bar', ax=ax1, color=['red', 'orange'])
        ax1.set_title("Attack Severity (ASR vs Completion Score)")
        ax1.set_ylabel("Rate (0.0 - 1.0)")
        ax1.set_ylim(0, 1.1)
        ax1.legend(["Full Exfiltration (ASR)", "Attack Progress (Completion)"])
        
        # Plot 2: Utility (TCR)
        benign_summary.plot(x='mode', y='tcr', kind='bar', ax=ax2, color='skyblue', legend=False)
        ax2.set_title("Benign Task Utility (TCR)")
        ax2.set_ylabel("Rate (0.0 - 1.0)")
        ax2.set_ylim(0, 1.1)
        
        plt.tight_layout()
        plt.savefig("experiment_results.png")
        print("\nVisualization saved to experiment_results.png")
    except Exception as e:
        print(f"\nCould not generate plot: {e}")

if __name__ == "__main__":
    generate_report()
