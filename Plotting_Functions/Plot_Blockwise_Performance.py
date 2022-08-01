import numpy as np
import matplotlib.pyplot as plt
import os


def plot_blockwise_performance(control_session_list, mutant_session_list):

    for session in control_session_list:

        # Load Performance Dictionary
        performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        blockwise_visual_d_prime = performance_dictionary['blockwise_visual_d_prime']
        blockwise_odour_d_prime = performance_dictionary['blockwise_odour_d_prime']

        # Start With First Visual
        if blockwise_visual_d_prime[0] > blockwise_odour_d_prime[0]:
            blockwise_odour_d_prime = blockwise_odour_d_prime[1:]
            blockwise_visual_d_prime = blockwise_visual_d_prime[1:]

        plt.plot(blockwise_visual_d_prime, c='b')
        plt.scatter(list(range(len(blockwise_visual_d_prime))), blockwise_visual_d_prime, c='b')

        count = 0
        for odour_d_prime in blockwise_odour_d_prime:
            if odour_d_prime != np.nan:
                plt.scatter(x=[count], y=[odour_d_prime], c='b')
            count += 1


    for session in mutant_session_list:

        # Load Performance Dictionary
        performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        blockwise_visual_d_prime = performance_dictionary['blockwise_visual_d_prime']
        blockwise_odour_d_prime = performance_dictionary['blockwise_odour_d_prime']

        # Start With First Visual
        if blockwise_visual_d_prime[0] > blockwise_odour_d_prime[0]:
            blockwise_odour_d_prime = blockwise_odour_d_prime[1:]
            blockwise_visual_d_prime = blockwise_visual_d_prime[1:]

        plt.plot(blockwise_visual_d_prime, c='g')
        plt.scatter(list(range(len(blockwise_visual_d_prime))), blockwise_visual_d_prime, c='g')

        count = 0
        for odour_d_prime in blockwise_odour_d_prime:
            if odour_d_prime != np.nan:
                plt.scatter(x=[count], y=[odour_d_prime], c='g')
            count += 1
    plt.show()


session_list = [
    r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"
]




control_session_list = [

    # 4.1B

        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging",


    # 7.1B

        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_22_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_23_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_24_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_27_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_30_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_31_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_01_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_02_Transition_Imaging",


    # 14.1A

        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_12_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_13_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_14_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_15_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_16_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_17_Transition_Behaviour",


    # 22.1A
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_26_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_29_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_02_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_03_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_04_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_05_Transition_Imaging",

]




mutant_session_list = [


        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_10_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_11_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_12_Transition_Imaging",




        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_13_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_14_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_16_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_17_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_18_Transition_Imaging",




        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_22_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_23_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_24_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_26_Transition_Imaging",



        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_05_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_10_Transition_Imaging",

]


plot_blockwise_performance(control_session_list, mutant_session_list)