# 📅 Reel Scheduler — How To Use (Daily Guide)

Your Instagram reel scheduler. You add reels, it posts them automatically — PC can be off.

---

## ⭐ THE GOLDEN ROUTINE (do this every time you add reels)

Open Claude Code in the project folder, then:

**1. SYNC (always first — gets latest statuses from the cloud)**
```
.\.venv\Scripts\python.exe sync.py
```
Wait for: `SYNC COMPLETE`

**2. EDIT your schedule**
- Drop new video files into the `videos\` folder.
- Open `schedule.xlsx`, add rows: Reel Name (exact filename incl. `.mp4`), Caption, Date & Time.
- Leave the **Status** and **Video URL** columns BLANK — the app fills them.
- **Save and CLOSE the file** (close it, or the next step can't write to it).

**3. PUSH (uploads videos + sends schedule to the cloud)**
```
.\.venv\Scripts\python.exe push.py
```
Wait for: `PUSH COMPLETE`

**That's it. Turn your PC off. The cloud posts each reel at its time.**

---

## 📝 RULES FOR THE EXCEL

| Column | You fill? | Notes |
|---|---|---|
| Reel Name | ✅ Yes | EXACT filename, including `.mp4`. e.g. `reel-7.mp4` |
| Caption | ✅ Yes | Emojis + hashtags fine |
| Date & Time of Publish | ✅ Yes | Format: `20-Jun-2026, 6:00 PM` (IST) |
| Status | ❌ No — leave blank | App writes: Posted / Missed / Failed |
| Video URL | ❌ No — leave blank | App fills after upload |

**Order always = SYNC → edit → PUSH.** Never edit without syncing first (avoids conflicts).

---

## ⏰ TIMING — IMPORTANT

- The cloud checks every ~10 minutes, and GitHub is often **5–15 min late**.
- A reel set for `6:00 PM` may actually post **6:05–6:15 PM**. This is normal (free tier).
- **Never schedule two reels less than ~15 min apart** — only one posts per check.
- A reel more than 10 min past its time when first seen = marked **Missed** (never posts late, by design).

---

## 🚦 WHAT THE STATUSES MEAN

- **Posted** → went live ✅
- **Missed** → its time passed before the app saw it; never posted.
- **Failed** → tried to post but errored (bad video, expired token). Check the reel/video.
- **Posting** → ⚠️ a run got interrupted mid-post. Check Instagram manually: if it posted, set Status to `Posted`; if not, clear the cell to retry.
- **(blank)** → scheduled, waiting.

To re-try a Missed/Failed reel: SYNC → clear its Status cell + set a new future time → PUSH.

---

## 🔑 THE TOKEN EXPIRES EVERY ~60 DAYS

Your Instagram token dies around **mid-August 2026**. After that, every post fails with a
`*** TOKEN EXPIRED ***` line in the logs.

**Set a phone reminder for ~55 days out.** When it expires, you regenerate the token
(see TOKEN_REFRESH.md) and update it in TWO places:
1. Local `config.env`
2. GitHub repo secret `IG_ACCESS_TOKEN`

---

## 🆘 IF SOMETHING BREAKS

- **"Close schedule.xlsx first"** → the file is open in Excel. Close it, re-run.
- **push.py says "run sync.py first"** → you forgot to sync. Run sync.py, then push.py.
- **Merge conflict** → don't fight it. Bring it to Claude.
- **A reel didn't post** → check its Status. Failed/Missed tells you why. Check token isn't expired.
- **Anything confusing** → open this project with Claude and paste the error.

---

## 📂 WHERE THINGS LIVE

- Videos (your PC only, never uploaded to GitHub): `videos\`
- Your schedule: `schedule.xlsx`
- Secrets (your PC only, never shared): `config.env`
- The cloud schedule + code: github.com/acesofallarticles-web/video-scheduler
- Cloud run logs: that repo → **Actions** tab
