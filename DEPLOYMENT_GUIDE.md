# Deployment Guide - Aadhaar Policy Impact Prediction System

This guide provides step-by-step instructions for deploying the Aadhaar Policy Impact Prediction System to production using Vercel (frontend) and Render (backend) with Supabase (database).

## Architecture Overview

```
Frontend (Vercel) → Backend API (Render) → Database (Supabase PostgreSQL)
```

## Prerequisites

- Node.js 18+ installed locally
- Python 3.10+ installed locally
- Git repository access
- Accounts on:
  - [Vercel](https://vercel.com)
  - [Render](https://render.com)
  - [Supabase](https://supabase.com)

## 1. Database Setup (Supabase)

### Step 1: Create Supabase Project

1. Go to [Supabase](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose organization and enter project details:
   - Name: `aadhaar-policy-prediction`
   - Database Password: Generate a strong password
   - Region: Choose closest to your users
4. Wait for project creation (2-3 minutes)

### Step 2: Create Database Table

1. Go to your project dashboard
2. Click "SQL Editor" in the sidebar
3. Run this SQL to create the predictions table:

```sql
-- Create predictions table
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

-- Create indexes for better performance
CREATE INDEX idx_predictions_policy_date ON predictions(policy_date);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust as needed)
CREATE POLICY "Allow all operations on predictions" ON predictions
    FOR ALL USING (true);
```

### Step 3: Get Connection Details

1. Go to "Settings" → "API"
2. Copy these values (you'll need them later):
   - Project URL (SUPABASE_URL)
   - Anon public key (SUPABASE_KEY)

## 2. Backend Deployment (Render)

### Step 1: Prepare Repository

1. Ensure your code is pushed to GitHub/GitLab
2. Make sure the `backend/` folder contains all required files:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - All service modules

### Step 2: Deploy to Render

1. Go to [Render](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub/GitLab repository
4. Configure the service:
   - **Name**: `aadhaar-ml-api`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### Step 3: Set Environment Variables

In Render dashboard, go to your service → "Environment":

```bash
FLASK_ENV=production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SECRET_KEY=your-secret-key-here
MODEL_PATH=data/models
DATA_PATH=.
MAX_FORECAST_DAYS=365
DEFAULT_FORECAST_DAYS=60
LOG_LEVEL=INFO
CACHE_TIMEOUT=3600
RATE_LIMIT=60
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Test the API at: `https://your-service.onrender.com/health`

## 3. Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. Ensure the `frontend/` folder contains all required files
2. Test locally:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

### Step 2: Deploy to Vercel

#### Option A: Vercel CLI (Recommended)

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from frontend directory:
   ```bash
   cd frontend
   vercel
   ```

4. Follow the prompts:
   - Set up and deploy? `Y`
   - Which scope? Choose your account
   - Link to existing project? `N`
   - Project name: `aadhaar-policy-frontend`
   - Directory: `./` (current directory)

#### Option B: Vercel Dashboard

1. Go to [Vercel](https://vercel.com) and sign up/login
2. Click "New Project"
3. Import your Git repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 3: Set Environment Variables

In Vercel dashboard, go to your project → "Settings" → "Environment Variables":

```bash
NEXT_PUBLIC_API_URL=https://your-render-service.onrender.com
```

### Step 4: Redeploy

1. Trigger a new deployment to apply environment variables
2. Test the frontend at your Vercel URL

## 4. Model Files Setup

### Option 1: Upload Existing Models

If you have trained models:

1. Create a `data/models/` directory in your backend
2. Upload these files:
   - `enrolment_baseline_model.pkl`
   - `update_baseline_model.pkl`
   - `enrolment_impact_model.pkl`
   - `update_impact_model.pkl`
   - `policy_feature_cols.pkl`

### Option 2: Use Fallback Models

The system includes fallback models that will be used if trained models are not available. This allows the system to run immediately after deployment.

## 5. Testing the Deployment

### Backend Health Check

```bash
curl https://your-render-service.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected",
  "models": "loaded",
  "timestamp": "2025-03-22T10:00:00Z"
}
```

### Frontend Test

1. Visit your Vercel URL
2. Fill out the prediction form
3. Submit a prediction
4. Verify results are displayed

### Database Test

1. Submit a prediction through the frontend
2. Check Supabase dashboard → "Table Editor" → "predictions"
3. Verify the prediction was stored

## 6. Custom Domain Setup (Optional)

### Backend Custom Domain (Render)

1. Go to Render dashboard → your service → "Settings"
2. Scroll to "Custom Domains"
3. Add your domain (e.g., `api.yoursite.com`)
4. Update DNS records as instructed
5. Update frontend environment variable with new domain

### Frontend Custom Domain (Vercel)

1. Go to Vercel dashboard → your project → "Settings" → "Domains"
2. Add your domain (e.g., `yoursite.com`)
3. Update DNS records as instructed

## 7. Monitoring and Maintenance

### Render Monitoring

- Check service logs in Render dashboard
- Set up alerts for service downtime
- Monitor resource usage

### Vercel Monitoring

- Check function logs in Vercel dashboard
- Monitor build times and deployment status

### Supabase Monitoring

- Monitor database usage in Supabase dashboard
- Set up database backups
- Monitor API usage

## 8. Troubleshooting

### Common Issues

#### Backend Not Starting

1. Check Render logs for errors
2. Verify all environment variables are set
3. Check Python dependencies in `requirements.txt`

#### Frontend API Calls Failing

1. Verify `NEXT_PUBLIC_API_URL` is correct
2. Check CORS configuration in backend
3. Test backend health endpoint directly

#### Database Connection Issues

1. Verify Supabase credentials
2. Check if database table exists
3. Verify network connectivity

#### Model Loading Issues

1. Check if model files exist in `data/models/`
2. Verify file permissions
3. Check fallback model creation

### Performance Optimization

1. **Backend**: Increase worker count in Procfile for higher traffic
2. **Frontend**: Enable Vercel Analytics for performance monitoring
3. **Database**: Add indexes for frequently queried columns
4. **Caching**: Implement Redis caching for model predictions

## 9. Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **API Rate Limiting**: Implement rate limiting for production
3. **Database Security**: Use Row Level Security in Supabase
4. **HTTPS**: Ensure all communications use HTTPS
5. **CORS**: Configure CORS properly for your domain

## 10. Scaling Considerations

### Backend Scaling

- Upgrade Render plan for more resources
- Implement horizontal scaling with multiple instances
- Add Redis for caching and session management

### Frontend Scaling

- Vercel automatically scales frontend
- Implement CDN for static assets
- Optimize bundle size

### Database Scaling

- Upgrade Supabase plan for more connections
- Implement connection pooling
- Consider read replicas for heavy read workloads

## Support

For deployment issues:

1. Check service logs first
2. Verify all environment variables
3. Test each component individually
4. Check network connectivity between services

The system is designed to be resilient with fallback mechanisms, so it should work even with minimal configuration.