'''
Code Author: Balaji Adithya Venkataramana

Paper: EbDa - A New Theory on Design and Verification of
               Deadlock-free Interconnection Networks
Paper Authors: Masoumeh Ebrahimi & Masoud Daneshtalab

Description: 
        1. This code provides the partitions for fully adaptive routing based on
            - number of dimensions --> 2D or 3D.
            - number of VCs per dimension.
        2. EbDa is applicable for
            - 2D/3D Mesh topologies
            - k-ary n-cube topologies
            - Irregular mesh-type topologies (such as 2.5D interposer topologies)
'''

import itertools

def reorder(set1, set2, set3):
    temp_sets = [set1, set2, set3]
    shift = 0
    for i in temp_sets:
        if i is None:
            shift = shift + 1
        elif i is not None:
            break
    
    print(f"shift = {shift}")
    
    ret_sets = temp_sets[shift:] + temp_sets[:shift]
    return ret_sets


def generate_partition(dirs_per_part=2, set1=None, set2=None, set3=None):
    partition = []
    numSets = 0

    if(set1 == None):
        return None
    if (set2 == None):
        numSets = 1
    elif (set3 == None):
        numSets = 2
    else:
        numSets = 3

    print(set1, set2, set3)
    print(f"From within the function - numLoops = {numSets}")

    if(numSets == 1):
        x = [i for j,i in enumerate(set1) if j<dirs_per_part]
        count1 = len(x)
        partition = x
        # print(x, count1)
        # print(partition)
        set1 = None if (count1 == len(set1)) else set1[count1:]
    
    elif(numSets == 2):
        x = [i for j,i in enumerate(set1) if j<2]
        count1 = len(x)
        y = [i for j,i in enumerate(set2) if j<dirs_per_part-count1]
        count2 = len(y)
        partition = x+y
        # print(x, y, count1, count2)
        # print(partition)
        set1 = None if (count1 == len(set1)) else set1[count1:]
        set2 = None if (count2 == len(set2)) else set2[count2:]
    
    else:
        x = [i for j,i in enumerate(set1) if j<2]
        count1 = len(x)
        y = [i for j,i in enumerate(set2) if j<dirs_per_part-count1-1]              # an extra -1 bcoz there's atleast one available in z.
        count2 = len(y)
        z = [i for j,i in enumerate(set3) if j<dirs_per_part-(count1 + count2)]
        count3 = len(z)
        partition = x+y+z
        # print(x, y, z, count1, count2, count3)
        # print(partition)
        set1 = None if (count1 == len(set1)) else set1[count1:]
        set2 = None if (count2 == len(set2)) else set2[count2:]
        set3 = None if (count3 == len(set3)) else set3[count3:]

    reordered_sets = reorder(set1, set2, set3)
    print(f"The reordered sets are {reordered_sets}")
    gen = generate_partition(dirs_per_part, reordered_sets[0], reordered_sets[1], reordered_sets[2])
    if gen is not None:
        len1 = len(partition)
        len2 = len(gen)
        if len1 + len2 > dirs_per_part:
            ret_partitions = [partition] + gen
        else:
            ret_partitions = [partition + i for i in gen]
    else:
        ret_partitions = [partition]
    
    print("-----------------------------")
    print(f"Returning the value {ret_partitions}")
    return ret_partitions


# ---------------

if __name__ == "__main__":
    dims = 3
    VCs = {
        'X': 3,
        'Y': 3,
        'Z': 3
        }

    num_partitions = 1<<(dims-1)
    dirs_per_part = dims+1
    partitions = []

    sets = {'X':[], 'Y':[], 'Z':[]}

    for key, channels in VCs.items():
        for i in range(channels):
            if key == 'X':
                sets['X'].append(f"E{i}")
                sets['X'].append(f"W{i}")
            
            if key == 'Y':
                sets['Y'].append(f"N{i}")
                sets['Y'].append(f"S{i}")
            
            if key == 'Z':
                sets['Z'].append(f"U{i}")
                sets['Z'].append(f"D{i}")

    # Hold the values of different iterations
    computed_channel_combo = set()
    computed_dim_combo = set()

    # For all unique combinations of X,Y,Z sets
    for perm in itertools.permutations(sets.keys(), 3):
        unique_channel_combo = tuple()
        unique_dim_combo = tuple()
        x = len(sets[perm[0]])
        y = len(sets[perm[1]])
        z = len(sets[perm[2]])

        print(x,y,z)
        print(perm[0], perm[1], perm[2])

        if(x > 0):
            unique_channel_combo = unique_channel_combo + (x,)
            unique_dim_combo = unique_dim_combo + (perm[0],)
        if(y > 0):
            unique_channel_combo = unique_channel_combo + (y,)
            unique_dim_combo = unique_dim_combo + (perm[1],)
        if(z > 0):
            unique_channel_combo = unique_channel_combo + (z,)
            unique_dim_combo = unique_dim_combo + (perm[2],)
        
        if(unique_channel_combo in computed_channel_combo 
        and unique_dim_combo in computed_dim_combo):
            continue
        else:
            computed_channel_combo.add(unique_channel_combo)
            computed_dim_combo.add(unique_dim_combo)
            print(unique_channel_combo)
            print(unique_dim_combo)
        
        assert(len(unique_channel_combo) == len(unique_dim_combo))
        num_loops = len(unique_dim_combo)

        # Determine number of loops based on non-zero channels in dimensions
        if(num_loops == 1):
            set1 = sets[unique_dim_combo[0]]
            num_channels1 = len(set1)

            for i in range(num_channels1):
                # print(set1)
                partitions = generate_partition(dirs_per_part, set1)
                print(f"Generated partitions = {partitions} \n")

                set1 = set1[1:] + set1[:1]
        
        elif(num_loops == 2):
            set1 = sets[unique_dim_combo[0]]
            num_channels1 = len(set1)

            set2 = sets[unique_dim_combo[1]]
            num_channels2 = len(set2)

            for i in range(num_channels1):
                for j in range(num_channels2):
                    # print(set1, set2)
                    partitions = generate_partition(dirs_per_part, set1, set2)
                    print(f"Generated partitions = {partitions} \n")

                    set2 = set2[1:] + set2[:1]
                set1 = set1[1:] + set1[:1]
        
        elif(num_loops == 3):
            set1 = sets[unique_dim_combo[0]]
            num_channels1 = len(set1)

            set2 = sets[unique_dim_combo[1]]
            num_channels2 = len(set2)

            set3 = sets[unique_dim_combo[2]]
            num_channels3 = len(set3)

            for i in range(num_channels1):
                for j in range(num_channels2):
                    for k in range(num_channels3):
                        # print(set1, set2, set3)
                        partitions = generate_partition(dirs_per_part, set1, set2, set3)
                        print(f"Generated partitions = {partitions} \n")

                        set3 = set3[1:] + set3[:1]
                    set2 = set2[1:] + set2[:1]
                set1 = set1[1:] + set1[:1]