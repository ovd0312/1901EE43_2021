def get_bad_inputs(input_nums):
    bad_inputs = []
    for num in input_nums:
        if not (isinstance(num,int)):
            bad_inputs.append(num)
    return bad_inputs

def get_memory_score(input_nums):
    bad_inputs = get_bad_inputs(input_nums)
    if len(bad_inputs)>0:
        print("Please enter a valid input list. Invalid inputs detected:",bad_inputs)
        return
    memory_limit = 5
    curr_memory = []
    score = 0
    for num in input_nums:
        found = False
        for seen_num in curr_memory:
            if(num==seen_num):
                found = True
                score += 1
                break
        if not found:
            curr_memory.append(num)
        if len(curr_memory)>memory_limit:
            curr_memory.pop(0)

    print("Score:",score)
    return


input_nums =  [3, 4, 1, 6, 3, 3, 9, 0, 0, 0]

print(get_memory_score(input_nums))