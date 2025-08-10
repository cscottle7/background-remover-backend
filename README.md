# CharacterCut Backend

Dedicated Vercel deployment for CharacterCut's background removal API.

## Features

- **Full rembg AI processing** with u2net model
- **CORS-enabled** for frontend integration
- **Optimized for Vercel** Python runtime
- **Session caching** for performance
- **Error handling** and logging

## Endpoints

- `GET /api/health` - Health check
- `POST /api/process` - Background removal

## Deployment

1. **Create new Vercel project** from this directory
2. **Connect to GitHub** (separate repo recommended)
3. **Deploy** - Vercel will auto-detect Python functions

```bash
# Local development
npm run dev

# Production deployment  
npm run deploy
```

## Configuration

The backend is configured to:
- Accept CORS requests from any origin
- Process images up to 10MB
- Use u2net model for high quality
- Cache rembg sessions for performance

## Integration

Update your frontend `API_BASE_URL` to point to this backend:

```typescript
const API_BASE_URL = 'https://your-backend.vercel.app';
```

## Requirements

- Python 3.9+
- rembg, Pillow, numpy (see requirements.txt)
- Vercel account for deployment