# AI Tool Discovery Engine

A web application that recommends the most relevant AI tools to users based on their role, workflow, skill level, and pain points. The system uses a rule-based recommendation engine to provide personalized tool suggestions without executing or proxying any third-party AI tools.

## Features

- **Personalized Recommendations**: Get AI tool suggestions based on your specific role, workflow, and challenges
- **Rule-Based Engine**: Smart algorithm that matches tools to user profiles using multiple criteria
- **Comprehensive Database**: Pre-populated with popular AI tools across various categories
- **User-Friendly Interface**: Clean, modern React frontend with intuitive onboarding
- **Safe & Secure**: Only recommends and links to official tool websites
- **No Third-Party Execution**: Fully compliant with terms of service

## Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database for storing tools and user responses

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **CSS3** - Styling with modern design patterns

## Project Structure

```
AI/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── init_db.py          # Database initialization script
│   ├── requirements.txt    # Python dependencies
│   └── ai_tools.db        # SQLite database (created automatically)
├── frontend/
│   ├── public/
│   │   └── index.html     # HTML template
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Homepage.js
│   │   │   ├── Onboarding.js
│   │   │   ├── Results.js
│   │   │   └── Navbar.js
│   │   ├── App.js         # Main App component
│   │   ├── index.js       # Entry point
│   │   └── index.css      # Global styles
│   └── package.json       # Node.js dependencies
└── README.md              # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize the database:
```bash
python init_db.py
```

6. Start the Flask server:
```bash
python app.py
```

The backend will be running at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be running at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Click "Discover AI Tools" to start the onboarding process
3. Fill out the form with your:
   - Role/Profession
   - Primary workflow
   - AI skill level
   - Current challenges/pain points
4. Receive personalized AI tool recommendations with explanations
5. Click on any tool to visit its official website

## API Endpoints

### GET `/api/tools`
Returns all AI tools in the database.

### GET `/api/categories`
Returns all available tool categories.

### GET `/api/roles`
Returns all target roles from the database.

### POST `/api/recommend`
Accepts user data and returns personalized recommendations.

**Request Body:**
```json
{
  "role": "Developer",
  "workflow": "Software Development",
  "skill_level": "intermediate",
  "pain_points": ["Slow coding", "Debugging time"]
}
```

### GET `/api/health`
Health check endpoint.

## Recommendation Algorithm

The recommendation engine uses a weighted scoring system:

- **Role Matching (30%)**: Tools designed for the user's role get higher scores
- **Skill Level (20%)**: Tools matching the user's skill level are preferred
- **Pain Points (30%)**: Tools that address the user's specific challenges
- **Workflow (20%)**: Tools that fit the user's primary workflow

Only tools with a score above 20% are recommended, ensuring relevance.

## Database Schema

### AI Tools Table
- `id`: Primary key
- `name`: Tool name
- `description`: Tool description
- `category`: Tool category
- `target_roles`: JSON array of target roles
- `skill_level`: Required skill level
- `use_cases`: JSON array of use cases
- `pain_points`: JSON array of pain points addressed
- `pricing_model`: Pricing model (free, freemium, subscription)
- `official_url`: Official website URL
- `features`: JSON array of key features
- `rating`: User rating (0-5)

### User Responses Table
- `id`: Primary key
- `role`: User's role
- `workflow`: User's workflow
- `skill_level`: User's skill level
- `pain_points`: JSON array of user's pain points
- `created_at`: Timestamp

## Deployment

### Backend Deployment (Heroku Example)

1. Install Heroku CLI and login
2. Add a `Procfile` to the backend directory:
```
web: python app.py
```
3. Create `runtime.txt`:
```
python-3.9.16
```
4. Deploy:
```bash
heroku create your-app-name
heroku config:set FLASK_APP=app.py
git push heroku main
```

### Frontend Deployment (Netlify/Vercel)

1. Build the frontend:
```bash
npm run build
```
2. Deploy the `build` folder to your preferred hosting service
3. Update the API URL in the frontend components to point to your deployed backend

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository.

## Safety & Compliance

- This application does NOT execute, proxy, or benchmark third-party AI tools
- It does NOT scrape websites or violate any terms of service
- The app only RECOMMENDS and EXPLAINS AI tools
- All links direct users to official tool websites
- No user data is shared with third parties
