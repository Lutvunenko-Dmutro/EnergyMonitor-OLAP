# 🚀 DEPLOYMENT GUIDE# 🚀 DEPLOYMENT GUIDE










































































































































































































































































































































































































Happy deploying! 🚀---- **GitHub Issues**: Report bugs in this repo- **Neon Docs**: https://neon.tech/docs- **Streamlit Docs**: https://docs.streamlit.io- **Render Docs**: https://render.com/docs## 📞 Support & Help---```6. App updated in 5-10 minutes5. Render auto-deploys4. If tests pass → Docker builds & pushes3. GitHub Actions runs tests2. git push origin main1. git commit -am "feat: add new feature"# Workflow:```bash**No manual deployment needed!** Just push to `main` and CI/CD takes care of everything.5. ✅ Auto-deploy to Render4. ✅ Push to Docker Hub3. ✅ Build Docker image2. ✅ Run code quality checks1. ✅ Run tests on every pushWe've configured GitHub Actions to:## 🎯 Continuous Deployment (CI/CD)---```git push origin main# Deploygit push origin v1.0.0git tag -a v1.0.0 -m "Release version 1.0.0"# Tag releaseblack --check src/ core/ ml/ ui/mypy src/ core/ ml/ --ignore-missing-importsflake8 src/ core/ ml/ ui/pytest tests/ -v# Final pre-deployment commands```bash- [ ] DEVELOPMENT.md updated (if applicable)- [ ] README updated (if applicable)- [ ] Version bumped (if using semantic versioning)- [ ] CHANGELOG updated- [ ] Database backup taken- [ ] Environment variables configured in Render UI- [ ] No hardcoded secrets- [ ] Type checking passes (`mypy src/ core/ ml/`)- [ ] Code linting passes (`flake8 src/ core/ ml/`)- [ ] All tests pass (`pytest tests/ -v`)Before deploying to production:## 📋 Release Checklist---- Alert threshold exceeded- Service crashes- Build failures- Deploy eventsRender → Settings → Notifications:### Enable Slack/Email Notifications## 🔔 Notifications & Alerts---3. Render will load-balance automatically2. Set replicas in configuration1. Upgrade to paid plan### Horizontal Scaling (Multiple Instances)3. Choose higher tier (Standard, Professional, etc.)2. Settings → Instance Type1. Render Dashboard → Select app### Vertical Scaling (Bigger Machine)## 📈 Scaling---3. Use pagination for large datasets   ```   CREATE INDEX idx_region ON data(region_name);   CREATE INDEX idx_timestamp ON data(timestamp);   -- Add indexes   ```sql2. Optimize queries:   ```   @st.cache_resource  # For expensive operations   @st.cache_data   ```python1. Enable caching:### Performance Issues4. Upgrade to paid plan if needed3. Clear caches: `@st.cache_data.clear()`2. Optimize pandas operations (use `dtype` conversions)1. Check Render plan (free tier has 512MB RAM limit)### Memory Issues```print("✅ Connected!"))    port=os.getenv("DB_PORT")    host=os.getenv("DB_HOST"),    password=os.getenv("DB_PASSWORD"),    user=os.getenv("DB_USER"),    dbname=os.getenv("DB_NAME"),conn = psycopg2.connect(import psycopg2# Test connection```python### Database Connection Issues   ```   git push origin main   # Fix issues, then redeploy      tail -f logs/energy-monitor.log   # Check logs      python -m streamlit run main.py   # Run locally first   ```bash3. Solution:   ```   ❌ Port already in use: Check Streamlit port config   ❌ Permission denied: Check file permissions   ❌ Connection refused: Database URL missing/wrong   ❌ ModuleNotFoundError: pip install missing package   ```2. Common issues:   ```   Settings → Logs   ```1. Check Render logs:### App Won't Start## 🚨 Troubleshooting---```git push origin main# Then deploypytest tests/ -v# Test locally first!pip install --upgrade pandas numpy streamlit# Update in requirements.txtpip install --upgrade pippip-audit# Check for security vulnerabilitiespip list --outdated# Check for outdated packages```bash### Update Dependencies   - Restart events   - Network I/O   - Memory usage   - CPU usage3. View:2. Select "energy-monitor"1. Go to Render Dashboard### View Application Metrics```curl -v https://energy-monitor.onrender.com/_stcore/health# Manual check# At: App URL / /_stcore/health# Render auto-checks health endpoint```bash### Health Checks## 📊 Monitoring & Maintenance---- [ ] Trust user input without validation- [ ] Deploy with DEBUG mode enabled- [ ] Expose database URL in logs- [ ] Use weak credentials- [ ] Hardcode passwords in code- [ ] Commit `.env` file (it's in `.gitignore`)### ❌ DON'T:- [ ] Keep dependencies updated (`pip-audit`)- [ ] Monitor logs for suspicious activity- [ ] Set `STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false` in prod- [ ] Enable SSL/TLS for database connection- [ ] Use strong database password (20+ characters)- [ ] Set environment variables in Render UI (NOT in code)- [ ] Use `.env.example` as template (NOT secrets!)### ✅ DO:## 🔒 Security Best Practices---```heroku logs --tail -a energy-monitor# View logsgit push heroku main# Deployecho "web: streamlit run main.py" > Procfile# Add Procfile (if needed)heroku config:set DB_PASSWORD=xxx -a energy-monitor# Set environment variablesheroku create energy-monitor# Create appheroku login# Loginbrew install heroku  # or download from heroku.com# Install Heroku CLI```bash> ℹ️ Heroku free tier is deprecated. Recommended: Use Render instead.## 🚢 Deploy with Heroku (Legacy)---4. Continue with environment setup...3. Image URL: `docker.io/yourusername/energy-monitor:latest`2. Select "Deploy existing image from a registry"1. Create new Web Service### Deploy on Render from Docker Hub```docker push yourusername/energy-monitor:v1.0.0docker tag yourusername/energy-monitor:latest yourusername/energy-monitor:v1.0.0# Tag versiondocker push yourusername/energy-monitor:latest# Push to Docker Hubdocker build -t yourusername/energy-monitor:latest .# Build imagedocker login# Login to Docker Hub```bash### Build & Push Docker Image## 🐳 Deploy with Docker Hub---3. Click "Deploy" button (top right)2. Select "energy-monitor" service1. Go to Render dashboardOption 2: **Manual via Render**```# Render auto-deploys!git push origin main# Just push to main branch```bashOption 1: **Automatic (via GitHub)**## 🔄 Update Deployment (After Code Changes)---```curl -I https://energy-monitor.onrender.com# Check application healthrender logs energy-monitor# Or use Render CLI (if installed)Settings → Logs# View logs in Render dashboard```bash### Monitor Deployment- [ ] No hardcoded secrets in logs- [ ] UI loads and displays data- [ ] Health check endpoint responds (port 10000)- [ ] Logs show no errors- [ ] Database connections work- [ ] App is accessible at the URL## 📋 Post-Deployment Checklist---4. App will be available at `https://energy-monitor.onrender.com`3. View logs during build2. Wait for build to complete (5-10 min)1. Click "Create Web Service"### Step 6: DeployRender will automatically detect `Dockerfile` in your repo.### Step 5: Configure Docker (Already Done!)⚠️ **DO NOT commit these values!** Use Render's environment variable UI.```STREAMLIT_LOGGER_LEVEL=infoSTREAMLIT_SERVER_PORT=10000DB_SSL=requireDB_PORT=5432DB_HOST=<your_cluster>.c-2.eu-central-1.aws.neon.techDB_PASSWORD=<your_neon_password>DB_USER=<your_neon_user>DB_NAME=neondb```Go to "Environment" section and add:### Step 4: Set Environment Variables| **Plan** | Free or Paid (free tier has limitations) || **Region** | Europe (Frankfurt) or your preferred || **Environment** | Docker || **Name** | energy-monitor ||---------|-------|| Setting | Value |### Step 3: Configure Web Service4. Select the repository and branch (`main`)3. Connect GitHub repository2. Click "New +" → "Web Service"1. Go to [render.com](https://render.com)### Step 2: Connect to Render```git push origin main# Push to main/master branchgit status  # Should be clean# Ensure everything is committed```bash### Step 1: Prepare Repository3. Environment variables configured2. Database URL from Neon (or your PostgreSQL provider)1. GitHub account connected to Render### Prerequisites## 🌐 Deploy to Render.com
## 🌐 Deploy to Render.com

### Prerequisites

1. GitHub account connected to Render
2. Database URL from Neon (or your PostgreSQL provider)
3. Environment variables configured

### Step 1: Prepare Repository

```bash
# Ensure everything is committed
git status  # Should be clean

# Push to main/master branch
git push origin main
```

### Step 2: Connect to Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Select the repository and branch (`main`)

### Step 3: Configure Web Service

| Setting | Value |
|---------|-------|
| **Name** | energy-monitor |
| **Environment** | Docker |
| **Region** | Europe (Frankfurt) or your preferred |
| **Plan** | Free or Paid (free tier has limitations) |

### Step 4: Set Environment Variables

Go to "Environment" section and add:

```
DB_NAME=neondb
DB_USER=<your_neon_user>
DB_PASSWORD=<your_neon_password>
DB_HOST=<your_cluster>.c-2.eu-central-1.aws.neon.tech
DB_PORT=5432
DB_SSL=require

STREAMLIT_SERVER_PORT=10000
STREAMLIT_LOGGER_LEVEL=info
```

⚠️ **DO NOT commit these values!** Use Render's environment variable UI.

### Step 5: Configure Docker (Already Done!)

Render will automatically detect `Dockerfile` in your repo.

### Step 6: Deploy

1. Click "Create Web Service"
2. Wait for build to complete (5-10 min)
3. View logs during build
4. App will be available at `https://energy-monitor.onrender.com`

---

## 📋 Post-Deployment Checklist

- [ ] App is accessible at the URL
- [ ] Database connections work
- [ ] Logs show no errors
- [ ] Health check endpoint responds (port 10000)
- [ ] UI loads and displays data
- [ ] No hardcoded secrets in logs

### Monitor Deployment

```bash
# View logs in Render dashboard
Settings → Logs

# Or use Render CLI (if installed)
render logs energy-monitor

# Check application health
curl -I https://energy-monitor.onrender.com
```

---

## 🔄 Update Deployment (After Code Changes)

Option 1: **Automatic (via GitHub)**
```bash
# Just push to main branch
git push origin main
# Render auto-deploys!
```

Option 2: **Manual via Render**
1. Go to Render dashboard
2. Select "energy-monitor" service
3. Click "Deploy" button (top right)

---

## 🐳 Deploy with Docker Hub

### Build & Push Docker Image

```bash
# Login to Docker Hub
docker login

# Build image
docker build -t yourusername/energy-monitor:latest .

# Push to Docker Hub
docker push yourusername/energy-monitor:latest

# Tag version
docker tag yourusername/energy-monitor:latest yourusername/energy-monitor:v1.0.0
docker push yourusername/energy-monitor:v1.0.0
```

### Deploy on Render from Docker Hub

1. Create new Web Service
2. Select "Deploy existing image from a registry"
3. Image URL: `docker.io/yourusername/energy-monitor:latest`
4. Continue with environment setup...

---

## 🚢 Deploy with Heroku (Legacy)

> ℹ️ Heroku free tier is deprecated. Recommended: Use Render instead.

```bash
# Install Heroku CLI
brew install heroku  # or download from heroku.com

# Login
heroku login

# Create app
heroku create energy-monitor

# Set environment variables
heroku config:set DB_PASSWORD=xxx -a energy-monitor

# Add Procfile (if needed)
echo "web: streamlit run main.py" > Procfile

# Deploy
git push heroku main

# View logs
heroku logs --tail -a energy-monitor
```

---

## 🔒 Security Best Practices

### ✅ DO:

- [ ] Use `.env.example` as template (NOT secrets!)
- [ ] Set environment variables in Render UI (NOT in code)
- [ ] Use strong database password (20+ characters)
- [ ] Enable SSL/TLS for database connection
- [ ] Set `STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false` in prod
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated (`pip-audit`)

### ❌ DON'T:

- [ ] Commit `.env` file (it's in `.gitignore`)
- [ ] Hardcode passwords in code
- [ ] Use weak credentials
- [ ] Expose database URL in logs
- [ ] Deploy with DEBUG mode enabled
- [ ] Trust user input without validation

---

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Render auto-checks health endpoint
# At: App URL / /_stcore/health

# Manual check
curl -v https://energy-monitor.onrender.com/_stcore/health
```

### View Application Metrics

1. Go to Render Dashboard
2. Select "energy-monitor"
3. View:
   - CPU usage
   - Memory usage
   - Network I/O
   - Restart events

### Update Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Check for security vulnerabilities
pip-audit
pip install --upgrade pip

# Update in requirements.txt
pip install --upgrade pandas numpy streamlit

# Test locally first!
pytest tests/ -v

# Then deploy
git push origin main
```

---

## 🚨 Troubleshooting

### App Won't Start

1. Check Render logs:
   ```
   Settings → Logs
   ```

2. Common issues:
   ```
   ❌ ModuleNotFoundError: pip install missing package
   ❌ Connection refused: Database URL missing/wrong
   ❌ Permission denied: Check file permissions
   ❌ Port already in use: Check Streamlit port config
   ```

3. Solution:
   ```bash
   # Run locally first
   python -m streamlit run main.py
   
   # Check logs
   tail -f logs/energy-monitor.log
   
   # Fix issues, then redeploy
   git push origin main
   ```

### Database Connection Issues

```python
# Test connection
import psycopg2

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
print("✅ Connected!")
```

### Memory Issues

1. Check Render plan (free tier has 512MB RAM limit)
2. Optimize pandas operations (use `dtype` conversions)
3. Clear caches: `@st.cache_data.clear()`
4. Upgrade to paid plan if needed

### Performance Issues

1. Enable caching:
   ```python
   @st.cache_data
   @st.cache_resource  # For expensive operations
   ```

2. Optimize queries:
   ```sql
   -- Add indexes
   CREATE INDEX idx_timestamp ON data(timestamp);
   CREATE INDEX idx_region ON data(region_name);
   ```

3. Use pagination for large datasets

---

## 📈 Scaling

### Vertical Scaling (Bigger Machine)
1. Render Dashboard → Select app
2. Settings → Instance Type
3. Choose higher tier (Standard, Professional, etc.)

### Horizontal Scaling (Multiple Instances)
1. Upgrade to paid plan
2. Set replicas in configuration
3. Render will load-balance automatically

---

## 🔔 Notifications & Alerts

### Enable Slack/Email Notifications

Render → Settings → Notifications:
- Deploy events
- Build failures
- Service crashes
- Alert threshold exceeded

---

## 📋 Release Checklist

Before deploying to production:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code linting passes (`flake8 src/ core/ ml/`)
- [ ] Type checking passes (`mypy src/ core/ ml/`)
- [ ] No hardcoded secrets
- [ ] Environment variables configured in Render UI
- [ ] Database backup taken
- [ ] CHANGELOG updated
- [ ] Version bumped (if using semantic versioning)
- [ ] README updated (if applicable)
- [ ] DEVELOPMENT.md updated (if applicable)

```bash
# Final pre-deployment commands
pytest tests/ -v
flake8 src/ core/ ml/ ui/
mypy src/ core/ ml/ --ignore-missing-imports
black --check src/ core/ ml/ ui/

# Tag release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Deploy
git push origin main
```

---

## 🎯 Continuous Deployment (CI/CD)

We've configured GitHub Actions to:

1. ✅ Run tests on every push
2. ✅ Run code quality checks
3. ✅ Build Docker image
4. ✅ Push to Docker Hub
5. ✅ Auto-deploy to Render

**No manual deployment needed!** Just push to `main` and CI/CD takes care of everything.

```bash
# Workflow:
1. git commit -am "feat: add new feature"
2. git push origin main
3. GitHub Actions runs tests
4. If tests pass → Docker builds & pushes
5. Render auto-deploys
6. App updated in 5-10 minutes
```

---

## 📞 Support & Help

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Neon Docs**: https://neon.tech/docs
- **GitHub Issues**: Report bugs in this repo

---

Happy deploying! 🚀
