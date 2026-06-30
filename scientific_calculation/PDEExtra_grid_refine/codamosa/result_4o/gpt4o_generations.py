

# Generated at 2026-05-13 11:28:11.040297
# Unit test for function refine_cells

# Generated at 2026-05-13 11:28:17.289231
# Unit test for function refine_cells

# Generated at 2026-05-13 11:28:22.377270
# Unit test for function refine_cells
def test_refine_cells():errors = [(0, 0.1), (1, 0.3), (2, 0.8), (3, 1.2)]
threshold = 0.25
expected = ["keep", "split", "split-twice", "keep"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.01), (1, 0.05), (2, 0.2), (3, 0.3)]
threshold = 0.2
expected = ["merge", "keep", "merge", "keep"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.5), (1, 0.6), (2, 1.0), (3, 2.0)]
threshold = 0.4
expected = ["split", "split", "split-twice", "keep"]
assert refine_cells(errors, threshold) == expected

# Generated at 2026-05-13 11:28:26.791886
# Unit test for function refine_cells

# Generated at 2026-05-13 11:28:46.442638
# Unit test for function refine_cells
def test_refine_cells():errors = [(0, 0.1), (1, 0.3), (2, 0.8), (3, 1.2)]
threshold = 0.25
expected = ["keep", "split", "split-twice", "keep"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.01), (1, 0.05), (2, 0.2), (3, 0.3)]
threshold = 0.2
expected = ["merge", "merge", "keep", "keep"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.5), (1, 0.6), (2, 1.0), (3, 2.0)]
threshold = 0.4
expected = ["split", "split", "split-twice", "keep"]
assert refine_cells(errors, threshold) == expected

# Generated at 2026-05-13 11:28:53.554157
# Unit test for function refine_cells

# Generated at 2026-05-13 11:28:57.535084
# Unit test for function refine_cells

# Generated at 2026-05-13 11:29:03.483183
# Unit test for function refine_cells

# Generated at 2026-05-13 11:29:08.333404
# Unit test for function refine_cells

# Generated at 2026-05-13 11:29:12.470422
# Unit test for function refine_cells
def test_refine_cells():errors = [(0, 0.1), (1, 0.3), (2, 0.8), (3, 0.05)]
threshold = 0.2
expected = ["split", "split", "keep", "merge"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.05), (1, 0.15), (2, 0.25), (3, 0.5)]
threshold = 0.2
expected = ["merge", "keep", "split", "split-twice"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.4), (1, 0.9), (2, 1.2), (3, 0.3)]
threshold = 0.3
expected = ["split", "split-twice", "keep", "keep"]
assert refine_cells(errors, threshold) == expected

# Generated at 2026-05-13 11:29:29.452297
# Unit test for function refine_cells

# Generated at 2026-05-13 11:29:32.665341
# Unit test for function refine_cells
def test_refine_cells():assert refine_cells([(0, 5), (1, 3), (2, 1)], 2) == ["split-twice", "split", "keep"]

# Generated at 2026-05-13 11:29:39.115983
# Unit test for function refine_cells

# Generated at 2026-05-13 11:29:47.916799
# Unit test for function refine_cells

# Generated at 2026-05-13 11:30:06.060408
# Unit test for function refine_cells
def test_refine_cells():errors = [(0, 0.1), (1, 0.3), (2, 0.8), (3, 1.2)]
threshold = 0.25
expected = ["keep", "split", "split-twice", "keep"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.01), (1, 0.05), (2, 0.2), (3, 0.3)]
threshold = 0.2
expected = ["merge", "keep", "merge", "keep"]
assert refine_cells(errors, threshold) == expected

errors = [(0, 0.5), (1, 0.6), (2, 1.0), (3, 1.5)]
threshold = 0.4
expected = ["split", "split", "split-twice", "keep"]
assert refine_cells(errors, threshold) == expected