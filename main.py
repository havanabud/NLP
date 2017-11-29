from multiprocessor_utils import MultiProcessorUtils
from edit_distance import EditDistance
from parser_utils import ParserUtils
from graph_utils import GraphUtils
from time_utils import TimeUtils
from params import Params
from infer import Infer


#NOTE: for multiprocessing in python, this function must be
#      picklable and callable from same script (i.e. main.py)
#      in which __main__ is invoked.
def calc_edit_distances(files, batch, max_lines, output):
    from nltk.metrics.distance import edit_distance
    import linecache

    edit_distance_counts = {}
    for filename in files:
        edit_distance_counts[filename] = {}
        for x_idx in batch:
            x_line = linecache.getline(filename, x_idx)
            for y_idx in range(x_idx + 1, max_lines):
                y_line = linecache.getline(filename, y_idx)
                e_dist = edit_distance(x_line, y_line)
                try:
                    edit_distance_counts[filename][e_dist] += 1
                except KeyError:
                    edit_distance_counts[filename][e_dist] = 1
    output.put(edit_distance_counts)
    output.close()
    print "INFO: one of the batch processes completed..."
    return


if __name__ == "__main__":
    # Parse args
    args = ParserUtils.get_args()
    total_num_lines = ParserUtils.get_total_lines(args.source, args.target)
    groupings = ParserUtils.get_groupings(args.groups)

    # Calculate edit distances for input_files and return dict of counts for each edit_distance by file
    cpu_start_time = TimeUtils.get_start_time()
    if args.batch and MultiProcessorUtils.has_multiple_cpus():
        edit_distance_counts = MultiProcessorUtils.process_in_batches(calc_edit_distances, [args.source, args.target], total_num_lines+1)
    else:
        edit_distance_counts = EditDistance.calc_edit_distances([args.source, args.target], total_num_lines+1)
    cpu_end_time = TimeUtils.get_end_time(cpu_start_time)

    # Calculate parameters using edit_distance_counts and write to output file.
    p = Params()
    params = p.calculate_parameters_by_grouping(args.source, args.target, edit_distance_counts, groupings=groupings)

    #TODO: client shuoldn't be allowed to group if we're inferring
    #TODO: we should make this ALL grouping known easily across code base
    if args.infer:
        Infer.infer(params[1000000],args.output)
    else:
        p.write_parameters_by_group(params, args.source, args.target, args.output, cpu_end_time)

    #TODO: create function to graph the PARAMS, not just the edit_distances
    #TODO: graph the different edit distances by groupings (if groupings were provided)
    #GraphUtils.plot_data(args.source, args.target, edit_distance_counts)