from nio.common.block.base import Block
from nio.common.signal.base import Signal
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.expression import ExpressionProperty
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.holder import PropertyHolder
from nio.metadata.properties.bool import BoolProperty


class LookupProperty(PropertyHolder):
    formula = ExpressionProperty(default='{{True}}', title='Formula')
    value = ExpressionProperty(default='value', title='Value')


class SignalField(PropertyHolder):
    title = StringProperty(default='', title="Attribute Title")
    lookup = ListProperty(LookupProperty, title='Lookup')


@Discoverable(DiscoverableType.block)
class ConditionalDynamicFields(Block):
    """ Conditional Dynamic Fields block.

    Adds a new new field, *title*, to input signals. The
    value of the attribute is determined by the *lookup*
    parameter. *lookup* is a list of formula/value pairs.
    In order, the *formula* of *lookup* are evaluated and
    when an evaluation is *True*, the *value* is assigned
    to the signal attribute *title*. If multiple formulas
    match, the first value is the one that is assigned
    to the signal.

    """

    fields = ListProperty(SignalField, title='Fields')
    exclude = BoolProperty(default=False, title='Exclude existing fields?')

    def process_signals(self, signals):
        """ Overridden from the block interface.

        """
        fresh_signals = []

        for signal in signals:

            # if we are including only the specified fields, create
            # a new, empty signal object
            tmp = Signal() if self.exclude else signal

            # iterate over the specified fields, evaluating the formula
            # in the context of the original signal
            for field in self.fields:
                try:
                    value = self._evaluate_lookup(field.lookup, signal)
                except Exception as e:
                    value = None

                setattr(tmp, field.title, value)

            # only rebuild the signal list if we're using new objects
            if self.exclude:
                fresh_signals.append(tmp)

        if self.exclude:
            signals = fresh_signals

        self.notify_signals(signals)

    def _evaluate_lookup(self, lookup, signal):
        for lu in lookup:
            try:
                value = lu.formula(signal)
                if value:
                    return lu.value(signal)
            except Exception as e:
                self._logger.error(
                    "Dynamic field {0} evaluation failed: {0}: {1}".format(
                        type(e).__name__, str(e))
                )
