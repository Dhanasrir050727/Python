from datetime import date

from date_ranges import DateRange, MAX_DATE

# end date defaults to MAX_DATE
dr = DateRange(date(2023, 11, 1))

date(2023, 11, 22) in dr
# True

# An empty date (0 days in range):
empty = DateRange.empty()
bool(empty)
# False

# Iteration
for d in DateRange(date(2023, 1, 1), date(2023, 1, 5)):
    print(d)
# 2023-01-01
# 2023-01-02
# 2023-01-03

# Create from strings
dr = DateRange.from_string('20230101-20230103')
repr(dr)
# 'DateRange(start=datetime.date(2023, 1, 1), end=datetime.date(2023, 1, 3))'

# Create range for a single date
dr = DateRange.from_string('20231031')
repr(dr)
# 'DateRange(start=datetime.date(2023, 10, 31), end=datetime.date(2023, 10, 31))'

# Create range for given year-month
dr = DateRange.from_string('202305')
repr(dr)
# 'DateRange(start=datetime.date(2023, 5, 1), end=datetime.date(2023, 5, 31))'

# Create range for multiple full months
dr = DateRange.from_string('202305-202311')
repr(dr)
# 'DateRange(start=datetime.date(2023, 5, 1), end=datetime.date(2023, 11, 30))'

# Formatted print
dr = DateRange(date(2023, 1, 1), date(2023, 1, 5))
dr
# 20230101-20230105
print(f'{dr:H}')   # H for human
# 2023-01-01 to 2023-01-03

# Full months rendered appropriately
dr = DateRange.from_string('202305')
f'{dr:H}'  # H for "human-readable"
# 'May 2023'
f'{dr:C}'  # C for compact
# '202305'
dr
# '202305'