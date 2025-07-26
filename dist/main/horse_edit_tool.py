import pickle
#manual tool for editing horse_team.pkl
save_path = "horse_team.pkl"
horse_team_file = ["sprint_team_1", "mile_team_1", "medium_team_1", "long_team_1", "dirt_team_1",
                  "sprint_team_2", "mile_team_2", "medium_team_2", "long_team_2", "dirt_team_2",
                  "sprint_team_3", "mile_team_3", "medium_team_3", "long_team_3", "dirt_team_3",]
horse_team_control = ["null", "null", "null", "null", "null",
                  "null", "null", "null", "null", "null",
                  "null", "null", "null", "null", "null",]

image_save_path = "horse_images.pkl"

def write_horse():
    try:
        with open(save_path, 'wb') as file:
            pickle.dump(horse_team_file,file)
        print("object saved")
    except Exception as e:
        print("error")

def print_team():
    with open(save_path, 'rb') as file:
        list_to_use = pickle.load(file)
        print(list_to_use)

def clear_list():
     try:
        with open(save_path, 'wb') as file:
            pickle.dump(horse_team_control,file)
        print("object saved")
     except Exception as e:
        print("error")