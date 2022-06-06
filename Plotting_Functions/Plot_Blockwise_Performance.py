import numpy as np
import matplotlib.pyplot as plt
import os


def plot_blockwise_performance(session_list):

    for session in session_list:

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
                plt.scatter(x=[count], y=[odour_d_prime], c='g')
            count += 1
    plt.show()


session_list = [
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"
]
plot_blockwise_performance(session_list)