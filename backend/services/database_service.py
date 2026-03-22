"""
Database Service for Aadhaar Policy Impact Prediction System
Handles Supabase PostgreSQL integration
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logging.warning("Supabase client not available. Database features will be disabled.")

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for database operations with Supabase"""
    
    def __init__(self):
        self.client = None
        if SUPABASE_AVAILABLE:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client"""
        try:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            if not url or not key:
                logger.warning("Supabase credentials not found. Database features will be disabled.")
                return
            
            self.client = create_client(url, key)
            logger.info("Supabase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            self.client = None
    
    def test_connection(self) -> bool:
        """Test database connection"""
        if not self.client:
            return False
        
        try:
            # Try to query the predictions table
            result = self.client.table('predictions').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False
    
    def create_predictions_table(self):
        """Create predictions table if it doesn't exist"""
        if not self.client:
            logger.warning("Database client not available")
            return False
        
        try:
            # Note: In production, you should create tables via Supabase dashboard or migrations
            # This is just for reference - the SQL would be:
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                policy_date DATE NOT NULL,
                forecast_days INTEGER NOT NULL,
                compliance_level DECIMAL(3,2) NOT NULL,
                policy_name VARCHAR(255),
                affected_states JSONB,
                results_json JSONB NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            CREATE INDEX idx_predictions_policy_date ON predictions(policy_date);
            CREATE INDEX idx_predictions_created_at ON predictions(created_at);
            """
            logger.info("Predictions table should be created via Supabase dashboard")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create predictions table: {str(e)}")
            return False
    
    def store_prediction(self, 
                        policy_date: str,
                        forecast_days: int,
                        compliance_level: float,
                        results: Dict,
                        policy_name: Optional[str] = None,
                        affected_states: Optional[List[str]] = None) -> Optional[int]:
        """
        Store prediction results in database
        
        Args:
            policy_date: Policy implementation date
            forecast_days: Number of forecast days
            compliance_level: Compliance level used
            results: Prediction results dictionary
            policy_name: Optional policy name
            affected_states: Optional list of affected states
            
        Returns:
            Prediction ID if successful, None otherwise
        """
        if not self.client:
            logger.warning("Database client not available - cannot store prediction")
            return None
        
        try:
            data = {
                'policy_date': policy_date,
                'forecast_days': forecast_days,
                'compliance_level': compliance_level,
                'policy_name': policy_name,
                'affected_states': affected_states,
                'results_json': results,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            result = self.client.table('predictions').insert(data).execute()
            
            if result.data and len(result.data) > 0:
                prediction_id = result.data[0]['id']
                logger.info(f"Stored prediction with ID: {prediction_id}")
                return prediction_id
            else:
                logger.error("Failed to store prediction - no data returned")
                return None
                
        except Exception as e:
            logger.error(f"Failed to store prediction: {str(e)}")
            return None
    
    def get_prediction(self, prediction_id: int) -> Optional[Dict]:
        """
        Get prediction by ID
        
        Args:
            prediction_id: Prediction ID
            
        Returns:
            Prediction data if found, None otherwise
        """
        if not self.client:
            logger.warning("Database client not available")
            return None
        
        try:
            result = self.client.table('predictions').select('*').eq('id', prediction_id).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                return None
                
        except Exception as e:
            logger.error(f"Failed to get prediction {prediction_id}: {str(e)}")
            return None
    
    def list_predictions(self, page: int = 1, limit: int = 10) -> List[Dict]:
        """
        List recent predictions with pagination
        
        Args:
            page: Page number (1-based)
            limit: Number of results per page
            
        Returns:
            List of prediction summaries
        """
        if not self.client:
            logger.warning("Database client not available")
            return []
        
        try:
            offset = (page - 1) * limit
            
            result = self.client.table('predictions').select(
                'id, policy_date, forecast_days, compliance_level, policy_name, created_at'
            ).order('created_at', desc=True).range(offset, offset + limit - 1).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Failed to list predictions: {str(e)}")
            return []
    
    def delete_prediction(self, prediction_id: int) -> bool:
        """
        Delete prediction by ID
        
        Args:
            prediction_id: Prediction ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("Database client not available")
            return False
        
        try:
            result = self.client.table('predictions').delete().eq('id', prediction_id).execute()
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete prediction {prediction_id}: {str(e)}")
            return False
    
    def get_predictions_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Get predictions within date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of predictions
        """
        if not self.client:
            logger.warning("Database client not available")
            return []
        
        try:
            result = self.client.table('predictions').select('*').gte(
                'policy_date', start_date
            ).lte('policy_date', end_date).order('policy_date').execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Failed to get predictions by date range: {str(e)}")
            return []
    
    def update_prediction(self, prediction_id: int, updates: Dict) -> bool:
        """
        Update prediction record
        
        Args:
            prediction_id: Prediction ID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("Database client not available")
            return False
        
        try:
            updates['updated_at'] = datetime.utcnow().isoformat()
            
            result = self.client.table('predictions').update(updates).eq('id', prediction_id).execute()
            return True
            
        except Exception as e:
            logger.error(f"Failed to update prediction {prediction_id}: {str(e)}")
            return False