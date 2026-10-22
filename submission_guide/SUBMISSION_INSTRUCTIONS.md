# Unified Mentor Submission Form: Step-by-Step Instructions

This guide provides instructions to fill out all four mandatory fields on the **Unified Mentor Project Submission Form**.

---

## Overview of the 4 Submission Fields

```
+---------------------------------------------------------------------------------------------------------+
|                                    SUBMISSION FORM FIELDS MAPPING                                       |
+---------------------------------------------------------------------------------------------------------+
| Field 1: Github Repository Link *      --> https://github.com/<your-username>/nassau-candy-optimization |
| Field 2: Research paper link *         --> GitHub link or Google Drive link to RESEARCH_PAPER.md / PDF  |
| Field 3: Deployed project link *       --> https://<your-subdomain>.streamlit.app                       |
| Field 4: Project Feedback video link * --> https://youtu.be/<your-video-id> or Google Drive Video Link   |
+---------------------------------------------------------------------------------------------------------+
```

---

## Field 1: GitHub Repository Link

### Step 1: Initialize and Push Your Local Project to GitHub
1. Create a new repository on your GitHub account ([github.com/new](https://github.com/new)):
   - **Repository Name:** `nassau-candy-optimization`
   - **Visibility:** Public
   - Do **not** initialize with a README (you already have a complete one).
2. Open your terminal in `C:\Users\Navin D\.gemini\antigravity\scratch\nassau-candy-optimization` and run:
   ```bash
   git init
   git add .
   git commit -m "feat: complete factory reallocation & shipping optimization recommendation system"
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/nassau-candy-optimization.git
   git push -u origin main
   ```
3. Copy the URL of your repository:
   - Example: `https://github.com/YourUsername/nassau-candy-optimization`

---

## Field 2: Research Paper Link

You have two professional options:

### Option A (Direct GitHub Markdown View - Recommended):
Once you push your repository to GitHub, link directly to the research paper on GitHub:
- `https://github.com/<YOUR_GITHUB_USERNAME>/nassau-candy-optimization/blob/main/research_paper/RESEARCH_PAPER.md`

### Option B (Google Drive PDF / Document):
1. Open `research_paper/RESEARCH_PAPER.md` and export or copy it to Google Docs.
2. In Google Drive, click **Share** -> Change General Access to **"Anyone with the link can view"**.
3. Copy and paste that link into the form.

---

## Field 3: Deployed Project Link (Streamlit Web App)

Deploy your application for free to **Streamlit Community Cloud** in 2 minutes:

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **"New app"**.
3. Fill in the deployment details:
   - **Repository:** `<YOUR_GITHUB_USERNAME>/nassau-candy-optimization`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"**.
5. Once your app is live (in about 1-2 minutes), copy the public URL:
   - Example: `https://nassau-candy-optimization.streamlit.app`
6. Paste this URL into the **Deployed project link** field.

---

## Field 4: Project Feedback Video Link

1. Review the full speaking script provided in:
   - `submission_guide/PROJECT_FEEDBACK_VIDEO_SCRIPT.md`
2. Record your screen and webcam for 3 to 5 minutes using any tool:
   - **Loom** (free browser extension)
   - **OBS Studio**
   - **Zoom** (start a meeting with just yourself, share screen, and click "Record to Computer")
3. Upload your recording:
   - **YouTube:** Upload video and set visibility to **"Unlisted"** (or Public).
   - **OR Google Drive:** Upload MP4 and set sharing to **"Anyone with the link can view"**.
4. Test the link in a private/incognito browser window to make sure anyone can view it.
5. Paste the video link into the form.

---

## Final Verification Before Clicking "Submit URLs"

- [x] **Github Repository Link** starts with `https://github.com/` and is publicly accessible.
- [x] **Research Paper Link** starts with `https://` and opens the research paper.
- [x] **Deployed Project Link** starts with `https://` and loads the live Streamlit dashboard.
- [x] **Project Feedback Video Link** starts with `https://` and plays the recorded feedback video.
