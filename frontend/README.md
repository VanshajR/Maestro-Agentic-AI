# Agentic AI Automator Frontend

React + Vite single-page app for launching autonomous research runs against the FastAPI backend.

## Features

- Goal input with adjustable plan depth and Framer Motion micro-interactions
- Axios API client that targets `/api/v1` by default and automatically respects Vercel env overrides
- Responsive layout inspired by Vercel styling with subtle gradients and skeleton loaders
- Results dashboard with ordered plan, execution timeline, and per-step outputs

## Getting Started

```bash
npm install
npm run dev
```

The dev server proxies `/api` requests to `http://localhost:8000` so the backend must run locally. Configure alternate endpoints with:

- `VITE_API_BASE_URL`
- `VITE_AGENT_ENDPOINT`
- `VITE_PLAN_ENDPOINT`

## Production Build

```bash
npm run build
npm run preview
```

Deploy the `dist/` folder to Vercel or any static host. Set the environment variables there to point at your FastAPI deployment.
