#!/usr/bin/env python3
"""
MoonSpeak to Text Converter

Simple utility to convert MoonSpeak expressions to natural language.
"""

import sys
import os
from moonspeak_parser import MoonSpeakParser

class MoonSpeakTextConverter:
    """Simple converter from MoonSpeak expressions to natural language"""
    
    def __init__(self, dict_path=None):
        self.parser = MoonSpeakParser(dict_path)
        self.symbol_to_description = {}
        self._initialize_mappings(dict_path)

    def _initialize_mappings(self, dict_path: str = None):
        """Create mappings from symbols to descriptions"""
        if dict_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            dict_path = os.path.join(parent_dir, "moonspeak.dict.txt")
        
        try:
            with open(dict_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split('|')
                    if len(parts) != 5:
                        continue
                    
                    symbol, _, _, _, description = parts
                    self.symbol_to_description[symbol] = description
        except FileNotFoundError:
            print(f"Error: Dictionary file not found: {dict_path}")
            sys.exit(1)
    
    def health_check(self):
        """Check dictionary and parser health"""
        print(f"Dictionary loaded: {len(self.parser.symbols)} symbols")
        return len(self.parser.symbols) > 0
    
    def convert(self, expression):
        """Convert MoonSpeak expression to natural language"""
        if not expression.strip():
            return ""
        
        # Simple token-by-token replacement
        tokens = self.parser.tokenize(expression)
        text_parts = []
        
        for token in tokens:
            if token in self.symbol_to_description:
                text_parts.append(self.symbol_to_description[token])
            else:
                text_parts.append(token)
        
        return " ".join(text_parts)

def main():
    """Main function"""
    converter = MoonSpeakTextConverter()
    
    # Health check
    print("=== Health Check ===")
    if not converter.health_check():
        print("ERROR: Dictionary not loaded properly!")
        sys.exit(1)
    print("Health check passed.\n")
    
    # Interactive loop
    while True:
        try:
            expression = input("Enter MoonSpeak expression (or 'exit' to quit): ")
            if expression.lower() in ['exit', 'quit']:
                break
            
            # Convert and display
            result = converter.convert(expression)
            print(f"English: {result}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()