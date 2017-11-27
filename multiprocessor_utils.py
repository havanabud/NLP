from collections import defaultdict
from math import ceil
import multiprocessing as mp


class MultiProcessorUtils(object):

    @classmethod
    def process_in_batches(cls, calc_edit_distances, input_files, total_num_lines):
        # Get set of batches indicating start/end lines from file to be processed
        batches = cls._get_set_of_batches(total_num_lines)

        output = mp.Queue()

        processes = []
        for batch in batches:
            processes.append(mp.Process(target=calc_edit_distances,
                                        args=(input_files, batch, total_num_lines, output)))
        for proc in processes:
            proc.start()

        for proc in processes:
            proc.join()

        results = [output.get() for proc in processes]
        return cls._merge_dicts(results)

    @staticmethod
    def _get_set_of_batches(total_num_lines):
        batches = set()
        cpu_count = mp.cpu_count()
        remainder = (total_num_lines % cpu_count)
        if remainder == 0:
            step = total_num_lines / cpu_count
            for lower_bound in range(1, total_num_lines, step):
                upper_bound = lower_bound + step - 1
                batches.add((lower_bound, upper_bound))
        else:
            step_floor = total_num_lines // cpu_count
            print "step_floor: ", step_floor
            print "step_floor cpus: ", (cpu_count - remainder)
            for lower_bound in range(1, (cpu_count - remainder) * step_floor + 1, step_floor):
                upper_bound = lower_bound + step_floor - 1
                batches.add((lower_bound, upper_bound))

            floor_max = lower_bound + step_floor
            print "floor_max: ", floor_max
            step_ceiling = int(ceil(total_num_lines / float(cpu_count)))
            print "step_ceiling: ", step_ceiling
            print "step_ceiling cpus: ", remainder
            for lower_bound in range(floor_max, total_num_lines, step_ceiling):
                upper_bound = total_num_lines if lower_bound + step_ceiling == total_num_lines else lower_bound + step_ceiling - 1
                batches.add((lower_bound, upper_bound))
        return batches

    @staticmethod
    def _merge_dicts(dicts):
        edit_distance_counts = defaultdict(lambda: defaultdict(int))
        for d in dicts:
            for filename in d.iterkeys():
                for e_dist, count in d[filename].iteritems():
                    edit_distance_counts[filename][e_dist] += count
        return edit_distance_counts
