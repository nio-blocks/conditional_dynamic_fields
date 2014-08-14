ConditionalDynamicFields
==========================

    Adds a new new field, *title*, to input signals. The value of the attribute is determined by the *lookup* parameter. *lookup* is a list of formula/value pairs. In order, the *formula* of *lookup* are evaluated and when an evaluation is *True*, the *value* is assigned to the signal attribute *title*. If multiple formulas match, the first value is the one that is assigned to the signal.

Properties
--------------

-   **fields**: List of attribute names and corresponding values to add to the incoming signals.
-   **exclude**: If True, output signals only contain the attributes specified by *fields*.


Dependencies
----------------
None

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
One signal for every incoming signal, modified according to *fields* and *exclude*.
