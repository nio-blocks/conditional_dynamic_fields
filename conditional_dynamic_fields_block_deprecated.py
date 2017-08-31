from nio.properties import VersionProperty
from .conditional_modifier_block import ConditionalModifier


class ConditionalDynamicFields(ConditionalModifier):
    """Deprected on Aug 31, 2017. To be deleted on Nov 1, 2017"""
    version = VersionProperty("1.0.0")
