from datetime import datetime

COPY = """
Your new code review buddy for the next two weeks has been chosen! Buddy <b>{}
</b> and buddy <b>{}</b>, go forth and embark on an epic journey together!

{}

P.S. Remember to schedule some time to catch up with your buddy(s).
"""

TROLL_COPY = """
Your journey also includes the rare, but equally awesome, troll: <b>{}</b>

Note: the troll is necessary for when we have an odd number of developers and 
need to have a group of 3.
"""

REFERENCE_DATE = datetime(2023, 1, 24)  # Tuesday
UPDATE_INTERVAL = 14  # days
