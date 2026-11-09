# Panel rating task (read fully before starting)

You are role-playing ONE real Indonesian TikTok user (persona below). You will rate 45 TikTok photo-carousel posts from a parenting account, exactly as that person would react while scrolling the For You page at night.

## Rules
- Only read files inside this folder: PANEL_DIR (packet.json and img/P01.jpg ... img/P45.jpg). Do NOT open any other file or folder, do not search the web, do not look for view counts. This is a blind test.
- For every post: first Read img/<code>.jpg (that is slide 1, what you see on the feed), decide "stop". Then read that post's slide text and caption in packet.json and decide the rest.
- Be a real scroller, not a reviewer. Most posts on a busy FYP get skipped within a second. Reward only what YOU (this persona, with your child's age and your life) would actually stop for, save or send. Quality you don't personally care about scores low. Use the full 1-10 range; a typical post should land around 3-5, and only a few should get 8+.
- Work through the posts in order P01 to P45. Do not compare or re-rank at the end; rate each on its own.

## Scores per post (integers 1-10)
- stop: seeing only slide 1 on the feed, how likely you stop scrolling
- swipe: if you stopped, how likely you swipe through to the last slide
- save: how likely you tap save (bookmark) to use later
- send: how likely you send it to someone (say who in the note)
- comment: how likely you comment
- note: one short line in casual Indonesian, in your voice, why

## Output
Write a JSON array to OUT_FILE: [{"code":"P01","stop":4,"swipe":5,"save":3,"send":2,"comment":1,"note":"..."}, ...] with all 45 codes. Validate it parses (python3 -c "import json;print(len(json.load(open('OUT_FILE'))))"). Then reply with just: done, the count, and your 3 highest-stop codes.
