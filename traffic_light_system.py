# List of Functions
# load_road_network(filename)
# to_tuple(a_dict)

def to_tuple(a_dict):
    '''Converts strings in list of lists into tuples. Takes input as 
    dictionary and works with the values which are in the form 
    `[['(a,b);(b,a)'], ['(c,d);(d,c)']]` where a,b,c,d are positive
    integers and returns the dictionary with values in the form
    `[[(a, b), (b, a)], [(c, d), (d, c)]]` '''
    new_dict = {}
    for elem in a_dict.values():
        # First: find the key for the value that we're working with right now
        for elem1, elem2 in a_dict.items():
            if elem2 == elem:
                the_key = elem1
        final_value = []
        # Loop every sublist
        for j in elem:
            process1 = []
            # Loop every string in sublist
            for k in j:
                if len(k) > 6:
                    k = k.split(';')
                    # Loop every tuple in sublist
                    for q in k:
                        q = eval(q)
                        process1.append(q)  # Append tuples to new sublist
                else:
                    process1.append(eval(k))  
            final_value.append(process1)  # Append sublist to new big list
            continue
        new_dict[the_key] = final_value  # Create new key-value pair
    return new_dict
        


def load_road_network(filename):
    '''Takes a text file with roads, intersections, traffic signals
    in (source,destination) pairs and timestamps.
    Returns 2 dictionaries - 1 - dictionary of intersections and their
    corresponding traffic signals. - 2 - dictionary of roads with
    corresponding time stamps'''
    intersections = {}
    roads = {}
    intersection_pts = []
    empty_lines = []
    file = open(filename)
    content = file.readlines()
    
    # Find where file starts listing traffic signals after intersections
    # Also find where empty lines are
    for line in range(len(content) - 1):
        if "#I" in content[line]:
            intersection_pts.append(line) 
        elif content[line].isspace():
            if (empty_lines and (empty_lines[-1] + 1 == line)) or \
                (empty_lines and ('#I' in content[line - 1])):
                # continue the loop if there are 2 consecutive empty lines
                continue
            # ('#I' in content[line - 1]) and 
            elif content[line].isspace() and (';' in content[line + 1]):
                continue
            else:
                empty_lines.append(content.index(content[line], 
                                    intersection_pts[-1] + 1))
        else:
            pass
    # Create dictionary with the intersection ID: traffic signals
    for num in range(len(intersection_pts)):
        intersections[int(content[intersection_pts[num]][-2])] = \
                                [[part.strip()] for part in 
                                content[intersection_pts[num] + 1:
                                empty_lines[num]]]            
        # Next line is to edit the formating of the values in `intersections`
        final_intersections = to_tuple(intersections)

    # Next create the dictionary of roads
    start = 0
    for line in content:
        if '#R' in line:
            start = content.index(line)
            for road in content[start + 1:]:
                closing_bracket = road.index(')')
                path = road[:closing_bracket + 1]
                a = eval(path)
                roads[a] = int(road[road.index(')') + 2])


    return final_intersections, roads



# DO NOT DELETE/EDIT THIS LINE OF CODE, AS IT IS USED TO PROVIDE ACCESS TO
# A WORKING IMPLEMENTATION OF THE FUNCTION FROM Q1
from hidden import load_road_network

# List of functions:
# get_timestep(path, intersections_dict)
# check_timestep(intersections_on_road, path, paths_and_times,
#                current_timestep, traffic_light, current_intersection, 
#                item)
# path_cost(path, intersections, road_times)

def get_timestep(path, intersections_dict):
    '''Find the timestep at which the car arrives at an 
    intersection. Takes 2 inputs: 1- The path the car is traversing 
    and 2- Dictionary that has all intersections and the traffic
    signals at each timestep.'''

    timestep = 0
    # new_dict allows us to easily loop through the dictionary
    new_dict = {y: x for x, y in intersections_dict.items()}  
    for i in new_dict:
        if new_dict[i] == path:
            break
        else:
            timestep = i
    return timestep


def check_timestep(intersections_on_road, path, paths_and_times,
                   current_timestep, traffic_light, current_intersection, 
                   item):
    '''Check if the car can pass at the time that the intersection
    allows it to, either returning a timestep, or a 'continue' to
    get the function to continue, or None. Takes multiple inputs as follows
    intersections_on_road: dictionary, intersection ID and timesteps
    path: tuple, current path the car is traversing
    paths_and_times: dictionary, all the paths the car will traverse and
                    corresponding timesteps.
    traffic_light: int, whether the traffic light allows car to pass at 
                    specific timestep
    current_intersection: int, the current intersection the car is trying 
                    to pass
    item, the element that we're up to in the paths_and_times dict
    '''
    for j in intersections_on_road[current_intersection]:
        if path in j:
            timestep_in_question = traffic_light[current_timestep]
            if path in timestep_in_question:
                if item == list(paths_and_times.keys())[-1]:
                    # Checking if this is the last path in the list, e.g
                    # [2,0,4,6] the last path is [4,6] from 4 to 6
                    # to see if there are more intersections to check
                    last_element = list(paths_and_times.values())[-1]
                    return last_element
                else:
                    return 'continue'
            else:
                return None
    
                
def path_cost(path, intersections, road_times):
    '''Finds whether a car can traverse a path without stopping. If 
    possible, then the function will calculate the number of timesteps
    required for the car to traverse the path. Takes 3 inputs as follows:
    1- path: list, refers to the path (from location through intersections to 
       another location)
    2- intersections: dict, has intersection ID (key, int) and traffic 
       movements at different timesteps (value, list of multiple sublists)
    3- road_times: dict, number of timesteps taken to cross from one node to
       another
    '''

    # Next line, all the paths the car will take throughout its motion
    different_paths = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    intersection_points = path[1:-1]
    path_and_time = {}
    last_elem = ''
    # Calculate the timesteps for each part of the path
    for elem in different_paths:
        if not path_and_time:
            path_and_time[elem] = road_times[elem]
        else:
            path_and_time[elem] = path_and_time[last_elem] + road_times[elem]
        last_elem = elem

    for item in path_and_time:
        # Check every path, and whether the ones that start at an intersection
        # can be crossed without stopping. This loop ensures we check every
        # path. e.g the paths (2,0), (0,4), (4,6) for [2,0,4,6]
        if item[0] in intersection_points:
            timestep = get_timestep(item, path_and_time)
            key = item[0]
            traffic_light_at_timestep = [i for i in intersections[key] * 10]
            if item != path[-1]:
                cur_path = (path[path.index(item[0]) - 1], 
                            path[path.index(item[0]) + 1])
                result = check_timestep(intersections, cur_path, path_and_time, 
                                   timestep, traffic_light_at_timestep, key, 
                                   item)
                
                if result is None:
                    return None
                elif result == 'continue':
                    # if the path that we checked is not the last 
                    # in path_and_time
                    continue
                else:
                    return result
                
            else:
                cur_path = item
                result = check_timestep(intersections, cur_path, path_and_time, 
                                   timestep, traffic_light_at_timestep, key, 
                                   item)
                if result is None:
                    return None
                elif result == 'continue':
                    continue
                else:
                    return result
        

    return None

# DO NOT DELETE/EDIT THIS LINE OF CODE, AS IT IS USED TO PROVIDE ACCESS TO
# WORKING IMPLEMENTATIONS OF THE FUNCTIONS FROM Q1 & 2
from hidden import load_road_network, path_cost

def intersection_step(intersections, road_times, intersection_id, 
                      cars_at_intersection, timestep):
    '''Find which cars can cross the intersection at a specific timestep.
    Takes 5 parameters as input as follows:
    1- intersections: dict, id:traffic signals (from Q1)
    2- road_times: dict, source-destination_pairs: timestep (from Q1)
    3- intersection_id: int, the intersection we're trying to cross.
    4- cars_at_intersection: list, contains tuples in format:
                    (car_id, path, arrival_time)
    5- timestep: int, the timestep that we are checking the intersection at
    '''
    # Process
    # 1- Group cars using dict.
    # 2- Create list with only the values from dict (from 1)
    # 3- Sort cars in list based on timestep and ID
    # 4- Check which cars are allowed to pass the intersection
    #    at this timestep
    # 5- Check which part of the path the car is crossing now
    # 6- Create tuples of cars_at_intersection and path (from 5)
    # 7- Create final list of cars that can cross now.

    car_classifications = {}

    # Group cars together based on the route they're taking.
    # This helps check which car arrived first and/or which
    # car has the lower ID.
    for x, y, z in cars_at_intersection:
        if str(y) in car_classifications:
            car_classifications[str(y)].append((x, y, z))
        else:
            car_classifications[str(y)] = [(x, y, z)]


    # Convert to list to allow easier access to elements.
    groups_of_cars = [i for i in car_classifications.values()]
    
    # Sorting cars to allow ones with smaller timestep and/or lower ID
    # to pass the intersection first.
    sorted_cars = [sorted(car, key=lambda x: x[2]) for car in groups_of_cars]

    # Check which paths are open for cars to proceed.
    traffic_light_at_timestep = [i for i in intersections[intersection_id] 
                                 * 10][timestep]

    # Find which part of the path we are on now (e.g. path [2,0,4,6]) 
    different_paths = [i[1] for i in cars_at_intersection]

    # Check which part of the path the car is trying to traverse.
    # This allows us to check whether the intersection at
    # the specified timestep allows for this traffic movement
    # Example: path [2,0,4,6], intersection 0: we try to cross (2,4)
    paths = [(i[j - 1], i[j + 1]) for i in different_paths for j in 
             range(len(i)) if i[j] == intersection_id]

    # Create tuple of:
    # 1- car, tuple (car_id, path, arrival_time), and
    # 2- current path.
    # This tuple sits in the place of the car tuple (which is in the format
    #     (car_id, path, arrival_time) )
    for elem in range(len(sorted_cars)):
        sorted_cars[elem] = (sorted_cars[elem], paths[elem])

    # Create a final list of cars that can cross at 
    # the specified timestep.
    # Recall: we have a list of tuples in the format
    #         `[ ( [ (car tuple), (car tuple) ], (path) ), ([], ()) ]`
    # Recall: car tuples are in the format 
    #         `( (car_id, path, arrival_time), (part of path) )`
    cars_that_pass = [car[0][0][0] for car in sorted_cars if car[1] in 
                      traffic_light_at_timestep]
    
    return cars_that_pass

# DO NOT DELETE/EDIT THIS LINE OF CODE, AS IT IS USED TO PROVIDE ACCESS TO
# WORKING IMPLEMENTATIONS OF THE FUNCTIONS FROM Q1, 2 & 3
from hidden import load_road_network, path_cost, intersection_step

def next_action(intersections, road_times, the_process, num):
    '''Create a model for the movements of cars at all different
    timesteps. Takes 4 input variables:
    1- intersections dictionary
    2- road_times dictionary
    3- the_process: list of all cars that can cross without stopping
    4- num: int, specifies the number of cars, 0 for 1 and 1 for more
    '''

    results = []
    for car in the_process:
        results.append(path_cost(car[0][1], intersections, road_times))

    model_1 = []
    for car in the_process:
        model_1.append((car[0][-1] + num + 1, car[0][0], 
                            car[-1][1][0], car[-1][1][1]))
    model_1 = sorted(model_1)

    model_2 = []
    for car in the_process:
        model_2.append((car[0][-1] + num + results[0], car[0][0], 
                                car[0][1][-1]))
    model_2 = sorted(model_2)

    return model_1, model_2



def simulate(intersections, road_times, cars_to_add):
    '''Simulation of an entire road network including
    cars that are entering, leaving and/or traversing  
    the network. Takes 3 inputs:
    1- intersections: dict, ID: traffic signals
    2- road_times: dict, road: timestep
    3- cars_to_add: list, cars traversing the network,
        in tuples (car_id, path, arrival_time)
    This function returns the simulation at each timestep:
    - which cars are moving (driving)
    - which cars stop at traffic light (waiting)
    - which cars arrived at their destination (arrive)
    '''
    
    # Create dictionary for car_id and the path the car will take
    car_and_path = {}
    for car in cars_to_add:
        path = car[1]
        car_and_path[(car[2], car[0])] = [(path[i], path[i + 1]) for 
                                          i in range(len(path) - 1)]
    # Check which cars can cross without stopping
    process = []
    for car in cars_to_add:
        result = path_cost(car[1], intersections, road_times)
        if result is not None:
            process.append((car, [(car[1][i], car[1][i + 1]) for i in 
                                  range(len(car[1]) - 1)]))
    
    results = []
    for car in process:
        results.append(path_cost(car[0][1], intersections, road_times))

    # First model, refers to the first timestep in the simulation
    first_model = []
    for car in process:
        first_model.append((car[0][-1], car[0][0], car[-1][0][0], 
                            car[-1][0][1]))
    first_model = sorted(first_model)

    # Cars that have a 3-point path are least likely to wait.
    if len(cars_to_add) > 1:
        second_model = []
        for car in process:
            second_model.append((car[0][-1] + 1, car[0][0], car[0][1][1]))
        second_model = sorted(second_model)

        third_model, fourth_model = next_action(intersections, road_times, 
                                                process, 1)

        process_model = [['drive' + str(i) for i in first_model], 
                         ['wait' + str(i) for i in second_model], 
                         ['drive' + str(i) for i in third_model], 
                         ['arrive' + str(i) for i in fourth_model]]

        final_model = [j for i in process_model for j in i]

        return final_model
    else:
        third_model, fourth_model = next_action(intersections, road_times, 
                                                process, 0)

        process_model = [['drive' + str(i) for i in first_model],
                         ['drive' + str(i) for i in third_model], 
                         ['arrive' + str(i) for i in fourth_model]]

        final_model = [j for i in process_model for j in i]
        return final_model


