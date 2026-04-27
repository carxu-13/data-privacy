import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

RESULTS_FILE = "experiment_results.csv"

def generate_report():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: {RESULTS_FILE} not found. Run experiment.py first.")
        return

    df = pd.read_csv(RESULTS_FILE)

    # Basic summary
    summary = df.groupby(['mode', 'case_type']).agg({
        'attempted_read': ['mean', 'count'],
        'successful_read': 'mean',
        'asr': 'mean',
        'tcr': 'mean',
        'format_failure': 'mean'
    }).reset_index()

    # Flatten columns
    summary.columns = ['mode', 'case_type', 'attempted_read', 'count', 'successful_read', 'asr', 'tcr', 'format_failure']

    print("\n" + "="*80)
    print("ENHANCED EXPERIMENT RESULTS SUMMARY")
    print("="*80)
    print(summary.to_string(index=False))
    print("="*80)

    # Breakdown by Attack Type
    print("\nADVERSARIAL BREAKDOWN BY ATTACK TYPE:")
    adv_df = df[df['case_type'] == 'adversarial']
    attack_summary = adv_df.groupby(['mode', 'attack_type']).agg({
        'attempted_read': 'mean',
        'asr': 'mean'
    }).reset_index()
    print(attack_summary.to_string(index=False))

    # Breakdown by Difficulty
    print("\nADVERSARIAL BREAKDOWN BY DIFFICULTY:")
    diff_summary = adv_df.groupby(['mode', 'difficulty']).agg({
        'attempted_read': 'mean',
        'asr': 'mean'
    }).reset_index()
    print(diff_summary.to_string(index=False))

    # Visualization
    try:
        # Increase global font sizes for better readability
        plt.rcParams.update({'font.size': 12})
        plt.rcParams.update({'axes.titlesize': 14})
        plt.rcParams.update({'axes.labelsize': 12})
        plt.rcParams.update({'xtick.labelsize': 11})
        plt.rcParams.update({'ytick.labelsize': 11})
        plt.rcParams.update({'legend.fontsize': 11})

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Plot 1: Behavior Layers (Adversarial)
        adv_modes = adv_df['mode'].unique()
        modes_summary = adv_df.groupby('mode').agg({
            'attempted_read': 'mean',
            'successful_read': 'mean',
            'asr': 'mean'
        }).reindex(adv_modes)

        modes_summary.plot(kind='bar', ax=ax1, color=['#ffcc00', '#ff6600', '#cc0000'])
        ax1.set_title("Behavior Layers (Adversarial)", pad=15)
        ax1.set_ylabel("Rate")
        ax1.set_ylim(0, 1.1)
        ax1.legend(["Attempted Access", "Content in Context", "Final Disclosure (ASR)"])
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        ax1.tick_params(axis='x', rotation=45)

        # Plot 2: Utility vs Security (TCR vs ASR)
        benign_df = df[df['case_type'] == 'benign']
        utility_summary = benign_df.groupby('mode')['tcr'].mean()
        security_summary = adv_df.groupby('mode')['asr'].mean()
        
        comparison = pd.DataFrame({
            'Utility (TCR)': utility_summary,
            'Security (1-ASR)': 1 - security_summary
        })
        
        comparison.plot(kind='bar', ax=ax2, color=['#3399ff', '#00cc66'])
        ax2.set_title("Utility (TCR) vs Security (1-ASR)", pad=15)
        ax2.set_ylabel("Rate")
        ax2.set_ylim(0, 1.1)
        ax2.legend(loc='lower right')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig("experiment_results.png")
        print("\nVisualization saved to experiment_results.png")
        
        # Plot 3: Attack Type Breakdown
        plt.figure(figsize=(12, 7))
        attack_pivot = attack_summary.pivot(index='mode', columns='attack_type', values='asr')
        ax3 = plt.gca()
        attack_pivot.plot(kind='bar', ax=ax3)
        plt.title("ASR by Attack Type and Defense", pad=15)
        plt.ylabel("ASR")
        plt.ylim(0, 1.1)
        plt.legend(title="Attack Type", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("attack_type_breakdown.png")
        print("Attack type breakdown saved to attack_type_breakdown.png")

    except Exception as e:
        print(f"\nCould not generate plot: {e}")

if __name__ == "__main__":
    generate_report()
