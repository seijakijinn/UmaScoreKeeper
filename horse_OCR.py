from PIL import Image
from PIL import ImageGrab
import os
import pytesseract
import pickle
import winsound


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

paths_to_score_files = [f"./scores/sprint_1.pkl",f"./scores/mile_1.pkl",f"./scores/medium_1.pkl", f"./scores/long_1.pkl", f"./scores/dirt_1.pkl",
                        f"./scores/sprint_2.pkl",f"./scores/mile_2.pkl",f"./scores/medium_2.pkl", f"./scores/long_2.pkl", f"./scores/dirt_2.pkl",
                        f"./scores/sprint_3.pkl",f"./scores/mile_3.pkl",f"./scores/medium_3.pkl", f"./scores/long_3.pkl", f"./scores/dirt_3.pkl"]


def find_all_horses():
    

    #initial setup, loads horse team from file
    with open('teaminfo/horse_team.pkl', 'rb') as file:
        teaminfo = pickle.load(file)
 

    
    # creates a 2dlist with the size of the horse team (15)
    # format is [(horse name, horse score, has horse been updated)]
    # has horse been updated is used to determine if the horse's score has been updated during this script
    # 0 = not updated, 1 = updated
    w,h = 3, 15
    horse_2d= [[0 for x in range(w)]for y in range(h)]
    for x in range(15):
        horse_2d[x][0] = teaminfo[x]


   

    for x in range(50):
        # check if all horses have been updated
        all_found = all(horse_2d[i][2] == 1 for i in range(15))
        if all_found:
            # save the updated scores to their respective files
            for i in range(15):
                try:
                    with open(paths_to_score_files[i], 'rb') as file:
                        existing_scores = pickle.load(file)
                    if not isinstance(existing_scores, list):
                        existing_scores = [existing_scores]
                except (EOFError, FileNotFoundError):
                    existing_scores = []
                existing_scores.append(horse_2d[i][1])
                with open(paths_to_score_files[i], 'wb') as file:
                    pickle.dump(existing_scores, file)
            print("All horses have been found and updated.")
            winsound.MessageBeep()
            print(horse_2d)
            break

        # takes a screenshot of the score menu
        score_menu_image = ImageGrab.grab(bbox=(400, 100, 750, 950))
        score_menu_image.save('score_menu.png')
        scores_screen = (pytesseract.image_to_string(Image.open('score_menu.png')).strip())

        # find and assign scores for any horses not yet updated
        for i in range(15):
            if horse_2d[i][2] == 1:
                continue
            str_to_find = horse_2d[i][0]
            if str_to_find in scores_screen:
                print("found horse: " + str_to_find + " with score: " + 
                    scores_screen[scores_screen.find(str_to_find) + len(str_to_find):
                    scores_screen.find("\n", scores_screen.find(str_to_find))])
                try:
                    horse_score = scores_screen[scores_screen.find(str_to_find) + len(str_to_find):
                        scores_screen.find("\n", scores_screen.find(str_to_find))].strip()
                    horse_score_str = horse_score.replace(',', '')
                    if len(horse_score_str) == 5 and horse_score_str.isdigit():
                        horse_2d[i][1] = horse_score_str
                        horse_2d[i][2] = 1
                except:
                    print ("error assigning score, OCR may have read the score incorrectly")

    
    
    #opens score files and writes scores to them
 
find_all_horses()
