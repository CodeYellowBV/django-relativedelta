# Change log

## unreleased

* Make sure deprecation warning doesn't trigger in Django 3 (#12).

## v1.1.3

* Introduced compatibility with non postgres databases. 


## v1.1.2

* Introduced pytest and tox for testing.

## v1.1.1

* Make check for Postgres more lenient by checking the vendor attribute (#11).

## v1.1.0

* Add support for Django 3.0 (#9, #10)
* Test on multiple Django/Python combinations

## v1.0.6

* Loosen up check for Postgres backend by using a substring search, so
  that the code won't break on custom Postgres adapters (#8).

## v1.0.5

* Do not coerce "weeks" numbers to float.
* Remove hard dependency on psycopg (#6).

## v1.0.4

* Also recognise Postgis contrib engine as a supported Postgres engine.

## v1.0.3

* Accidental upload; is identical to v1.0.2.

## v1.0.2

* Also accept `django.db.backends.postgresql` alias as Postgresql driver (#1).
* Do not serialize `weeks` value when storing in the database, which caused those days to be counted twice (#2).

## v1.0.1

* Ensure integer values are always parsed as integers.  This prevents
issues when performing date arithmetic on relativedelta objects, as
Python's date class demands integer arguments.
