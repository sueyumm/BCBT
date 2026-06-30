

# Generated at 2026-05-13 08:27:08.387358
# Unit test for function regression_loss

# Generated at 2026-05-13 08:27:12.816202
# Unit test for function regression_loss
def test_regression_loss():assert regression_loss([1, 2, 3], [1, 2, 3], loss="mse") == 0.0

# Generated at 2026-05-13 08:27:46.869894
# Unit test for function regression_loss

# Generated at 2026-05-13 08:27:52.066131
# Unit test for function regression_loss

# Generated at 2026-05-13 08:27:58.166445
# Unit test for function regression_loss

# Generated at 2026-05-13 08:28:19.679589
# Unit test for function regression_loss

# Generated at 2026-05-13 08:28:23.743043
# Unit test for function regression_loss
def test_regression_loss():# Test MSE loss
    assert regression_loss([1, 2, 3], [1, 2, 3], loss="mse") == 0.0
    assert regression_loss([1, 2, 3], [2, 3, 4], loss="mse") == 1.0

    # Test MAE loss
    assert regression_loss([1, 2, 3], [1, 2, 3], loss="mae") == 0.0
    assert regression_loss([1, 2, 3], [2, 3, 4], loss="mae") == 1.0

    # Test Huber loss
    assert regression_loss([1, 2, 3], [1, 2, 3], loss="huber", delta=1.0) == 0.0

# Generated at 2026-05-13 08:28:28.984883
# Unit test for function regression_loss

# Generated at 2026-05-13 08:28:36.569792
# Unit test for function regression_loss
def test_regression_loss():y_true = np.array([1.0, 2.0, 3.0])

# Generated at 2026-05-13 08:28:41.790755
# Unit test for function regression_loss