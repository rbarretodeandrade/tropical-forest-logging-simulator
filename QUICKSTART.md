# 🚀 Quick Start Guide - Tropical Forest Simulator Web App

## Run the App in 3 Commands

```bash
cd /Users/rbarretodeandrade/tropical_forest_streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## What You'll See

### Sidebar (Left)
- **Scenario Selector:** Choose Amazon, SE Asia, Congo, or Central America
- **Logging Controls:** 3 operations with year and intensity sliders

### Main Area (Center)
- **Metrics:** Final Carbon, Wood Products, Penalty, Final Score
- **Status:** Green (✅ Sustainable), Orange (⚠️ Moderate), Red (❌ Severe)
- **Interactive Chart:** Carbon dynamics over 100 years with threshold lines

### Expandable Sections
- **Compare Strategies:** See how you stack up against optimal approaches
- **Learn the Science:** Understanding old-growth dynamics

---

## Try These Strategies

### 1. Optimal Strategy (Should Score ~75 points)
- Operation 1: Year 10, Intensity 25%
- Operation 2: Year 55, Intensity 25%
- Operation 3: Leave at 0

**Expected Result:** 75.3 points, ⚠️ Moderate Degradation (but WINNER!)

### 2. Heavy Single Cut (Should Score ~44 points)
- Operation 1: Year 10, Intensity 35%
- Operation 2: Leave at 0
- Operation 3: Leave at 0

**Expected Result:** 44.0 points, ⚠️ Moderate Degradation (LOSES)

### 3. Three Cuts (Should FAIL - ~17 points)
- Operation 1: Year 10, Intensity 15%
- Operation 2: Year 45, Intensity 15%
- Operation 3: Year 80, Intensity 15%

**Expected Result:** 17.2 points, ❌ Severe Degradation (FAILED)

---

## Deploy to Cloud (FREE!)

### Option 1: Streamlit Cloud (Easiest)

1. **Create GitHub repo:**
   ```bash
   cd /Users/rbarretodeandrade/tropical_forest_streamlit_app
   git init
   git add .
   git commit -m "Initial commit - Tropical Forest Simulator"
   ```

2. **Push to GitHub:**
   - Create new repo at github.com
   - Follow instructions to push

3. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repo
   - Set main file: `app.py`
   - Click "Deploy"!

4. **Share:**
   - You'll get a URL like: `https://tropical-forest-sim.streamlit.app`
   - Share with students!

### Option 2: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

---

## Troubleshooting

### "streamlit: command not found"
```bash
pip install streamlit
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Chart not showing
- Make sure plotly is installed: `pip install plotly`

---

## Next Steps

1. ✅ Test locally
2. ✅ Try all 4 scenarios
3. ✅ Verify calculations match Excel version
4. 🚀 Deploy to Streamlit Cloud
5. 📧 Share URL with students
6. 🎓 Use in class!

---

**You're ready to go!** 🌴📊🎓
