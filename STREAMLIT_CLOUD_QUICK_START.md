# 🚀 Streamlit Cloud - Quick Start (5 Minutes)

## Step 1: Push to GitHub (2 min)

```bash
git init
git add app.py requirements.txt Procfile .gitignore soil_lookup.py adaboost.ipynb fertilizer_recommendation.csv models/ .streamlit/
git commit -m "AGRI-SMART deployment"
git remote add origin https://github.com/YOUR_USERNAME/agri-smart.git
git branch -M main
git push -u origin main
```

---

## Step 2: Create Streamlit Cloud Account (1 min)

1. Go to https://streamlit.io/cloud
2. Click "Sign up"
3. Click "Continue with GitHub"
4. Authorize Streamlit

---

## Step 3: Deploy Your App (1 min)

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select:
   - **Repository:** `agri-smart`
   - **Branch:** `main`
   - **Main file:** `app.py`
4. Click "Deploy"

---

## Step 4: Wait for Launch (30-60 sec)

Streamlit Cloud will:
- ✅ Clone your repo
- ✅ Install dependencies
- ✅ Launch your app
- ✅ Assign URL

---

## Step 5: Open Your App ✅

Your app is live at:
```
https://agri-smart-[random].streamlit.app
```

---

## Test Your App

1. Upload a leaf image
2. Click "Analyse"
3. Verify results display

---

## That's It! 🎉

Your AGRI-SMART app is now live on Streamlit Cloud!

---

## Useful Links

- **Streamlit Cloud:** https://streamlit.io/cloud
- **Dashboard:** https://share.streamlit.io
- **Docs:** https://docs.streamlit.io

---

**Status:** ✅ Ready to Deploy  
**Time:** 4-5 minutes  
**Cost:** FREE
