# Code written in python three
# Import the modules that we are to use in this program
import sys
import re
import os


## Program that ...
"""
* Takes as input a series of commands from standard input (stdin) that describe streets.
* Uses that input to construct a particular kind of undirected graph and prints it to standard output (stdout).
* Write your code in Python (version 3).
"""

# vertex and line for show
vertex_list = []
vertex_dict = {}
edge_list = []
edge_dict = {}
intersect_dict = {}

# to remove street with endpoints and intersections
street_dict = {}


def pp(x):
    """Returns a pretty-print string representation of a number.
       A float number is represented by an integer, if it is whole,
       and up to two decimal places if it isn't
    """
    if isinstance(x, float):
        if x.is_integer():
            return str(int(x))
        else:
            return "{0:.2f}".format(x)
    return str(x)


class point(object):
    """A point in a two dimensional space"""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    def __repr__(self):
        return '(' + pp(self.x) + ', ' + pp(self.y) + ')'


class line(object):
    """A line between two points"""
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
    def __repr__(self):
        return '[' + str(self.src) + '-->' + str(self.dst) + ']'


def intersect(l1, l2):
    """Returns a point at which two lines intersect"""
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y
    if POL([x1, y1], [x3, y3], [x4, y4]):
        return point(x1, y1)
    elif POL([x2, y2], [x3, y3], [x4, y4]):
        return point(x2, y2)
    elif POL([x3, y3], [x1, y1], [x2, y2]):
        return point(x3, y3)
    elif POL([x4, y4], [x1, y1], [x2, y2]):
        return point(x4, y4)
    xnum = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))
    xden = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    if xden == 0:
        return
    else:
        xcoor = xnum / xden
    ynum = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    yden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if yden == 0:
        return
    else:
        ycoor = ynum / yden
    return point(xcoor, ycoor)


def POL(A, B, I):
    if A[0]==B[0]:
        if I[0]==A[0]:
            return 1
        else:
            return 0
    if A[1]==B[1]:
        if I[1] == A[1]:
            return 1
        else:
            return 0
    AI=(I[0]-A[0],I[1]-A[1])
    AB=(B[0]-A[0],B[1]-A[1])
    VAL=(AI[0]*AB[1])-(AI[1]*AB[0])
    if round(VAL, 2) == 0:
        return 1
    else:
        return 0


"""
>l1 = line(point(1, 4), point(5, 8))
>l2 = line(point(5, 6), point(3, 8))
>l3 = line(point(1, 5), point(5, 8))
>print('Intersection of', l1, 'with', l2, 'is', intersect(l1, l2))
>print('Intersection of', l2, 'with', l3, 'is', intersect(l2, l3))
    
Intersection of [(1, 4)-->(5, 8)] with [(5, 6)-->(3, 8)] is (4, 7)
Intersection of [(5, 6)-->(3, 8)] with [(1, 5)-->(5, 8)] is (3.86, 7.14)
"""

## Commands the program should process
"""
* `add` is used to add a street. It is specified as: `add "Street Name" (x_1, y_1) (x_2, y_2) ... (x_n, y_n)`. Each ($x_i$, $y_i$) is a GPS coordinate. We interpret the coordinates as a poly-line segment. That is, we draw a line segment from ($x_i$, $y_i$) to ($x_{i+1}$, $y_{i+1}$). You are allowed to assume that
each $x_i$ and $y_i$ is an integer. (Note, however, that the coordinates of an intersection may not be integers.)
* `mod` is used to modify the specification of a street. Its format is the same as for add. It is a new specification for a street you've specified before.
* `rm` is used to remove a street. It is specified as `rm "Street Name""`.
* `gg` causes the program to output the corresponding graph.
"""


def show_vertex():
    print("V = {")
    for one_key in vertex_dict:
        print(f"  {vertex_dict[one_key]}:  {one_key}")
    print("}")
    return


def show_edge():
    if not edge_dict:
        print("E = {")
        print("}")
        return
    current_edge_label = []
    for one_center in edge_dict:
        current_edge_label.append(one_center)
        for one_point in edge_dict[one_center]:
            current_edge_label.append(one_point)
    max_edge_label = max(current_edge_label)
    min_edge_label = min(current_edge_label)
    live_edge_label = []
    for one_key in vertex_dict:
        live_edge_label.append(vertex_dict[one_key])
    lost_edge_label = []
    for i in range(min_edge_label, max_edge_label+1):
        if i not in live_edge_label:
            lost_edge_label.append(i)

    for one_center in edge_dict:
        if one_center in lost_edge_label:
            del edge_dict[one_center]
        else:
            should_remove = []
            for one_point in edge_dict[one_center]:
                if one_point in lost_edge_label:
                    should_remove.append(one_point)
            for one_2remove in should_remove:
                edge_dict[one_center].remove(one_2remove)

    # Edges between intersect points
    edge_between_intersect_dict = {}
    intersect_dict_key_list = []
    for cell in intersect_dict:
        intersect_dict_key_list.append(cell)
    for i in range(0, len(intersect_dict_key_list)):
        for j in range(i+1, len(intersect_dict_key_list)):
            intersect_pt1 = [intersect_dict[intersect_dict_key_list[i]], list(intersect_dict_key_list[i])]
            intersect_pt2 = [intersect_dict[intersect_dict_key_list[j]], list(intersect_dict_key_list[j])]
            for one_street in street_dict:
                street_pt_set = street_dict[one_street]
                for m in range(0, len(street_pt_set)):
                    pt3 = street_pt_set[m].split(',')
                    pt3[0] = float(pt3[0])
                    pt3[1] = float(pt3[1])
                    if POL(intersect_pt1[1], intersect_pt2[1], pt3):
                        if intersect_pt1[0] <= intersect_pt2[0]:
                            if intersect_pt1[0] in edge_between_intersect_dict:
                                edge_between_intersect_dict[intersect_pt1[0]].append(intersect_pt2[0])
                            else:
                                edge_between_intersect_dict[intersect_pt1[0]] = [intersect_pt2[0]]
                        else:
                            if intersect_pt2[0] in edge_between_intersect_dict:
                                edge_between_intersect_dict[intersect_pt2[0]].append(intersect_pt1[0])
                            else:
                                edge_between_intersect_dict[intersect_pt2[0]] = [intersect_pt1[0]]
    for one_key in edge_between_intersect_dict:
        edge_between_intersect_dict[one_key] = list(set(edge_between_intersect_dict[one_key]))

    print_count = 0
    for one_center in edge_dict:
        for one_point in edge_dict[one_center]:
            print_count = print_count + 1
    for one_center in edge_between_intersect_dict:
        for one_point in edge_between_intersect_dict[one_center]:
            print_count = print_count + 1

    print_position = 0
    print("E = {")
    for one_center in edge_dict:
        for one_point in edge_dict[one_center]:
            print_position = print_position + 1
            if print_position == print_count:
                print(f"  <{one_center},{one_point}>")
            else:
                print(f"  <{one_center},{one_point}>,")
    for one_center in edge_between_intersect_dict:
        for one_point in edge_between_intersect_dict[one_center]:
            print_position = print_position + 1
            if print_position == print_count:
                print(f"  <{one_center},{one_point}>")
            else:
                print(f"  <{one_center},{one_point}>,")
    print("}")
    return


def command_add(input_command):
    format_coordinate = re.compile(r'[(](.*?)[)]')
    format_street = re.compile('"(.*?)"')


    street_num = re.findall(format_street, input_command)
    street = "".join(re.findall(format_street, input_command))
    coordinate = re.findall(format_coordinate, input_command)
    space_check = input_command.split("(", 1)
    """
    > add "weber" (1,2) (3,4) (5,6)
    print(street_num) ['weber']
    print(street) weber
    print(coordinate) ['1,2', '3,4', '5,6']
    print(space_check) ['add "weber" ', '1,2) (3,4) (5,6)\n']
    """
    if list(street)[0] == " " or list(street)[-1] == ' ':
        sys.stderr.write("Error: No leading and trailing white spaces allowed in street names.\n")
        return
    elif not space_check[0][-1] == " ":
        sys.stderr.write("Error: Wrong format.\n")
        return
    elif len(street_num) != 1:
        sys.stderr.write("Error: One street to add once.\n")
        return
    elif not len(street):
        sys.stderr.write("Error: Street name required.\n")
        return
    # elif '-' in ''.join([str(i) for i in coordinate]) or '+' in ''.join([str(i) for i in coordinate]):
        # sys.stderr.write("Error: Symbols not allowed for numbers.\n")
        # return
    elif len(coordinate) < 2:
        sys.stderr.write("Error: Two coordinators needed for a street.\n")
        return
    elif street.lower() in street_dict:
        sys.stderr.write("Error: Street information already added.\n")
        return
    # Store information - "weber" : ['1,2', '3,4', '5,6']
    else:
        # print(street)
        # print(street.lower())
        # print(coordinate)
        street_dict[street.lower()] = coordinate
        # print(street_dict)
    return


def command_mod(input_command):
    format_coordinate = re.compile(r'[(](.*?)[)]')
    format_street = re.compile('"(.*?)"')

    street_num = re.findall(format_street, input_command)
    street = "".join(re.findall(format_street, input_command))
    coordinate = re.findall(format_coordinate, input_command)
    space_check = input_command.split("(", 1)
    """
    > add "weber" (1,2) (3,4) (5,6)
    print(street_num) ['weber']
    print(street) weber
    print(coordinate) ['1,2', '3,4', '5,6']
    print(space_check) ['add "weber" ', '1,2) (3,4) (5,6)\n']
    """
    if list(street)[0] == " " or list(street)[-1] == ' ':
        sys.stderr.write("Error: No leading and trailing white spaces allowed in street names.\n")
        return
    elif not space_check[0][-1] == " ":
        sys.stderr.write("Error: Wrong format.\n")
        return
    elif len(street_num) != 1:
        sys.stderr.write("Error: One street to add once.\n")
        return
    elif not len(street):
        sys.stderr.write("Error: Street name required.\n")
        return
    # elif '-' in ''.join([str(i) for i in coordinate]) or '+' in ''.join([str(i) for i in coordinate]):
        # return
    elif len(coordinate) < 2:
        sys.stderr.write("Error: Two coordinators needed for a street.\n")
        return
    elif not street_dict.__contains__(street.lower()):
        sys.stderr.write("Error: Street to modify not existed.\n")
        return
    else:
        # Store information - "weber" : ['1,2', '3,4', '5,6']
        # print(street)
        # print(street.lower())
        # print(coordinate)
        street_dict[street.lower()] = coordinate
        # print(street_dict)
    return


def command_rm(input_command):
    stress_pattern = '"(.*)"'
    street = "".join(re.findall(stress_pattern, input_command))
    if list(street)[0] == " " or list(street)[-1] == ' ':
        sys.stderr.write("Error: No leading and trailing white spaces allowed in street names\n")
        return
    elif street.lower() in street_dict:
        del street_dict[street.lower()]
        # streetnamelist.remove(street.lower())
    else:
        sys.stderr.write("Error: The street entered does not exist\n")
        return
    return


def command_gg():
    street_dict_key_list = []
    for keys in street_dict:
        street_dict_key_list.append(keys)
    vertex_dict_index = 0
    if len(street_dict_key_list) >= 2:
        for i in range(0, len(street_dict_key_list) - 1):
            one_street_i = street_dict_key_list[i]
            # print('street A: ', one_street_i)
            points_i = street_dict[one_street_i]
            for j in range(i + 1, len(street_dict_key_list)):
                one_street_j = street_dict_key_list[j]
                # print('street B: ', one_street_j)
                points_j = street_dict[one_street_j]
                for ii in range(0, len(points_i) - 1):
                    # print('i:', points_i[i])
                    num1 = points_i[ii].split(",")[0]
                    num2 = points_i[ii].split(",")[1]
                    # print('j:', points_i[i+1])
                    num3 = points_i[ii + 1].split(",")[0]
                    num4 = points_i[ii + 1].split(",")[1]
                    pt_11 = point(num1, num2)
                    pt_12 = point(num3, num4)
                    l1 = line(pt_11, pt_12)
                    # print("l1: ", l1)
                    for jj in range(0, len(points_j) - 1):
                        # print('i:', points_i[i])
                        num5 = points_j[jj].split(",")[0]
                        num6 = points_j[jj].split(",")[1]
                        # print('j:', points_i[i+1])
                        num7 = points_j[jj + 1].split(",")[0]
                        num8 = points_j[jj + 1].split(",")[1]
                        pt_21 = point(num5, num6)
                        pt_22 = point(num7, num8)
                        l2 = line(pt_21, pt_22)
                        # print("l2: ", l2)
                        if intersect(l1, l2):
                            intersect_pt = intersect(l1, l2)
                            condition_1 = float(max(min(num1, num3), min(num5, num7)))
                            condition_2 = float(min(max(num1, num3), max(num5, num7)))
                            condition_3 = float(max(min(num2, num4), min(num6, num8)))
                            condition_4 = float(min(max(num2, num4), max(num6, num8)))
                            if condition_1 <= float(pp(intersect_pt.x)) <= condition_2:
                                if condition_3 <= float(pp(intersect_pt.y)) <= condition_4:
                                    # print(intersect_pt)
                                    vertex_dict_index = vertex_dict_index + 1
                                    vertex_dict[(float(pp(intersect_pt.x)), float(pp(intersect_pt.y)))] = vertex_dict_index
                                    intersect_pt_index = vertex_dict_index
                                    intersect_dict[(float(pp(intersect_pt.x)), float(pp(intersect_pt.y)))] = intersect_pt_index
                                    edge_dict[intersect_pt_index] = []

                                    vertex_dict_index = vertex_dict_index + 1
                                    vertex_dict[(float(num1), float(num2))] = vertex_dict_index
                                    edge_dict[intersect_pt_index].append(vertex_dict_index)

                                    vertex_dict_index = vertex_dict_index + 1
                                    vertex_dict[(float(num3), float(num4))] = vertex_dict_index
                                    edge_dict[intersect_pt_index].append(vertex_dict_index)

                                    vertex_dict_index = vertex_dict_index + 1
                                    vertex_dict[(float(num5), float(num6))] = vertex_dict_index
                                    edge_dict[intersect_pt_index].append(vertex_dict_index)

                                    vertex_dict_index = vertex_dict_index + 1
                                    vertex_dict[(float(num7), float(num8))] = vertex_dict_index
                                    edge_dict[intersect_pt_index].append(vertex_dict_index)
    show_vertex()
    show_edge()
    return


## Error Handling
"""Error should be output to standard error. You can use exceptions in
your code to catch errors.

The above example is that of a "perfect" user - someone that did not make any mistakes with specifying the input. You should account for errors in the input. If a line in the input is erroneous, you should immediately output an error message. The format of the message is to be the string "Error:" followed by a brief descriptive message about the error. For example: `Error: 'mod' or 'rm' specified for a street that does not exist.`

Your program should recover from the error as well. That is, your program should reject the errorneous line, but continue to accept input. Your program should not crash because of an error. Any erroneous input we try will be of a relatively benign nature that mimics honest mistakes a user makes. We will not try malicious input, such as unduly long lines or weird control characters.
"""

## The Output Graph
"""There is a vertex corresponding to: (a) each intersection, and, (b) the end-point of a line segment of a street that intersects with another street. An example of (a) from above is Vertex 3. An example of (b) is Vertex 1. The identity of a vertex can be any string of letters or integers (but no special
characters). For example, v1xyz is acceptable as the identity of a vertex, but not v1 !!#xyz. (The space is unacceptable, as are '!' and '#'.

There is an edge between two vertices if: (a) at least one of them is an intersection, (b) both lie on the same street, and, (c) one is reachable from the other without traversing another vertex. An example from above is the edge h1; 3i, which connects the end-point of a line segment
"""


def main():
    # YOUR MAIN CODE GOES HERE
    format_add = re.compile(r'^add\s+\"[A-Za-z\s]+\"\s+(\((\-|\+)?\d{1,},(\-|\+)?\d{1,}\)\s*){2,}\s*$')
    format_mod = re.compile(r'^mod\s+\"[A-Za-z\s]+\"\s+(\((\-|\+)?\d{1,},(\-|\+)?\d{1,}\)\s*){2,}\s*$')
    format_rm = re.compile(r'^rm\s+\"[A-Za-z\s]+\"\s*$')
    format_gg = re.compile(r'^gg\s*$')

    while True:
        input_command = sys.stdin.readline()
        if input_command == "":
            break

        global vertex_set
        global street_name_set
        global line_set
        vertex_set = set()
        street_name_set = set()
        line_set = set()

        if re.match(format_add, input_command) is not None:
            command_add(input_command)
        elif re.match(format_mod, input_command) is not None:
            command_mod(input_command)
        elif re.match(format_rm, input_command) is not None:
            command_rm(input_command)
        elif re.match(format_gg, input_command) is not None:
            command_gg()
        else:
            sys.stderr.write("Error: Invalid Input\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
