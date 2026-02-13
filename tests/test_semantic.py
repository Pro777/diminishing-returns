from dr.semantic import cosine_similarity, mean_vector


def test_cosine_similarity_identity():
    assert round(cosine_similarity([1.0, 0.0], [1.0, 0.0]), 6) == 1.0


def test_cosine_similarity_orthogonal():
    assert round(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 6) == 0.0


def test_mean_vector():
    v = mean_vector([[1.0, 2.0], [3.0, 4.0]])
    assert v == [2.0, 3.0]
