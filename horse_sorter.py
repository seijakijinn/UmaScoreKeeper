import pickle

def get_sorted_horse_scores():
    paths_to_score_files = [f"scores/sprint_1.pkl",f"scores/mile_1.pkl",f"scores/medium_1.pkl", f"scores/long_1.pkl", f"scores/dirt_1.pkl",
                            f"scores/sprint_2.pkl",f"scores/mile_2.pkl",f"scores/medium_2.pkl", f"scores/long_2.pkl", f"scores/dirt_2.pkl",
                            f"scores/sprint_3.pkl",f"scores/mile_3.pkl",f"scores/medium_3.pkl", f"scores/long_3.pkl", f"scores/dirt_3.pkl"]

    with open('teaminfo/horse_team.pkl', 'rb') as file:
        horse_names = pickle.load(file)

    horse_scores_total_unsorted = []
    for item in range(0,15):
        with open(paths_to_score_files[item], 'rb') as file:
            scores = pickle.load(file)
        horse_scores_total_unsorted.append(scores)

    def return_average(input):
        input_int = []
        for item in input:
            try:
                input_int.append(int(item))
            except (ValueError, TypeError):
                continue
        if input_int:
            average = sum(input_int) / len(input_int)
        else:
            average = 0
        return average

    for item in range(0,15):
        try:
            avg = return_average(horse_scores_total_unsorted[item])
            horse_scores_total_unsorted[item] = [avg, horse_names[item]]
        except Exception as e:
            horse_scores_total_unsorted[item] = [0, horse_names[item]]

    try:
        sorted_horse_scores = sorted(horse_scores_total_unsorted, key=lambda x: x[0], reverse=True)
    except:
        sorted_horse_scores = []
        
    filtered_sorted_horse_scores = []
    for avg, name in sorted_horse_scores:
        if isinstance(avg, (int, float)):
            filtered_sorted_horse_scores.append([avg, name])
    return filtered_sorted_horse_scores




def return_single_average(horse): 
    paths_to_score_files = [f"scores/sprint_1.pkl",f"scores/mile_1.pkl",f"scores/medium_1.pkl", f"scores/long_1.pkl", f"scores/dirt_1.pkl",
                            f"scores/sprint_2.pkl",f"scores/mile_2.pkl",f"scores/medium_2.pkl", f"scores/long_2.pkl", f"scores/dirt_2.pkl",
                            f"scores/sprint_3.pkl",f"scores/mile_3.pkl",f"scores/medium_3.pkl", f"scores/long_3.pkl", f"scores/dirt_3.pkl"]

    with open(paths_to_score_files[horse], 'rb') as file:
        horse_to_average_raw = pickle.load(file)
    horse_to_average = []
    for item in horse_to_average_raw:
        try:
            horse_to_average.append(int(item))
        except (ValueError, TypeError):
            continue
    if horse_to_average:
        average = sum(horse_to_average) / len(horse_to_average) 
    else:
        average = 0 
    return average






