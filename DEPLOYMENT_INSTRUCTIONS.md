# DEPLOYMENT INSTRUCTIONS - HomeKare Django App

## Current Status
✅ Database connected successfully  
✅ Migrations completed  
✅ Initial data seeded (categories & services)  
✅ Website is LIVE at: https://homekare-we4j.onrender.com  
⚠️ Admin panel styling broken (static files issue)  
⚠️ Need to push code updates to GitHub

## Admin Login Credentials (Current - Local Database Only)
**Username:** admin  
**Password:** admin123  
**URL:** https://homekare-we4j.onrender.com/admin/

> ⚠️ NOTE: This admin account only exists in your Supabase database right now.
> When you redeploy with the updated build.sh, it will automatically create this account.

---

## Files Modified Locally (Need to Push to GitHub)

### 1. `.env`
- Updated DATABASE_URL to use Supabase connection pooler (port 6543)

### 2. `build.sh`
- Added verbose output for debugging
- Added automatic superuser creation
- Added database seeding step

### 3. `web/views.py`
- Added error handling for missing HeroContent

### 4. `web/management/commands/create_default_superuser.py` (NEW)
- Custom Django command to create admin user during deployment

---

## HOW TO DEPLOY (Choose One Method)

### METHOD 1: Using GitHub Desktop (RECOMMENDED)
1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Click "Add" → "Add Existing Repository"
4. Navigate to: `E:\Mtaani Connect James`
5. Click "Add Repository"
6. In GitHub Desktop:
   - You'll see all changed files on the left
   - Add a commit message: "Fix admin panel and auto-create superuser"
   - Click "Commit to main"
   - Click "Push origin"
7. Render will automatically detect the push and redeploy

### METHOD 2: Using Git Command Line
If you have Git installed:
```powershell
cd "E:\Mtaani Connect James"
git add .
git commit -m "Fix admin panel and auto-create superuser"
git push origin main
```

### METHOD 3: Using VS Code
If you have VS Code:
1. Open the project folder in VS Code
2. Click the Source Control icon (left sidebar)
3. Stage all changes (+ icon)
4. Enter commit message: "Fix admin panel and auto-create superuser"
5. Click ✓ Commit
6. Click "..." → "Push"

---

## After Deployment

### 1. Verify Build Logs
Watch for these success messages in Render:
```
===== Installing Python dependencies =====
===== Collecting static files =====
===== Running database migrations =====
===== Creating default superuser =====
✓ Superuser "admin" created successfully!
===== Seeding initial data =====
===== Build completed successfully =====
```

### 2. Test Admin Panel
1. Go to: https://homekare-we4j.onrender.com/admin/
2. Login with:
   - Username: `admin`
   - Password: `admin123`
3. The admin panel should now display correctly with proper styling

### 3. Optional: Add Environment Variables in Render
For security, you can customize the admin credentials:
1. Go to Render Dashboard → Your Service → Environment
2. Add these variables:
   - `DJANGO_SUPERUSER_USERNAME` = your_custom_username
   - `DJANGO_SUPERUSER_EMAIL` = your@email.com
   - `DJANGO_SUPERUSER_PASSWORD` = your_secure_password
3. Redeploy (Manual Deploy → Deploy latest commit)

---

## Static Files Issue - Why It Happens

The admin panel styling is broken because:
1. Django's admin requires static files (CSS/JS)
2. On production, these must be collected and served by WhiteNoise
3. The current GitHub version of `build.sh` runs `collectstatic`, but it might be failing silently
4. Our updated `build.sh` includes better error reporting

Once you push the updated code, this will be fixed automatically.

---

## If You Can't Install Git Right Now

### TEMPORARY WORKAROUND:
You can manually fix the admin styling by running this on Render:
1. Go to Render Dashboard
2. Select your service
3. Go to "Shell" tab
4. Run:
   ```bash
   python manage.py collectstatic --noinput
   python manage.py create_default_superuser
   ```

> ⚠️ Note: This is temporary. The fix will be undone on next deploy if you don't push the updated `build.sh`.

---

## Summary of Changes

| File | Change | Why |
|------|--------|-----|
| `.env` | Updated DATABASE_URL | Use IPv4-compatible connection pooler |
| `build.sh` | Added superuser creation | Auto-create admin on deploy |
| `build.sh` | Added data seeding | Auto-populate categories/services |
| `web/views.py` | Error handling | Prevent crash if HeroContent missing |
| `web/management/commands/` | New command file | Enable superuser auto-creation |

---

## Need Help?

If deployment fails:
1. Check Render build logs for error messages
2. Verify Supabase database is accessible
3. Ensure all environment variables are set in Render:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`

---

Generated: 2026-01-29
