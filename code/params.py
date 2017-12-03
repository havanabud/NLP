from collections import defaultdict


class Params(object):
    WORST_EXPAND = "worst_expanding_factor"
    WORST_CONTRACT = "worst_contracting_factor"
    WORST_STRETCH = "worst_stretching_factor"
    AVG_STRETCH = "average_stretching_factor"
    SUM_EXPAND = "sum_of_expanding_factors"
    SUM_CONTRACT = "sum_of_contracting_factors"
    TOTAL_COUNT = "total_count"
    ALL = 'ALL'
    FILE_OUTPUT = "output/parameters.txt"

    @classmethod
    def calculate_parameters_by_grouping(cls, file_source, file_target, edit_distance_counts, groupings=[]):
        print "Calculating parameters..."
        parameters = cls._get_empty_parameters_by_grouping(groupings)
        for e_dist_source, count_source in edit_distance_counts[file_source].iteritems():
            for e_dist_target, count_target in edit_distance_counts[file_target].iteritems():
                cls._calc_expanding_and_contracting_params_by_group(parameters,
                                                                    e_dist_source,
                                                                    e_dist_target,
                                                                    count_source * count_target)
        cls._calc_stretching_params_by_group(parameters)
        return parameters

    @classmethod
    def _calc_expanding_and_contracting_params_by_group(cls, params, e_dist_source, e_dist_target, count_multiplier):
        for group, group_params in params.iteritems():
            if (e_dist_source < group) and (e_dist_target < group):
                cls._store_expanding_and_contracting_factors(group_params,
                                                             e_dist_source,
                                                             e_dist_target,
                                                             count_multiplier)

    @classmethod
    def _store_expanding_and_contracting_factors(cls, params, e_dist_source, e_dist_target, count_multiplier):
        # Store worst expanding factor
        expanding_factor = Params._calc_expanding_factor(e_dist_source, e_dist_target)
        cls._store_max_factor(params, Params.WORST_EXPAND, expanding_factor)

        # Store worst contracting factor
        contracting_factor = Params._calc_contracting_factor(e_dist_source, e_dist_target)
        cls._store_max_factor(params, Params.WORST_CONTRACT, contracting_factor)

        # Store sum of expanding factors and sum of contracting factors
        cls._store_factor_sums(params, expanding_factor, contracting_factor, count_multiplier)

    @classmethod
    def _calc_stretching_params_by_group(cls, params):
        for group, group_params in params.iteritems():
            if group_params[cls.WORST_EXPAND] and group_params[cls.WORST_CONTRACT]:
                cls._store_worst_stretching_factor(group_params)
                cls._store_average_stretching_factor(group_params)
            else:
                print "WARNING: There were no edit distances for group {0}. " \
                      "Therefore, no parameters could be calculated for this group.".format(group)

    @classmethod
    def _store_worst_stretching_factor(cls, params):
        params[cls.WORST_STRETCH] = \
            cls._calc_worst_stretching_factor(
                params[cls.WORST_EXPAND],
                params[cls.WORST_CONTRACT] )

    @classmethod
    def _store_average_stretching_factor(cls, params):
        params[cls.AVG_STRETCH] = \
            cls._calc_avg_stretching_factor(params[cls.TOTAL_COUNT],
                                            params[cls.SUM_EXPAND],
                                            params[cls.SUM_CONTRACT])

    @classmethod
    def _store_max_factor(cls, params, param_name, factor_value):
        if (not params[param_name]) or (params[param_name] < factor_value):
            params[param_name] = factor_value

    # Count multiplier needed to account for number of times we see given edit_distance (e.g. e_dist=15) across 2 langs
    @classmethod
    def _store_factor_sums(cls, params, expanding_factor, contracting_factor, count_multiplier):
        cls._add_factor(params, cls.SUM_EXPAND, expanding_factor * count_multiplier)
        cls._add_factor(params, cls.SUM_CONTRACT, contracting_factor * count_multiplier)
        cls._add_factor(params, cls.TOTAL_COUNT, count_multiplier)

    @classmethod
    def _add_factor(cls, params, param_name, factor_value):
        try:
            params[param_name] += factor_value
        except:
            params[param_name] = factor_value

    @classmethod
    def _get_empty_parameters_by_grouping(cls, groupings):
        parameters = defaultdict(lambda: defaultdict(float))
        # Comparing non-numeric type against numeric value will always result
        # in numeric value being less than non-numeric type
        # whereby (type<int> < type<str>) e.g. (5 < "ALL")
        parameters[cls.ALL] = cls._get_empty_parameters_dict()
        if groupings:
            for group in groupings:
                parameters[group] = cls._get_empty_parameters_dict()

        return parameters

    @classmethod
    def _get_empty_parameters_dict(cls):
        return {
            cls.WORST_EXPAND: None,
            cls.WORST_CONTRACT: None,
            cls.WORST_STRETCH: None,
            cls.AVG_STRETCH: None,
            cls.SUM_EXPAND: None,
            cls.SUM_CONTRACT: None,
            cls.TOTAL_COUNT: None
        }

    @staticmethod
    def _calc_expanding_factor(e_dist_source, e_dist_target):
        try:
            result = e_dist_target / float(e_dist_source)
        # an e_dist of zero indicates the source and target sentence were the same string
        except ZeroDivisionError as e:
            result = 0
        return result

    @staticmethod
    def _calc_contracting_factor(e_dist_source, e_dist_target):
        try:
            result = e_dist_source / float(e_dist_target)
        # an e_dist of zero indicates the source and target sentence were the same string
        except ZeroDivisionError as e:
            result = 0
        return result

    @staticmethod
    def _calc_worst_stretching_factor(worst_expanding_factor, worst_contracting_factor):
        return worst_expanding_factor * worst_contracting_factor

    @staticmethod
    def _calc_avg_stretching_factor(total_count, sum_expanding_factors, sum_contracting_factors):
        return ( (1/float(total_count)) * sum_expanding_factors ) * \
            ( (1/float(total_count)) * sum_contracting_factors )

    @classmethod
    def write_params(cls, params, file_source, file_target, e_dist_clock_time):
        print "Writing parameters to {0}".format(cls.FILE_OUTPUT)
        header = "Parameters\n" \
                 "source: {0}\n" \
                 "target: {1}\n\n"\
                 .format(file_source, file_target)
        try:
            with open(cls.FILE_OUTPUT, 'w') as f_output:
                f_output.write(header)
                cls._write_parameters_by_group(f_output, params, e_dist_clock_time)
        except IOError as e:
            print "I/O Error: {0}".format(e)

    @staticmethod
    def _write_parameters_by_group(file_output, params, e_dist_clock_time):
        for group, group_params in sorted(params.iteritems()):
            file_output.write("Edit Distance Group: {0}\n".format(group))
            for param_name, param_value in sorted(group_params.iteritems()):
                if (param_name != Params.SUM_EXPAND) and \
                    (param_name != Params.SUM_CONTRACT) and \
                    (param_name != Params.TOTAL_COUNT):
                        file_output.write(': '.join([param_name, str(param_value)]))
                        file_output.write('\n')
            file_output.write('\n')
        file_output.write("Clock time for all edit distance calculations: {0}\n\n".format(e_dist_clock_time))
