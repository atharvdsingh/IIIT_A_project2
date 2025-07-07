def viz(filepath:str,regularization,rashomon_bound_multiplier,label:str=None):
    import pandas as pd
    import numpy as np
    import pathlib
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from treefarms.model.threshold_guess import compute_thresholds, cut
    from treefarms import TREEFARMS
    from treefarms.model.model_set import ModelSetContainer
    import json
    # read the dataset
    df=pd.read_csv(filepath)
    if label is None:
        label=df.columns[-1]
    if label not in df.columns:
        raise ValueError(f'lable is not in column{label}')
    
    X, y = df.iloc[:, :-1], df.iloc[:, -1]
    h = df.columns[:-1]

    # train TREEFARMS model
    config = {
    "regularization": regularization,  # regularization penalizes the tree with more leaves. We recommend to set it to relative high value to find a sparse tree.
    "rashomon_bound_multiplier":rashomon_bound_multiplier,  # rashomon bound multiplier indicates how large of a Rashomon set would you like to get
    }


    model = TREEFARMS(config)

    model.fit(X, y)
    path=model.get_decision_paths()

    return path