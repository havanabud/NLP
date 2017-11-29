from time import clock


class TimeUtils(object):

    @staticmethod
    def get_start_time():
        return clock()

    @staticmethod
    def get_end_time(start_time_secs):
        return start_time_secs - clock()