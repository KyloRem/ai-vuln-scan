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


    def _validate_config(self) -> None:
        """
        Validate that required configuration sections exist
        This ensures the config file has the structure we expect
        """
        # List of sections that MUST be in the config file
        required_sections = ['endpoints', 'probes', 'scan_settings']

        #Loop through each required section
        for section in required_sections:
            # Check if the section exists in the loaded config
            if section not in self.config: 
                # If missing, raise an error
                raise ValueError(
                    f"Missing required section '{section}' in config file"
                )

    
    def get_enabled_endpoints(self) -> List[Dict[str, Any]]:
        """
        Get list of enabled endpoints
        Filters out any endpoints where enabled=False
        
        Returns:
            List of endpoint configurations where enabled=True
            Each endpoint is a dictionary with keys like 'name', 'type', 'model', etc.
            """
        # Get the 'endpoints' section
        endpoints = self.config.get('endpoints',[])

        # List comprehension: filter to only include endpoints where enabled is True
        # ep.get('enabled', False) means: get the 'enabled' value, default to False if missing
        return [ep for ep in endpoints if ep.get('enabled', False)]

    
    def get_enabled_probes(self) -> List[Dict[str, Any]]:
        """
        Get a list of the enabled garak probes
        Filters out any probes where enabled=False

        Returns:
            List of probe configurations where enabled=True
            Each probe is a dictionary with keys like 'name', owasp_mapping', etc.
        """
        # Get the 'probes' section
        probes = self.config.get('probes', [])

        # Filter for only enabled probes. Same as endpoints
        return [probe for probe in probes if probe.get('enabled', False)]


    def get_scan_settings(self) -> Dict[str, Any]:
        """
        Get scan settings 
        Returns the entire scan_settings section from the config

        Returns:
            Dictionary of scan settings (generations, parallel, output_dir, etc.)
        """
        # Get the 'scan_settings' section 
        return self.config.get('scan_settings',{})
    

    def get_probe_names(self) -> List[str]:
        """
        Get list of enabled garak probe names
        Extracts onle the 'name' field from each enabled probe
        This is what we'll pass to garak when running scans

        Returns:
            List of probe names as strings (e.g. ['promptinject', 'xss', etc.])
        """
        # Get all enabled probes (returns a list of dictionaries)
        probes = self.get_enabled_probes()

        # Extract just the 'name' field from each probe dictionary
        # This is a list comprehension that transforms the list
        return [probe['name'] for probe in probes]
    

# Convenience function for quick loading
# Reads like a more natural command (e.g. config = load_config() reads better than config = ConfigLoader())
def load_config(config_path: str = "config/endpoints.yaml") -> ConfigLoader:
    """
    Load configuration from file
    Helper function so you can load the config in one line
    Instead of: config = ConfigLoader("config/endpoints.yaml")
    You can do: config = load_config()
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config Loader instance (an object with all our config data)
    """
    return ConfigLoader(config_path)