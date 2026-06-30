

# Generated at 2026-05-13 08:49:18.515372
# Unit test for function nanmean_with_min_count
def test_nanmean_with_min_count():assert np.isnan(nanmean_with_min_count([np.nan, np.nan], min_count=2))

# Generated at 2026-05-13 08:49:33.574880
# Unit test for function nanmean_with_min_count

# Generated at 2026-05-13 08:50:07.578585
# Unit test for function nanmean_with_min_count
def test_nanmean_with_min_count():assert np.isnan(nanmean_with_min_count([np.nan, np.nan], min_count=2))

# Generated at 2026-05-13 08:50:12.437002
# Unit test for function nanmean_with_min_count
def test_nanmean_with_min_count():assert np.isnan(nanmean_with_min_count([np.nan, np.nan], min_count=1))

# Generated at 2026-05-13 08:50:16.111443
# Unit test for function nanarg_extreme
def test_nanarg_extreme():# Test case 1: Normal case with mode="max"
    assert nanarg_extreme([1, 2, 3, np.nan], mode="max") == 2

    # Test case 2: Normal case with mode="min"
    assert nanarg_extreme([1, 2, 3, np.nan], mode="min") == 0

    # Test case 3: All values are NaN
    try:
        nanarg_extreme([np.nan, np.nan], mode="max")
    except ValueError as e:
        assert str(e) == "all values are NaN"

    # Test case 4: Empty array
    try:
        nanarg_extreme([], mode="max")
    except ValueError as e:
        assert str(e) == "all values are NaN"

    # Test case 5: Invalid mode

# Generated at 2026-05-13 08:50:19.956257
# Unit test for function nanmean_with_min_count
def test_nanmean_with_min_count():assert np.isclose(nanmean_with_min_count([1, 2, 3, np.nan]), 2.0)

# Generated at 2026-05-13 08:50:26.428101
# Unit test for function nanmean_with_min_count
def test_nanmean_with_min_count():assert np.isnan(nanmean_with_min_count([np.nan, np.nan], min_count=1))

# Generated at 2026-05-13 08:50:31.760368
# Unit test for function nanmean_with_min_count
def test_nanmean_with_min_count():assert np.isclose(nanmean_with_min_count([1, 2, 3, np.nan], min_count=2), 2.0)

# Generated at 2026-05-13 08:50:36.716356
# Unit test for function nanarg_extreme
def test_nanarg_extreme():values = [1, 3, np.nan, 2]

# Generated at 2026-05-13 08:50:40.236275
# Unit test for function nanmean_with_min_count
def test_nanmean_with_min_count():assert np.isclose(nanmean_with_min_count([1, 2, 3, np.nan]), 2.0)

# Generated at 2026-05-13 08:50:47.253016
# Unit test for function nanarg_extreme

# Generated at 2026-05-13 08:50:52.722593
# Unit test for function nanarg_extreme
def test_nanarg_extreme():values = [1, 3, np.nan, 2]

# Generated at 2026-05-13 08:51:04.495887
# Unit test for function nanarg_extreme

# Generated at 2026-05-13 08:51:07.733693
# Unit test for function nanarg_extreme