import numpy as np
import matplotlib.pyplot as plt
import os


def remove_all_occurences_of_item_from_list(myList, item):
    myList = list(filter((item).__ne__, myList))
    return myList


def plot_transition_over_time(session_list, direction="odour_to_visual"):

    for mouse_list in session_list:
        mouse_distribution_list = []

        for session in mouse_list:

            # Load Performance Dictionary
            performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]

            # Get distribution
            session_distribution = performance_dictionary[direction + "_transition_distribution"]

            # Remove 0s and nans
            session_distribution = np.nan_to_num(session_distribution)
            session_distribution = remove_all_occurences_of_item_from_list(session_distribution, 0)
            print(session_distribution)
            if len(session_distribution) > 0:
                # Get Session Mean
                session_mean = np.mean(session_distribution)

                # Add Session Mean To Mouse Distribution List
                mouse_distribution_list.append(session_mean)


        plt.plot(mouse_distribution_list, c='b')
        plt.scatter(list(range(len(mouse_distribution_list))), mouse_distribution_list, c='b')

    plt.show()






control_session_list = [

    # 4.1B
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"
    ],

    # 7.1B
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_22_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_23_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_24_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_27_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_30_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_31_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_01_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_02_Transition_Imaging",
    ],

    # 14.1A
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_12_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_13_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_14_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_15_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_16_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_17_Transition_Behaviour",
    ],

    # 22.1A
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_26_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_29_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_02_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_03_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_04_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_05_Transition_Imaging",
    ],
]



mutant_session_list = [

    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_10_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_11_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_12_Transition_Imaging",
    ],


    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_13_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_14_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_16_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_17_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_18_Transition_Imaging",
    ],


    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_22_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_23_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_24_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_26_Transition_Imaging",
    ],

    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_05_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_10_Transition_Imaging",
    ]
]


plot_transition_over_time(control_session_list)
plot_transition_over_time(mutant_session_list)