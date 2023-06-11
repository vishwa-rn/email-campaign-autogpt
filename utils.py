import os
import pickle


def update_pickle_file(key, value, filename="data/memory.pkl"):
    data = {}

    # Load the existing dictionary if the pickle file exists
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)

    # Update the dictionary
    data[key] = value

    # Save the updated dictionary
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def get_value_from_pickle(key, filename="data/memory.pkl"):
    # Load the existing dictionary if the pickle file exists
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            # Return the value if the key exists, otherwise return None
            return data.get(key, None)

    else:
        return None  # Return None if the file does not exist


get_value_from_pickle(key="test")
