


def test_soto():
    nonlocal x_1
    x_1 = 0
    x_2 = 0
    def nonlocal_test():

        x_1 = 2
        print(x_1)
        return

    def local_test():
        #x_1 = 5
        print(x_1)
        return

    local_test()
    #nonlocal_test()

    print(x_1)
    return
x_1 = 1
test_soto()
print(x_1)
