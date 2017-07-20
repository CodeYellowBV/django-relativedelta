# Change log

## v1.0.1

* Ensure integer values are always parsed as integers.  This prevents
issues when performing date arithmetic on relativedelta objects, as
Python's date class demands integer arguments.
