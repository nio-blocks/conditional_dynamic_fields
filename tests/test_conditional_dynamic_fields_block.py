from unittest.mock import patch
from ..conditional_dynamic_fields_block import ConditionalDynamicFields
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.common.signal.base import Signal


class FlavorSignal(Signal):
    def __init__(self, flavor, size=None):
        self.flavor = flavor
        self.size = size


class KeyValueSignal(Signal):
    def __init__(self, key, value):
        self.key = key
        self.value = value


class TestConditionalDynamicFields(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        self.last_notified = []

    def signals_notified(self, signals):
        self.last_notified = signals

    def test_pass(self):
        signals = [FlavorSignal("banana")]
        attrs = signals[0].__dict__
        blk = ConditionalDynamicFields()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        self.assertDictEqual(attrs, self.last_notified[0].__dict__)

    def test_add_field(self):
        signals = [FlavorSignal("banana")]
        blk = ConditionalDynamicFields()
        config = {
            "fields": [{
                "title": "greeting",
                "lookup": [{
                    "formula": "{{True}}",
                    "value": "i am a banana!"
                }]
            }]
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals(signals)
        sig = self.last_notified[0]
        self.assertTrue(hasattr(sig, 'greeting'))
        self.assertTrue(hasattr(sig, 'flavor'))
        self.assertEqual(sig.greeting, "i am a banana!")

    def test_lookup(self):
        signals = [FlavorSignal("banana", "S"),
                   FlavorSignal("banana", "M"),
                   FlavorSignal("banana"),
                   FlavorSignal("apple", "S"),
                   FlavorSignal("coffee", "S")]
        blk = ConditionalDynamicFields()
        config = {
            "fields": [{
                "title": "greeting",
                "lookup": [
                    {"formula": "{{$flavor == 'banana' and " \
                                "$size == 'S'}}",
                     "value": "i am a banana!"},
                    {"formula": "{{$flavor == 'apple'}}",
                     "value": "i am an apple!"},
                    {"formula": "{{$flavor == 'banana'}}",
                     "value": "i am a banana again!"},
                    {"formula": "{{True}}",
                     "value": "i am nothing :("}
                ]
            }]
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(self.last_notified[0].greeting,
                         "i am a banana!")
        self.assertEqual(self.last_notified[1].greeting,
                         "i am a banana again!")
        self.assertEqual(self.last_notified[2].greeting,
                         "i am a banana again!")
        self.assertEqual(self.last_notified[3].greeting,
                         "i am an apple!")
        self.assertEqual(self.last_notified[4].greeting,
                         "i am nothing :(")

    def test_lookup_bad_syntax(self):
        signals = [FlavorSignal("banana", "S"),
                   FlavorSignal("banana", "M"),
                   FlavorSignal("banana"),
                   FlavorSignal("apple", "S"),
                   FlavorSignal("coffee", "S")]
        blk = ConditionalDynamicFields()
        config = {
            "fields": [{
                "title": "greeting",
                "lookup": [
                    {"formula": "{{$flavor == {this is bad} }}",
                     "value": "i am an apple!"},
                    {"formula": "{{$flavor == 'banana' and " \
                                "$size == 'S'}}",
                     "value": "i am a banana!"},
                    {"formula": "{{$flavor == 'apple'}}",
                     "value": "i am an apple!"},
                    {"formula": "{{$flavor == 'banana'}}",
                     "value": "i am a banana again!"},
                    {"formula": "{{True}}",
                     "value": "i am nothing :("}
                ]
            }]
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(self.last_notified[0].greeting,
                         "i am a banana!")
        self.assertEqual(self.last_notified[1].greeting,
                         "i am a banana again!")
        self.assertEqual(self.last_notified[2].greeting,
                         "i am a banana again!")
        self.assertEqual(self.last_notified[3].greeting,
                         "i am an apple!")
        self.assertEqual(self.last_notified[4].greeting,
                         "i am nothing :(")

    def test_exclude(self):
        signals = [FlavorSignal("banana")]
        blk = ConditionalDynamicFields()
        config = {
            "exclude": True,
            "fields": [{
                "title": "greeting",
                "lookup": [{
                    "formula": "{{True}}",
                    "value": "i am a banana!"
                }]
            }]
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals(signals)
        sig = self.last_notified[0]
        self.assertTrue(hasattr(sig, 'greeting'))
        self.assertFalse(hasattr(sig, 'flavor'))
        self.assertEqual(sig.greeting, "i am a banana!")

    def test_bogus_field(self):
        signals = [FlavorSignal("you won't see me")]
        blk = ConditionalDynamicFields()
        self.configure_block(blk, {
            "exclude": True,
            "fields": [{
                "title": "greeting",
                "lookup": [{
                    "formula": "{{dict($val)}}",
                    "value": "i am a banana!"
                }]
            }]
        })
        blk.start()
        blk.process_signals(signals)
        sig = self.last_notified[0]
        self.assertTrue(hasattr(sig, 'greeting'))
        self.assertIsNone(sig.greeting)
