ConditionalModifier
===================
Just like the [Modifier](https://blocks.n.io/Modifier) block, the ConditionalModifier block adds new attributes to a signal. But with the ConditionalModifier, the value of each new attribute is conditional, based on the evaluation of one or more **lookup** expressions. If the expression inside a **lookup** evaluates to `True`, the **value** parameter is assigned to the **name** attribute. **lookup** expressions are evaluated top to bottom, and if multiple formulas in the same field evaluate to `True`, the first value is the one that is assigned to the new **title** attribute on the signal.

Properties
----------
- **exclude**: If checked (true), the attributes of the incoming signal will be excluded from the outgoing signal. If unchecked (false), the attributes of the incoming signal will be included in the outgoing signal.
- **fields**: Fields and values to add to the incoming signal based on the **lookup** expression.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: One signal for every incoming signal, modified according to 'fields'.

Commands
--------
None

