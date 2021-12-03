# old smooth functions


def smooth(l):
    """ Funzione originale con variabile 'n' hardcoded """
    new_l = []
    new_l.append(l[0])

    for i in range(1, len(l) - 1):
        value = (l[i-1] + l[i] + l[i+1]) / 3
        new_l.append(value)

    new_l.append(l[-1])
    return new_l


def smooth2(l, n=15):
    """ Takes a list and returns it smoothed
        use recursion to deal with large number of 'n'
    """

    # per n grandi (n>50) l'inizio e la fine si vede che sono brutti
    if n < 1:
        # chiude il loop
        return l

    # inserisce la prima parte che viene saltata
    # smoothing con n=n/10 perchè non sia troppo brutto
    new_l = [] + smooth2(l[:n], n=int(n/10))

    for i in range(n, len(l) - n):
        # temp list su cui calcolare la media
        temp_list = mean(l[i-n:i+n+1])

        new_l.append(temp_list)

    # inserisce l'ultima parte che viene saltata
    # stessa cosa dell'inizio
    new_l += smooth2(l[-n:], n=int(n/10))

    return new_l


def smooth3(l, n=15):
    """ Takes a list and returns it smoothed
        doesn't use recursion to deal with large values of 'n' but instead
        makes the moving mean of the first and last 'n' elements
    """

    new_l = []
    new_l.append(l[0])

    for i in range(1, len(l)-1):
        a = i-n
        b = i+n+1
        if a < 0:
            a = 0
        if b > len(l):
            b = len(l)

        temp_list = mean(l[a:b])
        new_l.append(temp_list)

    new_l.append(l[-1])

    return new_l

 
def smooth4(l, n=15):
    """ Takes a list and returns it smoothed
        In the range (1, n) each mean must be done with that number of elements
    """

    # creates new list
    new_l = []
    # appends first element
    new_l.append(l[0])

    for i in range(1, len(l)-1):

        # corrected_n is the range around the 'i'th element
        # it is not always equal to 'n' because in the first and last 'n' elements
        # it is equal to the largest possible range
        if i < n:
            corrected_n = i
        elif len(l) - i < n:
            corrected_n = len(l) - i
        else:
            corrected_n = n

        # temp list with the elements used to calculate the mean
        temp_l = l[i-corrected_n:i+corrected_n+1]
        new_l.append(mean(temp_l))

    # appends last element
    new_l.append(l[-1])

    return new_l
