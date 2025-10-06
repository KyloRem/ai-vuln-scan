"""
Garak Scanner Wrapper
Wraps garak vulnerability scanner to make it easy to scan AI endpoints
"""

import subprocess # For running garak as a command (like Terminal)
import json # For parsing garak's JSON output files 
from pathlib import Path # For handling file paths
from typing import Dict, List, Any, Optional # Type hints

from src.config import ConfigLoader 


class GarakScanner:
    """Wrapper for running garak vulnerability scans"""

    def __init__(self, config: ConfigLoader):
        """
        Initialize the scanner with configuration
        
        Args:
            config: ConfigLoader instance with endpoints and probes
        """
        self.config = config
        self.scan_settings = config.get_scan_settings()



    def _build_garak_command(self, endpoint: Dict[str, Any], probes: List[str]) -> List[str]:
        """
        Build the garak command as a list of arguments

        Args:
            endpoint: Endpoint configuration dictionary
            probes: List of probe names to run

        Returns:
            List of command arguments for subprocess
        """
        # Start with the base garak command
        cmd = ["garak"]

        # Add LLM model type and name based on the endpoint config
        if endpoint['type'] == 'huggingface':
            cmd.extend([
                "--model_type", "huggingface",
                "--model_name", endpoint['model']
            ])
        
        # Add each probe
        for probe in probes:
            cmd.extend(["--probes", probe])

        # Add the number of generations from settings
        generations = self.scan_settings.get('generations', 5)
        cmd.extend(["--generations", str(generations)])

        # Add the output scan results directory
        output_dir = self.scan_settings.get('output_dir', 'results')
        cmd.extend(["--report_prefix", output_dir])

        return cmd
    
    
    
    def _run_garak(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """
        Run garak command using subprocess
        
        Args:
            cmd: List of command arguments
            
        Returns:
            CompletedProcess object with results
        """
        print(f"Running garak command: {' '.join(cmd)}")

        try:
            # Run the command and capture output
            result = subprocess.run(
                cmd,
                capture_output=True, # Capture stdout and stderr
                text=True,           # Return strings instead of bytes
                check=True           # Raise error if command fails
            )
            return result
        
        # Error handling
        except subprocess.CalledProcessError as e:
            print(f"Error running garak: {e}")
            print(f"Output: {e.output}")
            raise



    def scan_endpoint(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan a single endpoint with configured probes
        
        Args:
            endpoint: Endpoint configuration dictionary
            
        Returns:
            Dictionary with scan results
        """
        print(f"\n{'='*50}")
        print(f"Scanning: {endpoint['name']}")
        print(f"{'='*50}")
        
        # Get the list of probe names from config
        probes = self.config.get_probe_names()
        print(f"Running {len(probes)} probes: {', '.join(probes)}")
        
        # Build the garak command
        cmd = self._build_garak_command(endpoint, probes)
        
        # Run garak
        result = self._run_garak(cmd)
        
        # Return basic results for now
        return {
            'endpoint': endpoint['name'],
            'probes_run': probes,
            'success': result.returncode == 0,
            'output': result.stdout
        }