"""
Config loader for ai-vuln-scan
This loads and validates configurations for endpoints and garak probes from YAML
"""

# Imported modules
import yaml # For parsing YAML
from pathlib import Path # For working with file paths cross-platform
from typing import Dict, List, Any # Type hints for clarity


class ConfigLoader:
    """Loads and manages scanner configuration from YAML file"""

    def __init__(self, config_path: str = "config/endpoints.yaml"):
        """
        Initialize the configuration loader
        This runs automatically when you create a new ConfigLoader object

        Args:
            config_path: Path to the YAML config file (defaults to config/endpoints.yaml)
        """
        # Convert string path to a Path object to simplify file handling
        self.config_path = Path(config_path)

        # Holds our parsed config data (Starts as None)
        self.config = None

        # Load the config file immediately when the object is created
        self._load_config()

    def _load_config(self) -> None:
        """
        Load configuration from YAML file
        The underscore prefix (_load_config) indicates this is private -
        it's meant to be used internally, not called by users

        Returns:
            None (but sets self.config with the loaded data)
        """
        # Check if the config file actually exitst
        if not self.config_path.exists():
            # If not, return an error message
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )
        
        try:
            # Open the file in read mode ('r')
            with open(self.config_path, 'r') as f:
                # Parse the YAML and store it in self.config
                # safe_load prevents arbitrary code execution
                self.config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            # If the YAML is malformed, raise a clear error
            raise ValueError(f"Invalid YAML in config file: {e}")
        
        # After loading, validate that required sections are present
        self._validate_config()