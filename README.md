# 🚀 AI Lead Automation Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Transform your lead management with AI-powered automation, intelligent scoring, and real-time analytics**

An enterprise-grade lead management platform that combines artificial intelligence, automated workflows, and interactive dashboards to revolutionize how businesses handle lead qualification, scoring, and conversion optimization.

## ✨ Key Features

### 🤖 **AI-Powered Intelligence**
- **Smart Lead Scoring**: Machine learning algorithms analyze lead behavior and characteristics
- **Automated Qualification**: AI-driven lead assessment and categorization
- **Predictive Analytics**: Forecast lead conversion probability and revenue potential

### 📊 **Comprehensive Analytics**
- **Real-time Dashboard**: Interactive React-based analytics interface
- **Performance Metrics**: Track conversion rates, lead quality, and pipeline health
- **Custom Reports**: Generate detailed insights and export data

### 🔄 **Automated Workflows**
- **Lead Ingestion**: Automated data import from multiple sources
- **Data Enrichment**: Enhance lead profiles with additional information
- **Pipeline Management**: Streamlined lead progression tracking

### 🛠 **Advanced Integration**
- **MCP Protocol**: Model Context Protocol for seamless AI integration
- **RESTful API**: FastAPI-powered backend for easy integrations
- **Database Management**: SQLite with automated schema management

## 🏗 Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI Backend │    │   AI/ML Engine  │
│   ┌───────────┐ │    │   ┌────────────┐  │    │   ┌───────────┐ │
│   │Dashboard  │ │◄──►│   │API Routes  │  │◄──►│   │Lead Scorer│ │
│   │Analytics  │ │    │   │Data Layer  │  │    │   │Enrichment │ │
│   └───────────┘ │    │   └────────────┘  │    │   └───────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │     SQLite Database        │
                    │  ┌─────────┬─────────────┐ │
                    │  │ Leads   │ Analytics   │ │
                    │  │ Scores  │ Metrics     │ │
                    │  └─────────┴─────────────┘ │
                    └────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aabhi2002/AI-Lead-Automation.git
   cd AI-Lead-Automation
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env  # Configure your settings
   
   # Initialize database
   python scripts/create_tables.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Start the Application**
   ```bash
   # Terminal 1: Start backend
   python api.py
   
   # Terminal 2: Start frontend (already running from step 3)
   # Access at http://localhost:5173
   ```

## 📋 Usage Examples

### Lead Processing Pipeline
```bash
# Run complete lead automation pipeline
python run_pipeline.py

# Individual operations
python scripts/ingest_leads.py      # Import new leads
python scripts/enrich_leads.py      # Enhance lead data
python scripts/score_leads.py       # AI-powered scoring
```

### API Integration
```python
import requests

# Get lead scores
response = requests.get("http://localhost:8000/api/leads/scores")
leads = response.json()

# Qualify a lead
qualification = requests.post("http://localhost:8000/api/leads/qualify", 
                            json={"lead_id": 123})
```

### MCP Integration
```bash
# Start MCP server for AI interactions
cd mcp-lead-query
python mcp_server.py

# Test MCP functionality
python demo_usage.py
```

## 📁 Project Structure

```
AI-Lead-Automation/
├── 📱 frontend/                 # React dashboard application
│   ├── src/components/         # UI components
│   ├── public/                 # Static assets
│   └── package.json           # Frontend dependencies
├── 🔧 scripts/                 # Automation scripts
│   ├── ingest_leads.py        # Data ingestion
│   ├── score_leads.py         # AI scoring engine
│   └── analytics.py           # Analytics generation
├── 🛠 utils/                   # Utility modules
│   ├── ai.py                  # AI/ML functions
│   ├── db.py                  # Database operations
│   └── enrichment.py          # Data enrichment
├── 🤖 mcp-lead-query/          # MCP integration
├── 📊 data/                    # Data storage
├── 🗄 db/                      # Database files
├── api.py                     # FastAPI backend
└── run_pipeline.py            # Main automation pipeline
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following configuration:

```env
# Database
DATABASE_URL=sqlite:///./db/database.db

# AI/ML Settings
OPENAI_API_KEY=your_openai_key_here
MODEL_NAME=gpt-3.5-turbo

# API Configuration
API_HOST=localhost
API_PORT=8000
DEBUG=True

# Frontend
FRONTEND_URL=http://localhost:5173
```

## 📊 Features Deep Dive

### Lead Scoring Algorithm
Our AI-powered scoring system evaluates leads based on:
- **Demographic Data**: Company size, industry, location
- **Behavioral Signals**: Website engagement, email interactions
- **Historical Patterns**: Similar lead conversion rates
- **Custom Criteria**: Industry-specific scoring rules

### Analytics Dashboard
- **Lead Pipeline Visualization**: Track leads through qualification stages
- **Conversion Metrics**: Monitor success rates and identify bottlenecks
- **Performance Trends**: Historical analysis and forecasting
- **Custom Filters**: Segment data by various criteria

### Data Enrichment
- **Company Information**: Automatically fetch company details
- **Contact Validation**: Verify email addresses and phone numbers
- **Social Media Integration**: Gather additional contact insights
- **Industry Classification**: Categorize leads by business sector

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for AI/ML capabilities
- FastAPI for the robust backend framework
- React team for the frontend framework
- The open-source community for various tools and libraries

## 📞 Support

- 📧 Email: [your-email@example.com](mailto:abhishekrajput90094@gmail.com)
- 🐛 Issues: [GitHub Issues](https://github.com/Aabhi2002/AI-Lead-Automation/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Aabhi2002/AI-Lead-Automation/discussions)

---

<div align="center">
  <strong>⭐ Star this repository if you find it helpful!</strong>
  <br>
  <sub>Built with ❤️ by <a href="https://github.com/Aabhi2002">Aabhi2002</a></sub>
</div>
