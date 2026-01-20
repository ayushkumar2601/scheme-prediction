"""
Visualization Module for Policy Impact Analysis
Creates charts and plots for policy impact predictions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

class PolicyImpactVisualizer:
    """Create visualizations for policy impact analysis"""
    
    def __init__(self):
        self.colors = {
            'enrolment': '#2E86AB',
            'update': '#A23B72',
            'total': '#F18F01',
            'baseline': '#C73E1D'
        }
    
    def plot_time_series_impact(self, daily_impact: pd.DataFrame, policy_date: str, 
                               save_path: str = "time_series_impact.png"):
        """Plot time series of policy impact"""
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Convert date column
        daily_impact['date'] = pd.to_datetime(daily_impact['date'])
        policy_dt = pd.to_datetime(policy_date)
        
        # Plot 1: Total impact over time
        ax1 = axes[0]
        ax1.plot(daily_impact['date'], daily_impact['total_impact'], 
                color=self.colors['total'], linewidth=2, label='Total Impact')
        ax1.axvline(policy_dt, color='red', linestyle='--', linewidth=2, 
                   label=f'Policy Date: {policy_date}')
        ax1.fill_between(daily_impact['date'], 0, daily_impact['total_impact'], 
                        alpha=0.3, color=self.colors['total'])
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Number of People Affected', fontsize=12)
        ax1.set_title('Total Policy Impact Over Time', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Enrolment vs Update impact
        ax2 = axes[1]
        ax2.plot(daily_impact['date'], daily_impact['enrolment_impact'], 
                color=self.colors['enrolment'], linewidth=2, label='Enrolment Impact')
        ax2.plot(daily_impact['date'], daily_impact['update_impact'], 
                color=self.colors['update'], linewidth=2, label='Update Impact')
        ax2.axvline(policy_dt, color='red', linestyle='--', linewidth=2, 
                   label=f'Policy Date')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Number of People', fontsize=12)
        ax2.set_title('Enrolment vs Update Impact', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Time series plot saved to {save_path}")
        plt.close()
    
    def plot_regional_impact(self, regional_impact: Dict, top_n: int = 15,
                           save_path: str = "regional_impact.png"):
        """Plot regional impact distribution"""
        # Convert to DataFrame
        df = pd.DataFrame({
            'state': list(regional_impact['total_impact'].keys()),
            'total_impact': list(regional_impact['total_impact'].values()),
            'enrolment_impact': list(regional_impact['enrolment_impact'].values()),
            'update_impact': list(regional_impact['update_impact'].values())
        })
        
        # Sort and get top N
        df = df.sort_values('total_impact', ascending=False).head(top_n)
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Plot 1: Total impact by state
        ax1 = axes[0]
        bars = ax1.barh(df['state'], df['total_impact'], color=self.colors['total'])
        ax1.set_xlabel('Total People Affected', fontsize=12)
        ax1.set_ylabel('State', fontsize=12)
        ax1.set_title(f'Top {top_n} States by Total Impact', fontsize=14, fontweight='bold')
        ax1.invert_yaxis()
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2, 
                    f'{int(width):,}', ha='left', va='center', fontsize=9)
        
        # Plot 2: Stacked bar chart
        ax2 = axes[1]
        x = np.arange(len(df))
        width = 0.6
        
        ax2.barh(x, df['enrolment_impact'], width, label='Enrolment Impact',
                color=self.colors['enrolment'])
        ax2.barh(x, df['update_impact'], width, left=df['enrolment_impact'],
                label='Update Impact', color=self.colors['update'])
        
        ax2.set_yticks(x)
        ax2.set_yticklabels(df['state'])
        ax2.set_xlabel('Number of People', fontsize=12)
        ax2.set_title('Impact Breakdown: Enrolment vs Update', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.invert_yaxis()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Regional impact plot saved to {save_path}")
        plt.close()
    
    def plot_impact_heatmap(self, predictions: pd.DataFrame, policy_date: str,
                          save_path: str = "impact_heatmap.png"):
        """Create heatmap of impact by state and time"""
        # Filter post-policy data
        predictions['date'] = pd.to_datetime(predictions['date'])
        policy_dt = pd.to_datetime(policy_date)
        post_policy = predictions[predictions['date'] >= policy_dt].copy()
        
        if len(post_policy) == 0:
            print("No post-policy data for heatmap")
            return
        
        # Create week column
        post_policy['week'] = ((post_policy['date'] - policy_dt).dt.days // 7) + 1
        
        # Aggregate by state and week
        heatmap_data = post_policy.groupby(['state', 'week'])['total_impact'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='state', columns='week', values='total_impact')
        
        # Get top 20 states
        top_states = heatmap_pivot.sum(axis=1).nlargest(20).index
        heatmap_pivot = heatmap_pivot.loc[top_states]
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 10))
        sns.heatmap(heatmap_pivot, cmap='YlOrRd', annot=False, fmt='.0f', 
                   cbar_kws={'label': 'People Affected'}, ax=ax)
        ax.set_xlabel('Week After Policy', fontsize=12)
        ax.set_ylabel('State', fontsize=12)
        ax.set_title('Policy Impact Heatmap: State vs Time', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Impact heatmap saved to {save_path}")
        plt.close()
    
    def plot_cumulative_impact(self, daily_impact: pd.DataFrame, policy_date: str,
                             save_path: str = "cumulative_impact.png"):
        """Plot cumulative impact over time"""
        daily_impact = daily_impact.copy()
        daily_impact['date'] = pd.to_datetime(daily_impact['date'])
        
        # Calculate cumulative sums
        daily_impact['cumulative_enrolment'] = daily_impact['enrolment_impact'].cumsum()
        daily_impact['cumulative_update'] = daily_impact['update_impact'].cumsum()
        daily_impact['cumulative_total'] = daily_impact['total_impact'].cumsum()
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        ax.plot(daily_impact['date'], daily_impact['cumulative_total'], 
               color=self.colors['total'], linewidth=3, label='Total Cumulative Impact')
        ax.plot(daily_impact['date'], daily_impact['cumulative_enrolment'], 
               color=self.colors['enrolment'], linewidth=2, linestyle='--', 
               label='Cumulative Enrolment Impact')
        ax.plot(daily_impact['date'], daily_impact['cumulative_update'], 
               color=self.colors['update'], linewidth=2, linestyle='--', 
               label='Cumulative Update Impact')
        
        policy_dt = pd.to_datetime(policy_date)
        ax.axvline(policy_dt, color='red', linestyle='--', linewidth=2, 
                  label=f'Policy Date: {policy_date}')
        
        ax.fill_between(daily_impact['date'], 0, daily_impact['cumulative_total'], 
                       alpha=0.2, color=self.colors['total'])
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Cumulative People Affected', fontsize=12)
        ax.set_title('Cumulative Policy Impact', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Cumulative impact plot saved to {save_path}")
        plt.close()
    
    def create_summary_dashboard(self, results: Dict, save_path: str = "summary_dashboard.png"):
        """Create comprehensive summary dashboard"""
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        summary = results['summary']
        daily_impact = results['daily_impact']
        regional_impact = results['regional_impact']
        
        # Convert date
        daily_impact['date'] = pd.to_datetime(daily_impact['date'])
        policy_dt = pd.to_datetime(summary['policy_date'])
        
        # 1. Key metrics text
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.axis('off')
        metrics_text = f"""
        POLICY IMPACT SUMMARY
        
        Policy Date: {summary['policy_date']}
        Forecast Period: {summary['forecast_days']} days
        
        Total People Affected: {summary['total_people_affected']:,}
        
        Enrolment Increase: {summary['total_enrolment_increase']:,}
        Update Increase: {summary['total_update_increase']:,}
        
        Peak Impact Date: {summary['peak_impact_date']}
        Peak Daily Volume: {summary['peak_impact_volume']:,}
        
        Impact Duration: {summary['significant_impact_duration_days']} days
        """
        ax1.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 2. Time series
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(daily_impact['date'], daily_impact['total_impact'], 
                color=self.colors['total'], linewidth=2)
        ax2.axvline(policy_dt, color='red', linestyle='--', linewidth=1.5)
        ax2.set_title('Daily Impact Over Time', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('People Affected')
        ax2.grid(True, alpha=0.3)
        
        # 3. Top states
        ax3 = fig.add_subplot(gs[1, :])
        df_regional = pd.DataFrame({
            'state': list(regional_impact['total_impact'].keys()),
            'impact': list(regional_impact['total_impact'].values())
        }).sort_values('impact', ascending=False).head(10)
        
        bars = ax3.bar(df_regional['state'], df_regional['impact'], color=self.colors['total'])
        ax3.set_title('Top 10 Most Affected States', fontsize=12, fontweight='bold')
        ax3.set_xlabel('State')
        ax3.set_ylabel('Total People Affected')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Enrolment vs Update
        ax4 = fig.add_subplot(gs[2, 0])
        categories = ['Enrolment\nImpact', 'Update\nImpact']
        values = [summary['total_enrolment_increase'], summary['total_update_increase']]
        colors = [self.colors['enrolment'], self.colors['update']]
        ax4.bar(categories, values, color=colors)
        ax4.set_title('Impact Breakdown', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Number of People')
        
        # 5. Cumulative impact
        ax5 = fig.add_subplot(gs[2, 1])
        cumulative = daily_impact['total_impact'].cumsum()
        ax5.plot(daily_impact['date'], cumulative, color=self.colors['total'], linewidth=2)
        ax5.fill_between(daily_impact['date'], 0, cumulative, alpha=0.3, color=self.colors['total'])
        ax5.axvline(policy_dt, color='red', linestyle='--', linewidth=1.5)
        ax5.set_title('Cumulative Impact', fontsize=12, fontweight='bold')
        ax5.set_xlabel('Date')
        ax5.set_ylabel('Cumulative People Affected')
        ax5.grid(True, alpha=0.3)
        
        plt.suptitle('Aadhaar Policy Impact Analysis Dashboard', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Summary dashboard saved to {save_path}")
        plt.close()
    
    def generate_all_visualizations(self, results: Dict):
        """Generate all visualizations"""
        print("\n=== Generating Visualizations ===")
        
        self.plot_time_series_impact(results['daily_impact'], results['summary']['policy_date'])
        self.plot_regional_impact(results['regional_impact'])
        self.plot_cumulative_impact(results['daily_impact'], results['summary']['policy_date'])
        self.plot_impact_heatmap(results['full_predictions'], results['summary']['policy_date'])
        self.create_summary_dashboard(results)
        
        print("\nAll visualizations generated successfully!")

if __name__ == "__main__":
    # Example usage
    import pickle
    
    # Load results (assuming they exist)
    try:
        with open('prediction_results.pkl', 'rb') as f:
            results = pickle.load(f)
        
        viz = PolicyImpactVisualizer()
        viz.generate_all_visualizations(results)
    except FileNotFoundError:
        print("Run prediction_system.py first to generate results")
