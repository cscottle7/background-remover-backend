# CharacterCut Backend Deployment

## Repository Setup

1. **Create new GitHub repository:**
   - Name: `charactercut-backend`
   - Visibility: Public (or Private if preferred)

2. **Initialize and push this directory:**
   ```bash
   git init
   git add .
   git commit -m "Initial CharacterCut Backend setup"
   git remote add origin https://github.com/YOUR-USERNAME/charactercut-backend.git
   git push -u origin main
   ```

## Vercel Deployment

1. **Go to [vercel.com](https://vercel.com)**
2. **Click "New Project"**
3. **Import your `charactercut-backend` repository**
4. **Configure project:**
   - Framework Preset: **Other**
   - Root Directory: **/** (leave default)
   - Build Command: **Leave empty**
   - Install Command: **Leave empty**

5. **Deploy!**

## Expected Result

After deployment, you'll get:
- **Health endpoint:** `https://your-backend.vercel.app/api/health`
- **Process endpoint:** `https://your-backend.vercel.app/api/process`

## Update Frontend

Once deployed, update the frontend `API_BASE_URL` in:
`frontend/src/lib/services/api.ts`

```typescript
const API_BASE_URL = 'https://your-actual-backend-url.vercel.app';
```

## File Structure

```
charactercut-backend/
├── api/
│   ├── health.py          # Health check endpoint
│   └── process.py         # Background removal endpoint
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration (auto-detect)
├── package.json          # Project metadata
├── README.md             # Documentation
└── DEPLOYMENT.md         # This file
```

## Troubleshooting

- **500 errors:** Check Vercel function logs
- **CORS issues:** Endpoints include CORS headers
- **Size limit:** This deployment should be under 250MB
- **Dependencies:** All requirements are in requirements.txt

## Testing

Test the health endpoint:
```bash
curl https://your-backend.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": 1704067200,
  "version": "2.0.0-backend-dedicated",
  "environment": "vercel-backend",
  "service": "charactercut-backend"
}
```