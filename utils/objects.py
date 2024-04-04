from datetime import datetime, timezone
from logging import Logger


class log_time_passed:
    def __init__(self, fName="", callback: Logger = None):
        self.start = datetime.now(timezone.utc)
        self.end = None
        self.fName = fName
        self._callback: Logger = callback

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        # xception handling here
        if self._callback is not None:
            self._callback.debug(
                f" took {self.get_timepassed_string(self.start,self.end)} to complete {self.fName}"
            )

    @staticmethod
    def get_timepassed_string(start_time: datetime, end_time: datetime = None) -> str:
        if not end_time:
            end_time = datetime.now(timezone.utc)
        _timelapse = end_time - start_time
        _passed = _timelapse.total_seconds()
        if _passed < 60:
            _timelapse_unit = "seconds"
        elif _passed < 60 * 60:
            _timelapse_unit = "minutes"
            _passed /= 60
        elif _passed < 60 * 60 * 24:
            _timelapse_unit = "hours"
            _passed /= 60 * 60
        else:
            _timelapse_unit = "days"
            _passed /= 60 * 60 * 24

        return "{:,.2f} {}".format(_passed, _timelapse_unit)

    def stop(self):
        self.end = datetime.now(timezone.utc)
