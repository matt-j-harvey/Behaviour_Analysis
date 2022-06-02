import sys
sys.path.append("/home/matthew/Documents/Github_Code/Behaviour_Analysis")

import Create_Behaviour_Matrix

session_list = [
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK14.1A/2021_06_17_Transition_Imaging", 0.30],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK16.1B/2021_07_08_Transition_Imaging", 0.30],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK10.1A/2021_06_18_Transition_Imaging", 0.30],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK7.1B/2021_04_02_Transition_Imaging",  0.08],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK4.1B/2021_04_10_Transition_Imaging",  0.08],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK4.1A/2021_04_12_Transition_Imaging",  0.08],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK12.1F/2021_09_22_Transition_Imaging", 0.30],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NRXN78.1A/2020_12_09_Switching_Imaging",  0.08],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NRXN78.1D/2020_11_29_Switching_Imaging",  0.08],
                ["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NRXN71.2A/2020_12_17_Switching_Imaging",  0.08]
]

session_list= [
    ["/media/matthew/Seagate Expansion Drive1/Switching_Analysis/Homs/NRXN71.2A/2020_12_17_Switching_Imaging", 0.08],
    #["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK10.1A/2021_06_18_Transition_Imaging", 0.30],
    #["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK16.1B/2021_07_08_Transition_Imaging", 0.30],
    #["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK4.1A/2021_04_10_Transition_Imaging", 0.08],
    #["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK4.1A/2021_04_12_Transition_Imaging", 0.08],
    #["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK24.1C/2021_11_10_Transition_Imaging", 0.30],
    #["/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Transition_Analysis/NXAK24.1C/2021_11_10_Transition_Imaging", 0.30],
    #["/media/matthew/Seagate Expansion Drive1/Transition_2/NXAK20.1B/2021_11_22_Transition_Imaging", 0.30],
    #["/media/matthew/Seagate Expansion Drive1/Transition_2/NXAK20.1B/2021_11_24_Transition_Imaging", 0.30],
    #["/media/matthew/Seagate Expansion Drive1/Transition_2/NXAK20.1B/2021_11_26_Transition_Imaging", 0.30]
]






for session in session_list:
    Create_Behaviour_Matrix.create_behaviour_matrix(session[0], lick_threshold=session[1]),