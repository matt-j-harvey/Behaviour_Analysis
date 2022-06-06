import numpy as np
import matplotlib.pyplot as plt

def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)


delta_f_matrix = np.load(r"/media/matthew/Seagate Expansion Drive2/No_Filter_Test/Cluster_Activity_Matrix.npy")
mean_activity = np.mean(delta_f_matrix, axis=1)

plt.plot(mean_activity)
plt.show()


figure_1 = plt.figure()
axis_1 = figure_1.add_subplot(1,1,1)
axis_1.imshow(np.transpose(delta_f_matrix))
forceAspect(axis_1)
plt.show()
