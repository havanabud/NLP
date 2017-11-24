from collections import defaultdict


class Params(object):
    WORST_EXPAND = "worst_expanding_factor"
    WORST_CONTRACT = "worst_contracting_factor"
    WORST_STRETCH = "worst_stretching_factor"
    AVG_STRETCH = "average_stretching_factor"
    SUM_EXPAND = "sum_of_expanding_factors"
    SUM_CONTRACT = "sum_of_contracting_factors"
    TOTAL_COUNT = "total_count"

    @classmethod
    def calculate_parameters_by_grouping(cls, file_source, file_target, edit_distance_counts, groupings=[]):
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
    def write_parameters_by_group(cls, params, file_source, file_target, file_output):
        header = "Parameters for source: {0} and target: {1} \n\n".format(file_source, file_target)
        try:
            with open(file_output, 'a') as f_output:
                f_output.write(header)
                for group, group_params in sorted(params.iteritems()):
                    print "Writing parameters to file for group {0}: ".format(group)
                    cls._write_parameters(group, group_params, f_output)
        except IOError as e:
            print "I/O Error({0}): {1}".format(e.errno, e.strerror)

    @classmethod
    def _write_parameters(cls, group, parameters, f_output):
        f_output.write("Group: {0}\n".format(group))
        for param_name, param_value in sorted(parameters.iteritems()):
            if (param_name != cls.SUM_EXPAND) and \
                (param_name != cls.SUM_CONTRACT) and \
                (param_name != cls.TOTAL_COUNT):
                    f_output.write(': '.join([param_name, str(param_value)]))
                    f_output.write('\n')
        f_output.write('\n')


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
        for group_params in params.itervalues():
                cls._store_stretching_factors(group_params)

    @classmethod
    def _store_stretching_factors(cls, params):
        if params[cls.WORST_EXPAND] and params[cls.WORST_CONTRACT]:
            cls._store_worst_stretching_factor(params)
            cls._store_average_stretching_factor(params)
        else:
            print "Error: Cannot calculate stretching factors due to invalid values! \n " \
                  "{0}: {1} \n " \
                  "{2}: {3}. \n " \
                  "Cannot store {2}!".format(cls.WORST_EXPAND,
                                             params[cls.WORST_EXPAND],
                                             cls.WORST_CONTRACT,
                                             params[cls.WORST_CONTRACT],
                                             cls.AVG_STRETCH)

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
        if not groupings:
            print "INFO: no groupings provided so defaulting to ALL (i.e. 1M)"
            parameters[1000000] = cls._get_empty_parameters_dict()
        else:
            print "INFO: creating groupings: {0}".format(groupings)
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
        return e_dist_target / float(e_dist_source)

    @staticmethod
    def _calc_contracting_factor(e_dist_source, e_dist_target):
        return e_dist_source / float(e_dist_target)

    @staticmethod
    def _calc_worst_stretching_factor(worst_expanding_factor, worst_contracting_factor):
        return worst_expanding_factor * worst_contracting_factor

    @staticmethod
    def _calc_avg_stretching_factor(total_count, sum_expanding_factors, sum_contracting_factors):
        return ( (1/float(total_count)) * sum_expanding_factors ) * \
            ( (1/float(total_count)) * sum_contracting_factors )
