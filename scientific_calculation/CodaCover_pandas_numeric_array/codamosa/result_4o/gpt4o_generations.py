

# Generated at 2026-05-13 08:51:44.006509
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:51:53.269549
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:51:57.804946
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:52:04.408036
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:52:10.446337
# Unit test for function coerce_numeric
def test_coerce_numeric():assert np.array_equal(coerce_numeric([1, 2, 3]), np.array([1.0, 2.0, 3.0]))

# Generated at 2026-05-13 08:52:14.386885
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:52:21.362056
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:52:26.997402
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:52:29.897923
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:52:34.128706
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:52:47.264385
# Unit test for function coerce_numeric
def test_coerce_numeric():# Test case 1: Normal conversion to float
    assert np.array_equal(coerce_numeric(["1", "2.5", "3"]), np.array([1.0, 2.5, 3.0]))

    # Test case 2: Coerce invalid values to NaN
    assert np.array_equal(coerce_numeric(["1", "invalid", "3"], errors="coerce"), np.array([1.0, np.nan, 3.0]))

    # Test case 3: Ignore invalid values
    assert np.array_equal(coerce_numeric(["1", "invalid", "3"], errors="ignore"), np.array(["1", "invalid", "3"], dtype=object))

    # Test case 4: Raise error for invalid values
    try:
        coerce_numeric(["1", "invalid", "3"], errors="raise")
        assert False  # Should not reach here
    except ValueError:
        assert True

# Generated at 2026-05-13 08:52:52.822795
# Unit test for function coerce_numeric

# Generated at 2026-05-13 08:53:09.673764
# Unit test for function coerce_numeric
def test_coerce_numeric():assert np.array_equal(coerce_numeric([1, 2, 3]), np.array([1.0, 2.0, 3.0]))

# Generated at 2026-05-13 08:53:13.229094
# Unit test for function coerce_numeric