import argparse
from edit_distance import EditDistance
from graph_utils import GraphUtils
from file_utils import FileUtils
from main_utils import MainUtils
from params import Params

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculates edit distances and four parameters for two languages.")
    parser.add_argument('-s', '--source', type=str, required=True, help="Path to filename containing source language.")
    parser.add_argument('-t', '--target', type=str, required=True, help="Path to filename containing target language.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to filename for writing parameters.")
    parser.add_argument('-g', '--groups', help="Comma separated integers representing the edit distances "
                                               "you wish to group by when calculating parameters")

    # Get args
    args = parser.parse_args()
    input_files = [args.source, args.target]
    groupings = MainUtils.parse_groups(args.groups)

    # Read-in and cache lines of input_files and calculate number of lines in each file
    total_num_lines_array = []
    FileUtils.populate_total_num_lines_array(input_files, total_num_lines_array)

    # Calculate edit distances for input_files and return defaultdict of counts for each edit_distance by file
    edit_distance_counts = EditDistance.calc_edit_distances(input_files, total_num_lines_array)

    # Calculate parameters using edit_distance_counts and write to output file.
    p = Params()
    params = p.calculate_parameters_by_grouping(args.source, args.target, edit_distance_counts, groupings=groupings)
    p.write_parameters_by_group(params, args.source, args.target, args.output)

    #TODO: create function to graph the PARAMS, not just the edit_distances
    GraphUtils.plot_data(args.source, args.target, edit_distance_counts)