"""
App configuration for the `rest_api` application.
"""


import logging
from django.apps import AppConfig
from utils.knowledge_base import KnowledgeBase
from django.conf import settings


class RestApiConfig(AppConfig):
    """
    Configures the `rest_api` application and initializes its components.

    Attributes:
        name (str): The name of the application.
        knowledge_base (KnowledgeBase): An instance of the `KnowledgeBase` class
            that is initialized during application startup.
    """
    name = "rest_api"
    knowledge_base = None

    def ready(self):
        """
        Initializes the application components.

        This method is called when the Django application is ready to start.
        It loads the knowledge base from the file path defined in the `KNOWLEDGE_BASE_PATH`
        of .env file and assigns the resulting object to the `knowledge_base` attribute.
        """
        logger = logging.getLogger('rest_api')
        try:
            knowledge_base_path = settings.KNOWLEDGE_BASE_PATH
            self.knowledge_base = KnowledgeBase(knowledge_base_path)
            logger.info("Knowledge base loaded successfully from %s", knowledge_base_path)
        except FileNotFoundError as e:
            logger.critical("Knowledge base file not found: %s", e)
        # TODO: Further exceptions catching: KeyError, ValueError etc. (e.g. Patricia Trie)
        except Exception as e:
            logger.error("An unexpected error occurred while initializing the knowledge base: %s", e)
