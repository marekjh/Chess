def triangle_constructor(input_file):
    f = open(input_file, "r")
    triangle_list = []
    
    for line in f:
        line = line.strip()
        row = line.split()
        row = [int(x) for x in row]
        triangle_list.append(row)
    f.close()
    
    return triangle_list

def max_sum(triangle):
    if len(triangle) == 1:
        return triangle[0][0]

    check_row = triangle[-1]
    current_row = triangle[-2]
    replacement_row = []
    
    for i in range(len(current_row)):
        left_path = check_row[i]
        right_path = check_row[i + 1]
        best_path = current_row[i] + max([left_path, right_path])
        replacement_row.append(best_path)
    
    del triangle[-1]
    triangle[-1] = replacement_row
    
    return max_sum(triangle)
            
input_triangle = triangle_constructor("nums_in_triangle2.txt")
print(max_sum(input_triangle))
