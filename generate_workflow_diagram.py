"""
Generate System Workflow Diagram
Creates a professional workflow diagram of the Aadhaar Policy Impact Prediction System
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Color scheme - Professional blues
color_data = '#e3f2fd'
color_process = '#bbdefb'
color_model = '#90caf9'
color_output = '#64b5f6'
color_interface = '#42a5f5'
color_arrow = '#1565c0'
color_text = '#0d47a1'

# Title
ax.text(5, 11.5, 'Aadhaar Policy Impact Prediction System', 
        ha='center', va='top', fontsize=22, fontweight='bold', color=color_text)
ax.text(5, 11.1, 'End-to-End Workflow Architecture', 
        ha='center', va='top', fontsize=14, color='#1976d2')

# Helper function to create boxes
def create_box(ax, x, y, width, height, text, color, fontsize=10, fontweight='normal'):
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.1",
                         edgecolor=color_arrow,
                         facecolor=color,
                         linewidth=2)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
           ha='center', va='center', fontsize=fontsize, 
           fontweight=fontweight, color=color_text, wrap=True)

# Helper function to create arrows
def create_arrow(ax, x1, y1, x2, y2, label=''):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->,head_width=0.4,head_length=0.4',
                           color=color_arrow,
                           linewidth=2.5,
                           zorder=1)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 0.2, mid_y, label, fontsize=8, 
               color=color_arrow, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                        edgecolor=color_arrow, linewidth=1))

# ============= LAYER 1: DATA SOURCES =============
y_data = 9.5
ax.text(5, y_data + 0.8, '1. DATA SOURCES', ha='center', fontsize=12, 
       fontweight='bold', color=color_text,
       bbox=dict(boxstyle='round,pad=0.5', facecolor=color_data, 
                edgecolor=color_arrow, linewidth=2))

create_box(ax, 0.5, y_data - 0.5, 2.5, 0.8, 
          'Enrolment Data\n(Date, State, District,\nAge Groups)', 
          color_data, fontsize=9, fontweight='bold')
create_box(ax, 3.5, y_data - 0.5, 2.5, 0.8, 
          'Biometric Updates\n(Date, State, District,\nAge Groups)', 
          color_data, fontsize=9, fontweight='bold')
create_box(ax, 6.5, y_data - 0.5, 2.5, 0.8, 
          'Demographic Updates\n(Date, State, District,\nAge Groups)', 
          color_data, fontsize=9, fontweight='bold')

# ============= LAYER 2: DATA PROCESSING =============
y_process = 7.5
create_arrow(ax, 1.75, y_data - 0.5, 2.5, y_process + 0.8)
create_arrow(ax, 4.75, y_data - 0.5, 4, y_process + 0.8)
create_arrow(ax, 7.75, y_data - 0.5, 5.5, y_process + 0.8)

ax.text(5, y_process + 1.3, '2. DATA PROCESSING', ha='center', fontsize=12, 
       fontweight='bold', color=color_text,
       bbox=dict(boxstyle='round,pad=0.5', facecolor=color_process, 
                edgecolor=color_arrow, linewidth=2))

create_box(ax, 2, y_process, 6, 0.8, 
          'Data Loader: Clean, Standardize States, Aggregate by Date & Region\ndata_loader.py', 
          color_process, fontsize=9, fontweight='bold')

# ============= MASTER DATASET =============
y_master = 6.2
create_arrow(ax, 5, y_process, 5, y_master + 0.5)

create_box(ax, 2.5, y_master, 5, 0.5, 
          'Master Dataset (CSV)\n3,853 records | 36 States/UTs | Time Series', 
          '#fff9c4', fontsize=9, fontweight='bold')

# ============= LAYER 3: FEATURE ENGINEERING =============
y_feature = 5
create_arrow(ax, 5, y_master, 5, y_feature + 0.8)

ax.text(5, y_feature + 1.3, '3. FEATURE ENGINEERING', ha='center', fontsize=12, 
       fontweight='bold', color=color_text,
       bbox=dict(boxstyle='round,pad=0.5', facecolor=color_model, 
                edgecolor=color_arrow, linewidth=2))

create_box(ax, 1.5, y_feature, 7, 0.8, 
          'Feature Engineer: 40+ Features (Temporal, Lag, Rolling Avg, Growth Rate, Policy Indicators)\nfeature_engineering.py', 
          color_model, fontsize=9, fontweight='bold')

# ============= LAYER 4: MODEL TRAINING =============
y_model = 3.5
create_arrow(ax, 5, y_feature, 3, y_model + 0.8)
create_arrow(ax, 5, y_feature, 7, y_model + 0.8)

ax.text(5, y_model + 1.3, '4. MACHINE LEARNING MODELS', ha='center', fontsize=12, 
       fontweight='bold', color=color_text,
       bbox=dict(boxstyle='round,pad=0.5', facecolor=color_model, 
                edgecolor=color_arrow, linewidth=2))

create_box(ax, 0.5, y_model, 3.5, 0.8, 
          'Baseline Model\nGradient Boosting Regressor\nNormal Behavior Prediction\nbaseline_model.py', 
          color_model, fontsize=8.5, fontweight='bold')

create_box(ax, 5.5, y_model, 3.5, 0.8, 
          'Policy Impact Model\nInterrupted Time Series\nPolicy Effect Estimation\npolicy_impact_model.py', 
          color_model, fontsize=8.5, fontweight='bold')

# ============= LAYER 5: PREDICTION SYSTEM =============
y_predict = 2
create_arrow(ax, 2.25, y_model, 3.5, y_predict + 0.5)
create_arrow(ax, 7.25, y_model, 6.5, y_predict + 0.5)

ax.text(5, y_predict + 1, '5. PREDICTION ENGINE', ha='center', fontsize=12, 
       fontweight='bold', color=color_text,
       bbox=dict(boxstyle='round,pad=0.5', facecolor=color_output, 
                edgecolor=color_arrow, linewidth=2))

create_box(ax, 2.5, y_predict, 5, 0.5, 
          'Prediction System: Scenario Simulation & Impact Calculation\nprediction_system.py', 
          color_output, fontsize=9, fontweight='bold')

# ============= LAYER 6: WEB INTERFACE =============
y_web = 0.5
create_arrow(ax, 5, y_predict, 5, y_web + 0.8)

ax.text(5, y_web + 1.3, '6. USER INTERFACE', ha='center', fontsize=12, 
       fontweight='bold', color=color_text,
       bbox=dict(boxstyle='round,pad=0.5', facecolor=color_interface, 
                edgecolor=color_arrow, linewidth=2))

create_box(ax, 1, y_web, 3.5, 0.8, 
          'Flask Web Application\nPolicy Input Form\nReal-time Predictions\napp.py', 
          color_interface, fontsize=9, fontweight='bold')

create_box(ax, 5.5, y_web, 3.5, 0.8, 
          'Visualization Engine\nCharts & Regional Maps\nBento Box Dashboard\nvisualization.py', 
          color_interface, fontsize=9, fontweight='bold')

# ============= OUTPUT INDICATORS =============
# Add output boxes at the bottom
output_y = -0.5
create_box(ax, 0.5, output_y, 1.8, 0.4, 
          'Total Affected', '#e8f5e9', fontsize=8, fontweight='bold')
create_box(ax, 2.5, output_y, 1.8, 0.4, 
          'Peak Volume', '#e8f5e9', fontsize=8, fontweight='bold')
create_box(ax, 4.5, output_y, 1.8, 0.4, 
          'Duration', '#e8f5e9', fontsize=8, fontweight='bold')
create_box(ax, 6.5, output_y, 1.8, 0.4, 
          'Regional Impact', '#e8f5e9', fontsize=8, fontweight='bold')
create_box(ax, 8.5, output_y, 1, 0.4, 
          'Risk Levels', '#e8f5e9', fontsize=8, fontweight='bold')

# Add arrows from web interface to outputs
create_arrow(ax, 2.75, y_web, 1.4, output_y + 0.4)
create_arrow(ax, 7.25, y_web, 7.4, output_y + 0.4)

# ============= SIDE ANNOTATIONS =============
# Left side - Key Technologies
ax.text(0.2, 10.5, 'KEY TECHNOLOGIES', fontsize=10, fontweight='bold', 
       color=color_text, rotation=0)
ax.text(0.2, 10.1, '• Python 3.x', fontsize=8, color=color_text)
ax.text(0.2, 9.8, '• Scikit-learn', fontsize=8, color=color_text)
ax.text(0.2, 9.5, '• Pandas/NumPy', fontsize=8, color=color_text)
ax.text(0.2, 9.2, '• Flask', fontsize=8, color=color_text)
ax.text(0.2, 8.9, '• Matplotlib', fontsize=8, color=color_text)

# Right side - Key Metrics
ax.text(9.8, 10.5, 'KEY METRICS', fontsize=10, fontweight='bold', 
       color=color_text, rotation=0, ha='right')
ax.text(9.8, 10.1, '3,853 Records', fontsize=8, color=color_text, ha='right')
ax.text(9.8, 9.8, '36 States/UTs', fontsize=8, color=color_text, ha='right')
ax.text(9.8, 9.5, '40+ Features', fontsize=8, color=color_text, ha='right')
ax.text(9.8, 9.2, '2 ML Models', fontsize=8, color=color_text, ha='right')
ax.text(9.8, 8.9, 'Real-time Viz', fontsize=8, color=color_text, ha='right')

# Add legend at bottom
legend_elements = [
    mpatches.Patch(facecolor=color_data, edgecolor=color_arrow, label='Data Layer'),
    mpatches.Patch(facecolor=color_process, edgecolor=color_arrow, label='Processing'),
    mpatches.Patch(facecolor=color_model, edgecolor=color_arrow, label='ML Models'),
    mpatches.Patch(facecolor=color_output, edgecolor=color_arrow, label='Prediction'),
    mpatches.Patch(facecolor=color_interface, edgecolor=color_arrow, label='Interface'),
]
ax.legend(handles=legend_elements, loc='lower center', ncol=5, 
         frameon=True, fontsize=9, bbox_to_anchor=(0.5, -0.15))

# Add footer
ax.text(5, -1.2, 'Aadhaar Policy Impact Prediction System | ML-Powered Decision Support', 
       ha='center', fontsize=10, color='#666', style='italic')

plt.tight_layout()
plt.savefig('system_workflow_diagram.png', dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')
print("✓ Workflow diagram saved as 'system_workflow_diagram.png'")
plt.close()

# Also create a simplified version
fig2, ax2 = plt.subplots(1, 1, figsize=(14, 8))
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 8)
ax2.axis('off')

# Simplified title
ax2.text(5, 7.5, 'System Workflow - Simplified View', 
        ha='center', va='top', fontsize=20, fontweight='bold', color=color_text)

# Simplified flow
y_pos = 6.5
create_box(ax2, 2, y_pos, 6, 0.7, 
          '1. DATA COLLECTION\nEnrolment + Biometric + Demographic Data', 
          color_data, fontsize=10, fontweight='bold')

create_arrow(ax2, 5, y_pos, 5, y_pos - 0.8)

y_pos = 5
create_box(ax2, 2, y_pos, 6, 0.7, 
          '2. DATA PROCESSING\nClean, Standardize, Aggregate', 
          color_process, fontsize=10, fontweight='bold')

create_arrow(ax2, 5, y_pos, 5, y_pos - 0.8)

y_pos = 3.5
create_box(ax2, 2, y_pos, 6, 0.7, 
          '3. FEATURE ENGINEERING\n40+ Temporal & Policy Features', 
          color_model, fontsize=10, fontweight='bold')

create_arrow(ax2, 5, y_pos, 5, y_pos - 0.8)

y_pos = 2
create_box(ax2, 2, y_pos, 6, 0.7, 
          '4. ML PREDICTION\nBaseline + Policy Impact Models', 
          color_model, fontsize=10, fontweight='bold')

create_arrow(ax2, 5, y_pos, 5, y_pos - 0.8)

y_pos = 0.5
create_box(ax2, 2, y_pos, 6, 0.7, 
          '5. WEB INTERFACE\nInteractive Dashboard with Visualizations', 
          color_interface, fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('system_workflow_simplified.png', dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')
print("✓ Simplified workflow diagram saved as 'system_workflow_simplified.png'")
plt.close()

print("\n✓ Both diagrams generated successfully!")
print("  - system_workflow_diagram.png (detailed)")
print("  - system_workflow_simplified.png (simplified)")
