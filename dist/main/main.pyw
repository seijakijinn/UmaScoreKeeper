
from time import time
from tkinter import *
from tkfilterlist import FilterList
from assets.character_list import character_list
import assets.icons
import pickle
from tkinter import ttk
from tkinter import messagebox
from horse_sorter import get_sorted_horse_scores
import winsound
from horse_sorter import return_single_average
import subprocess
import sys


#imports character_list sets save path for images
horse_data_list = character_list
save_path='./teaminfo/horse_team.pkl'
image_save_path = './teaminfo/horse_images.pkl'




#creates root window and rightside frame for team and input
root = Tk()
root.geometry("1280x720")
root.title('Umamusume Score Keeper')
frame_rightside = Frame(root)
frame_rightside.pack(side=RIGHT,expand=TRUE,fill=BOTH)
frame_spacer=Frame(root)
frame_spacer.pack(side=RIGHT,expand=TRUE,fill=Y)


# creates lines of frames for putting team members into
frame_line_1=Frame(frame_rightside)
frame_line_1.pack(side=TOP,fill=BOTH, expand=FALSE)
frame_line_1.configure(height=50)
frame_line_2=Frame(frame_rightside)
frame_line_2.pack(side=TOP,fill=X,expand=FALSE)
frame_line_2.configure(height=50)
frame_line_3=Frame(frame_rightside)
frame_line_3.pack(side=TOP,fill=X,expand=FALSE)
frame_line_3.configure(height=50)

#this frame contains the data input, average scores, most recent scores, and the currently editing label
frame_label_spacer=Frame(frame_rightside)
frame_label_spacer.pack(side=TOP,fill=BOTH,expand=FALSE)
frame_label_spacer.configure()
frame_info_container=Frame(frame_rightside)
frame_info_container.pack(side=TOP, fill=BOTH, expand=FALSE)
#widgets for score entry and clear
score_label = Label(frame_info_container) # label for score entry
score_label.pack(anchor = N,side=LEFT)
score_label.configure(text= "Enter score here: ")
score_entry = Entry(frame_info_container) # score entry box
score_entry.pack(anchor=N, side=LEFT)
score_button = Button(frame_info_container, command = lambda: score_button_press(), text="Enter", font='bold') # score enter button
score_button.pack(anchor=N, side=LEFT)
undo_button = Button(frame_info_container, command = lambda : undo_last_score(), text="Remove Latest Score", font= 'bold') # score undo button
undo_button.pack(anchor=N, side=LEFT)
clear_button = Button(frame_info_container, command = lambda: clear_button_confirm(), text="Clear Scores", font= 'bold') # Clear current horse's scores button
clear_button.pack(anchor=N, side=LEFT)
clear_all_scores = Button(frame_spacer,command = lambda : clear_all_button_confirm(), text="Clear All Scores" ,font='bold') # clear all scores button
clear_all_scores.pack(side=TOP)
clear_horse_team = Button(frame_spacer, command = lambda: clear_all_horses_confirm(), text="Clear All Horses", font ='bold') # clear all horses and all scores
clear_horse_team.pack(side=TOP)

def error_label_ocr_show():
    error_label_ocr.pack(side=LEFT,anchor=N, fill=X, expand=FALSE)
    error_label_ocr.after(5000, lambda: error_label_ocr.pack_forget())
    subprocess.Popen(["python", "horse_OCR.py"], shell=TRUE)

OCR_button = Button(frame_spacer, command=error_label_ocr_show, text="Enter scores with OCR", font='bold') # button to show OCR text
OCR_button.pack(side=TOP)
score_label = Label(frame_spacer, text="Average Score: ") # label for average score
score_label.pack(side=TOP) 
horse_current_average = Listbox(frame_spacer,height=1,font='bold') # listbox to display current horse's average score
horse_current_average.pack(side=TOP, fill=X, expand=FALSE)
horse_current_average.configure(bd=5,relief="raised")
score_label = Label(frame_spacer, text="Scores: ") # label for recent scores
score_label.pack(side=TOP)
#label if non-int is entered
error_label = Label(frame_rightside, text="Please enter a valid score (integer only)", fg="red",)
error_label_ocr = Label(frame_rightside, text="Please scroll the scores up and down until OCR finishes", fg="red",)

def error_label_ocr_show():
    error_label_ocr.pack(side=LEFT,anchor=N, fill=X, expand=FALSE)
    error_label_ocr.after(5000, lambda: error_label_ocr.pack_forget())
    subprocess.Popen([sys.executable, "horse_OCR.py"], shell=TRUE)

#listbox to display all scores
recent_scores = Listbox(frame_spacer)
recent_scores.pack(side=TOP,expand=TRUE,fill=BOTH)
recent_scores.configure(bd=5,relief="raised")
#listbox that displays current horse's average




    #contains all the paths to the horses' respective score files
paths_to_score_files = [f"./scores/sprint_1.pkl",f"./scores/mile_1.pkl",f"./scores/medium_1.pkl", f"./scores/long_1.pkl", f"./scores/dirt_1.pkl",
                        f"./scores/sprint_2.pkl",f"./scores/mile_2.pkl",f"./scores/medium_2.pkl", f"./scores/long_2.pkl", f"./scores/dirt_2.pkl",
                        f"./scores/sprint_3.pkl",f"./scores/mile_3.pkl",f"./scores/medium_3.pkl", f"./scores/long_3.pkl", f"./scores/dirt_3.pkl"]

#clears current horse's scores
def clear_button_confirm():
    response =messagebox.askyesno("Are you sure", "This action cannot be undone")
    print(response)
    if response: #user confirms deletion
        empty_array = []
        horse_selection = (current_horse[0] - 1)
        with open(paths_to_score_files[horse_selection], 'wb') as file:
            pickle.dump(empty_array,file )

    with open(paths_to_score_files[horse_selection], 'rb') as file:
            score_list = pickle.load(file)
    recent_scores.delete(0,END)
    for item in score_list:
            recent_scores.insert(0,item)
    update_top_scores()
    update_recent_scores_unsorted()

# removes latest score from horse
def undo_last_score():
    horse_selection = (current_horse[0] - 1)
    with open(paths_to_score_files[horse_selection], 'rb') as file:
        score_holder_temp=pickle.load(file)
    score_holder_temp.pop()
    with open(paths_to_score_files[horse_selection], 'wb') as file:
            pickle.dump(score_holder_temp,file )
    with open(paths_to_score_files[horse_selection], 'rb') as file:
            score_list = pickle.load(file)
    recent_scores.delete(0,END)
    for item in score_list:
        recent_scores.insert(0,item)
    update_top_scores()
    update_recent_scores_unsorted()


# clears all scores from all horses
def clear_all_button_confirm():
    response =messagebox.askyesno("Are you sure", "This will delete ALL scores from ALL horses\n This action cannot be undone",)
    print(response)
    if response: #user confirms deletion
        empty_array = []
        for x in range(0,15):
            with open(paths_to_score_files[x], 'wb') as file:
                pickle.dump(empty_array,file )
    with open(paths_to_score_files[0], 'rb') as file:
            score_list = pickle.load(file)
    recent_scores.delete(0,END)
    for item in score_list:
        recent_scores.insert(0,item)  
    update_top_scores()
    update_recent_scores_unsorted()


def clear_all_horses_confirm():
    response = messagebox.askyesno("Are you sure", "This will delete ALL horses and their data\n This action cannot be undone",)
    if response:
        for i in range(15):
            photo_loader[i] = PhotoImage(file="./assets/icons/no_character.png")
        button_1.configure(image=photo_loader[0], width=150, height=150, text="Enter Sprint 1")
        button_2.configure(image=photo_loader[1], width=150, height=150, text="Enter Mile 1")
        button_3.configure(image=photo_loader[2], width=150, height=150, text="Enter Medium 1")
        button_4.configure(image=photo_loader[3], width=150, height=150, text="Enter Long 1")
        button_5.configure(image=photo_loader[4], width=150, height=150, text="Enter Dirt 1")
        button_6.configure(image=photo_loader[5], width=150, height=150, text="Enter Sprint 2")
        button_7.configure(image=photo_loader[6], width=150, height=150, text="Enter Mile 2")
        button_8.configure(image=photo_loader[7], width=150, height=150, text="Enter Medium 2")
        button_9.configure(image=photo_loader[8], width=150, height=150, text="Enter Long 2")
        button_10.configure(image=photo_loader[9], width=150, height=150, text="Enter Dirt 2")
        button_11.configure(image=photo_loader[10], width=150, height=150, text="Enter Sprint 3")
        button_12.configure(image=photo_loader[11], width=150, height=150, text="Enter Mile 3")
        button_13.configure(image=photo_loader[12], width=150, height=150, text="Enter Medium 3")
        button_14.configure(image=photo_loader[13], width=150, height=150, text="Enter Long 3")
        button_15.configure(image=photo_loader[14], width=150, height=150, text="Enter Dirt 3")
        # save default images for all slots
        horse_images_clear = ["./assets/icons/no_character.png"] * 15
        with open('./teaminfo/horse_images.pkl', 'wb') as file:
            pickle.dump(horse_images_clear, file)

        horse_team_clear = ["None", "None", "None", "None", "None",
                            "None", "None", "None", "None", "None",
                            "None", "None", "None", "None", "None"]
        with open('./teaminfo/horse_team.pkl' ,'wb') as file:
            pickle.dump(horse_team_clear,file)
        for x in range(1,16):
            text_update(x)

        empty_array = []
        for x in range(0,15):
            with open(paths_to_score_files[x], 'wb') as file:
                pickle.dump(empty_array,file )

        with open(paths_to_score_files[0], 'rb') as file:
            score_list = pickle.load(file)
        print("scorelist")
        print(score_list)
        recent_scores.delete(0,END)
        for item in score_list:
            recent_scores.insert(0,item)  
        current_horse[0] = 1
        text_update(1)
        update_top_scores()
        update_recent_scores_unsorted()




            
            

                





# Searchbox with filter
source = horse_data_list
fl = FilterList(root,
                source=horse_data_list,
                display_rule=lambda item: item[0],
                filter_rule=lambda item, text:
                            item[0].lower().startswith(text.lower()))
fl.pack(side='top', expand=FALSE, fill="y", ipadx=80, anchor=W,ipady=60)
#label: "highest averages"
top_score_label = Label(root, text= "Highest Averages: ")
top_score_label.pack(side=TOP,expand=FALSE)
top_score_label.configure(font='bold', relief='flat')
#top score listbox
top_scores = Listbox(root)
top_scores.pack(anchor = E, side=BOTTOM,expand = TRUE, fill=BOTH)
top_scores.configure(bd=5,relief="raised")
with(open('./scores/sorted_horse_scores.pkl', 'rb') as file):
    sorted_horse_scores = pickle.load(file)
#loads top scores into listbox
for item in sorted_horse_scores:
    if item:
        top_scores.insert(END, f"{item[1]}: {item[0]}")




# creates variables for handling assigning photos to buttons
current_horse=[]
current_horse.append(0)
photo_loader =[]
for x in range(0,15):
    photo_loader.append(0)



score_holder_temp= []
def score_button_press():
        score_tracker[0] = score_entry.get() # adds current score to tracker
        print("score to input " + score_tracker[0]) # prints score to be added
        if not score_tracker[0].isdigit(): # checks if score is a number
            winsound.MessageBeep()
            error_label.pack(side=LEFT,anchor=N, fill=X, expand=FALSE)
            error_label.after(3000, lambda: error_label.pack_forget())
            score_entry.delete(0,END) # deletes entry box
        else:
            score_entry.delete(0,END)
            horse_selection = (current_horse[0] - 1)
            with open(paths_to_score_files[horse_selection], 'rb') as file:
                score_holder_temp=pickle.load(file)
            score_holder_temp.append(score_tracker[0])
            with open(paths_to_score_files[horse_selection], 'wb') as file:
                pickle.dump(score_holder_temp,file )
            print(score_holder_temp)
            with open(paths_to_score_files[horse_selection], 'rb') as file:
                score_list = pickle.load(file)
            print("scorelist for test")
            print(score_list)
            recent_scores.delete(0,END)
            print(score_list)
            for item in score_list:
                recent_scores.insert(0,item)
            update_top_scores()
            update_recent_scores_unsorted()
        

       


# Loads picture of selected horse in listbox
def select(item):
    item=fl.selection() 
    #loads horse_team and saves selected horse to file
    with open('teaminfo/horse_team.pkl', 'rb') as file:
        horse_team=pickle.load(file)
        horse_team[current_horse[0]-1]=item[0]
    with open('teaminfo/horse_team.pkl', 'wb') as file:
        pickle.dump(horse_team,file)


    #loads horse_images and saves selected image to file
    with open('teaminfo/horse_images.pkl', 'rb') as file:
        fileid=item[1]
        horse_images= pickle.load(file)
        horse_images[current_horse[0]-1]= f"assets/icons/{fileid}.png"
    with open('teaminfo/horse_images.pkl', 'wb') as file:
        pickle.dump(horse_images,file)


    text_update(current_horse[0])

    match current_horse[0]:
        case 1: 
            fileid = item[1] 
            photo_loader[0] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_1.configure(image=photo_loader[0],height=150, width=150)
            print("horse slot #1 updated")
        case 2:
            fileid = item[1]
            photo_loader[1] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_2.configure(image=photo_loader[1],height=150, width=150)
        case 3:
            fileid = item[1]
            photo_loader[2] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_3.configure(image=photo_loader[2],height=150, width=150)
        case 4:
            fileid = item[1]
            photo_loader[3] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_4.configure(image=photo_loader[3], height=150,width=150)
        case 5:
            fileid = item[1]
            photo_loader[4] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_5.configure(image=photo_loader[4],height=150, width=150)
        case 6:
            fileid = item[1]
            photo_loader[5] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_6.configure(image=photo_loader[5],height=150, width=150)
        case 7:
            fileid = item[1]
            photo_loader[6] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_7.configure(image=photo_loader[6],height=150, width=150)
        case 8:
            fileid = item[1]
            photo_loader[7] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_8.configure(image=photo_loader[7],height=150, width=150)
        case 9:
            fileid = item[1]
            photo_loader[8] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_9.configure(image=photo_loader[8],height=150, width=150)
        case 10:
            fileid = item[1]
            photo_loader[9] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_10.configure(image=photo_loader[9],height=150, width=150)
        case 11:
            fileid = item[1]
            photo_loader[10] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_11.configure(image=photo_loader[10],height=150, width=150)
        case 12:
            fileid = item[1]
            photo_loader[11] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_12.configure(image=photo_loader[11],height=150, width=150)
        case 13:
            fileid = item[1]
            photo_loader[12] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_13.configure(image=photo_loader[12],height=150, width=150)
        case 14:
            fileid = item[1]
            photo_loader[13] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_14.configure(image=photo_loader[13],height=150, width=150)
        case 15:
            fileid = item[1]
            photo_loader[14] = PhotoImage(file = f"assets/icons/{fileid}.png")
            button_15.configure(image=photo_loader[14],height=150, width=150)
        
#creates currently editing label
editing_label = Label(frame_label_spacer,text="Currently editing:\n None")
editing_label.pack(anchor=S, side=LEFT)
editing_label.configure(font='bold')

#updates editing label text on horse icon pressed
def text_update(input):
    print("horse button pressed: " + str(input))
    
    with open('teaminfo/horse_team.pkl', 'rb') as file:
        horse_team=pickle.load(file)
    editing_label.configure(text="Currently editing: \n" +horse_team[input-1] )
    current_horse[0] =input
    score_list=[]

    with open(paths_to_score_files[input-1], 'rb') as file:
        score_list = pickle.load(file)
    recent_scores.delete(0,END)
    for item in score_list:
        recent_scores.insert(0,item)
    update_top_scores()
    update_recent_scores_unsorted()
    
                         



#Creates buttons for team selection
button_1 = Button(frame_line_1,text="Enter Sprint 1",command=lambda: text_update(1),height=10,width=20,)
button_1.pack(anchor=N, side=LEFT)
button_2 = Button(frame_line_1, text="Enter Mile 1",command=lambda: text_update(2),height=10,width=20)
button_2.pack(anchor=N, side= LEFT)
button_3 = Button(frame_line_1, text="Enter Medium 1",command=lambda: text_update(3),height=10,width=20)
button_3.pack(anchor=N, side= LEFT)
button_4 = Button(frame_line_1, text="Enter Long 1",command=lambda: text_update(4),height=10,width=20)
button_4.pack(anchor=N, side= LEFT)
button_5 = Button(frame_line_1, text="Enter Dirt 1",command=lambda: text_update(5),height=10,width=20)
button_5.pack(anchor=N, side= LEFT)

button_6 = Button(frame_line_2, text="Enter Sprint 2",command=lambda: text_update(6),height=10,width=20)
button_6.pack(anchor=N, side= LEFT)
button_7 = Button(frame_line_2, text="Enter Mile 2",command=lambda: text_update(7),height=10,width=20)
button_7.pack(anchor=N, side= LEFT)
button_8 = Button(frame_line_2, text="Enter Medium 2",command=lambda: text_update(8),height=10,width=20)
button_8.pack(anchor=N, side= LEFT)
button_9 = Button(frame_line_2, text="Enter Long 2",command=lambda: text_update(9),height=10,width=20)
button_9.pack(anchor=N, side= LEFT)
button_10 = Button(frame_line_2, text="Enter Dirt 2",command=lambda: text_update(10),height=10,width=20)
button_10.pack(anchor=N, side= LEFT)

button_11 = Button(frame_line_3, text="Enter Sprint 3",command=lambda: text_update(11),height=10,width=20)
button_11.pack(anchor=N, side= LEFT)
button_12 = Button(frame_line_3, text="Enter Mile 3",command=lambda: text_update(12),height=10,width=20)
button_12.pack(anchor=N, side= LEFT)
button_13 = Button(frame_line_3, text="Enter Medium 3",command=lambda: text_update(13),height=10,width=20)
button_13.pack(anchor=N, side= LEFT)
button_14 = Button(frame_line_3, text="Enter Long 3",command=lambda: text_update(14),height=10,width=20)
button_14.pack(anchor=N, side= LEFT)
button_15 = Button(frame_line_3, text="Enter Dirt 3",command=lambda: text_update(15),height=10,width=20)
button_15.pack(anchor=N, side= LEFT)

#makes sure assigned horses' images are persistent
with open('teaminfo/horse_images.pkl', 'rb') as file:
    horse_image = pickle.load(file)
    try:
        photo_loader[0] = PhotoImage(file=f"{horse_image[0]}")
        button_1.configure(image=photo_loader[0],height=150,width=150,text= "Sprint 1")
        photo_loader[1] = PhotoImage(file=f"{horse_image[1]}")
        button_2.configure(image=photo_loader[1],height=150,width=150, text= "Mile 1")
        photo_loader[2] = PhotoImage(file=f"{horse_image[2]}")
        button_3.configure(image=photo_loader[2],height=150,width=150)
        photo_loader[3] = PhotoImage(file=f"{horse_image[3]}")
        button_4.configure(image=photo_loader[3],height=150,width=150)
        photo_loader[4] = PhotoImage(file=f"{horse_image[4]}")
        button_5.configure(image=photo_loader[4],height=150,width=150)
        photo_loader[5] = PhotoImage(file=f"{horse_image[5]}")
        button_6.configure(image=photo_loader[5],height=150,width=150)
        photo_loader[6] = PhotoImage(file=f"{horse_image[6]}")
        button_7.configure(image=photo_loader[6],height=150,width=150)
        photo_loader[7] = PhotoImage(file=f"{horse_image[7]}")
        button_8.configure(image=photo_loader[7],height=150,width=150)
        photo_loader[8] = PhotoImage(file=f"{horse_image[8]}")
        button_9.configure(image=photo_loader[8],height=150,width=150)
        photo_loader[9] = PhotoImage(file=f"{horse_image[9]}")
        button_10.configure(image=photo_loader[9],height=150,width=150)
        photo_loader[10] = PhotoImage(file=f"{horse_image[10]}")
        button_11.configure(image=photo_loader[10],height=150,width=150)
        photo_loader[11] = PhotoImage(file=f"{horse_image[11]}")
        button_12.configure(image=photo_loader[11],height=150,width=150)
        photo_loader[12] = PhotoImage(file=f"{horse_image[12]}")
        button_13.configure(image=photo_loader[12],height=150,width=150)
        photo_loader[13] = PhotoImage(file=f"{horse_image[13]}")
        button_14.configure(image=photo_loader[13],height=150,width=150)
        photo_loader[14] = PhotoImage(file=f"{horse_image[14]}")
        button_15.configure(image=photo_loader[14],height=150,width=150)  
    except:
        print("Image for horse not found! It's probably not set yet....")

#loads all horse scores

score_tracker =[0]

def update_top_scores():
    top_scores.delete(0, END)
    sorted_horse_scores = get_sorted_horse_scores()
    for item in sorted_horse_scores:
        if item:
            top_scores.insert(END, f"{item[1]}: {item[0]}")


def update_recent_scores_unsorted():
    recent_scores.delete(0, END)
    horse_selection = current_horse[0] - 1
    with open(paths_to_score_files[horse_selection], 'rb') as file:
        score_list = pickle.load(file)
    for score in score_list:
        try:
            score_int = int(score)
            recent_scores.insert(END, f"{score_int}")
        except (ValueError, TypeError):
            continue
    horse_current_average.delete(0, END)
    # calculates average score for current horse
    average_score = return_single_average(horse_selection)
    horse_current_average.insert(END, str(average_score))



update_top_scores()
fl.bind("<Double-Button-1>", select)
root.mainloop()


