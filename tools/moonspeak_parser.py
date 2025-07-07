#!/usr/bin/env python3
"""
MoonSpeak Parser - Minimal parser for tokenizing MoonSpeak expressions
"""

import re
import os
import sys
from typing import Dict, List

class MoonSpeakParser:
    """Minimal parser for MoonSpeak expressions"""
    
    def __init__(self, dict_path: str = None):
        self.symbols: Dict[str, str] = {}
        
        # Load dictionary if provided, otherwise use default
        if dict_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            dict_path = os.path.join(parent_dir, "moonspeak.dict.txt")
        
        self.load_dictionary(dict_path)
    
    def health_check(self) -> None:
        """Perform a health check on the parser"""
        print(f"Health Check: Loaded {len(self.symbols)} symbols")
    
    def load_dictionary(self, dict_path: str) -> None:
        """Load the MoonSpeak dictionary from a file"""
        try:
            with open(dict_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split('|')
                    if len(parts) != 5:
                        continue
                    
                    symbol, name, category, priority_str, description = parts
                    self.symbols[symbol] = name
        except FileNotFoundError:
            print(f"Error: Dictionary file not found: {dict_path}")
            sys.exit(1)
    
    def tokenize(self, expression: str) -> List[str]:
        """Tokenize a MoonSpeak expression into individual tokens"""
        # Sort symbols by length (longest first) to avoid partial matches
        sorted_symbols = sorted(self.symbols.keys(), key=len, reverse=True)
        
        # Create a regex pattern that matches any symbol or other token
        symbol_pattern = '|'.join(re.escape(s) for s in sorted_symbols)
        pattern = f"({symbol_pattern}|\\w+|\\d+|\\(|\\)|,|\\s+)"
        
        tokens = re.findall(pattern, expression)
        # Filter out whitespace tokens
        return [t for t in tokens if not t.isspace()]
    
    def is_valid_symbol(self, token: str) -> bool:
        """Check if a token is a valid MoonSpeak symbol"""
        return token in self.symbols

def main():
    """Main function to run the parser from command line"""
    parser = MoonSpeakParser()
    parser.health_check()
    
    if len(sys.argv) < 2:
        print("Usage: moonspeak_parser.py <expression>")
        print("Enter MoonSpeak expression to tokenize:")
        expression = input().strip()
    else:
        expression = ' '.join(sys.argv[1:])
    
    tokens = parser.tokenize(expression)
    print(f"Tokens: {tokens}")
    
    # Show which tokens are valid symbols
    for token in tokens:
        if parser.is_valid_symbol(token):
            print(f"'{token}' -> {parser.symbols[token]}")
        else:
            print(f"'{token}' -> literal")

if __name__ == "__main__":
    main()