from playwright.sync_api import sync_playwright
from pynput.mouse import Button, Controller
import keyboard
import time
import re

class MWPlaywright:
    def __init__(self, url, DPI_scale = 1.25):
        self.url = url
        self.playwright = None
        self.browser = None
        self.context = None #for maximum screen
        self.page = None
        self.is_running = False
        self.face_state = None
        self.face_coord = (0,0)
        self.cell_datas = {}
        self.Status_Translater = { #Didn't add "bomb-death" and "bomb-revealed" becasue they show up on death 
            "blank": "?",
            "bombflagged": "!",
            "open0": 0,
            "open1": 1,
            "open2": 2,
            "open3": 3,
            "open4": 4,
            "open5": 5,
            "open6": 6,
            "open7": 7,
            "open8": 8}
        self.mode = ""
        self.starting_x_coord = None
        self.starting_y_coord = None
        self.col_count = None
        self.row_count = None
        self.bomb_count = None
        self.mouse = Controller() #for clicking function
        self.DPI_scale = float(DPI_scale) #get this from your display settings, e.g., 125% = 1.25
        self.Win_scores = []
        self.Last_win_score = None
        self.Restart_count = 0

    def Add_Blocker(self, route): #to block adverts and make the site faster
        try: 
            url = route.request.url.lower()
            blocked_keywords=[
            "googleads",
            "doubleclick",
            "adservice",
            "analytics",
            "adnxs",
            "facebook"]
            if any(keyword in url for keyword in blocked_keywords):
                route.abort()
            else:
                route.continue_()

        except Exception as e:
            print(f"ADD BLOCKER ERROR:{e}")
            route.continue_()

    def Open_Browser(self):
        print("Starting browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False, args=["--start-maximized","--disable-blink-features=AutomationControlled"]) #headless=False to see the browser...MAYBE ADD SLOW_MO LATER 
        self.context = self.browser.new_context(no_viewport=True) #maximum screen
        self.page = self.context.new_page()
        self.page.route("**/*", self.Add_Blocker) #opens add bllocker
        self.page.goto(self.url)
        self.Set_Mode_Details() 

    def Set_Mode_Details(self): #Game Mode details (row/col count, bomb count, starting cell x/y posissions, face coord)
        if "beginner" in self.url:
            self.mode = "Beginner"
            self.starting_x_coord = 660 #+30 to first cell
            self.starting_y_coord = 228 #+30 to first cell
            self.col_count = 9
            self.row_count = 9
            self.bomb_count = 10
            self.face_coord = (810,190)

        elif "intermediate" in self.url:
            self.mode = "Intermediate"
            self.starting_x_coord = 650 #+30 to first cell
            self.starting_y_coord = 220 #+30 to first cell
            self.col_count = 16
            self.row_count = 16
            self.bomb_count = 40
            self.face_coord = (900,200)

        else:
            self.mode = "Expert"
            self.starting_x_coord = 480 #+30 to first cell
            self.starting_y_coord = 220 #+30 to first cell
            self.col_count = 30
            self.row_count = 16
            self.bomb_count = 99
            self.face_coord = (950,200)

    def Click(self, row, col, action, coords=()): #Clicking function (right,left,middle)
        Absuolute_scale_multiplayer = 1 / self.DPI_scale
        if coords:
            self.mouse.position = (coords[0]*Absuolute_scale_multiplayer,coords[1]*Absuolute_scale_multiplayer)
            if action == "left":
                self.mouse.click(Button.left, 1)
            elif action == "right":
                self.mouse.click(Button.right, 1)
            elif action == "middle": 
                self.mouse.click(Button.middle, 1)
            time.sleep(0.5)
        
        else:
            x = int((self.starting_x_coord + col*30) * Absuolute_scale_multiplayer)
            y = int((self.starting_y_coord + row*30) * Absuolute_scale_multiplayer)

            self.mouse.position = (x, y)
            if action == "left":
                self.mouse.click(Button.left, 1)
            elif action == "right":
                self.cell_datas[(row,col)] = "!" #To change cell to flagged immediately
                self.mouse.click(Button.right, 1)
            elif action == "middle": 
                self.mouse.click(Button.middle, 1)
            time.sleep(0.015)

    def Open_first_cell(self): #automaticly opening middle cell
        self.Click(self.row_count/2,self.col_count/2, "left")

    def Restart_on_Death(self, Auto_Start=False):
        if self.face_state == "facedead":
            time.sleep(0.5) #preventing miss click
            #print("The bot died. Restarting.")
            self.Click(0,0,"left",self.face_coord) #pressing face to restart
            self.Restart_count += 1
            if Auto_Start: self.Open_first_cell()

    def Restart_on_Win(self, Auto_Start=False):
        if self.face_state == "facewin":

            share_text = self.page.inner_text("#share-text")
            Win_score = int(re.findall(r"\d", share_text)[0]) #getting win score (int) from share text
            if Win_score:
                self.Win_scores.append(Win_score)
                self.Last_win_score = Win_score

            time.sleep(0.5)
            #print(f"The bot won the game in {self.Last_win_score} seconds. Restarting.")
            self.Click(0,0,"left",self.face_coord) #pressing face to restart
            self.Restart_count += 1
            if Auto_Start: self.Open_first_cell()

    def Set_DOM_data(self): #cell datas come as "CELL Y_X" --- Javascript code works in browser
        javascript_cell_datas = self.page.evaluate("""() => {
            const squares = document.querySelectorAll('#game .square');
            const data = {};
                
            squares.forEach(sq => {
                if (sq.style.display === 'none') return;                 // Skip hidden squares
                data[sq.id] = sq.className.replace('square ', '');       //1_1: "blank"
            });                   
            return data;
        }""")
        self.cell_datas = {
            (int(key.split("_")[0]),int(key.split("_")[1])): self.Status_Translater.get(status, "?") 
            for key, status in javascript_cell_datas.items()}
        #######
        self.face_state = self.page.get_attribute("#face", "class")
    
    def Get_Neighbors(self, y, x, type="dict"): 
        neighbors_list = []
        for r in [-1,0,1]:
            for c in [-1,0,1]:
                if r == 0 and c == 0:
                    continue
                new_row = y + r
                new_col = x + c
                if 1 <= new_row <= self.row_count and 1 <= new_col <= self.col_count:
                    neighbors_list.append((new_row, new_col))
        
        if type == "list":
            return neighbors_list
        elif type == "dict":
            neighbors_dict = {cell: self.cell_datas[cell] for cell in neighbors_list}
            return neighbors_dict

    def Get_Neighbor_Flaggeds(self, y, x):
        bomb_flag_count = 0
        neighbors = self.Get_Neighbors(y, x, type="dict")
        for cell, status in neighbors.items():
            if status == "!":
                bomb_flag_count += 1
        return bomb_flag_count

    def Get_Cell_Value(self, y, x): #cell's number - flagged neighbors(near bombs)
        cell_num= self.cell_datas.get((y,x))
        if cell_num == "!":
            return "!"
        elif cell_num == "?":
            return "?"
        else:
            return cell_num - self.Get_Neighbor_Flaggeds(y,x)

    def Get_Cell_Details(self, y, x): #--- TO GET Neighbor statuses, USE self.cell_datas[(ny, nx)] --- Y(row), X(col), STATUS, FLAGGED N. COUNT, NUM N. COUNT, UNKNOWN N. LIST, ALL N. LIST 
        neighbors_coords = self.Get_Neighbors(y, x, type="list")
        cell_status = self.cell_datas[(y, x)]
        unknown_neighbors = []
        flag_count= 0
        number_count= 0
        
        for  ny, nx in neighbors_coords:
            neighbor_status = self.cell_datas[(ny, nx)]
            if neighbor_status == "?":
                unknown_neighbors.append((ny, nx))
            elif neighbor_status == "!":
                flag_count += 1
            elif isinstance(neighbor_status, int):
                number_count += 1

        cell_details = {
            "row":y,
            "col":x,
            "status":cell_status,
            "flag_count":flag_count,
            "number_count":number_count,
            "unknown_neighbors":unknown_neighbors,
            "all_neighbors":neighbors_coords}
        return cell_details

    def Skip_cell(self, cell_details):
        status = cell_details["status"]
        if status in ["?", "!", 0]:
            return True
        if not cell_details["unknown_neighbors"]:
            return True
        return False

    def Basic_Logic(self, cell_details): #BASIC LOGIC: If num = flags + unknowns -> flag all unknowns; If num = flags -> open all unknowns
        if cell_details["status"] == len(cell_details["unknown_neighbors"]) + cell_details["flag_count"]:
            for ny, nx in cell_details["unknown_neighbors"]:
                self.Click(ny, nx, "right")

        if cell_details["status"] == cell_details["flag_count"]:
            self.Click(cell_details["row"], cell_details["col"], "middle")

    def OTO_Logic(self, cell_details): #One-Two-One Logic (not neccesary but cool ig)
        row = cell_details["row"]
        col = cell_details["col"]

        if self.Get_Cell_Value(row,col) != 2: return
        
        Directions = [(0,1),(1,0)] #first right and left cells then top and bottom cells
        for dy , dx in Directions:
            prev_y , prev_x = row-dy, col-dx # left  cell - top cell 
            next_y , next_x = row+dy, col+dx # right cell - bottom cell
            
            if not (1 <= prev_y <= self.row_count and 1 <= prev_x <= self.col_count): #TO skip on borders
                continue
            if not (1 <= next_y <= self.row_count and 1 <= next_x <= self.col_count):
                continue

            val_prev_cell = self.Get_Cell_Value(prev_y, prev_x)
            val_next_cell = self.Get_Cell_Value(next_y, next_x)

            if val_next_cell == 1 and val_prev_cell == 1:
                unknowns = cell_details["unknown_neighbors"]
                if len(unknowns) == 3:
                    unknowns.sort()
                    self.Click(unknowns[0][0], unknowns[0][1], "right")
                    self.Click(unknowns[2][0], unknowns[2][1], "right")
                    self.Click(prev_y, prev_x, "middle")    
                    self.Click(next_y, next_x, "middle")
                    return

    def Difference_Logic(self, cell_details):
        row = cell_details["row"]
        col = cell_details["col"]
        main_cell_value = self.Get_Cell_Value(row,col)
        main_cell_unknowns_set = set(cell_details["unknown_neighbors"])

        Directions = [(0,1), (0,-1), (1,0), (-1,0)] #right , left , top , bottom cells
        for dy , dx in Directions:
            near_cell_y , near_cell_x = row+dy , col+dx     #the cell we will be looking to 
            
            if not (1 <= near_cell_y <= self.row_count and 1 <= near_cell_x <= self.col_count): continue #TO skip on borders
            
            val_near_cell = self.Get_Cell_Value(near_cell_y, near_cell_x)

            if isinstance(val_near_cell, int) and val_near_cell >0:
                val_diff = main_cell_value - val_near_cell

                near_cell_neighbors_list = self.Get_Neighbors(near_cell_y, near_cell_x, "list")
                near_cell_unknowns_set = {
                    (ny, nx) for ny, nx in near_cell_neighbors_list 
                    if self.cell_datas.get((ny, nx)) == "?"
                }
                Diff_unknown_neighbors_near= main_cell_unknowns_set - near_cell_unknowns_set

                if len(Diff_unknown_neighbors_near) == val_diff:
                    for item in Diff_unknown_neighbors_near:
                        self.Click(item[0],item[1],"right")

                if Diff_unknown_neighbors_near:
                    if near_cell_unknowns_set.issubset(main_cell_unknowns_set):
                        if not val_diff:
                            for item in Diff_unknown_neighbors_near:
                                self.Click(item[0],item[1],"left")
                
    def Two_Steps_ahead_Logic(self, cell_details): #Looking two cells ahead
        row = cell_details["row"]
        col = cell_details["col"]
        main_cell_value = self.Get_Cell_Value(row,col)
        main_cell_unknowns_set = set(cell_details["unknown_neighbors"])

        Directions = [(0,1), (0,-1), (1,0), (-1,0)] #right , left , top , bottom cells
        for dy , dx in Directions:
            near_cell_y , near_cell_x = row + dy , col + dx # near cell
            far_cell_y , far_cell_x = row + dy*2 , col + dx*2 

            if not (1 <= far_cell_y <= self.row_count and 1 <= far_cell_x <= self.col_count): continue #TO skip on borders
            
            val_near_cell = self.Get_Cell_Value(near_cell_y,near_cell_x)
            val_far_cell = self.Get_Cell_Value(far_cell_y,far_cell_x)

            if val_near_cell == "?" and isinstance(val_far_cell,int):
                far_cell_neighbors_list = self.Get_Neighbors(far_cell_y, far_cell_x , "list")
                far_cell_unknowns_set = {
                    (ny, nx) for ny, nx in far_cell_neighbors_list 
                    if self.cell_datas.get((ny,nx)) == "?"}
                
                if main_cell_unknowns_set.issubset(far_cell_unknowns_set):
                    diff_cells = far_cell_unknowns_set - main_cell_unknowns_set
                    value_diff = val_far_cell - main_cell_value
                    if value_diff == len(diff_cells) and value_diff > 0:
                        for by , bx in diff_cells:
                            if self.cell_datas.get((by,bx)) == "?":
                                self.Click(by, bx, "right")

                    elif value_diff == 0 and len(diff_cells) > 0:
                        for cy , cx in diff_cells:
                            self.Click(cy, cx, "left")

                elif far_cell_unknowns_set.issubset(main_cell_unknowns_set):
                    diff_cells = main_cell_unknowns_set - far_cell_unknowns_set
                    value_diff = main_cell_value - val_far_cell
                    if value_diff == len(diff_cells) and value_diff > 0:
                        for by , bx in diff_cells:
                            if self.cell_datas.get((by,bx)) == "?":
                                self.Click(by, bx, "right")
                                
                    elif value_diff == 0 and len(diff_cells) > 0:
                        for cy , cx in diff_cells:
                            self.Click(cy, cx, "left")

    def Logic_actions(self, cell_details):
        if self.Skip_cell(cell_details): return #Skip_cell if not needed
        
        self.Two_Steps_ahead_Logic(cell_details)
        self.OTO_Logic(cell_details)
        self.Difference_Logic(cell_details)
        self.Basic_Logic(cell_details) 

    def Start_BOT(self, Auto_Start=False, will_Restart_on_Death=True, will_Restart_on_Win=False, Auto_Start_on_Death_Restart=False, Auto_Start_on_Win_Restart=False):
        print('Browser is starting. Press "R" to Stop, Press "ESC" to Quit. It may take some time at the first time.\n')
        time.sleep(1)
        self.Open_Browser()
        is_browser_running = True
        is_bot_active = True
        print(f"Mode: {self.mode}\nColumns: {self.col_count}\nRows: {self.row_count}\nBombs: {self.bomb_count}\n")

        #Before while
        if Auto_Start: self.Open_first_cell()

        while is_browser_running:
            if keyboard.is_pressed("ESC"): #Press ESC to stop the program
                print("Stopping the program...")
                is_browser_running = False
                is_bot_active = False
                break

            elif keyboard.is_pressed("r"): #Press R to pause/resume the bot
                is_bot_active = not is_bot_active
                if is_bot_active:
                    print("Bot Resumed.")
                else:
                    print("Bot Paused. Press 'R' to Resume.")
                time.sleep(0.5)

            if is_bot_active:
                self.Set_DOM_data()

                for y in range(1, self.row_count + 1):
                    for x in range(1, self.col_count + 1):
                        self.Logic_actions(self.Get_Cell_Details(y, x))

                if will_Restart_on_Death: self.Restart_on_Death(Auto_Start_on_Death_Restart)
                if will_Restart_on_Win: self.Restart_on_Win(Auto_Start_on_Win_Restart)

            else:
                time.sleep(0.1)

        if sum(self.Win_scores) != 0:
            print(f"\nBOT STATISTICS:\nWon: {len(self.Win_scores)}    Lost: {self.Restart_count-len(self.Win_scores)}\nTotal game(s): {self.Restart_count}\nWin Rate: %{len(self.Win_scores)*100/(self.Restart_count)}\nAverage score: {sum(self.Win_scores)/len(self.Win_scores)} second(s)\n")
        else:
            print(f"\nBot didn't win.\n")
            
        self.Close_Browser() #Close the Bot and the Broswer

    def Close_Browser(self):
        if self.browser:
            self.browser.close()
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
        print("Browser closed.")

if __name__ == "__main__":
    Gamemode_Selection = input('Please select the GAME MODE you want to "see" then press enter. The default mode is Expert.\n1: Beginner\n2: Intermediate\n3: Expert\nYour selection: ')
    if Gamemode_Selection == "1":
        url = "https://minesweeperonline.com/#beginner-150-night"
        print("Beginner mode has been selected.\n")
    elif Gamemode_Selection == "2":
        url = "https://minesweeperonline.com/#intermediate-150-night"
        print("Intermediate mode has been selected.\n")
    elif Gamemode_Selection == "3":
        url = "https://minesweeperonline.com/#150-night"
        print("Expert mode has been selected.\n")
    else:
        url = "https://minesweeperonline.com/#150-night"
        print("Invalid input. Defaulting to Expert mode.\n")

    MW_BOT = MWPlaywright(url, DPI_scale=1.25)
    MW_BOT.Start_BOT(
        Auto_Start=True,
        will_Restart_on_Death=True,
        will_Restart_on_Win=True,
        Auto_Start_on_Death_Restart=True,
        Auto_Start_on_Win_Restart=True)
