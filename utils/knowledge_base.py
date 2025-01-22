import orjson
import pytricia
import ipaddress
import logging
from typing import List
from functools import lru_cache


logger = logging.getLogger(__name__)


class KnowledgeBase:
    """
    Represents a knowledge base for storing and retrieving IP network tags.

    This class loads data from a JSON file, processes it into a Patricia trie
    (a memory-efficient prefix tree), and provides methods for retrieving tags
    associated with specific IP addresses.

    Example of JSON file for knowledge_base:
    [
        {"tag": "foo", "ip_network": "192.0.2.0/24"},
        {"tag": "bar", "ip_network": "192.0.2.8/29"},
        {"tag": "bar", "ip_network": "10.20.0.0/16"},
        {"tag": "SPAM", "ip_network": "10.20.30.40/32"}
    ]
    """
    def __init__(self, path: str):
        """
        Initializes the KnowledgeBase.

        Args:
            path (str): The file path to the JSON data.
        """
        self.path = path
        self.data = None
        self.load_data()
        self.trie = pytricia.PyTricia()
        self.__create_patricia_trie()
        logger.info("KnowledgeBase initialization completed successfully.")

    def load_data(self):
        """
        Loads JSON data from the file.

        This method reads the file at the path provided during initialization
        and loads its contents into the `data` attribute.

        Raises:
            FileNotFoundError: If the specified file is not found.
            orjson.JSONDecodeError: If the file contains invalid JSON data.
        """
        logger.debug("Attempting to load data from file: %s", self.path)
        try:
            with open(self.path, 'rb') as file:
                self.data = orjson.loads(file.read())
                logger.info("Data successfully loaded from file: %s", self.path)
        except FileNotFoundError as e:
            logger.error("File not found: %s", self.path)
            raise FileNotFoundError(f"File not found: {self.path}") from e
        except orjson.JSONDecodeError as e:
            logger.error("Error decoding JSON from file: %s", self.path)
            raise orjson.JSONDecodeError(
                f"Error decoding JSON from file: {self.path}",
                doc=e.doc,
                pos=e.pos,
            ) from e
        """
            TODO: catch more errors the same way
        """

    def __create_patricia_trie(self):
        """
        Constructs a Patricia trie from the loaded data.

        The trie maps IP networks (as strings) to their associated tags,
        allowing for efficient prefix-based lookups.

        Raises:
            KeyError: If a record is missing the required keys ('ip_network' or 'tag').
            ValueError: If an invalid network address is encountered in the data.
        """
        logger.debug("Starting construction of Patricia trie.")
        for record in self.data:
            try:
                network = record['ip_network']
                tag = record['tag']
                network_obj = ipaddress.ip_network(network)
                self.trie[str(network_obj)] = tag

            except KeyError as e:
                logger.error("Missing required key %s in record: %s", e, record)
                raise KeyError(
                    f"Missing required key {str(e)} in record: {record}. "
                    f"Expected keys are 'ip_network' and 'tag'."
                ) from e
            except ValueError as e:
                logger.error("Invalid network address in record: %s. Error: %s", record, e)
                raise ValueError(
                    f"Invalid network address in record {record}. "
                    f"Error: {str(e)}"
                ) from e

            logger.info("Patricia trie construction completed successfully.")
            """
                TODO: catch more errors the same way
            """

    @lru_cache
    def retrieve_tags_using_ip(self, ip: str) -> List[str]:
        """
        Retrieves tags associated with the given IP address.

        This method performs a prefix-based lookup in the Patricia trie to find
        all matching tags for the given IP address. Tags are:
        1. Sorted and unique in the result.
        2. Derived from the most specific network (if multiple matches exist).
        3. De-duplicated if the same tag appears multiple times.

        Args:
            ip (str): The IP address to search for.

        Returns:
            List[str]: A sorted list of unique tags associated with the IP address.

        Notes:
            - The method retrieves up to 10 unique tags for the given IP.
            - Tags are sorted for consistency.
        """
        logger.debug("Looking up tags for IP address: %s", ip)
        matched_tags = {}
        prefix = self.trie.get_key(ipaddress.ip_address(ip))
        network = ipaddress.ip_network(ip)

        if not isinstance(network, ipaddress.IPv4Network):
            logger.error("Only IPv4 networks are supported.")
            raise ValueError(f"Only IPv4 networks are supported. Found: {network}")

        while prefix is not None:
            matched_tags[prefix] = self.trie[prefix]
            logger.debug("Found tag '%s' for prefix '%s'.", self.trie[prefix], prefix)
            prefix = self.trie.parent(prefix)
            if len(matched_tags) == 10:
                logger.warning("Reached the maximum limit of 10 tags for IP: %s", ip)
                break

        result = sorted(set(matched_tags.values()))
        logger.info("Retrieved %d tags for IP %s: %s", len(result), ip, result)
        return result
