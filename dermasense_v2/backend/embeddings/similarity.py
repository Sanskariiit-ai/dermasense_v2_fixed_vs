import numpy as np


def cosine_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Cosine similarity between every row of a and every row of b."""
    a = np.atleast_2d(a)
    b = np.atleast_2d(b)
    an = np.linalg.norm(a, axis=1, keepdims=True)
    bn = np.linalg.norm(b, axis=1, keepdims=True)
    return (a / np.where(an == 0, 1, an)) @ (b / np.where(bn == 0, 1, bn)).T
