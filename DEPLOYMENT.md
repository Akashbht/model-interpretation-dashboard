# Deployment Guide

## Quick Start (Development)

1. **Clone and Setup**
```bash
git clone https://github.com/Akashbht/model-interpretation-dashboard.git
cd model-interpretation-dashboard
./setup.sh
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Start Backend**
```bash
cd backend
source venv/bin/activate
python app.py
```

4. **Start Frontend** (new terminal)
```bash
cd frontend
npm start
```

5. **Access Dashboard**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Production Deployment

### Backend (Flask API)

#### Option 1: Using Gunicorn
```bash
cd backend
source venv/bin/activate
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Frontend (React)

#### Build for Production
```bash
cd frontend
npm run build
```

#### Option 1: Serve with Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/frontend/build;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Option 2: Using Docker
```dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Full Stack with Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

## Environment Variables

### Required
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key

### Optional
- `FLASK_ENV`: development/production
- `REACT_APP_API_URL`: Backend API URL for frontend

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **CORS**: Configure appropriate CORS settings for production
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **HTTPS**: Use HTTPS in production
5. **Firewall**: Restrict access to backend ports

## Monitoring

### Health Checks
```bash
# Backend health
curl http://localhost:5000/api/models

# Frontend health
curl http://localhost:3000
```

### Logging
- Backend logs to stdout (configure log aggregation)
- Frontend errors logged to browser console

## Scaling

### Backend Scaling
- Use multiple Gunicorn workers
- Deploy behind load balancer
- Consider Redis for session storage

### Frontend Scaling
- Use CDN for static assets
- Enable gzip compression
- Implement caching headers

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check REACT_APP_API_URL in frontend
   - Verify CORS configuration in Flask app

2. **API Connection Failed**
   - Ensure backend is running on correct port
   - Check firewall/network settings

3. **Model Connection Issues**
   - Verify API keys are correct
   - Check API key permissions and quotas

4. **Build Failures**
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall

### Performance Optimization

1. **Frontend**
   - Enable code splitting
   - Optimize bundle size
   - Use React.memo for expensive components

2. **Backend**
   - Implement caching for model responses
   - Use connection pooling
   - Add database indexing for results storage

## Backup and Recovery

### Data Backup
- Backup benchmark results database
- Export model configurations
- Save custom prompt collections

### Recovery
- Restore from database backups
- Reconfigure API keys
- Verify model connections