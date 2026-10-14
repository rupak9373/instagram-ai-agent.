# Instagram GitHub Actions agent — safe preview

Creates a daily short vertical video preview on GitHub Actions (no VPS). **Does NOT auto-publish to Instagram.**

- Research: public Google News RSS headlines about design, colors and motion (not Instagram trends).
- Planning: transparent keyword scoring, **not an AI language model**.
- Generation: 8-second 720×1280 procedural animation via Pillow and FFmpeg, **not a text-to-video model**.
- Output: GitHub Actions artifact with `reel.mp4` and `plan.json`; artifact retained for 3 days.

## Run
1. Open **Actions → Daily Instagram Agent (Safe Preview) → Run workflow**.
2. Wait for the run to complete.
3. Download `reel-preview-...` from the workflow run's Artifacts.

## Important
No passwords required for the preview. Never commit API tokens to this **public** repository. Proper AI topic research, generative video API, Meta/Instagram Graph API publishing, storage of a publicly downloadable video and account-performance analytics must be implemented and tested separately. Scheduled GitHub Actions may be delayed or skipped, and public repository scheduled workflows may be disabled after 60 days without repository activity. Free access cannot be guaranteed forever.
