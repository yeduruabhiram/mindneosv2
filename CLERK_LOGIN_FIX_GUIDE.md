# Clerk Login Not Working - Fix Guide

## Problem
When clicking the login button in the chatbot page, the Clerk sign-in modal does not open.

## Root Cause
The Clerk publishable key might be:
1. Expired or invalid
2. Not properly configured in Clerk dashboard
3. Domain restrictions not set up correctly

## Solution Steps

### 1. Verify Clerk Dashboard Setup

Go to: https://dashboard.clerk.com

**Check the following:**
- ✅ Your application is active (not paused)
- ✅ The publishable key matches the one in `.env`
- ✅ Your domain is whitelisted in "Allowed domains"

### 2. Update Allowed Domains

In Clerk Dashboard → Settings → Domains:
- Add `localhost:3003` (or your dev port)
- Add your production domain (e.g., `mindneox-ai.vercel.app`)

### 3. Verify Environment Variables

Check your `.env` file:
```bash
VITE_CLERK_PUBLISHABLE_KEY=pk_test_ZWFzeS1tYXJtb3QtMzguY2xlcmsuYWNjb3VudHMuZGV2JA
```

**Current Key:** `pk_test_ZWFzeS1tYXJtb3QtMzguY2xlcmsuYWNjb3VudHMuZGV2JA`

### 4. Test Clerk Status

Open browser console (F12) and look for:
```
Clerk status: {
  isLoaded: true/false,
  hasUser: true/false,
  clerkExists: true/false,
  publishableKey: 'Set'/'Missing'
}
```

### 5. Get a New Clerk Key (If Needed)

If the key is expired:

1. Go to https://dashboard.clerk.com
2. Create a new application or use existing
3. Go to API Keys
4. Copy the **Publishable Key**
5. Update `.env`:
   ```
   VITE_CLERK_PUBLISHABLE_KEY=your_new_key_here
   ```
6. Restart dev server: `npm run dev`

### 6. Alternative: Use Clerk Hosted Pages

If modal still doesn't work, you can redirect to Clerk's hosted pages:

Update the code to use `redirectUrl` instead of `mode="modal"`:

```jsx
<SignInButton 
  redirectUrl="/chatbot"
  afterSignInUrl="/chatbot"
>
  <button>Login</button>
</SignInButton>
```

## Quick Test

1. Open browser console
2. Click login button
3. Check for errors in console
4. Look for Clerk status log

## Common Issues

### Issue 1: "Clerk is not defined"
**Solution:** Clerk package not installed or not imported
```bash
npm install @clerk/clerk-react
```

### Issue 2: Modal doesn't appear
**Solution:** Domain not whitelisted in Clerk dashboard

### Issue 3: "Invalid publishable key"
**Solution:** Get new key from Clerk dashboard

### Issue 4: CORS errors
**Solution:** Add your domain to Clerk's allowed origins

## Current Implementation

The chatbot page now has:
- ✅ `SignInButton` component for login
- ✅ `SignOutButton` component for logout
- ✅ Debug logging in console
- ✅ Fallback alert if Clerk fails
- ✅ Proper error handling

## Next Steps

1. Check browser console for Clerk status
2. Verify Clerk dashboard configuration
3. Update publishable key if needed
4. Test login functionality
5. Check for any console errors

## Support

If issues persist:
- Check Clerk documentation: https://clerk.com/docs
- Verify your Clerk plan supports the features you're using
- Contact Clerk support if the key is invalid
