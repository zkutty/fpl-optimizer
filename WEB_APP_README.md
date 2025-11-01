# FPL Optimizer Web Application

A beautiful, modern web interface for the Fantasy Premier League Team Optimizer with advanced analytics and AI-powered recommendations.

## 🌟 Features

### 📊 Team Dashboard
- Enter your FPL Team ID to get comprehensive analysis
- View team statistics: overall points, rank, and gameweek performance
- Interactive tabs for different analysis types

### 👥 Optimal Squad Builder
- Generate the best possible team within budget constraints
- Advanced optimization using linear programming
- Adjustable budget and gameweek horizon
- Visual breakdown by position

### ⚡ Transfer Suggestions
- Smart transfer recommendations based on fixtures and form
- Expected points improvement calculations
- Cost-effective transfer options
- Multi-transfer planning

### 👑 Captain Selector
- Data-driven captain recommendations
- Vice-captain suggestions
- Differential picks for mini-league gains
- Fixture difficulty analysis
- High ceiling vs. safe floor options

### 🎯 Chip Advisor
- Strategic recommendations for all FPL chips:
  - **Wildcard**: Team overhaul analysis
  - **Triple Captain**: Best timing for 3x points
  - **Bench Boost**: Double gameweek optimization
  - **Free Hit**: One-week team transformation
- Overall chip strategy guidance

### ⭐ Value Players
- Discover best points-per-million players
- Filter by position
- Form and fixture analysis
- Value score rankings

## 🚀 Quick Start

### Option 1: Using the Run Script (Recommended)

```bash
chmod +x run.sh
./run.sh
```

The script will:
1. Create a virtual environment
2. Install all dependencies
3. Start the web server

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Option 3: Direct Run (if dependencies already installed)

```bash
python app.py
```

## 🌐 Using the Application

1. **Start the server** using one of the methods above
2. **Open your browser** to `http://localhost:5000`
3. **Enter your FPL Team ID** on the home page (find it in your FPL profile URL)
4. **Explore the analysis** through the dashboard and other features

### Finding Your Team ID

Your FPL Team ID is in your team's URL on the official FPL website:
- Go to https://fantasy.premierleague.com/
- Click on "Points" or "Transfers"
- Your URL will look like: `https://fantasy.premierleague.com/entry/123456/...`
- Your Team ID is `123456`

## 📱 Page Overview

### Home Page (`/`)
- Welcome screen with feature overview
- Team ID input for quick access
- Links to all major features

### Dashboard (`/dashboard`)
- Comprehensive team analysis
- Multiple analysis tabs:
  - Starting XI optimization
  - Transfer suggestions
  - Captain recommendations
  - Chip strategy advice

### Optimal Squad (`/optimal-squad`)
- Build the best possible team from scratch
- Adjustable parameters:
  - Budget (£50m - £100m)
  - Gameweek horizon (1-10 weeks)

### Value Players (`/value-players`)
- Browse best value players by position
- Sort and filter options
- Detailed stats for each player

## 🎨 Design Features

- **Modern UI**: Clean, professional design with Tailwind CSS
- **Responsive**: Works on desktop, tablet, and mobile
- **Interactive**: Dynamic content with Alpine.js
- **Beautiful Animations**: Smooth transitions and hover effects
- **Color-Coded**: Position-based color schemes for easy reading
- **Dark Gradients**: Premium purple gradient theme

## 🔧 Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Tailwind CSS, Alpine.js
- **Icons**: Font Awesome 6
- **Data**: Official Fantasy Premier League API
- **Optimization**: PuLP (Linear Programming)
- **Analysis**: Pandas, NumPy

## 📊 API Endpoints

The application exposes several REST API endpoints:

- `POST /api/initialize` - Initialize FPL data
- `POST /api/optimal-squad` - Generate optimal squad
- `GET /api/team-analysis/{team_id}` - Get comprehensive team analysis
- `POST /api/transfers/{team_id}` - Get transfer suggestions
- `GET /api/captain/{team_id}` - Get captain recommendations
- `GET /api/chips/{team_id}` - Get chip recommendations
- `GET /api/lineup/{team_id}` - Get optimal starting XI
- `GET /api/value-players` - Get best value players

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, you can change it by setting the PORT environment variable:
```bash
PORT=8000 python app.py
```

### Module Not Found Errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### FPL API Errors
The application fetches data from the official FPL API. If you see errors:
- Check your internet connection
- The FPL API might be down temporarily (try again later)
- During gameweek deadlines, the API might be slower

### Team ID Not Found
- Make sure you're using your Team ID, not your player ID
- Verify the team is active for the current season
- Check that the team ID exists on the FPL website

## 🔒 Privacy & Data

- **No Data Storage**: Your team ID and data are only used for analysis
- **No Authentication**: No login required, no personal data collected
- **Real-Time Data**: All data fetched directly from FPL API
- **Client-Side Processing**: Most computations happen in your browser

## 📝 Notes

- The optimization algorithms can take 10-30 seconds for complex analyses
- Expected points are calculated based on:
  - Recent form (last 5 games)
  - Season points per game
  - Fixture difficulty
  - Minutes played tendency
- All prices and points are from the official FPL API

## 🤝 Contributing

This is an open-source project. Feel free to:
- Report bugs
- Suggest features
- Improve algorithms
- Enhance the UI

## 📜 License

This project uses data from the official Fantasy Premier League API.
All trademarks belong to the Premier League.

## 🎮 Enjoy and Good Luck!

May your team dominate your mini-leagues! 🏆

