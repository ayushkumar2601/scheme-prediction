# Aadhaar Policy Impact Prediction System - Production Ready

A comprehensive machine learning system for predicting the impact of Aadhaar policy changes on enrollment and update volumes across India. Built with modern web technologies and deployed on cloud infrastructure.

## 🏗️ Architecture

```
Frontend (Next.js) → Backend API (Flask) → Database (PostgreSQL)
     ↓                    ↓                      ↓
   Vercel              Render                Supabase
```

## 🚀 Live Demo

- **Frontend**: [https://aadhaar-policy-frontend.vercel.app](https://aadhaar-policy-frontend.vercel.app)
- **API**: [https://aadhaar-ml-api.onrender.com](https://aadhaar-ml-api.onrender.com)
- **Health Check**: [https://aadhaar-ml-api.onrender.com/health](https://aadhaar-ml-api.onrender.com/health)

## 📋 Features

### Core Functionality
- **Policy Impact Prediction**: ML-powered predictions for enrollment and update volumes
- **Regional Analysis**: State-wise impact breakdown across all 28 states + 8 UTs
- **Time Series Forecasting**: 30-365 day prediction windows
- **Risk Assessment**: Automated risk level calculation and recommendations
- **Peak Analysis**: Identification of peak impact dates and volumes

### Technical Features
- **Production-Ready**: Deployed on enterprise cloud platforms
- **Scalable Architecture**: Microservices with independent scaling
- **Real-time API**: RESTful API with comprehensive error handling
- **Responsive UI**: Modern React-based interface with mobile support
- **Data Persistence**: PostgreSQL database with automated backups
- **Monitoring**: Health checks and performance monitoring

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom components
- **Charts**: Chart.js with React integration
- **State Management**: React hooks and context
- **Deployment**: Vercel with automatic deployments

### Backend
- **Framework**: Flask 2.3+ with Python 3.10
- **ML Libraries**: scikit-learn, pandas, numpy
- **API**: RESTful with JSON responses
- **Database ORM**: Supabase client
- **Deployment**: Render with Docker support

### Database
- **Database**: PostgreSQL 15+ (Supabase)
- **Features**: Row-level security, real-time subscriptions
- **Backup**: Automated daily backups
- **Scaling**: Connection pooling and read replicas

### DevOps
- **CI/CD**: GitHub Actions with automated testing
- **Monitoring**: Render metrics and Vercel analytics
- **Logging**: Structured logging with error tracking
- **Security**: HTTPS, CORS, environment variables

## 📊 System Capabilities

### Prediction Accuracy
- **Baseline Models**: R² > 0.80 (explains 80%+ of variance)
- **Policy Impact Models**: R² > 0.75
- **Mean Absolute Error**: < 10% of mean volume
- **Processing Time**: 30-60 seconds for full predictions

### Performance Metrics
- **API Response Time**: < 10 seconds (excluding ML processing)
- **Frontend Load Time**: < 3 seconds
- **Database Queries**: < 5 seconds average
- **Uptime**: 99.9% target availability

### Scale Handling
- **Concurrent Users**: 100+ simultaneous users
- **Daily Predictions**: 1000+ predictions per day
- **Data Processing**: 2M+ records processed
- **Storage**: Unlimited prediction history

## 🔧 Local Development

### Prerequisites
- Node.js 18+
- Python 3.10+
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your Supabase credentials

# Run development server
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install

# Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:10000" > .env.local

# Run development server
npm run dev
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:10000
- Health Check: http://localhost:10000/health

## 🚀 Deployment

### Quick Deploy

1. **Database (Supabase)**:
   - Create project at [supabase.com](https://supabase.com)
   - Run SQL from `DEPLOYMENT_GUIDE.md`
   - Copy connection details

2. **Backend (Render)**:
   - Connect GitHub repo to [render.com](https://render.com)
   - Set root directory to `backend`
   - Add environment variables
   - Deploy automatically

3. **Frontend (Vercel)**:
   - Connect GitHub repo to [vercel.com](https://vercel.com)
   - Set root directory to `frontend`
   - Add API URL environment variable
   - Deploy automatically

### Detailed Instructions
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete step-by-step instructions.

## 📖 API Documentation

### Core Endpoints

#### Generate Prediction
```bash
POST /api/predict
Content-Type: application/json

{
  "policy_date": "2025-04-01",
  "forecast_days": 60,
  "compliance_level": 0.8,
  "policy_name": "New Aadhaar Policy"
}
```

#### Get States
```bash
GET /api/states
```

#### Health Check
```bash
GET /health
```

### Response Format
```json
{
  "success": true,
  "results": {
    "summary": {
      "total_people_affected": 1250000,
      "total_enrolment_impact": 750000,
      "total_update_impact": 500000
    },
    "daily_impact": [...],
    "regional_impact": {...},
    "peak_analysis": {...},
    "risk_assessment": {...}
  }
}
```

Complete API documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🔒 Security

### Data Protection
- **Encryption**: All data encrypted in transit and at rest
- **Authentication**: API key authentication (configurable)
- **CORS**: Restricted to authorized domains
- **Input Validation**: Comprehensive request validation

### Privacy Compliance
- **No PII**: System processes aggregated data only
- **Data Retention**: Configurable retention policies
- **Audit Logs**: Complete request/response logging
- **GDPR Ready**: Data export and deletion capabilities

## 📈 Monitoring & Analytics

### System Monitoring
- **Health Checks**: Automated endpoint monitoring
- **Performance Metrics**: Response time and throughput tracking
- **Error Tracking**: Comprehensive error logging and alerting
- **Resource Usage**: CPU, memory, and database monitoring

### Business Analytics
- **Usage Statistics**: Prediction volume and patterns
- **Popular Scenarios**: Most requested policy types
- **Regional Insights**: Geographic usage patterns
- **Performance Trends**: Accuracy and processing time trends

## 🧪 Testing

### Automated Testing
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### Load Testing
```bash
# API load test
curl -X POST https://your-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{"policy_date":"2025-04-01","forecast_days":60,"compliance_level":0.8}'
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test locally
4. Submit pull request with description

### Code Standards
- **Python**: PEP 8 compliance, type hints
- **TypeScript**: ESLint configuration, strict mode
- **Testing**: Unit tests for new features
- **Documentation**: Update docs for API changes

## 📞 Support

### Getting Help
- **Documentation**: Check README and guides first
- **Issues**: Create GitHub issue with details
- **API Problems**: Check health endpoint and logs
- **Deployment**: Follow deployment guide step-by-step

### Common Issues
- **CORS Errors**: Verify frontend URL in backend config
- **Database Connection**: Check Supabase credentials
- **Model Loading**: Verify model files exist or use fallbacks
- **Timeout Errors**: Increase timeout for prediction endpoint

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- **Data Source**: Aadhaar enrollment and update statistics
- **ML Framework**: scikit-learn community
- **Cloud Providers**: Vercel, Render, and Supabase
- **Open Source**: All dependencies and libraries used

---

**Built with ❤️ for policy makers and data scientists**

*Last updated: March 2025*