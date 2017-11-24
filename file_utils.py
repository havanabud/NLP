import linecache


class FileUtils(object):

    @staticmethod
    def populate_total_num_lines_array(files, total_num_lines_array):
        success = FileUtils._has_valid_files(files)
        if success:
            for filename in files:
                total_lines = FileUtils._get_total_lines(filename)
                total_num_lines_array.append(total_lines)
            success = FileUtils._has_valid_num_lines(files[0], files[1], total_num_lines_array)

        return success

    @staticmethod
    def _get_total_lines(filename):
        try:
            print "Reading file: {0}".format(filename)
            with open(filename, 'r') as f_input:
                for idx, line in enumerate(f_input, start=1):
                    linecache.getline(filename, idx)
                print "Number of lines read: {0}".format(idx)
                # NOTE: must add 1 to idx for max_num_lines to be correct later in program
                return idx + 1
        except IOError as e:
            print "I/O Error({0}): {1}".format(e.errno, e.strerror)
            return None

    @staticmethod
    def _has_valid_files(files):
        success = True
        if not files:
            print "Error: no files to read!"
            success = False

        if len(files) != 2:
            print "Error: there should be exactly two files!"
            success = False

        return success

    @staticmethod
    def _has_valid_num_lines(source_file, target_file, total_num_lines_array):
        success = True
        if not total_num_lines_array:
            print "Error: no lines were recorded for one or both files.\n" \
                  "source: {0} '\n'" \
                  "target: {1}".format(source_file, target_file)
            success = False

        elif len(total_num_lines_array) != 2:
            print "Error: there should be exaclty two values corresponding to the number of lines per file!"
            success = False

        elif total_num_lines_array[0] != total_num_lines_array[1]:
            print "Error: the total number of lines in each file must be equal \n" \
                  "{0} line count: {1} \n" \
                  "{2} line count: {3}".format(source_file, total_num_lines_array[0],
                                               target_file, total_num_lines_array[1])
            success = False

        return success
