import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
from datetime import datetime
import cv2
from sklearn.decomposition import PCA
from matplotlib import cm
from scipy import ndimage

def get_blue_file(base_directory):
    file_list = os.listdir(base_directory)
    for file in file_list:
        if "Blue" in file:
            return base_directory + "/" + file

def get_violet_file(base_directory):
    file_list = os.listdir(base_directory)
    for file in file_list:
        if "Violet" in file:
            return base_directory + "/" + file

def check_max_projection(home_directory):
    print("Getting Max Projection")

    # Load Data
    blue_file = get_blue_file(home_directory)
    blue_data_container = h5py.File(blue_file, 'r')
    blue_data = blue_data_container["Data"]

    sample = blue_data[:, 0:1000]
    max_projection = np.max(sample, axis=1)
    max_projection = np.reshape(max_projection, (600, 608))

    max_value = np.percentile(max_projection, 99)
    max_projection = np.divide(max_projection, max_value)
    plt.imshow(max_projection, vmax=1)
    plt.show(block=False)
    plt.pause(5)
    plt.close()


def get_chunk_structure(chunk_size, array_size):
    number_of_chunks = int(np.ceil(array_size / chunk_size))
    remainder = array_size % chunk_size

    # Get Chunk Sizes
    chunk_sizes = []
    if remainder == 0:
        for x in range(number_of_chunks):
            chunk_sizes.append(chunk_size)

    else:
        for x in range(number_of_chunks - 1):
            chunk_sizes.append(chunk_size)
        chunk_sizes.append(remainder)

    # Get Chunk Starts
    chunk_starts = []
    chunk_start = 0
    for chunk_index in range(number_of_chunks):
        chunk_starts.append(chunk_size * chunk_index)

    # Get Chunk Stops
    chunk_stops = []
    chunk_stop = 0
    for chunk_index in range(number_of_chunks):
        chunk_stop += chunk_sizes[chunk_index]
        chunk_stops.append(chunk_stop)

    return number_of_chunks, chunk_sizes, chunk_starts, chunk_stops


def load_mask(home_directory):

    # Loads the mask for a video, returns a list of which pixels are included, as well as the original image height and width
    mask = np.load(home_directory + "/Generous_Mask.npy")

    image_height = np.shape(mask)[0]
    image_width = np.shape(mask)[1]

    mask = np.where(mask>0.1, 1, 0)
    mask = mask.astype(int)
    flat_mask = np.ndarray.flatten(mask)
    indicies = np.argwhere(flat_mask)
    indicies = np.ndarray.astype(indicies, int)
    indicies = np.ndarray.flatten(indicies)

    return indicies, image_height, image_width



def calculate_delta_f(activity_matrix, baseline_vector):

    # Transpose Baseline Vector so it can be used by numpy subtract
    baseline_vector = baseline_vector[:, np.newaxis]

    # Get Delta F
    delta_f = np.subtract(activity_matrix, baseline_vector)

    # Remove Negative Values
    delta_f = np.clip(delta_f, a_min=0, a_max=None)

    # Divide by baseline
    delta_f_over_f = np.divide(delta_f, baseline_vector)

    # Remove NANs
    delta_f_over_f = np.nan_to_num(delta_f_over_f)

    return delta_f_over_f


def normalise_traces(data_sample):

    # Subtract Baseline
    baseline = np.min(data_sample, axis=1)
    baseline = baseline[:, np.newaxis]
    data_sample = np.subtract(data_sample, baseline)

    # Divide By Max
    max_vector = np.max(data_sample, axis=1)
    max_vector = max_vector[:, np.newaxis]
    data_sample = np.divide(data_sample, max_vector)

    return data_sample





def process_pixels(base_directory, delta_f_file):

    print("Processing Pixels")

    # Load Data
    blue_file = get_blue_file(base_directory)
    data_file = os.path.join(base_directory, blue_file)
    data_container = h5py.File(data_file, 'r')
    blue_matrix = data_container["Data"]

    # Load Mask
    indicies, image_height, image_width = load_mask(base_directory)

    # Get Data Structure
    number_of_images = np.shape(blue_matrix)[1]
    number_of_pixels = len(indicies)

    # Define Chunking Settings
    preferred_chunk_size = 20000
    number_of_chunks, chunk_sizes, chunk_starts, chunk_stops = get_chunk_structure(preferred_chunk_size, number_of_pixels)

    with h5py.File(delta_f_file, "w") as f:
        dataset = f.create_dataset("Data", (number_of_images, number_of_pixels), dtype=np.float32, chunks=True, compression="gzip")

        for chunk_index in range(number_of_chunks):
            print("Chunk:", str(chunk_index).zfill(2), "of", number_of_chunks, "at", datetime.now())

            # Load Chunk Data
            chunk_start = int(chunk_starts[chunk_index])
            chunk_stop = int(chunk_stops[chunk_index])
            chunk_pixels = indicies[chunk_start:chunk_stop]
            blue_data = blue_matrix[chunk_pixels]

            # Perform Delta F
            blue_baseline = np.percentile(blue_data, axis=1, q=5)
            blue_data = calculate_delta_f(blue_data, blue_baseline)

            # Normalise Delta F
            processed_data = normalise_traces(blue_data)

            # Insert Back
            dataset[:, chunk_start:chunk_stop] = np.transpose(processed_data)




def create_sample_video(processed_file_location, home_directory, blur_size=1):
    print("Creating Sample Delta F Video")

    # Load Mask
    mask = np.load(home_directory + "/Generous_Mask.npy")
    mask = np.where(mask>0.1, 1, 0)
    mask = mask.astype(int)

    flat_mask = np.ndarray.flatten(mask)
    indicies = np.argwhere(flat_mask)
    indicies = np.ndarray.astype(indicies, int)
    indicies = np.ndarray.flatten(indicies)

    # Load Processed Data
    processed_data_file = h5py.File(processed_file_location, 'r')
    processed_data = processed_data_file["Data"]

    # Get Sample Data
    sample_size = 7000
    sample_data = processed_data[1000:1000 + sample_size]
    sample_data = np.nan_to_num(sample_data)

    # Denoise with dimensionality reduction
    model = PCA(n_components=150)
    transformed_data = model.fit_transform(sample_data)
    sample_data = model.inverse_transform(transformed_data)

    # Get Colour Boundaries
    cm = plt.cm.ScalarMappable(norm=None, cmap='inferno')

    colour_max = 0.7
    colour_min = 0.1

    cm.set_clim(vmin=colour_min, vmax=colour_max)

    # Get Original Pixel Dimenions
    frame_width = 608
    frame_height = 600

    video_name = home_directory + "/Movie_Baseline.avi"
    video_codec = cv2.VideoWriter_fourcc(*'DIVX')
    video = cv2.VideoWriter(video_name, video_codec, frameSize=(frame_width, frame_height), fps=30)  # 0, 12

    # plt.ion()
    window_size = 3

    for frame in range(sample_size - window_size):  # number_of_files:
        template = np.zeros((frame_height * frame_width))

        image = sample_data[frame:frame + window_size]
        image = np.mean(image, axis=0)
        image = np.nan_to_num(image)
        np.put(template, indicies, image)
        image = np.reshape(template, (frame_height, frame_width))
        image = ndimage.gaussian_filter(image, blur_size)

        colored_image = cm.to_rgba(image)
        colored_image = colored_image * 255

        image = np.ndarray.astype(colored_image, np.uint8)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        video.write(image)

    cv2.destroyAllWindows()
    video.release()



base_directory = r"/media/matthew/Seagate Expansion Drive2/No_Filter_Test"
delta_f_file = r"/media/matthew/Seagate Expansion Drive2/No_Filter_Test/Delta_F.hdf5"

#process_pixels(base_directory, delta_f_file)
create_sample_video(delta_f_file, base_directory)