ConditionalModifier
===================
Just like the [Modifier](https://blocks.n.io/Modifier) block, the ConditionalModifier block adds new attributes to a signal. But with the ConditionalModifier, the value of each new attribute is based on the evaluation of one or more **Lookup** expressions. For every **Field** specified, the **Formula** of each **Lookup** will be evaluated, and if `True` that **Value** will be assigned to that **Title** as a key-value pair on the outgoing signal. Once a value is assigned, no further lookups are evaluated for that field, and if no lookup's formula evaluates as `True` a value of `None` will be assigned.

Properties
----------
- **Fields**: List of attributes to add to the incoming signals.
  - *Title*: The key of this attribute.
  - *Lookup*: List of conditions to evaluate.
    - *Formula*: An expression to be evaluated as `True` or `False`.
    - *Value*: The value to assign to this attribute if the evaluation of **Formula** is `True`.
- **Exclude Existing Fields**: If checked (True) incoming signals will be discarded, and new signals created with only the fields specified. If False, the incoming signals will have the specified fields added to them, or updated if present.

Examples
--------
The conditional modifier is especially useful when defining the contents of a message. In this example, if the first two lookups do not evaluate as `True`, the final lookup will and therefore act as an `else` statement.:
```
Exclude Existing Fields: True
Fields:
  Title: message
  Lookup:
    Formula: {{ $temp_C > 4 }}
    Value: Perishables in Freezer {{ $unit }} have spoiled! Current temp: {{ $temp_C }}C
    
    Formula: {{ $temp_C >= 0 }}
    Value: Critical temperature in Freezer {{ $unit }}! Current temp: {{ $temp_C }}C
    
    Formula: {{ True }}
    Value: Freezer {{ $unit }} OK: {{ $temp_C }}C
```
<table width=100%>
<tr>
<th align="left">Incoming Signals</th>
<th align="left">Outgoing Signals</th>
</tr>
<tr>
<td>
<pre>
[
  {"unit": 1, "temp_C": 2.2},
  {"unit": 2, "temp_C": -1.0}
]
</pre>
</td>
<td>
<pre>
[
  {"message": "Critical temperature in Freezer 1! Current temp: 2.2C"},
  {"message": "Freezer 2 OK: -1.0C"}
]
</pre>
</td>
</tr>
</table>

Commands
--------
None
