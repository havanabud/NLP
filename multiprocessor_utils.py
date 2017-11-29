from collections import defaultdict
import multiprocessing as mp


class MultiProcessorUtils(object):

    @staticmethod
    def has_multiple_cpus():
        return mp.cpu_count() > 1

    @classmethod
    def process_in_batches(cls, calc_edit_distances, input_files, total_num_lines):
        batches = cls._get_list_of_batches(total_num_lines)

        output = mp.Queue()

        processes = []
        for batch in batches:
            processes.append(mp.Process(target=calc_edit_distances,
                                        args=(input_files, batch, total_num_lines, output)))
        for idx, proc in enumerate(processes):
            print "Fork and start a new batch process #",idx,"...."
            proc.start()

        results = [output.get() for proc in processes]
        return cls._merge_dicts(results)

    @staticmethod
    def _get_list_of_batches(total_num_lines):
        batches = [[] for cpu in range(mp.cpu_count())]

        idx = 0
        for linenum in range(1,total_num_lines):
            batches[idx].append(linenum)
            idx += 1
            if idx >= len(batches):
                idx = 0
        return batches

    @staticmethod
    def _merge_dicts(dicts):
        edit_distance_counts = defaultdict(lambda: defaultdict(int))
        for d in dicts:
            for filename in d.iterkeys():
                for e_dist, count in d[filename].iteritems():
                    edit_distance_counts[filename][e_dist] += count
        return edit_distance_counts
