# Python-Minesweeper-Bot
Minesweeper Solver Bot with Playwright library

# LAST CHANGES:
- Added "Non_Logical_action" function. It is responsible for trying to solve 50/50 or other luck-based, unsolvable with logic parts. Check "Explanation.md" if you want more detail about how it works.

- Added a function called "No_Unflagged_Bomb_Left_Action" and its purpose is: when all the bombs are found, it opens all the unopened cells/boxes to finish the game.
  
- Click function has changed again. Now it doesn't click on the screen, it clicks on the browser so you can close the window and it is going to run in the backround. This change also made clicking safer and no need left to check DPI scale.

- Added some optional settings that you set when you are starting the bot. Check "Explanation.md" if you want to see.
  
- Deleted "OTO_Logic" function because it makes mistakes and there was no need for it.
### Small changes:
- Added Statistics. It shows up when you close the bot (Only works if "Restart_on_Win" and other settings are enabled).
  - I need to explain something. If you look at the statistics of survival chances on death and win, you'll see that the average survival chance on win is actually lower than on death. And it looks a bit strange. The reason for this is:

    In order for the bot to win the game, it has to survive all the luck-based situations. Since there are many of them, the cumulative survival chance gets lower and lower. However, the survival chance on death is different. For example, in a 50/50 situation, if the bot picks the bomb cell/box to open and dies, the survival chance would be 50%. But if the bot picks the safe cell/box to open, it can find itself with another 50/50 situation and if it dies there, the survival chance would be 25%. So, when the bot dies early, it doesn't face all the possible risks, which makes its recorded survival chance higher than a full winning run.
- Added found bomb counter.
- Added chance calculator. It shows chance of survival when the bot dies and wins.
## OLD CHANGES:
- Click function has changed. I was using win32api/win32con library and it doesn't work on non-windows operating systems so I changed function to use pynput for better cross-platform compatibility.
  
- I added AddBlocker so you won't see any adverts and it helps to load page faster.

# Please read whole text for better understanding about the bot.
After you run the code and choose the difficulty, chrome browser and then the website (https://minesweeperonline.com) will open.

If you didn't change "Auto_Start" to true when calling the bot, you need to click a cell/box to the bot to start.It wont restart on win if you didn't change "Restart_on_Win" to true (by the way you need to press emoji face to restart if you didn't know). Check "Explanation.md" for settings.

#
It has an issue: normally when you set a record, a pop-up or alert shows up but, for reasons I've yet to know the pop-up is not opening and the record's name becomes "unknown" by default. The website has an anti-bot detector which prevents our records from being saved on the leaderboard but, it's not a problem because I made this code only for educational purposes. I like playing minesweeper and I respect other players so I won't try to get past the anti-bot detector.

WARING: When you use the bot and win, the anti-bot detection bans your IP (I guess but I'm not very sure). At the first time your record will stay on leaderboard for some time but when it detected and deleted, your name won't even show up on the leaderboard.

#
It has another issue for now. Sometimes it keeps flagging and unflagging same place. I yet to know why that is happening. To solve this you need to click another cell/box to break the loop or quit.

# Controls:
Press "R" to Pause/Resume

Press "ESC" to CLOSE the program.

# USED LIBRARIES:
1) PlayWright (sync_playwright)
2) pynput (mouse)
3) keyboard
4) time
5) re 


