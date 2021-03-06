import pickle


def loadpickles(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model
