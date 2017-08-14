ConditionalDynamicFields
========================

Adds a new new field, *title*, to input signals. The
value of the attribute is determined by the *lookup*
parameter. *lookup* is a list of formula/value pairs.
In order, the *formula* of *lookup* are evaluated and
when an evaluation is *True*, the *value* is assigned
to the signal attribute *title*. If multiple formulas
match, the first value is the one that is assigned
to the signal.


Properties
----------
- **exclude**(Bool): Whether to exclude existing fields on an incoming signal.
- **fields**(List): A list of fields to add to an incoming signal.
Each field has a *lookup* attribute, which evaluates the *formula* attribute
to determine whether to add the field onto the signal. If *formula* evaluates
to True, the field is added.

Commands
--------

Dependencies
------------
None

Input
-----
Any list of signals.

Output
------
One signal for every incoming signal, modified according to `fields` and `exclude`.

