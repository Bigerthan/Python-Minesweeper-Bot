# How the bot works?
Let's understand how actually bot works.

Firstly, you need to choose between 3 game modes. Then the browser and the website will open and start updateing cell/box data.

## How it "updates" cell/box data?
We can get the website's DOM (Document Object Model) or what I like to say "Live HTML". As you can see at the bottom DOM can give us what we need but how will we get them?

![](MW_PW_photos/DOM.png)

Because we opened the browser with Playwright, we can get all DOM structure whenever we want and filter it to get what we want. But isn't there any better way to do that?

Well, yes. We can use the browser to get cell/box data we need. Because we use the browser we can use Javascript code to filter and get cell/box data and it is faster than getting *all* DOM then filtering it in Python. After we get filtered cell/box data, we are going to process it in Python then feed it to other functions. 

## Then what is after updateing cell/box data?
Quick answer is useing "Logical Actions". But what are those actions that led us to win the game?
#### 1) Basic Logic:

#### 2) Difference Logic:

#### 3) Two Steps Ahead Logic:

#### 4) No Unflagged Bomb Left Action:

#
But are they enough, do you need only this much logical action to win the game?

Well, no. As you know sometimes minesweeper is only a guessing game and you can't do anything with logics so we need some "Non-Logical Functions".
# Setting The Settings:
![](MW_PW_photos/Settings_expl.png)

As you can see, there are 5 parameters at the bot's main (starting) function, which I refer to as "settings". Let's see what is their meanings.
#### 1) AUTO START: 
- ( True / False ; Default = False )
- This is automatic "first click" parameter. If you make this parameter "True", the bot will automaticly start the game when page is loaded; else if you leave this parameter as "False", the bot won't start until you open the first cell/box.

#### 2) Will Reset On Death: 
- ( True / False ; Default = True )
- If you leave this parameter as "True", the bot will automaticly restart if it dies; else if you make this parameter "False", the bot won't restart when it dies and you have to click the face emoji in order to restart and then click a cell/box to start the bot again.

#### 3) Auto Start on Death Restart:
- ( True / False ; Default = True )
- This parameter only makes a difference when 'Will Restart On Death' is "True".
- If you leave this parameter as "True", the bot will automaticly open the first cell/box when "Will Restart On Death" restarts the game; else if you make this parameter "False", it won't open the first cell.

#### 4) Will Reset On Win: 
- ( True / False ; Default = False )
- If you make this parameter "True", the bot will automaticly restart if it wins; else if you leave this parameter as "False", the bot won't restart when it wins and you have to click the face emoji in order to restart and then click a cell/box to start the bot again.

#### 5) Auto Start on Win Restart: 
- ( True / False ; Default = True )
- This parameter only makes a difference when 'Will Reset On Win' is "True".
- If you leave this parameter as "True", the bot will automaticly open the first cell/box when "Will Reset On Win" restarts the game; else if you make this parameter "False", it won't open the first cell.
