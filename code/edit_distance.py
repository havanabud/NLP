from nltk.metrics.distance import edit_distance
from collections import defaultdict
import linecache


class EditDistance(object):

    @classmethod
    def calc_edit_distances(cls, files, total_num_lines):
        '''
        Calculates edit_distance for each file in files
        :param files: array of filenames as string
        :param total_num_lines_array: total number of lines in each file
        :return: type defaultdict { "filename" : { "edit_distance_value" : <count> } }
        '''
        edit_distance_counts = defaultdict(lambda: defaultdict(int))

        for filename in files:
            for x_idx in range(1, total_num_lines):
                x_line = linecache.getline(filename, x_idx)
                for y_idx in range(x_idx + 1, total_num_lines):
                    y_line = linecache.getline(filename, y_idx)
                    e_dist = edit_distance(x_line, y_line)
                    cls._increment_count(edit_distance_counts, filename, e_dist)

        return edit_distance_counts

    @staticmethod
    def _increment_count(edit_distance_counts, filename, e_dist):
        edit_distance_counts[filename][e_dist] += 1