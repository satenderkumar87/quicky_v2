"""
Clean logging utility to avoid terminal escape sequence issues.
"""

import sys
import re
from typing import Any

class CleanLogger:
    """Logger that removes terminal escape sequences and provides clean output."""
    
    def __init__(self):
        self.escape_pattern = re.compile(r'\x1b\[[0-9;]*[mGKHF]|\x1b\[[0-9]*~')
    
    def clean_text(self, text: str) -> str:
        """Remove terminal escape sequences from text."""
        if not isinstance(text, str):
            text = str(text)
        
        # Remove common escape sequences
        cleaned = self.escape_pattern.sub('', text)
        
        # Remove bracketed paste mode sequences
        cleaned = re.sub(r'\[200~|\[201~', '', cleaned)
        
        # Remove other control characters except newlines and tabs
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', cleaned)
        
        return cleaned
    
    def log(self, message: Any, prefix: str = ""):
        """Log a message with clean output."""
        clean_message = self.clean_text(str(message))
        if prefix:
            clean_prefix = self.clean_text(str(prefix))
            print(f"{clean_prefix} {clean_message}")
        else:
            print(clean_message)
        sys.stdout.flush()
    
    def info(self, message: Any):
        """Log an info message."""
        self.log(message, "ℹ️")
    
    def success(self, message: Any):
        """Log a success message."""
        self.log(message, "✅")
    
    def warning(self, message: Any):
        """Log a warning message."""
        self.log(message, "⚠️")
    
    def error(self, message: Any):
        """Log an error message."""
        self.log(message, "❌")
    
    def processing(self, message: Any):
        """Log a processing message."""
        self.log(message, "🔄")

# Global logger instance
logger = CleanLogger()

def clean_print(*args, **kwargs):
    """Clean print function that removes escape sequences."""
    message = ' '.join(str(arg) for arg in args)
    logger.log(message)

def log_processing(filename: str):
    """Log processing message for a file."""
    logger.processing(f"Processing layout for: {filename}")

def log_success(message: str):
    """Log success message."""
    logger.success(message)

def log_error(message: str):
    """Log error message."""
    logger.error(message)

def log_info(message: str):
    """Log info message."""
    logger.info(message)
