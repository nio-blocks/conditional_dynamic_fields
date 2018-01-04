ConditionalModifier
===================
The ConditionalModifier block adds a new attribute to input signals, labeled by the *title* attribute. The value of the attribute is determined by the *lookup* parameter. If the expression inside *lookup* evaluates to True, the *value* parameter is assigned to the *title* attribute. *lookup*s are evaluated top to bottom, and if multiple formulas in the same field evaluate to True, the first value is the one that is assigned to the signal.

Properties
----------
- **exclude**: If checked (true), the attributes of the incoming signal will be excluded from the outgoing signal. If unchecked (false), the attributes of the incoming signal will be included in the outgoing signal.
- **fields**: Fields and values to add onto the incoming signal based on the lookup expression.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: One signal for every incoming signal, modified according to 'fields'.

Commands
--------
None

