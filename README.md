# Python-Minesweeper-Bot
Minesweeper Solver Bot with Playwright library

# LAST CHANGES:
Click function is changed. I was useing win32api/win32con library and it doesn't work on non-windows operating systems so I changed function to use pynput for better cross-platform compatibility.

# Please read whole text for better understanding about the Bot.
After you run the code and choose the difficulty, chrome browser and then the website (https://minesweeperonline.com) will open.

Because I haven't added First_click funcion to make the bot to start you need to click a cell/box.

When you calling the bot you might want to check your computer's DPI (Dots Per Inch) in settings otherwise the clicking function might click wrong place. Because I'm on laptop, my DPI is 1.25 (default).

#
I added AddBlocker so you won't see any adverts and it helps to load page faster (I guess. I didn't test it but it should).

I haven't added Reset_on_death and Reset_on_Win functions so it does't restart when it dies or wins. For who don't know the website or minesweeper you should click to the emoji face to restart.

Important: When it dies, it may click non-stop and you won't be able to resart. If that happens Press "R" to Pause the bot or Press "ESC" to close program.

Minesweeper isn't a game you can win with 100% certainty. You might get stuck with a lot of luck dependent situations and that also goes for the Bot. Because of that, I am going to add random click function and it will click random unopened cell to chanse of being able to continue.

#
It has an issue: normally when you set a record, a pop-up or alert shows up but, for reasons I've yet to know the pop-up is not opening and the record's name becomes "unknown" by default. The website has an anti-bot detector which prevents our records from being saved on the leaderboard but, it's not a problem because I made this code only for educational purposes. I like playing minesweeper and I respect other players so I won't try to get past the anti-bot detector.

WARING: When you use the bot and win, the anti-bot detection bans your IP (I guess. I'm not very sure what it does). First your record will stay on leaderboard for some time but when it detected and deleted, your name won't even show up on the leaderboard.

# Controls:
Press "R" to Pause/Resume

Press "ESC" to CLOSE program.

# USED LIBRARIES:
1) PlayWright (sync_playwright)
2) pynput
3) keyboard
4) time
