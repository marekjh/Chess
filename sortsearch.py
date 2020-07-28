def merge_sort(unsorted_list):
    sorter = []
    for item in unsorted_list:
        sorter.append([item])
    
    while len(sorter) > 1:
        count = 0
        
        for i in range(len(sorter) // 2):
            list_1 = sorter[i]
            list_2 = sorter[i + 1]
            combined_list = []
            
            while len(list_1) > 0 and len(list_2) > 0:
                if list_1[0] <= list_2[0]:
                    combined_list.append(list_1[0])
                    del list_1[0]
                else:
                    combined_list.append(list_2[0])
                    del list_2[0]
            
            if len(list_1) == 0:
                del sorter[i]
                for item in list_2:
                    combined_list.append(item)
                del sorter[i]
            else:
                del sorter[i + 1]
                for item in list_1:
                    combined_list.append(item)
                del sorter[i]
            
            sorter.insert(count, combined_list)
            count += 1
    
    return sorter[0]


def binary_search(sorted_list, search_item, pos_tracker): #Function must be called with pos_tracker set to a value equivalent to mid_index's initial value within the function
    mid_index = len(sorted_list) // 2
    front_half = sorted_list[:mid_index]
    back_half = sorted_list[mid_index + 1:]
    
    if sorted_list[mid_index] == search_item:
        return pos_tracker
    
    if sorted_list[mid_index] > search_item:
        index_offset = len(front_half) // 2
        if len(front_half) % 2 == 1:
            index_offset += 1
        pos_tracker -= index_offset
        return binary_search(front_half, search_item, pos_tracker)
    else:
        index_offset = (len(back_half) // 2) + 1
        pos_tracker += index_offset
        return binary_search(back_half, search_item, pos_tracker)        
