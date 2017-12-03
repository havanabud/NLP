from code.multiprocessor_utils import MultiProcessorUtils
from code.edit_distance import EditDistance
from code.parser_utils import ParserUtils
from code.graph_utils import GraphUtils
from code.time_utils import TimeUtils
from code.params import Params
from code.infer import Infer


#NOTE: for multiprocessing in python, this function must be
#      picklable and callable from same script
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
    print "Calculating edit distances..."
    if args.batch and MultiProcessorUtils.has_multiple_cpus():
        edit_distance_counts = MultiProcessorUtils.process_in_batches(calc_edit_distances, [args.source, args.target], total_num_lines+1)
    else:
        edit_distance_counts = EditDistance.calc_edit_distances([args.source, args.target], total_num_lines+1)
    cpu_end_time = TimeUtils.get_end_time(cpu_start_time)

    # Calculate parameters using edit_distance_counts
    p = Params()
    params = p.calculate_parameters_by_grouping(args.source, args.target, edit_distance_counts, groupings=groupings)
    p.write_params(params, args.source, args.target, cpu_end_time)

    # Calculate Inference if specified, and write results to file.
    if args.infer:
        inferences = Infer.infer(params[p.ALL])
        Infer.write_infer(inferences, args.source, args.target)

    # Plot ALL edit distances in graph
    if args.plot:
        GraphUtils.plot_data(args.source, args.target, edit_distance_counts)
