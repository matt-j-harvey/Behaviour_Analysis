import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn


def plot_odour_performance(meta_group_list, group_names=None, mouse_names=None):

    odour_performance_list = []
    group_id_list = []
    mouse_id_list = []

    number_of_groups = len(meta_group_list)

    mouse_count = 0
    for group_index in range(number_of_groups):
        group = meta_group_list[group_index]
        group_size = len(group)

        if group_names != None:
            group_name = group_names[group_index]
        else:
            group_name = group_index

        for mouse_index in range(group_size):
            mouse = group[mouse_index]
            mouse_count += 1

            if mouse_names != None:
                mouse_name = mouse_names[group_index][mouse_index]
            else:
                mouse_name = mouse_count


            for session in mouse:

                # Load Performance Dictionary
                performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]

                # Extract Irrel Performance
                odour_d_prime = performance_dictionary["odour_d_prime"]

                odour_performance_list.append(odour_d_prime)
                mouse_id_list.append(mouse_name)
                group_id_list.append(group_name)

    # Combine_Into Dataframe
    dataframe = pd.DataFrame()
    dataframe["Odour Performance"] = odour_performance_list
    dataframe["Mouse"] = mouse_id_list
    dataframe["Genotype"] = group_id_list

    print("Dataframe", dataframe)
    # seaborn.swarmplot(y="Irrel Performance", orient='v', hue="Mouse", data=dataframe)
    axis = seaborn.swarmplot(y="Odour Performance", hue="Genotype", x="Genotype", data=dataframe, size=8)
    axis.set_ylim(0, 5)
    plt.show()




control_session_list = [

    # 4.1B
    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging",
    ],

    # 7.1B
    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_22_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_23_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_24_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_27_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_30_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_31_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_01_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_02_Transition_Imaging",
    ],

    # 14.1A
    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_12_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_13_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_14_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_15_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_16_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_17_Transition_Behaviour",
    ],

    # 22.1A
    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_26_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_29_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_02_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_03_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_04_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_05_Transition_Imaging",
    ],
]




mutant_session_list = [

    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_10_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_11_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_12_Transition_Imaging",
    ],


    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_13_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_14_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_16_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_17_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_18_Transition_Imaging",
    ],


    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_22_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_23_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_24_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_26_Transition_Imaging",
    ],

    [
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_05_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_10_Transition_Imaging",
    ]
]



group_names =["Wildtype", "Neurexin"]
mouse_names = [["NXAK4.1b", "NXAK7.1b", "NXAK14.1a", "NXAK22.1a"],["NXAK4.1a", "NXAK10.1a", "NXAK20.1b", "NXAK24.1c"]]
plot_odour_performance([control_session_list, mutant_session_list], group_names=group_names, mouse_names=mouse_names)
#plot_blockwise_performance(session_list)