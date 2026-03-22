"""
API Routes for Aadhaar Policy Impact Prediction System
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import traceback

from services.prediction_service import PredictionService
from services.database_service import DatabaseService

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

@api_bp.route('/predict', methods=['POST'])
def predict_policy_impact():
    """
    Predict policy impact
    
    Expected JSON payload:
    {
        "policy_date": "2025-04-01",
        "forecast_days": 60,
        "compliance_level": 0.8,
        "policy_name": "New Aadhaar Policy",
        "affected_states": ["Karnataka", "Maharashtra"] (optional)
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        
        # Required fields
        required_fields = ['policy_date', 'forecast_days', 'compliance_level']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate data types and ranges
        try:
            policy_date = datetime.strptime(data['policy_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            forecast_days = int(data['forecast_days'])
            compliance_level = float(data['compliance_level'])
            
            if forecast_days < 1 or forecast_days > 365:
                return jsonify({"error": "forecast_days must be between 1 and 365"}), 400
            
            if compliance_level < 0.0 or compliance_level > 1.0:
                return jsonify({"error": "compliance_level must be between 0.0 and 1.0"}), 400
                
        except ValueError as e:
            return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
        
        # Optional fields
        policy_name = data.get('policy_name', f'Policy {policy_date}')
        affected_states = data.get('affected_states', None)
        
        # Get prediction service
        prediction_service = PredictionService()
        
        # Generate predictions
        logger.info(f"Generating prediction for policy_date={policy_date}, forecast_days={forecast_days}")
        
        results = prediction_service.predict_policy_impact(
            policy_date=policy_date,
            forecast_days=forecast_days,
            compliance_level=compliance_level,
            affected_states=affected_states
        )
        
        # Store prediction in database
        try:
            db_service = DatabaseService()
            prediction_id = db_service.store_prediction(
                policy_date=policy_date,
                forecast_days=forecast_days,
                compliance_level=compliance_level,
                results=results,
                policy_name=policy_name,
                affected_states=affected_states
            )
            results['prediction_id'] = prediction_id
            logger.info(f"Stored prediction with ID: {prediction_id}")
        except Exception as e:
            logger.warning(f"Failed to store prediction in database: {str(e)}")
            # Continue without storing - don't fail the request
        
        return jsonify({
            "success": True,
            "results": results,
            "metadata": {
                "policy_date": policy_date,
                "forecast_days": forecast_days,
                "compliance_level": compliance_level,
                "policy_name": policy_name,
                "affected_states": affected_states,
                "generated_at": datetime.utcnow().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": "Prediction failed",
            "message": str(e)
        }), 500

@api_bp.route('/states', methods=['GET'])
def get_states():
    """Get list of available states"""
    try:
        # Official list of 28 States + 8 UTs
        official_states = [
            # States (28)
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
            'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
            'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
            # Union Territories (8)
            'Andaman and Nicobar Islands', 'Chandigarh',
            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi',
            'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
        ]
        
        return jsonify({
            "success": True,
            "states": sorted(official_states)
        })
        
    except Exception as e:
        logger.error(f"States endpoint error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch states"
        }), 500

@api_bp.route('/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    """Get stored prediction by ID"""
    try:
        db_service = DatabaseService()
        prediction = db_service.get_prediction(prediction_id)
        
        if not prediction:
            return jsonify({
                "success": False,
                "error": "Prediction not found"
            }), 404
        
        return jsonify({
            "success": True,
            "prediction": prediction
        })
        
    except Exception as e:
        logger.error(f"Get prediction error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch prediction"
        }), 500

@api_bp.route('/predictions', methods=['GET'])
def list_predictions():
    """List recent predictions with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 10)), 100)  # Max 100 per page
        
        db_service = DatabaseService()
        predictions = db_service.list_predictions(page=page, limit=limit)
        
        return jsonify({
            "success": True,
            "predictions": predictions,
            "pagination": {
                "page": page,
                "limit": limit
            }
        })
        
    except Exception as e:
        logger.error(f"List predictions error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch predictions"
        }), 500