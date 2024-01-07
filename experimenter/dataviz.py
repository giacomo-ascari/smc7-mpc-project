import math
from matplotlib import pyplot as plt
from matplotlib import rc

import os


# plot = [title, x, y, color, linestyle]
# solid, dotted, dashed, dashdot
def createPlots(plots, title, log=False, figsize=(8, 5)):
    plt.figure(figsize=figsize)
    for p in plots:
        plt.plot(p[1], p[2], label=p[0], color=p[3], linestyle=p[4])
    if log:
        plt.xscale('log')
    plt.title(title)
    plt.grid(True)
    plt.legend()

def savePlot(name):
    if not os.path.exists(os.path.join("data", "_plots")):
        os.mkdir(os.path.join("data", "_plots"))
    plt.savefig(os.path.join("data", "_plots", name), dpi=200) #600

def createErrorbar(x, y, e, range, xlabel, ylabel, cap_color, mark_color, title=None, figsize=(8, 5)):
    plt.figure(figsize=figsize)
    plt.errorbar(x, y, yerr=e, linestyle='none', marker='d', capsize=4, c=cap_color, markeredgecolor=mark_color, markerfacecolor=mark_color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)  
    plt.ylim(range[0], range[1])
    if not title == None:
        plt.title(title)
    plt.grid(True)

def round(x):
    if x < math.floor(x) + 0.5:
        return math.floor(x)
    else:
        return math.ceil(x)

experiment_ids = []
experiment = {}

forbidden = [["t9u3cg0d8y", 1]]

def main():

    rc('font',**{'family':'serif'})
    rc('text')

    # LOAD EXPERIMENT DATA
    for id in os.listdir("data"):

        if id != "_plots":

            experiment_ids.append(id)
            experiment[id] = {}

            # NAME and MUSICIAN
            with open(os.path.join("data", id, "general_data.txt")) as file:
                lines = file.readlines()
                experiment[id]["name"] = lines[0].split(" ")[1]
                if str.strip(lines[1].split(" ")[1]) == "1":
                    experiment[id]["musician"] = True
                else:
                    experiment[id]["musician"] = False

            # BASELINE TEMPO, PERTURBATIONs TEMPO, PERTURBATIONs COUNT
            with open(os.path.join("data", id, "proc_data.txt")) as file:
                lines = file.readlines()
                experiment[id]["baseline_bpm"] = float(lines[0].split(" ")[1])
                experiment[id]["repper_bpm"] = []
                experiment[id]["deviations"] = []
                experiment[id]["repper_count"] = 0

                for i in range(1, len(lines)):
                    experiment[id]["repper_bpm"].append(float(lines[i].split(" ")[1]))
                    experiment[id]["repper_count"] += 1
                
                for i in range(experiment[id]["repper_count"]):
                    deviation = experiment[id]["repper_bpm"][i] / experiment[id]["baseline_bpm"]
                    deviation = round(deviation * 100 - 100)
                    experiment[id]["deviations"].append(str(deviation))

            # REPPER TIMESTAMPS
            experiment[id]["repper_ts"] = []
            for i in range(experiment[id]["repper_count"]):
                experiment[id]["repper_ts"].append([])
                with open(os.path.join("data", id, f"repper_ts_{i}.txt")) as file:
                    lines = file.readlines()
                    #offset = float(str.strip(lines[0])) # first element
                    offset = float(str.strip(lines[-1])) - 95 # last element - 95
                    for l in lines:
                        experiment[id]["repper_ts"][i].append(float(str.strip(l)) - offset)

    # PROCESS THE REPPER BPM
    # iterates the experiments
    for id in experiment_ids:
        experiment[id]["repper_proc_bpms"] = []
        experiment[id]["repper_proc_data"] = []
        # iterates the perturbation
        for i in range(experiment[id]["repper_count"]):
            
            n = len(experiment[id]["repper_ts"][i])
            ts = experiment[id]["repper_ts"][i]
            diff = []
        
            for j in range(n-1):
                diff.append(ts[j+1] - ts[j])
            diff.append(diff[-1])

            raw_bpm = []
            for j in range(n):
                raw_bpm.append(60 / diff[j])

            avg_bpm = []
            up_window = 5  # windows is 11 elements
            down_window = 5 # 5 + 1 + 5 elements
            for j in range(n):
                res = raw_bpm[j]
                div = 1
                for k in range(1, down_window+1):
                    if j-k > 0:
                        res += raw_bpm[j-k]
                        div += 1
                for k in range(1, up_window+1):
                    if j+k < n:
                        res += raw_bpm[j+k]
                        div += 1
                avg_bpm.append(res/div)
            
            experiment[id]["repper_proc_bpms"].append(avg_bpm)

            repper_data = {}
            avg_reprisal_bpm, avg_reprisal_count = 0, 0
            avg_pause_bpm, avg_pause_count = 0, 0
            avg_perturbation_bpm, avg_perturbation_count = 0, 0
            for j in range(n):
                if ts[j] <= 30:
                    avg_reprisal_bpm += raw_bpm[j]
                    avg_reprisal_count += 1
                elif ts[j] > 30 and ts[j] <= 35:
                    avg_pause_bpm += raw_bpm[j]
                    avg_pause_count += 1
                else:
                    avg_perturbation_bpm += raw_bpm[j]
                    avg_perturbation_count += 1
            avg_reprisal_bpm /= avg_reprisal_count
            avg_pause_bpm /= avg_pause_count
            avg_perturbation_bpm /= avg_perturbation_count
                
            repper_data["avg_reprisal_bpm"] = avg_reprisal_bpm
            repper_data["avg_pause_bpm"] = avg_pause_bpm
            repper_data["avg_perturbation_bpm"] = avg_perturbation_bpm

            experiment[id]["repper_proc_data"].append(repper_data)
            


    # PLOT THE INDIVIDUAL EXPERIMENTS
    if True:
        for id in experiment_ids:
            musician = ""
            if experiment[id]['musician']:
                musician = "musician"
            else:
                musician = "non-mus."

            # iterates the perturbation
            for i in range(experiment[id]["repper_count"]):

                metronome_x = [0, 30]
                metronome_y = [experiment[id]["baseline_bpm"], experiment[id]["baseline_bpm"]]
                avg_reprisal_bpm_y = [experiment[id]["repper_proc_data"][i]["avg_reprisal_bpm"], experiment[id]["repper_proc_data"][i]["avg_reprisal_bpm"]]

                pause_x = [30, 35]
                avg_pause_bpm_y = [experiment[id]["repper_proc_data"][i]["avg_pause_bpm"], experiment[id]["repper_proc_data"][i]["avg_pause_bpm"]]

                perturbation_x = [35, 95]
                perturbation_y = [experiment[id]["repper_bpm"][i], experiment[id]["repper_bpm"][i]]
                avg_perturbation_bpm_y = [experiment[id]["repper_proc_data"][i]["avg_perturbation_bpm"], experiment[id]["repper_proc_data"][i]["avg_perturbation_bpm"]]

                deviation = experiment[id]['deviations'][i]

                createPlots(
                [
                    [
                        f"Tapping bpm",
                        experiment[id]["repper_ts"][i],
                        experiment[id]["repper_proc_bpms"][i],
                        "#999999",
                        "solid"
                    ],
                    [
                        f'SPR/metronome ({math.floor(metronome_y[0])})',
                        metronome_x,
                        metronome_y,
                        "#0000FF",
                        "dashed"
                    ], 
                    [
                        f'Perturbation bpm ({math.floor(perturbation_y[0])})',
                        perturbation_x,
                        perturbation_y,
                        "#FF0000",
                        "dashed"
                    ], 
                    [
                        f'Avg. repr. ({round(avg_reprisal_bpm_y[0])})',
                        metronome_x,
                        avg_reprisal_bpm_y,
                        "#000000",
                        "solid"
                    ],
                    [
                        f'Avg. pause ({round(avg_pause_bpm_y[0])})',
                        pause_x,
                        avg_pause_bpm_y,
                        "#000000",
                        "solid"
                    ],
                    [
                        f'Avg. perturb. ({round(avg_perturbation_bpm_y[0])})',
                        perturbation_x,
                        avg_perturbation_bpm_y,
                        "#000000",
                        "solid"
                    ],
                ], f"Experiment {id}, iteration #{i+1}, difference {deviation}%, {musician}")
                
                print(f"experiment_{id}_{i+1}")
                savePlot(f"experiment_{id}_{i+1}.png")
                #plt.show()
                plt.close()
    
    #print(experiment)
    # similarity of tapping bpm and perturbation bpm grouped by deviation percentage
    
    ratio_count = {}
    ratio_avg = {}
    ratio_sd = {}

    # iterates experiments for the average
    for id in experiment_ids:
        for i in range(experiment[id]["repper_count"]):
            if not [id, i+1] in forbidden:
                label = str(abs(int(experiment[id]["deviations"][i])))
                if not label in ratio_avg.keys():
                    ratio_avg[label] = 0
                    ratio_sd[label] = 0
                    ratio_count[label] = 0
                ratio = experiment[id]["repper_bpm"][i] / experiment[id]["repper_proc_data"][i]["avg_perturbation_bpm"]
                ratio_count[label] += 1
                ratio_avg[label] += ratio
    for label in list(ratio_count.keys()):
        ratio_avg[label] /= ratio_count[label]

    # second round just for standard deviation
    for id in experiment_ids:
        for i in range(experiment[id]["repper_count"]):
            if not [id, i+1] in forbidden:
                label = str(abs(int(experiment[id]["deviations"][i])))
                ratio = experiment[id]["repper_bpm"][i] / experiment[id]["repper_proc_data"][i]["avg_perturbation_bpm"]
                ratio_sd[label] += (ratio - ratio_avg[label])**2

    for label in list(ratio_count.keys()):
        ratio_sd[label] /= ratio_count[label]

    print("average (mean)", ratio_avg)
    print("standard deviation", ratio_sd)

    createErrorbar(
        ["±4%", "±8%", "±16%"],
        [ratio_avg["4"], ratio_avg["8"], ratio_avg["16"]],
        [ratio_sd["4"], ratio_sd["8"], ratio_sd["16"]],
        [0.94, 1],
        "Perturbation BPM to SPR difference",
        "Perturbation BPM to tapping ratio",
        "#FF0000", # cap color
        "#0000FF", # mark color
        #title="Perturbation BPM to SPR difference VS.\n Perturbation BPM to tapping ratio"
        figsize=(8, 4)
    )

    savePlot("errorbar.png")
    plt.show()
    




if __name__ == "__main__":
    main()