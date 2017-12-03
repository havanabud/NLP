from collections import defaultdict

class Infer(object):
    ZH = "zh"
    RU = "ru"
    FR = "fr"
    ES = "es"
    DE = "de"
    CS = "cs"
    DIFF = "diff"
    PROBABILITY = "probability"
    WORST_EXPAND = "worst_expanding_factor"
    WORST_CONTRACT = "worst_contracting_factor"
    WORST_STRETCH = "worst_stretching_factor"
    AVG_STRETCH = "average_stretching_factor"
    FILE_PARAMS = "code/known_lang_parameters.txt"
    FILE_OUTPUT = "output/inference.txt"
    EXPECTED_DATA_POINTS = 5

    @classmethod
    def infer(cls, unknown_lang_params):
        print "Calculating inferences..."
        known_langs_params = cls._load_known_lang_params()
        lang_probabilities = cls._infer_by_params(known_langs_params, unknown_lang_params)
        sorted_lang_probabilities = cls._sort_probabilities(lang_probabilities)
        return sorted_lang_probabilities

    @classmethod
    def _infer_by_params(cls, known_langs_params, unknown_lang_params):
        total_diff = 0
        lang_probabilities = {}
        for lang in known_langs_params.iterkeys():
            diff = 0
            lang_probabilities[lang] = {}
            for param_name, param_value in known_langs_params[lang].iteritems():
                diff += abs(param_value - unknown_lang_params[param_name])

            lang_probabilities[lang][cls.DIFF] = diff
            total_diff += diff

        for lang in lang_probabilities.iterkeys():
            try:
                lang_probabilities[lang][cls.PROBABILITY] = 1 - (lang_probabilities[lang][cls.DIFF] / float(total_diff))
            except ZeroDivisionError:
                lang_probabilities[lang][cls.PROBABILITY] = 0.0
        return lang_probabilities

    @classmethod
    def _load_known_lang_params(cls):
        params = defaultdict(lambda: defaultdict(float))
        with open(cls.FILE_PARAMS, 'r') as f_params:
            for f_idx, line in enumerate(f_params):
                if f_idx == 0:
                    continue
                data = line.split('|')
                cls._populate_params_dict(params, data)
        return params

    @classmethod
    def _populate_params_dict(cls, params, data):
        cls._is_valid_data(data)
        params[data[0]][cls.WORST_CONTRACT] = float(data[1])
        params[data[0]][cls.WORST_EXPAND]   = float(data[2])
        params[data[0]][cls.WORST_STRETCH]  = float(data[3])
        params[data[0]][cls.AVG_STRETCH]    = float(data[4])

    @classmethod
    def _is_valid_data(cls, data):
        valid_langs = [cls.ZH, cls.RU, cls.FR, cls.ES, cls.DE, cls.CS]
        if len(data) < cls.EXPECTED_DATA_POINTS:
            print "ERROR: expected exactly 5 data points but read {0}\n" \
                  "Expected data: [lang, worst_contract, worst_expand, worst_stretch, avg_stretch]\n" \
                  "Invalid data: {1}".format(cls.FILE_PARAMS,data)
            raise Exception

        if data[0] not in valid_langs:
            print "ERROR: invalid lang {0} found in {1}".format(data[0], cls.FILE_PARAMS)
            raise Exception

    @classmethod
    def _sort_probabilities(cls, lang_probabilities):
        data = []
        for lang in lang_probabilities.iterkeys():
            data.append((lang, lang_probabilities[lang][cls.PROBABILITY]))
        return sorted(data, key=lambda tup: tup[1], reverse=True)

    @classmethod
    def write_infer(cls, sorted_lang_probabilities, file_source, file_target):
        print "Writing inferences to {0}".format(cls.FILE_OUTPUT)
        header = "Inferences\n" \
                 "source: {0}\n" \
                 "target: {1}\n\n"\
                 .format(file_source, file_target)
        try:
            with open(cls.FILE_OUTPUT, 'w') as f_output:
                f_output.write(header)
                for data in sorted_lang_probabilities:
                    f_output.write("{0}: {1}\n".format(data[0], data[1]))
        except IOError as e:
            print "I/O Error: {0}".format(e)