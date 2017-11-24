

class MainUtils(object):

    @staticmethod
    def parse_groups(groups):
        if not groups:
            return []

        try:
            return [int(group) for group in groups.split(',')]
        except Exception as e:
            print "ERROR({0}): {1}.\n" \
                  "Failed to process groups argument: {2}\n" \
                  "Please specify groups as comma separated integeres (e.g. 50,100,500,1000)"\
                .format(e.errno, e.strerror, groups)
