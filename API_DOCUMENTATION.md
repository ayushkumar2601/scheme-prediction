# API Documentation - Aadhaar Policy Impact Prediction System

## Base URL

- **Production**: `https://your-render-service.onrender.com`
- **Development**: `http://localhost:10000`

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Content Type

All requests and responses use `application/json` content type.

## Rate Limiting

- **Default**: 60 requests per minute per IP
- **Prediction endpoint**: Additional timeout of 120 seconds

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable

## Endpoints

### 1. Health Check

Check API health and service status.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok",
  "database": "connected",
  "models": "loaded",
  "timestamp": "2025-03-22T10:00:00Z"
}
```

**Example**:
```bash
curl https://your-api.onrender.com/health
```

---

### 2. Get States

Retrieve list of available Indian states and union territories.

**Endpoint**: `GET /api/states`

**Response**:
```json
{
  "success": true,
  "states": [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry"
  ]
}
```

**Example**:
```bash
curl https://your-api.onrender.com/api/states
```

---

### 3. Generate Prediction

Generate policy impact prediction based on input parameters.

**Endpoint**: `POST /api/predict`

**Request Body**:
```json
{
  "policy_date": "2025-04-01",
  "forecast_days": 60,
  "compliance_level": 0.8,
  "policy_name": "New Aadhaar Update Policy",
  "affected_states": ["Karnataka", "Maharashtra"]
}
```

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `policy_date` | string | Yes | Policy implementation date (YYYY-MM-DD) |
| `forecast_days` | integer | Yes | Number of days to forecast (1-365) |
| `compliance_level` | number | Yes | Expected compliance rate (0.0-1.0) |
| `policy_name` | string | No | Name of the policy |
| `affected_states` | array | No | List of affected states (empty = all states) |

**Response**:
```json
{
  "success": true,
  "results": {
    "summary": {
      "total_people_affected": 1250000,
      "total_enrolment_impact": 750000,
      "total_update_impact": 500000,
      "average_daily_impact": 20833,
      "policy_date": "2025-04-01",
      "forecast_days": 60
    },
    "daily_impact": [
      {
        "date": "2025-04-01",
        "enrolment_impact": 12500,
        "update_impact": 8300,
        "total_impact": 20800
      }
    ],
    "regional_impact": {
      "by_state": [
        {
          "state": "Uttar Pradesh",
          "enrolment_impact": 125000,
          "update_impact": 83000,
          "total_impact": 208000
        }
      ],
      "top_10_states": [
        {
          "state": "Uttar Pradesh",
          "enrolment_impact": 125000,
          "update_impact": 83000,
          "total_impact": 208000
        }
      ],
      "total_impact": {
        "Uttar Pradesh": 208000,
        "Maharashtra": 156000
      },
      "enrolment_impact": {
        "Uttar Pradesh": 125000,
        "Maharashtra": 94000
      },
      "update_impact": {
        "Uttar Pradesh": 83000,
        "Maharashtra": 62000
      }
    },
    "peak_analysis": {
      "peak_date": "2025-04-15",
      "peak_volume": 45000,
      "peak_enrolments": 27000,
      "peak_updates": 18000
    },
    "risk_assessment": {
      "high_impact_states": ["Uttar Pradesh", "Maharashtra", "Bihar"],
      "states_at_risk": 3,
      "risk_level": "High"
    }
  },
  "metadata": {
    "policy_date": "2025-04-01",
    "forecast_days": 60,
    "compliance_level": 0.8,
    "policy_name": "New Aadhaar Update Policy",
    "affected_states": ["Karnataka", "Maharashtra"],
    "generated_at": "2025-03-22T10:00:00Z",
    "prediction_id": 123
  }
}
```

**Example**:
```bash
curl -X POST https://your-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "policy_date": "2025-04-01",
    "forecast_days": 60,
    "compliance_level": 0.8,
    "policy_name": "New Aadhaar Update Policy"
  }'
```

**Validation Errors**:

```json
{
  "success": false,
  "error": "Missing required field: policy_date"
}
```

```json
{
  "success": false,
  "error": "forecast_days must be between 1 and 365"
}
```

```json
{
  "success": false,
  "error": "compliance_level must be between 0.0 and 1.0"
}
```

---

### 4. Get Prediction by ID

Retrieve a stored prediction by its ID.

**Endpoint**: `GET /api/predictions/{prediction_id}`

**Path Parameters**:
- `prediction_id` (integer): The prediction ID

**Response**:
```json
{
  "success": true,
  "prediction": {
    "id": 123,
    "policy_date": "2025-04-01",
    "forecast_days": 60,
    "compliance_level": 0.8,
    "policy_name": "New Aadhaar Update Policy",
    "affected_states": ["Karnataka", "Maharashtra"],
    "results_json": { /* full prediction results */ },
    "created_at": "2025-03-22T10:00:00Z",
    "updated_at": "2025-03-22T10:00:00Z"
  }
}
```

**Example**:
```bash
curl https://your-api.onrender.com/api/predictions/123
```

**Error Response** (404):
```json
{
  "success": false,
  "error": "Prediction not found"
}
```

---

### 5. List Predictions

Retrieve a paginated list of recent predictions.

**Endpoint**: `GET /api/predictions`

**Query Parameters**:
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Results per page (default: 10, max: 100)

**Response**:
```json
{
  "success": true,
  "predictions": [
    {
      "id": 123,
      "policy_date": "2025-04-01",
      "forecast_days": 60,
      "compliance_level": 0.8,
      "policy_name": "New Aadhaar Update Policy",
      "created_at": "2025-03-22T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10
  }
}
```

**Example**:
```bash
curl "https://your-api.onrender.com/api/predictions?page=1&limit=5"
```

---

## Data Models

### Summary Data

```typescript
interface SummaryData {
  total_people_affected: number      // Total expected impact
  total_enrolment_impact: number     // New enrollments expected
  total_update_impact: number        // Updates expected
  average_daily_impact: number       // Daily average impact
  policy_date: string               // Policy implementation date
  forecast_days: number             // Forecast period
}
```

### Daily Impact

```typescript
interface DailyImpact {
  date: string                      // Date (YYYY-MM-DD)
  enrolment_impact: number          // Enrollment impact for this date
  update_impact: number             // Update impact for this date
  total_impact: number              // Total impact for this date
}
```

### Regional Impact

```typescript
interface RegionalData {
  state: string                     // State name
  enrolment_impact: number          // Enrollment impact for state
  update_impact: number             // Update impact for state
  total_impact: number              // Total impact for state
}
```

### Peak Analysis

```typescript
interface PeakAnalysis {
  peak_date: string                 // Date of peak impact
  peak_volume: number               // Peak daily volume
  peak_enrolments: number           // Peak enrollments on peak date
  peak_updates: number              // Peak updates on peak date
}
```

### Risk Assessment

```typescript
interface RiskAssessment {
  high_impact_states: string[]      // States with high impact
  states_at_risk: number            // Number of high-impact states
  risk_level: string                // "Low", "Medium", or "High"
}
```

## Error Codes

### Validation Errors (400)

- `MISSING_REQUIRED_FIELD`: Required field is missing
- `INVALID_DATE_FORMAT`: Date format is invalid (must be YYYY-MM-DD)
- `INVALID_RANGE`: Numeric value is outside valid range
- `INVALID_STATE`: State name is not recognized

### Server Errors (500)

- `MODEL_LOADING_ERROR`: ML models failed to load
- `PREDICTION_ERROR`: Error during prediction generation
- `DATABASE_ERROR`: Database operation failed

### Not Found Errors (404)

- `PREDICTION_NOT_FOUND`: Requested prediction ID doesn't exist

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **General endpoints**: 60 requests per minute per IP
- **Prediction endpoint**: 10 requests per minute per IP (due to computational cost)

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640995200
```

## CORS Policy

The API supports Cross-Origin Resource Sharing (CORS) for the following origins:

- `http://localhost:3000` (development)
- `https://*.vercel.app` (Vercel deployments)
- Configured production frontend URL

## Performance Notes

- **Prediction endpoint**: Typically takes 30-60 seconds to complete
- **Health check**: Responds in < 1 second
- **States endpoint**: Responds in < 1 second
- **Database queries**: Typically < 5 seconds

## SDK Examples

### JavaScript/TypeScript

```typescript
const API_URL = 'https://your-api.onrender.com'

async function predictPolicyImpact(request: PredictionRequest) {
  const response = await fetch(`${API_URL}/api/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return await response.json()
}
```

### Python

```python
import requests

API_URL = 'https://your-api.onrender.com'

def predict_policy_impact(request_data):
    response = requests.post(
        f'{API_URL}/api/predict',
        json=request_data,
        timeout=120
    )
    response.raise_for_status()
    return response.json()
```

### cURL

```bash
# Generate prediction
curl -X POST https://your-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "policy_date": "2025-04-01",
    "forecast_days": 60,
    "compliance_level": 0.8
  }'

# Get states
curl https://your-api.onrender.com/api/states

# Health check
curl https://your-api.onrender.com/health
```

## Changelog

### v1.0.0 (2025-03-22)
- Initial API release
- Prediction generation endpoint
- States listing endpoint
- Health check endpoint
- Database integration
- Basic error handling and validation