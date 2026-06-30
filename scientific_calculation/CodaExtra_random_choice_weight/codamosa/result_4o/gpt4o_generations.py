

# Generated at 2026-05-13 09:11:53.063228
# Unit test for function weighted_choice_bucket
def test_weighted_choice_bucket():# Test with valid weights and value
    assert weighted_choice_bucket([1, 2, 3], 0.0) == 0
    assert weighted_choice_bucket([1, 2, 3], 0.5) == 1
    assert weighted_choice_bucket([1, 2, 3], 0.9) == 2

    # Test with single weight
    assert weighted_choice_bucket([10], 0.0) == 0
    assert weighted_choice_bucket([10], 0.5) == 0
    assert weighted_choice_bucket([10], 1.0) == 0

    # Test with empty weights
    try:
        weighted_choice_bucket([], 0.5)
    except ValueError as e:
        assert str(e) == "empty weights"

    # Test with negative weight

# Generated at 2026-05-13 09:11:57.000807
# Unit test for function weighted_choice_bucket

# Generated at 2026-05-13 09:12:05.947448
# Unit test for function weighted_choice_bucket

# Generated at 2026-05-13 09:12:11.803761
# Unit test for function weighted_choice_bucket

# Generated at 2026-05-13 09:12:29.482319
# Unit test for function weighted_choice_bucket

# Generated at 2026-05-13 09:12:34.618215
# Unit test for function weighted_choice_bucket
def test_weighted_choice_bucket():weights = [0.1, 0.3, 0.4, 0.2]

# Generated at 2026-05-13 09:12:42.768658
# Unit test for function weighted_choice_bucket

# Generated at 2026-05-13 09:12:46.893426
# Unit test for function weighted_choice_bucket

# Generated at 2026-05-13 09:13:04.502396
# Unit test for function weighted_choice_bucket

# Generated at 2026-05-13 09:13:11.639613
# Unit test for function weighted_choice_bucket
def test_weighted_choice_bucket():weights = [0.1, 0.3, 0.4, 0.2]