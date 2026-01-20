"""
Policy Scenario Builder - Flask Web Application
Interactive web interface for Aadhaar policy impact prediction
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from prediction_system import PolicyImpactPredictor
from visualization import PolicyImpactVisualizer

app = Flask(__name__)

# Global predictor instance (loaded once)
predictor = None

def initialize_predictor():
    """Initialize the predictor on first request"""
    global predictor
    if predictor is None:
        print("Initializing predictor...")
        predictor = PolicyImpactPredictor()
        predictor.load_and_prepare_data(use_cached=True)
        
        # Train baseline models
        try:
            predictor.baseline_model.load_models()
            print("Loaded existing baseline models")
        except:
            print("Training baseline models...")
            predictor.train_baseline()
    return predictor

@app.route('/')
def index():
    """Main page - Policy Scenario Builder"""
    return render_template('index.html')

@app.route('/api/states', methods=['GET'])
def get_states():
    """Get list of available states - ONLY official 28 states + 8 UTs"""
    
    # Official list of 28 States + 8 UTs (hardcoded - no data dependency)
    official_states = [
        # States (28)
        'Andhra Pradesh',
        'Arunachal Pradesh',
        'Assam',
        'Bihar',
        'Chhattisgarh',
        'Goa',
        'Gujarat',
        'Haryana',
        'Himachal Pradesh',
        'Jharkhand',
        'Karnataka',
        'Kerala',
        'Madhya Pradesh',
        'Maharashtra',
        'Manipur',
        'Meghalaya',
        'Mizoram',
        'Nagaland',
        'Odisha',
        'Punjab',
        'Rajasthan',
        'Sikkim',
        'Tamil Nadu',
        'Telangana',
        'Tripura',
        'Uttar Pradesh',
        'Uttarakhand',
        'West Bengal',
        # Union Territories (8)
        'Andaman and Nicobar Islands',
        'Chandigarh',
        'Dadra and Nagar Haveli and Daman and Diu',
        'Delhi',
        'Jammu and Kashmir',
        'Ladakh',
        'Lakshadweep',
        'Puducherry'
    ]
    
    # Return only official states (already sorted)
    return jsonify({'states': sorted(official_states)})

@app.route('/api/predict', methods=['POST'])
def predict_policy_impact():
    """
    Main prediction endpoint
    Receives policy parameters and returns predictions
    """
    try:
        # Get policy parameters from request
        data = request.json
        
        policy_name = data.get('policy_name', 'New Policy')
        policy_date = data.get('policy_date')
        policy_type = data.get('policy_type', 'Both')
        age_groups = data.get('age_groups', [])
        gender = data.get('gender', 'All')
        states = data.get('states', [])
        districts = data.get('districts', [])
        compliance_level = float(data.get('compliance_level', 0.8))
        forecast_days = int(data.get('forecast_days', 60))
        
        # Validate inputs
        if not policy_date:
            return jsonify({'error': 'Policy date is required'}), 400
        
        # Initialize predictor
        pred = initialize_predictor()
        
        # Train policy model for this date
        print(f"Training policy model for {policy_date}...")
        pred.train_policy_model(policy_date)
        
        # Generate predictions
        print(f"Generating predictions...")
        results = pred.predict_policy_impact(
            policy_date=policy_date,
            forecast_days=forecast_days
        )
        
        # Apply filters based on policy parameters
        filtered_results = apply_policy_filters(
            results, 
            policy_type, 
            age_groups, 
            states, 
            compliance_level
        )
        
        # Prepare response
        response = {
            'success': True,
            'policy_name': policy_name,
            'policy_date': policy_date,
            'summary': {
                'total_people_affected': int(filtered_results['total_affected']),
                'total_enrolments': int(filtered_results['total_enrolments']),
                'total_updates': int(filtered_results['total_updates']),
                'peak_date': filtered_results['peak_date'],
                'peak_volume': int(filtered_results['peak_volume']),
                'duration_days': int(filtered_results['duration'])
            },
            'regional_impact': filtered_results['regional_data'],
            'daily_impact': filtered_results['daily_data'],
            'risk_assessment': filtered_results['risk_levels']
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def apply_policy_filters(results, policy_type, age_groups, states, compliance_level):
    """
    Apply policy-specific filters to results
    """
    summary = results['summary']
    regional = results['regional_impact']
    daily = results['daily_impact']
    
    # Apply compliance level adjustment
    compliance_factor = compliance_level
    
    # Calculate filtered totals - ensure positive values
    total_enrolments = max(0, summary['total_enrolment_increase'] * compliance_factor)
    total_updates = max(0, summary['total_update_increase'] * compliance_factor)
    
    # Apply policy type filter
    if policy_type == 'Enrolment':
        total_updates = 0
    elif policy_type == 'Update':
        total_enrolments = 0
    
    total_affected = total_enrolments + total_updates
    
    # Official list of valid states
    valid_states = {
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
        'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
        'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
        'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
        'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
        'Andaman and Nicobar Islands', 'Chandigarh',
        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi',
        'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
    }
    
    # Filter regional data - ONLY official states
    regional_data = []
    for state in regional['total_impact'].keys():
        # STRICT CHECK: Only include if in official list
        if state not in valid_states:
            continue
            
        # Skip if specific states selected and this state not in list
        if states and 'All States' not in states and state not in states:
            continue
        
        enrol_impact = max(0, regional['enrolment_impact'][state] * compliance_factor)
        update_impact = max(0, regional['update_impact'][state] * compliance_factor)
        
        if policy_type == 'Enrolment':
            update_impact = 0
        elif policy_type == 'Update':
            enrol_impact = 0
        
        total_impact = enrol_impact + update_impact
        
        if total_impact > 0:
            # Calculate percentage increase (mock calculation)
            baseline = 10000  # Mock baseline
            pct_increase = (total_impact / baseline) * 100
            
            # Determine risk level
            if pct_increase > 50:
                risk_level = 'High'
            elif pct_increase > 25:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            regional_data.append({
                'state': state,
                'predicted_enrolments': int(enrol_impact),
                'predicted_updates': int(update_impact),
                'total_impact': int(total_impact),
                'pct_increase': round(pct_increase, 1),
                'risk_level': risk_level
            })
    
    # Sort by total impact
    regional_data.sort(key=lambda x: x['total_impact'], reverse=True)
    
    # Prepare daily data - ensure positive values
    daily_data = []
    for _, row in daily.iterrows():
        enrol = max(0, row['enrolment_impact'] * compliance_factor)
        update = max(0, row['update_impact'] * compliance_factor)
        
        if policy_type == 'Enrolment':
            update = 0
        elif policy_type == 'Update':
            enrol = 0
        
        daily_data.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'enrolments': int(enrol),
            'updates': int(update),
            'total': int(enrol + update)
        })
    
    # Find peak - ensure positive
    if daily_data:
        peak_day = max(daily_data, key=lambda x: x['total'])
        peak_date = peak_day['date']
        peak_volume = max(0, peak_day['total'])
    else:
        peak_date = policy_date
        peak_volume = 0
    
    # Calculate duration
    if daily_data and total_affected > 0:
        avg_daily = total_affected / len(daily_data) if len(daily_data) > 0 else 0
        significant_days = [d for d in daily_data if d['total'] > avg_daily]
        duration = len(significant_days)
    else:
        duration = 0
    
    # Risk assessment
    risk_levels = {
        'high_risk_states': [r['state'] for r in regional_data if r['risk_level'] == 'High'],
        'medium_risk_states': [r['state'] for r in regional_data if r['risk_level'] == 'Medium'],
        'low_risk_states': [r['state'] for r in regional_data if r['risk_level'] == 'Low']
    }
    
    return {
        'total_affected': max(0, total_affected),
        'total_enrolments': max(0, total_enrolments),
        'total_updates': max(0, total_updates),
        'peak_date': peak_date,
        'peak_volume': max(0, peak_volume),
        'duration': max(0, duration),
        'regional_data': regional_data,
        'daily_data': daily_data,
        'risk_levels': risk_levels
    }

@app.route('/api/visualize', methods=['POST'])
def generate_visualization():
    """Generate visualization for the prediction"""
    try:
        data = request.json
        daily_data = data.get('daily_data', [])
        regional_data = data.get('regional_data', [])
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Time series
        if daily_data:
            dates = [d['date'] for d in daily_data]
            totals = [d['total'] for d in daily_data]
            axes[0, 0].plot(dates, totals, linewidth=2, color='#2E86AB')
            axes[0, 0].set_title('Daily Impact Over Time', fontweight='bold')
            axes[0, 0].set_xlabel('Date')
            axes[0, 0].set_ylabel('People Affected')
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Top states
        if regional_data:
            top_states = regional_data[:10]
            states = [r['state'] for r in top_states]
            impacts = [r['total_impact'] for r in top_states]
            axes[0, 1].barh(states, impacts, color='#F18F01')
            axes[0, 1].set_title('Top 10 Affected States', fontweight='bold')
            axes[0, 1].set_xlabel('People Affected')
            axes[0, 1].invert_yaxis()
        
        # Plot 3: Enrolment vs Update
        if regional_data:
            top_states = regional_data[:10]
            states = [r['state'] for r in top_states]
            enrols = [r['predicted_enrolments'] for r in top_states]
            updates = [r['predicted_updates'] for r in top_states]
            
            x = np.arange(len(states))
            width = 0.35
            axes[1, 0].bar(x - width/2, enrols, width, label='Enrolments', color='#2E86AB')
            axes[1, 0].bar(x + width/2, updates, width, label='Updates', color='#A23B72')
            axes[1, 0].set_title('Enrolment vs Update Impact', fontweight='bold')
            axes[1, 0].set_xticks(x)
            axes[1, 0].set_xticklabels(states, rotation=45, ha='right')
            axes[1, 0].legend()
        
        # Plot 4: Risk levels
        if regional_data:
            risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}
            for r in regional_data:
                risk_counts[r['risk_level']] += 1
            
            colors = {'High': '#C73E1D', 'Medium': '#F18F01', 'Low': '#06A77D'}
            axes[1, 1].pie(
                risk_counts.values(),
                labels=risk_counts.keys(),
                autopct='%1.1f%%',
                colors=[colors[k] for k in risk_counts.keys()],
                startangle=90
            )
            axes[1, 1].set_title('Risk Level Distribution', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}'
        })
        
    except Exception as e:
        print(f"Error generating visualization: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Policy Scenario Builder...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
