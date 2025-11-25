# Fix: "EMFILE: too many open files" on Mac

This error happens on macOS when the system file watcher limit is too low.

## Quick Fix

Run these commands in terminal:

```bash
# Increase file watcher limit
echo kern.maxfiles=65536 | sudo tee -a /etc/sysctl.conf
echo kern.maxfilesperproc=65536 | sudo tee -a /etc/sysctl.conf
sudo sysctl -w kern.maxfiles=65536
sudo sysctl -w kern.maxfilesperproc=65536

# Verify the change
ulimit -n
```

## Alternative: Use Watchman

Install Watchman (recommended for React Native development):

```bash
# Using Homebrew
brew install watchman

# Then restart your terminal and try again
cd mobile-app
npm start
```

## Temporary Fix

If you just want to test quickly:

```bash
# Increase limit for current session
ulimit -n 65536

# Then start the app
npm start
```

## After Fixing

Once you've applied the fix:

```bash
cd mobile-app
npm start
```

The app should start without errors!

## Still Having Issues?

Try clearing the cache:

```bash
# Clear Metro bundler cache
expo start -c

# Or clear everything
rm -rf node_modules .expo
npm install
expo start -c
```
