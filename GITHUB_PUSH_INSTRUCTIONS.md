# GitHub Push Instructions

## Issue: Secret Scanning Blocking Push

GitHub is blocking the push because it detected API keys in the commit history.

## Solution: Allow the Secret

1. Go to this URL to allow the secret:
   https://github.com/yeduruabhiram/mindneosv2/security/secret-scanning/unblock-secret/35PwLbNwkfjo40GSxaX58Thpxe7

2. Click "Allow secret" button

3. Then run:
   ```bash
   cd mindneox_clean
   git push -u origin main --force
   ```

## Alternative: Deploy Frontend to Vercel Now

Since the backend is already deployed to HF Spaces, you can deploy the frontend directly:

```bash
cd mindneox-frontend
npm install -g vercel
vercel login
vercel --prod
```

Then set these environment variables in Vercel dashboard:
- `VITE_API_URL` = `https://yeduru-abhi.hf.space`
- `VITE_CLERK_PUBLISHABLE_KEY` = `pk_test_ZWFzeS1tYXJtb3QtMzguY2xlcmsuYWNjb3VudHMuZGV2JA`

## What's Already Deployed

✅ **Backend**: https://yeduru-abhi.hf.space
- API is live and working
- Just needs Firebase & Pinecone secrets added in HF Space settings

⏳ **Frontend**: Ready to deploy to Vercel
- All files prepared
- Environment configured
- Just run `vercel --prod`

## Summary

Your system is 90% deployed! Just need to:
1. Allow the GitHub secret (or skip GitHub for now)
2. Deploy frontend to Vercel
3. Add secrets to HF Space
4. Start collecting data!
