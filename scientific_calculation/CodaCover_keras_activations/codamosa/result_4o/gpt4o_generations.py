

# Generated at 2026-05-13 08:24:55.245296
# Unit test for function activation
def test_activation():assert np.array_equal(activation([1, -1, 0], kind="relu"), [1, 0, 0])

# Generated at 2026-05-13 08:25:06.869543
# Unit test for function activation

# Generated at 2026-05-13 08:25:13.911132
# Unit test for function activation
def test_activation():assert np.allclose(activation([1, -1, 0], kind="relu"), [1, 0, 0])

# Generated at 2026-05-13 08:25:17.543431
# Unit test for function activation
def test_activation():assert np.array_equal(activation([1, -1, 0], kind="relu"), [1, 0, 0])

# Generated at 2026-05-13 08:25:21.693877
# Unit test for function activation
def test_activation():assert np.allclose(activation([1, -1, 0], kind="relu"), [1, 0, 0])

# Generated at 2026-05-13 08:25:27.577974
# Unit test for function activation
def test_activation():assert np.array_equal(activation([1, -1, 0], kind="relu"), [1, 0, 0])

# Generated at 2026-05-13 08:25:33.168736
# Unit test for function activation

# Generated at 2026-05-13 08:25:37.399119
# Unit test for function activation
def test_activation():assert np.allclose(activation([1, -2, 3], kind="relu"), [1, 0, 3])

# Generated at 2026-05-13 08:25:43.964155
# Unit test for function activation
def test_activation():# Test ReLU activation
    assert np.array_equal(activation([-1, 0, 1], kind="relu"), [0, 0, 1])
    
    # Test Leaky ReLU activation
    assert np.array_equal(activation([-1, 0, 1], kind="leaky_relu", alpha=0.1), [-0.1, 0, 1])
    
    # Test Leaky ReLU with invalid alpha
    try:
        activation([-1, 0, 1], kind="leaky_relu", alpha=-0.1)
    except ValueError as e:
        assert str(e) == "alpha must be non-negative"
    
    # Test Sigmoid activation
    assert np.allclose(activation([-1, 0, 1], kind="sigmoid"), [0.26894142, 0.5, 0.73105858])
    
    # Test Tanh activation

# Generated at 2026-05-13 08:26:15.421665
# Unit test for function activation

# Generated at 2026-05-13 08:26:22.053104
# Unit test for function activation
def test_activation():assert np.array_equal(activation([1, -1, 0], kind="relu"), [1, 0, 0])

# Generated at 2026-05-13 08:26:27.293219
# Unit test for function activation
def test_activation():assert np.allclose(activation([1, -2, 3], kind="relu"), [1, 0, 3])

# Generated at 2026-05-13 08:26:33.329195
# Unit test for function activation
def test_activation():# Test ReLU activation
    assert np.array_equal(activation([-1, 0, 1], kind="relu"), [0, 0, 1])
    
    # Test Leaky ReLU activation
    assert np.array_equal(activation([-1, 0, 1], kind="leaky_relu", alpha=0.1), [-0.1, 0, 1])
    
    # Test Leaky ReLU with invalid alpha
    try:
        activation([-1, 0, 1], kind="leaky_relu", alpha=-0.1)
    except ValueError as e:
        assert str(e) == "alpha must be non-negative"
    
    # Test Sigmoid activation
    assert np.allclose(activation([-1, 0, 1], kind="sigmoid"), [0.26894142, 0.5, 0.73105858])
    
    # Test Tanh activation

# Generated at 2026-05-13 08:26:45.499665
# Unit test for function activation
def test_activation():assert np.allclose(activation([1, -1, 0], kind="relu"), [1, 0, 0])

# Generated at 2026-05-13 08:26:49.595676
# Unit test for function activation
def test_activation():assert np.array_equal(activation([1, -1, 0], kind="relu"), [1, 0, 0])