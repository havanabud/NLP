import argparse
import linecache


class ParserUtils(object):

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(description="Calculates edit distances and four parameters for two languages.")
        param_or_infer = parser.add_mutually_exclusive_group(required=True)
        param_or_infer.add_argument('--param', action='store_true')
        param_or_infer.add_argument('--infer', action='store_true')
        parser.add_argument('-b', '--batch', help="Calculate edit distance in batches using mutliple processes.")
        parser.add_argument('-s', '--source', type=str, required=True,
                            help="Path to filename containing source language.")
        parser.add_argument('-t', '--target', type=str, required=True,
                            help="Path to filename containing target language.")
        parser.add_argument('-o', '--output', type=str, required=True, help="Path to filename for writing parameters.")
        parser.add_argument('-g', '--groups', help="Comma separated integers representing the edit distances "
                                                   "you wish to group by when calculating parameters")
        return parser.parse_args()

    @classmethod
    def get_total_lines(cls, source, target):
        source_num_lines = cls._count_lines_in_file(source)
        target_num_lines = cls._count_lines_in_file(target)
        if source_num_lines != target_num_lines:
            print "Error: the total number of lines in each file must be equal \n" \
                            "{0} line count: {1} \n" \
                            "{2} line count: {3}".format(source, source_num_lines,
                                                         target, target_num_lines)
            raise
        # Don't forget to deduct 1
        return source_num_lines - 1

    @staticmethod
    def _count_lines_in_file(filename):
        try:
            print "Reading file: {0}".format(filename)
            with open(filename, 'r') as f_input:
                for idx, line in enumerate(f_input, start=1):
                    linecache.getline(filename, idx)
                print "Number of lines read: {0}".format(idx)
                # NOTE: must add 1 to idx for max_num_lines to be correct later in program
                return idx + 1
        except IOError as e:
            print "I/O Error: {0}".format(e)
            return None

    @staticmethod
    def get_groupings(groups):
        if not groups:
            return []

        try:
            return [int(group) for group in groups.split(',')]
        except Exception as e:
            print "ERROR: {0}. " \
                  "Failed to process groups argument: {1} " \
                  "Please specify groups as comma separated integeres (e.g. 50,100,500,1000)"\
                .format(e, groups)
            raise
