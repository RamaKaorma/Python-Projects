def first_lock(gems):
    '''Finding the most common type of gem in a panel, to figure which
    button (represented by a gem) should be pressed.'''
    
    gems_dict = {}  # holds "gem: frequency" as key-value pairs. 
    gems_list = []  # list of gems as tuple(frequency, gem), sorted
    most_freq_gems = [] 
    
    if gems == []:
        return None
    else:
        # Find the frequency of each type of gem in gems.
        # Add them to gems_dict to have key-value pairs to compare values.
        for item in gems:
            if item in gems_dict:
                gems_dict[item] += 1
            else:
                gems_dict[item] = 1


        # Sort dictionary in descending order based on frequency of gem:
        for key, value in gems_dict.items():
            gems_list.append((value, key))

        sorted_gems_list = sorted(gems_list, reverse=True)

        # highest frequency allows the comparison against other gems
        highest_freq = sorted_gems_list[0][0]

        # Check highest_freq against other frequencies in sorted_gems_list.
        # This allows the creation of a list with the most frequent gems.
        for element in sorted_gems_list:    
            if element[0] == highest_freq:
                most_freq_gems.append(element[1])
                continue


        # Check if there is a tie in most_frequent_gems list and break it.        
        if len(most_freq_gems) > 1:
            return sorted(most_freq_gems) 
        else:    
            return [sorted_gems_list[0][1]]
    


def second_lock(gems):
    '''Find whether a list of numbered gems in a source can be moved
    to a destination in ascending order (with the help of a store)''' 
    
    # Variables and lists
    source = gems.copy()
    store = []
    destination = []
    store_count = 0
    length = len(gems) // 2
    first_half = gems[:length]
    
    
    # check if there are duplicates in gems, if so, return False
    source_set = set(source)
    if len(source_set) != len(gems):
        return (False, -1)    
    
    # Checking for gems in list ensures no indexError exceptions arise later
    if gems:
        # Check if gems are already sorted in ascending or descending order
        if (sorted(gems) == gems) or (sorted(gems) == gems[::-1]):
            if sorted(gems) == gems:
                return (True, len(gems) - 1)
            else:
                return (True, 0)
        
        # If gems are not already sorted   
        else:
            # The following tests whether the gems can be sorted in 
            # ascending order. It cannot be achieved if a number in the
            # list is between two numbers that are less than itself
            
            # E.g. of this case would be having [7, 3] in the 'store'.
            # 3 cannot be moved as 7 blocks it.
            
            for x in first_half:
                # Gems can be sorted, count refers to the number
                # that we will be moving next to the destination.
                count = 1
                while len(destination) < len(gems):
                    # 'while' loop ensures we don't loop
                    # over source when it is empty

                    # First case: if list cannot be solved, when
                    # neither outmost store item nor outmost source
                    # item is equal to the count.
                    if (store and store[-1] != count) and \
                       (source and source[-1] != count):
                        if count in store:
                            return (False, -1)
                        else:
                            store.append(source[-1])
                            source.remove(source[-1])
                            store_count += 1
                            continue
                    
                    # Second case: the next value is outmost in source
                    elif source and (source[-1] == count):
                        destination.append(count)
                        source.remove(count)
                        count += 1
                        if len(destination) < len(gems):
                            continue
                    
                    # Third case: the next value is outmost in store
                    elif store and (store[-1] == count):
                        destination.append(count)
                        store.remove(count)
                        count += 1
                        if len(destination) < len(gems):
                            continue
                            
                    # Fourth case: Yey! We're done!       
                    elif (not source) and (not store):
                        return (True, store_count)
                    
                    # Fifth case: we only have items in store, but last 
                    # item added is not the next value.
                    elif store and (store[-1] != count):
                        return (False, -1)
                    
                    # Sixth case: next value is in source, we move the
                    # preceding values to the store to get to next value.
                    else:
                        store.append(source[-1])
                        source.remove(source[-1])
                        store_count += 1
                        continue
                                
    # Cannot be sorted                
    else:
        return (True, 0)
    
    return (True, store_count)   
     


""" List of my functions:
        rotate_once(elem)
        pair_and_compare(list1, list2)
        check all orientations(key, stone, row, column)
        first_stone(key, stone)
        move_stone_down(key, stone)
        move_stone_right(key, stone)
        move_stone_down_and_right(key, stone)
        third_lock(key, stone)
        
"""

import itertools

def rotate_once(elem):  
    '''Rotates the key 90 degrees, once, in clockwise direction'''
    
    new_elem = list(zip(*reversed(elem)))
    new_elem = [list(thing) for thing in new_elem]

    return new_elem


def pair_and_compare(list1, list2):
    '''Checks the given lists, and creates pairs based on indexes,
       elements in the pairs are then compared 
       (see check_all_orientations() function)'''
    
    # Use itertools module's chain function to:  
    # 1 -- Join the sublists in list1 (and same for list2)
    list1 = itertools.chain.from_iterable(list1)
    list2 = itertools.chain.from_iterable(list2)
    
    # 2 -- Convert the final list into a string to allow grouping characters
    list1 = ''.join(list1)
    list2 = ''.join(list2)
    
    # Use itertools module's zip_longest function to create the pairs
    # (one part of the key vs one part of the stone)
    ziped_pair = list((itertools.zip_longest(list1, list2)))
    
    # The pairs
    return ziped_pair

    

def check_all_orientations(key, stone, row, column):
    ''' Checks whether the key fits the stone in the 4 differnt orientations
    N, E, S, W, using the rotate_once and pair_and_compare functions '''
    
    # dict allows for us to find the orientation that we are checking now
    # first time we check, there is no rotation, thus N
    # third time we check, we rotated twice, hence S is the orientation
    
    orientation = {
        1: 'N',
        2: 'E',
        3: 'S',
        4: 'W',
    }
    
    # new variable so that we don't loop over function argument
    the_key = key.copy() 

    orientation_num = 1
    while orientation_num <= 4:  # ensures we check 4 orientations
        part_num = 1  # refers to the part of key we're checking now
        ziped_pair = pair_and_compare(the_key, stone)  # the pairs
        
        # stone was previously the_stone

        num_of_parts = 0  # count 'raised' and 'blank' parts the key has
        for elem in key:
            num_of_parts += len(elem)
        
        # check the pairs of key, stone parts
        for i, j in ziped_pair:
            if (i == "*" and j == ".") or (i == "." and j == "#") \
                                        or (i == "." and j == "."):
                
                if part_num == num_of_parts: 
                    # if we checked all the parts
                    return (row, column, orientation.get(orientation_num)) 
                else:
                    part_num += 1  # Check the next part of key
                    continue
            else:
                # If key can't fit in stone on this point, rotate the key
                the_key = rotate_once(the_key)
                orientation_num += 1  # To check the next orientation
                part_num = 1
                continue


    return None

def first_stone(key, stone):
    '''Checks the first part of the stone, the top left hand corner.
    Check if the key fits on this part of the stone'''
    the_stone = stone[:len(key)]
    # Get the number of rows
    index = len(key[0])
    # Get the number of columns
    for w in the_stone:
        del w[index + 1:]

    # check all orientations for this position
    result = check_all_orientations(key, the_stone, 0, 0)
    return result

def move_stone_down(key, stone):  
    '''Check the botton right hand corner of the stone.
    Check if the key fits on this part of the stone'''
    # if the key and stone have the same num of rows,
    # then the key cannot be moved down. Hence rotate then move.
    if len(key) == len(stone):
        key = rotate_once(key)
        
    # Get num of rows
    the_stone = stone[:-len(key)]
    index = len(key[0])
    # Get num of columns
    for w in the_stone:
        del w[index:]

    result = check_all_orientations(key, the_stone, 1, 0)
    return result


def move_stone_right(key, stone):  
    '''Check the top right hand corner of the stone
    Check if the key fits on this part of the stone'''
    # Key cannot be moved right if key and stone have same num of columns
    if len(key[0]) == len(stone[0]):
        key = rotate_once(key)
        
    # Get num of rows
    the_stone = stone[:len(key)]
    index = len(key[0])
    # Get num of columns
    for w in the_stone:
        del w[:-index]

    result = check_all_orientations(key, the_stone, 0, 1)
    return result

def move_stone_down_and_right(key, stone):  
    '''Check the bottom right hand corner of the stone
    Check if the key fits on this part of the stone'''
    
    # Get num of rows
    the_stone = stone[len(key) - 1:]
    index = len(key[0])
    # Get num of columns
    for w in the_stone:
        del w[:index - 1]

    result = check_all_orientations(key, the_stone, 1, 1)
    return result


def third_lock(key, original_stone):
    '''find if key can fit within stone (both are rectangular)
    this function checks all possible positions and orientations'''

    # if key and stone have the exact same dimensions
    checked_0 = check_all_orientations(key, original_stone, 0, 0)
    
    # top left hand corner of stone
    checked_1 = first_stone(key, original_stone) 
    
    # top right hand corner of stone
    checked_2 = move_stone_right(key, original_stone)
    
    # bottom left hand corner of stone
    checked_3 = move_stone_down(key, original_stone)
    
    # bottom right hand corner of stone
    checked_4 = move_stone_down_and_right(key, original_stone)
    
    if checked_0 is None:
        if checked_1 is None:
            if checked_2 is None:
                if checked_3 is None:
                    if checked_4 is None:
                        return None  # key can't fit within stone
                    # if the key can fit:
                    else:
                        return checked_4
                else:
                    return checked_3
            else:
                return checked_2
        else:
            return checked_1
    else:
        return checked_0                



