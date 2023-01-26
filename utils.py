from datetime import datetime

from constants import REFERENCE_DATE, UPDATE_INTERVAL


def should_generate_new_pairs():
    """
    Return true whenever the number of days since the reference date is a factor
    of the update interval
    """
    return (datetime.utcnow() - REFERENCE_DATE).days % UPDATE_INTERVAL == 0
