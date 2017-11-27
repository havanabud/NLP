from multiprocessor_utils import MultiProcessorUtils
from edit_distance import EditDistance
from parser_utils import ParserUtils
from graph_utils import GraphUtils
from params import Params
import time


#NOTE: for multiprocessing in python, this function must be
#      picklable and callable from same script (i.e. main.py)
#      in which __main__ is invoked.
def calc_edit_distances(files, range_bound, max_lines, output):
    '''
    Calculates edit_distance for each file in files and stores
    in a dictionary.
    :param files: array of filenames as string
    :param total_num_lines_array: total number of lines in each file
    '''
    from nltk.metrics.distance import edit_distance
    import linecache

    lower_bound = range_bound[0]
    upper_bound = range_bound[1]
    #print "lower_bound: ",lower_bound
    #print "upper_bound: ",upper_bound
    edit_distance_counts = {}
    for filename in files:
        edit_distance_counts[filename] = {}
        for x_idx in range(lower_bound, upper_bound):
            x_line = linecache.getline(filename, x_idx)
            for y_idx in range(x_idx + 1, max_lines):
                y_line = linecache.getline(filename, y_idx)
                e_dist = edit_distance(x_line, y_line)
                try:
                    edit_distance_counts[filename][e_dist] += 1
                except KeyError:
                    edit_distance_counts[filename][e_dist] = 1
    output.put(edit_distance_counts)


if __name__ == "__main__":
    # Parse args
    args = ParserUtils.get_args()
    #TODO: build out inference functionality
    if args.infer:
        print "ERROR: inference not built out, yet. Use --param instead."
        exit()
    total_num_lines = ParserUtils.get_total_lines(args.source, args.target)
    groupings = ParserUtils.get_groupings(args.groups)

    # Calculate edit distances for input_files and return dict of counts for each edit_distance by file
    wall_start_time = time.time()
    cpu_start_time = time.clock()
    if args.batch:
        print "Calculating edit distances using multiple processes..."
        edit_distance_counts = MultiProcessorUtils.process_in_batches(calc_edit_distances, [args.source, args.target], total_num_lines)
    else:
        edit_distance_counts = EditDistance.calc_edit_distances([args.source, args.target], total_num_lines)
    cpu_end_time = time.clock() - cpu_start_time
    wall_end_time = time.time() - wall_start_time
    print "EditDistance Wall Time: ", wall_end_time
    print "EditDistance CPU Time: ", cpu_end_time

    # Calculate parameters using edit_distance_counts and write to output file.
    p = Params()
    params = p.calculate_parameters_by_grouping(args.source, args.target, edit_distance_counts, groupings=groupings)
    p.write_parameters_by_group(params, args.source, args.target, args.output)

    #TODO: create function to graph the PARAMS, not just the edit_distances
    GraphUtils.plot_data(args.source, args.target, edit_distance_counts)