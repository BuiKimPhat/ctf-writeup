# def func(x):
    # Returns the number of distinct pairs (y, z) from the numbers in the file "numbers.txt" whose y != z and (y + z) == x
    # Note that two pairs (y, z) and (z, y) are considered the same and are counted only once
def cntDisPairs(arr, N, K):
     
    # Stores count of distinct pairs
    # whose sum equal to K
    cntPairs = 0
 
    # Sort the array
    arr = sorted(arr)
 
    # Stores index of
    # the left pointer
    i = 0
 
    # Stores index of
    # the right pointer
    j = N - 1
 
    # Calculate count of distinct
    # pairs whose sum equal to K
    while (i < j):
 
        # If sum of current pair
        # is equal to K
        if (arr[i] + arr[j] == K):
 
            # Remove consecutive duplicate
            # array elements
            while (i < j and arr[i] == arr[i + 1]):
 
                # Update i
                i += 1
 
            # Remove consecutive duplicate
            # array elements
            while (i < j and arr[j] == arr[j - 1]):
 
                # Update j
                j -= 1
 
            # Update cntPairs
            cntPairs += 1
 
            # Update i
            i += 1
 
            # Update j
            j -= 1
 
        # If sum of current pair
        # less than K
        elif (arr[i] + arr[j] < K):
 
            # Update i
            i += 1
        else:
 
            # Update j
            j -= 1
             
    return cntPairs

filename = "numbers.txt"
with open(filename) as file:
    lines = file.readlines()
    lines = [int(line.rstrip()) for line in lines]

def func(x):
    return cntDisPairs(lines, len(lines), x)

def get_flag(res):
    flag = []
    for i in range(len(res)):
        flag.append(chr(func(res[i])))
    flag = ''.join(flag)
    return flag


if __name__ == "__main__":
    res = [751741232, 519127658, 583555720, 3491231752, 3333111256, 481365731, 982100628, 1001121327, 3520999746,
           915725624, 3218509573, 3621224627, 3270950626, 3321456817, 3091205444, 999888800, 475855017, 448213157,
           3222412857, 820711846, 3710211491, 3119823672, 3333211607, 812955676, 971211391, 3210953872, 289789909,
           781213400, 578265122, 910021887, 653886578, 3712776506, 229812345, 582319118, 1111276998, 1151016390,
           700123328, 1074521304, 3210438183, 817210125, 501231350, 753244584, 3240911853, 415234677, 469125436,
           592610671, 612980665, 291821367, 344199617, 1011100412, 681623864, 897219249, 3132267885, 565913000,
           301203203, 3100544737, 432812663, 1012813485, 510928797, 671553831, 3216409218, 3191288433, 698777123,
           3512778698, 810476845, 3102989588, 3621432709, 812321695, 526486561, 378912454, 3316207359, 623111580,
           344209171, 537454826, 691277475, 2634678623, 1112182335, 792111856, 762989676, 666210267, 871278369,
           581009345, 391231132, 921732469, 717217468, 3101412929, 3101217354, 831912337, 532666530, 701012510,
           601365919, 492699680, 2843119525]
    print("The flag is", get_flag(res))
    # func(751741232)
