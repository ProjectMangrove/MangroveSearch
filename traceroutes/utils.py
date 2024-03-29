import pickle

def pickle_list(to_pickle, filename):
        '''
        Pickles a list.

        ### Parameters
            1. to_pickle: list/dict
                a list/dict object to be pickled
            2. filename:
                the name of the pickle file to be saved to. should end in .pk

        ### Returns
            None
        '''
        with open("pickles/"+filename, 'wb') as f:
            pickle.dump(to_pickle, f)

def unpickle_list(filename):
    '''
    Unpickles a list.

    ### Parameters
        1. filename: string
            the pickle file containing the object to be unpickled

    ### Returns
        1. l: object
            the unpickled object
    '''
    if filename:
        with open("pickles/"+filename, 'rb') as f:
            l = pickle.load(f)
    return l
