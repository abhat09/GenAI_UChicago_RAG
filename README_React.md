# UChicago ADS AI Assistant - React Chat Interface

A modern, responsive chat interface built with React for the UChicago ADS RAG chatbot.

## Features

- **Modern UI**: Clean, dark-themed chat interface
- **Real-time Chat**: Instant message updates with loading indicators
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Source Citations**: Shows sources for AI responses
- **Smooth Animations**: Fade-in effects and hover states
- **Auto-scroll**: Automatically scrolls to latest messages

## Project Structure

```
GenAI_UChicago_RAG/
├── src/
│   ├── App.js          # Main React component
│   ├── App.css         # Styling
│   └── index.js        # React entry point
├── public/
│   └── index.html      # HTML template
├── backend_api.py      # Flask backend API
├── package.json        # Node.js dependencies
└── README_React.md     # This file
```

## Setup Instructions

### 1. Install Node.js Dependencies

```bash
cd GenAI_UChicago_RAG
npm install
```

### 2. Install Python Backend Dependencies

```bash
pip install flask flask-cors
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Start the Backend API

```bash
python backend_api.py
```

The API will run on `http://localhost:5000`

### 5. Start the React Frontend

In a new terminal:
```bash
npm start
```

The React app will run on `http://localhost:3000`

## How It Works

1. **Frontend (React)**: Handles UI, user input, and message display
2. **Backend (Flask)**: Processes chat requests using your existing RAG pipeline
3. **RAG System**: Uses Chroma DB and Gemini to generate responses
4. **Real-time Updates**: Messages appear instantly with smooth animations

## Customization

### Styling
- Edit `src/App.css` to modify appearance
- All styles use CSS custom properties for easy theming
- Responsive breakpoints at 768px and 480px

## Responsive Design

- **Desktop**: Full-width layout with sidebar
- **Tablet**: Adjusted spacing and sizing
- **Mobile**: Optimized for touch, full-width messages

## API Endpoints

- `POST /api/chat` - Send a message and get AI response
- `GET /api/health` - Health check endpoint

## Deployment

### Build for Production
```bash
npm run build
```

### Deploy Backend
- Use any Python hosting service (Heroku, DigitalOcean, etc.)
- Update CORS settings for your domain
- Set environment variables on your hosting platform

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure backend is running and CORS is enabled
2. **API Connection**: Check that backend is running on port 5000
3. **Environment Variables**: Verify `.env` file exists with correct API key
4. **Port Conflicts**: Change ports in `backend_api.py` and `package.json` if needed

### Debug Mode

Both frontend and backend run in debug mode by default:
- Frontend: Hot reloading enabled
- Backend: Detailed error messages and auto-restart

## Dependencies

### Frontend
- React 18.2.0
- React DOM 18.2.0
- React Scripts 5.0.1

### Backend
- Flask
- Flask-CORS
- Google Generative AI
- LangChain Community
- Chroma DB

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the UChicago GenAI Principles & Applications course. 