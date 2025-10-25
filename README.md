# 🌴 Tropical Forest Logging Simulator - Streamlit Web App

Interactive web application for exploring trade-offs between timber extraction and forest carbon conservation in old-growth tropical rainforests.

## 🚀 Quick Start

### Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

### Deploy to Streamlit Cloud (FREE!)

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Select `app.py` as the main file
5. Click "Deploy"!

Your app will be live at: `https://your-app-name.streamlit.app`

---

## 📊 Features

### Interactive Controls
- **Scenario Selector:** Choose from 4 tropical forest regions (Amazon, SE Asia, Congo, Central America)
- **Logging Operations:** Design up to 3 logging entries with sliders for year and intensity
- **Real-time Results:** See carbon dynamics chart and score update instantly

### Visualizations
- **Dynamic Chart:** Plotly interactive chart showing carbon recovery over 100 years
- **Threshold Lines:** Visual indicators for 97% and 90% degradation thresholds
- **Logging Annotations:** Arrows showing when and how much you logged

### Scoring System
- **2-Tier Penalty:** -40 points for <97%, -80 points for <90%
- **Base Score:** Wood Products × 2
- **Final Score:** Base Score + Penalty
- **Status Indicators:** ✅ Sustainable, ⚠️ Moderate Degradation, ❌ Severe Degradation

### Educational Content
- **Strategy Comparison:** Compare your strategy with optimal approaches
- **Science Explanation:** Learn about old-growth dynamics and recovery
- **Tips & Score Ranges:** Guidance for optimal strategies

---

## 🎓 How to Use in Class

### Option 1: Live Demo (20 minutes)
1. Open the app in class
2. Demonstrate different strategies:
   - One heavy cut (35%)
   - Two moderate cuts (25% each)
   - Three light cuts (15% each)
3. Show how scores change
4. Discuss trade-offs

### Option 2: Student Activity (50 minutes)
1. Share the app URL with students
2. Assign each group a different scenario
3. Groups design optimal strategy for their region
4. Present strategies and scores
5. Class discussion on trade-offs

### Option 3: Homework Assignment
1. Students explore all 4 scenarios
2. Find optimal strategy for each
3. Write brief report justifying choices
4. Compare across scenarios

---

## 🌍 Scenarios

### 1. Amazon Basin (Brazil) 🌳
- **Context:** FSC-certified, high-value mahogany
- **Constraints:** Environmental scrutiny, certification requirements
- **Intensities:** Low 15% | Medium 25% | High 35%

### 2. SE Asian Dipterocarp (Borneo) 🌴
- **Context:** Steep terrain, orangutan habitat
- **Constraints:** Erosion risk, biodiversity concerns, REDD+ available
- **Intensities:** Low 15% | Medium 20% | High 30%

### 3. Congo Basin (Central Africa) 🦍
- **Context:** Remote, minimal infrastructure
- **Constraints:** High costs, wildlife corridor
- **Intensities:** Low 12% | Medium 22% | High 32%

### 4. Central America (Costa Rica/Panama) 🐒
- **Context:** Ecotourism value, biological corridor
- **Constraints:** PES payments, environmental protection
- **Intensities:** Low 10% | Medium 20% | High 30%

---

## 📈 Optimal Strategies

| Strategy | Final Carbon | Score | Result |
|----------|--------------|-------|--------|
| Two 25% (Years 10, 55) | 270.6 Mg (90%) | **75.3** | ⭐ Best |
| Two 20% (Years 10, 55) | 276.2 Mg (92%) | 53.0 | ✓ Good |
| One 25% (Year 10) | 292.5 Mg (98%) | 60.0 | ✓ Good |
| One 35% (Year 10) | 289.5 Mg (97%) | 44.0 | ⚠️ Poor |
| Three 15% (Years 10, 45, 80) | 260.4 Mg (87%) | 17.2 | ❌ Failed |

**Key Insight:** Two moderate entries maximize wood products while staying above severe degradation threshold.

---

## 🔬 The Science

### Old-Growth Equilibrium
- Mature tropical forests at dynamic equilibrium (300 Mg C/ha)
- Tree growth = Tree mortality
- **Not net carbon sinks!**

### Very Slow Recovery
**Formula:** C(t+5) = C(t) + 0.12 × (300 - C(t))

After 25% logging (300 → 225 Mg):
- Year 25: 245 Mg (27% recovered)
- Year 50: 267 Mg (56% recovered)
- Year 75: 283 Mg (77% recovered)
- Year 100: 294 Mg (92% recovered)

### 2-Tier Penalty System
- **≥97% (291 Mg):** No penalty (sustainable)
- **<97% (291 Mg):** -40 points (moderate degradation)
- **<90% (270 Mg):** -80 points (severe degradation)

**Why these thresholds?**
- 97%: Ecosystem function begins to decline
- 90%: Biodiversity significantly affected
- Based on empirical studies of logged tropical forests

---

## 💻 Technical Details

### Key Functions

**`recover_carbon(initial_carbon, years, k=0.12)`**
- Calculates exponential recovery to equilibrium
- Uses 5-year time steps
- Returns final carbon stock

**`simulate_logging(operations)`**
- Simulates 100 years of forest dynamics
- Applies logging at specified years
- Returns DataFrame with carbon over time

**`calculate_score(df, operations)`**
- Calculates wood products (40% of harvested)
- Applies 2-tier penalty system
- Returns score breakdown and status

### Technologies
- **Streamlit:** Web framework
- **Plotly:** Interactive charting
- **Pandas:** Data manipulation
- **NumPy:** Numerical calculations

---

## 🎨 Customization

### Change Recovery Rate
Edit `k` parameter in `recover_carbon()`:
```python
def recover_carbon(initial_carbon, years, k=0.12):  # Default: 0.12
```
- Higher k = faster recovery
- Lower k = slower recovery

### Adjust Penalty Thresholds
Edit thresholds in `calculate_score()`:
```python
if final_carbon < 270:  # Change 270 to adjust 90% threshold
    penalty = -80
elif final_carbon < 291:  # Change 291 to adjust 97% threshold
    penalty = -40
```

### Add New Scenarios
Add to `SCENARIOS` dictionary:
```python
"Your Region": {
    "description": "...",
    "context": "...",
    "intensities": [low, medium, high],
    "icon": "🌲"
}
```

---

## 📚 Educational Value

### Learning Objectives
Students will:
- ✓ Understand old-growth forests are carbon-neutral
- ✓ Recognize extremely slow tropical forest recovery
- ✓ Quantify trade-offs between extraction and conservation
- ✓ Evaluate "sustained yield" concept
- ✓ Discuss whether cumulative degradation is sustainable

### Discussion Questions
1. **Is "sustained yield" sustainable?** Two 25% entries leave forest at 90%
2. **Who wins and who loses?** Current generation gets timber, future inherits degraded forest
3. **Are penalties appropriate?** Should degradation be penalized more/less?
4. **Scale matters:** One hectare vs. entire landscape?
5. **Alternatives?** REDD+ payments for standing forests?

---

## 🆚 Streamlit App vs. Excel

| Feature | Excel | Streamlit App |
|---------|-------|---------------|
| Accessibility | Need Excel | Just a URL |
| Interactivity | Manual edits | Real-time sliders |
| Visualizations | Static | Animated, zoomable |
| Deployment | Email file | One URL |
| Mobile-friendly | Poor | Excellent ✓ |
| Updates | Resend file | Update once, live for all |
| Engagement | Low | High ✓ |

---

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended - FREE!)
- Push to GitHub
- Deploy at share.streamlit.io
- Gets URL like `your-app.streamlit.app`
- Auto-updates when you push changes

### 2. Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### 3. AWS/GCP/Azure
- Run as Docker container
- Use any cloud platform
- More control, but costs money

---

## 📦 Project Structure

```
tropical_forest_streamlit_app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

---

## 🤝 Contributing

Suggestions for improvements:
- Add leaderboard functionality
- Export results as PDF report
- Add more scenarios
- Include biodiversity metrics
- Add economic analysis (NPV, timber prices)
- Multi-language support

---

## 📝 License

This educational tool is provided as-is for classroom use.

---

## 📧 Support

For questions or issues, refer to the Streamlit documentation: https://docs.streamlit.io

---

## 🎯 Next Steps

1. **Run locally** to test
2. **Deploy to Streamlit Cloud** for class use
3. **Share URL** with students
4. **Collect feedback** and iterate!

**Enjoy teaching the complexities of tropical forest management!** 🌴📊🎓
