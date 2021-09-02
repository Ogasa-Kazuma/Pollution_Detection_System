
x_1 = 6
x_2 = 7
x_3 = 99

def test_soto(x_1, x_2):

    print(x_1)
    print(x_2)

    x_3 = 80

    # x_1 = 0
    # x_2 = 0

    def nonlocal_test(x_4):
        nonlocal x_3
        x_3 = x_3 + x_4
        print(x_3)
        #
        
        print(x_1)
        # x_2 = 1
        # x_1 = x_2 + 2

        return

    def local_test():
        #x_1 = 5
        return

    nonlocal_test(30)
    nonlocal_test(300)
    nonlocal_test(3000)
    #nonlocal_test()

    x_1 = x_1 + 3
    print(x_1)


    return

test_soto(x_1, x_2)
print(x_3)
