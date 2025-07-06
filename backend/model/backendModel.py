import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from treefarms import TREEFARMS
from multiprocessing import Process, Queue
import json

def train_model(X, y, config, queue):
    try:
        model = TREEFARMS(config)
        model.fit(X, y)
        paths = model.get_decision_paths()
        queue.put(paths)
    except Exception as e:
        queue.put({'error': str(e)})

def viz(filepath: str, label: str = None):
    # Load dataset
    df = pd.read_csv(filepath)
    if label is None:
        label = df.columns[-1]
    if label not in df.columns:
        raise ValueError(f"Label '{label}' not found in dataset columns")

    X, y = df.drop(columns=[label]), df[label]

    config = {
        "regularization": 0.01,
        "rashomon_bound_multiplier": 0.05
    }

    queue = Queue()
    p = Process(target=train_model, args=(X, y, config, queue))
    p.start()
    p.join(timeout=20)

    if p.is_alive():
        p.terminate()
        p.join()
        raise TimeoutError("Training took too long and was stopped after 20 seconds.")

    if queue.empty():
        raise RuntimeError("Training failed or no output produced.")
    
    result = queue.get()

    if isinstance(result, dict) and 'error' in result:
        raise RuntimeError(f"Training failed: {result['error']}")

    return result  # JSON-serializable decision paths
