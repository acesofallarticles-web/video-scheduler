# 📅 Reel Scheduler — How To Use (Daily Guide)

Your Instagram reel scheduler. You add reels from your PC, then post them with one tap in the GitHub app — your PC can be off when you post.

---

## ⭐ THE GOLDEN ROUTINE (do this every time you add reels)

Open Claude Code in the project folder, then:

**1. EDIT your schedule**
- Drop new video files into the `videos\` folder.
- Open `schedule.xlsx`, add rows: Reel Name (exact filename incl. `.mp4`), Caption, Date & Time.
- Leave the **Status** and **Video URL** columns BLANK — the app fills them.
- **Save and CLOSE the file** (close it, or push.py can't run).

**2. PUSH (this is now the only command you need)**
\`\`\`
.\.venv\Scripts\python.exe push.py
\`\`\`
push.py automatically does everything in the safe order:
- Checks the Excel file is closed
- Syncs the latest statuses from the cloud (no more manual sync needed)
- Uploads your new videos to Cloudinary
- Pushes the schedule to GitHub

Wait for: \`PUSH COMPLETE\`

**That's it for adding reels. Your PC can now be off.**

**3. POST (from your phone, around each slot)**
- Open the **GitHub app** → your `video-scheduler` repo → **Actions** tab → **Reel Scheduler**.
- Tap **"Run workflow"**.
- **One tap posts ALL currently-due reels** (any reel whose time has passed and isn't already posted), **oldest first**, a few seconds apart.

So you just tap "Run workflow" around each posting slot (e.g. after 10 AM, 3 PM, 6 PM). It doesn't have to be exact — whatever is due will go out on the next tap. There is **no automatic timer**; nothing posts until you tap.

> 💡 push.py now syncs by itself. You only run \`sync.py\` separately if you just want
> to refresh statuses into your local Excel WITHOUT uploading anything (e.g. to check
> what posted). For normal use, \`push.py\` alone is enough.

---

## 📝 RULES FOR THE EXCEL

| Column | You fill? | Notes |
|---|---|---|
| Reel Name | ✅ Yes | EXACT filename, including \`.mp4\`. e.g. \`reel-7.mp4\` |
| Caption | ✅ Yes | Emojis + hashtags fine |
| Date & Time of Publish | ✅ Yes | Format: \`20-Jun-2026, 6:00 PM\` (IST) |
| Status | ❌ No — leave blank | App writes: Posted / Failed |
| Video URL | ❌ No — leave blank | App fills after upload |

---

## ⏰ TIMING — IMPORTANT

- **Posting is manual.** Nothing posts on its own — a reel goes live only when you tap **"Run workflow"** in the GitHub app.
- The Date & Time in the Excel just decides *when a reel becomes due* (eligible to post). It is not an automatic timer.
- **One tap posts everything that's currently due**, oldest first. Tap a bit after each slot (e.g. just after 10 AM, 3 PM, 6 PM).
- Being late to tap is fine — a reel that's overdue stays due and posts on your next tap. Reels are **never** skipped for being late.
- You can schedule reels as close together as you like — a single tap posts all of them, in scheduled order.

---

## 🚦 WHAT THE STATUSES MEAN

- **Posted** → went live ✅
- **Failed** → tried to post but errored (bad video, expired token). Check the reel/video.
- **Posting** → ⚠️ a run got interrupted mid-post. Check Instagram manually: if it posted, set Status to \`Posted\`; if not, clear the cell to retry.
- **(blank)** → due or waiting; will post on your next "Run workflow" tap once its time has passed.

To re-try a Failed reel: clear its Status cell → run \`push.py\` → tap "Run workflow" (it's due immediately if its time has passed).

---

## 🔑 THE TOKEN EXPIRES EVERY ~60 DAYS

Your Instagram token dies around **mid-August 2026**. After that, every post fails with a
\`*** TOKEN EXPIRED ***\` line in the logs.

**Set a phone reminder for ~55 days out.** When it expires, you regenerate the token
and update it in TWO places:
1. Local \`config.env\`
2. GitHub repo secret \`IG_ACCESS_TOKEN\` (Settings → Secrets and variables → Actions → Repository secrets)

---

## 🆘 IF SOMETHING BREAKS

- **"Close schedule.xlsx first"** → the file is open in Excel. Close it, re-run push.py.
- **"Conflict pulling latest"** → don't fight it. Bring it to Claude.
- **A reel didn't post** → check its Status. Failed/Missed tells you why. Check the token isn't expired.
- **Anything confusing** → open this project with Claude and paste the error.

---

## 📂 WHERE THINGS LIVE

- Videos (your PC only, never uploaded to GitHub): \`videos\\\`
- Your schedule: \`schedule.xlsx\`
- Secrets (your PC only, never shared): \`config.env\`
- The cloud schedule + code: github.com/acesofallarticles-web/video-scheduler
- Cloud run logs: that repo → **Actions** tab

---

## 🧰 THE COMMANDS (reference)

| Command | What it does | When you use it |
|---|---|---|
| \`.\.venv\Scripts\python.exe push.py\` | Sync + upload videos + push schedule | **Every time you add/edit reels** (main command) |
| \`.\.venv\Scripts\python.exe sync.py\` | Just pull latest statuses into local Excel | Only to check what posted, without uploading |
| \`.\.venv\Scripts\python.exe worker.py\` | Post all currently-due reels right now from your PC | Optional — same job as tapping "Run workflow", but run from your PC instead of the phone |
