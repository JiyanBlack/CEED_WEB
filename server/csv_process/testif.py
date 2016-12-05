def test_if():
    print("test_if executing..")
    return True
a = [1, 2, 3]
if 4 not in a or test_if():
    print(1)
