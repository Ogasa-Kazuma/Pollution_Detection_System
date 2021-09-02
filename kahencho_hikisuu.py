

def TestChangeableArguments(element1, *elements):

    collection = list()
    for i in range(len(elements)):
        collection.append(elements[i])

    print(collection)

    return collection




def main():

    test = list()
    test.append(100)
    test.append(200)
    TestChangeableArguments(1, test,"memo", 20,30,40,50)

if __name__ == "__main__":
    main()
