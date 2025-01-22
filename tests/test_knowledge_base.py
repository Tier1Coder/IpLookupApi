"""
Unit tests for the KnowledgeBase class.

This module contains unit tests for the `KnowledgeBase` class, which is responsible for
handling and retrieving tags associated with IP addresses from JSON data files. The tests
are divided into three categories to ensure comprehensive coverage:

1. **Original Data Tests** (`TestKnowledgeBaseOriginalData`):
   Tests retrieval of tags for various IP addresses using a valid `original_data.json` file.

2. **Invalid Data Tests** (`TestKnowledgeBaseInvalidData`):
   Tests handling of edge cases and invalid inputs, such as:
   - Non-existent files.
   - Malformed JSON files.
   - Invalid or unsupported IP network addresses.
   - Missing required keys in JSON data.
   - Unsupported IPv6 addresses.
   - Empty JSON files.

3. **Duplicate Data Tests** (`TestKnowledgeBaseDuplicatesData`):
   Tests retrieval of tags in the presence of duplicate entries in the `duplicates_data.json` file.


Notes:
- This test suite assumes the existence of JSON files in the current directory:
  - `original_data.json`
  - `invalid_json_decode.json`
  - `invalid_network_address.json`
  - `invalid_key.json`
  - `invalid_ipv6_address.json`
  - `empty.json`
  - `duplicates_data.json`
- Some tests include TODOs to be implemented later for additional edge cases.
- Each function uses descriptive names to clearly indicate the specific functionality being tested.
"""


import os
import orjson
import unittest
from utils.knowledge_base import KnowledgeBase


os.chdir(os.path.dirname(__file__))


class TestKnowledgeBaseOriginalData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase("original_data.json")

    def test_tags_for_ip_192_0_2_7(self):
        tags = self.kb.retrieve_tags_using_ip("192.0.2.7")
        self.assertEqual(len(tags), 1)
        self.assertEqual("foo", tags[0])
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_192_0_2_9(self):
        tags = self.kb.retrieve_tags_using_ip("192.0.2.9")
        self.assertEqual(len(tags), 2)
        expected_tags = [
            "bar", "foo"
        ]
        self.assertEqual(expected_tags, tags)
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_20_30_40(self):
        tags = self.kb.retrieve_tags_using_ip("10.20.30.40")
        self.assertEqual(len(tags), 2)
        expected_tags = [
            "SPAM", "bar"
        ]
        self.assertEqual(expected_tags, tags)
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_20_30_41(self):
        tags = self.kb.retrieve_tags_using_ip("10.20.30.41")
        self.assertEqual(len(tags), 1)
        self.assertEqual("bar", tags[0])
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_120_30_40(self):
        tags = self.kb.retrieve_tags_using_ip("10.120.30.40")
        self.assertEqual(len(tags), 0)
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_20_130_40(self):
        tags = self.kb.retrieve_tags_using_ip("10.20.130.40")
        self.assertEqual(len(tags), 1)
        self.assertEqual("bar", tags[0])
        self.assertEqual(list, type(tags))

class TestKnowledgeBaseInvalidData(unittest.TestCase):
    def test_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            KnowledgeBase("non_existent_file.json")

    def test_invalid_json_decode(self):
        with self.assertRaises(orjson.JSONDecodeError):
            KnowledgeBase("invalid_json_decode.json")

    def test_invalid_network_address(self):
        with self.assertRaises(ValueError) as cm:
            KnowledgeBase("invalid_network_address.json")
        self.assertIn("Invalid network address", str(cm.exception))

    def test_missing_key(self):
        with self.assertRaises(KeyError) as cm:
            KnowledgeBase("invalid_key.json")
        self.assertIn("Missing required key", str(cm.exception))

    def test_empty_file(self):
        with self.assertRaises(orjson.JSONDecodeError):
            KnowledgeBase("empty.json")

class TestKnowledgeBaseDuplicatesData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase("duplicates_data.json")
    def test_tags_for_ip_192_0_2_7(self):
        tags = self.kb.retrieve_tags_using_ip("192.0.2.7")
        self.assertEqual(len(tags), 1)
        self.assertEqual("foo", tags[0])
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_192_0_2_9(self):
        tags = self.kb.retrieve_tags_using_ip("192.0.2.9")
        self.assertEqual(len(tags), 2)
        expected_tags = [
            "bar", "foo"
        ]
        self.assertEqual(expected_tags, tags)
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_20_30_40(self):
        tags = self.kb.retrieve_tags_using_ip("10.20.30.40")
        self.assertEqual(len(tags), 2)
        expected_tags = [
            "SPAM", "foo"
        ]
        self.assertEqual(expected_tags, tags)
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_20_30_41(self):
        tags = self.kb.retrieve_tags_using_ip("10.20.30.41")
        self.assertEqual(len(tags), 1)
        self.assertEqual("foo", tags[0])
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_120_30_40(self):
        tags = self.kb.retrieve_tags_using_ip("10.120.30.40")
        self.assertEqual(len(tags), 0)
        self.assertEqual(list, type(tags))

    def test_tags_for_ip_10_20_130_40(self):
        tags = self.kb.retrieve_tags_using_ip("10.20.130.40")
        self.assertEqual(len(tags), 1)
        self.assertEqual("foo", tags[0])
        self.assertEqual(list, type(tags))


"""
    TODO: Implement more tests for different file contents
    
    Examples:
        kb.retrieve_tags_using_ip("300.300.300.300")
        kb.retrieve_tags_using_ip("abcd")
        kb.retrieve_tags_using_ip("300.300.300.30!!!")
        kb.retrieve_tags_using_ip("300.300.300")
"""
