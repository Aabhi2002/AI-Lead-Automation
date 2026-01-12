# Lead Management System - Frontend

A minimal internal ops UI for the AI-powered lead qualification system.

## Features

### Page 1: Lead Qualification Tool
- Simple form to submit new leads with fields:
  - Name (required)
  - Email (required) 
  - Company (required)
  - Message (required)
- Submit button: "Run AI Qualification"
- Real-time results display showing:
  - AI score (0-100)
  - Category (Hot/Warm/Cold) with color coding
  - Recommended action (notify_sales/review/ignore)
  - AI reasoning explanation
  - Enrichment summary

### Page 2: Analytics Dashboard
- Real-time metrics from the backend:
  - Total leads count
  - Hot/Warm/Cold lead breakdown
  - Average score
  - Conversion rate calculation
- Refresh button to update metrics
- Clean card-based layout

## Tech Stack

- **React 19** with Vite
- **Vanilla CSS** for styling
- **Fetch API** for backend communication
- **No external dependencies** beyond React

## Running the Application

1. **Start the backend** (required):
   ```bash
   uvicorn api:app --reload
   ```
   Backend runs on: http://localhost:8000

2. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs on: http://localhost:5175 (or next available port)

## API Integration

The frontend connects to these backend endpoints:

- `POST /submit-lead` - Submit new lead for AI qualification
- `GET /metrics` - Fetch current analytics metrics
- `GET /` - Health check

## Component Structure

```
src/
├── App.jsx                           # Main app with tab navigation
├── App.css                          # All styles
├── components/
│   ├── LeadQualificationTool.jsx    # Lead submission form & results
│   └── AnalyticsDashboard.jsx       # Metrics display
└── main.jsx                         # React entry point
```

## Design Principles

- **Internal tool aesthetic** - Clean, functional, no fancy animations
- **Minimal dependencies** - Only React, no UI frameworks
- **Error handling** - Graceful error states and loading indicators
- **Responsive design** - Works on desktop and mobile
- **Interview-ready code** - Clean, readable, well-structured

## Usage

1. **Submit a Lead**: Use the Lead Qualification tab to test the AI system
2. **View Analytics**: Switch to Analytics Dashboard to see system metrics
3. **Real-time Updates**: Both pages fetch live data from the backend

The UI is designed for internal ops teams to demonstrate and monitor the AI lead qualification system.