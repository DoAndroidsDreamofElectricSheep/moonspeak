#!/usr/bin/env python3
"""
Text to MoonSpeak Converter

Simple utility to convert natural language descriptions to MoonSpeak expressions.
"""

import sys
import os
from moonspeak_parser import MoonSpeakParser

class TextToMoonSpeakConverter:
    """Simple converter from natural language to MoonSpeak expressions"""
    
    def __init__(self, dict_path: str = None):
        self.parser = MoonSpeakParser(dict_path)
        self.description_to_symbol = {}
        self.name_to_symbol = {}
        self._initialize_mappings(dict_path)
    
    def _initialize_mappings(self, dict_path: str = None):
        """Create mappings from descriptions and names to symbols"""
        # Load dictionary directly to get descriptions
        if dict_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            dict_path = os.path.join(parent_dir, "moonspeak.dict.txt")
        
        # Define common synonyms for better matching
        synonyms = {
            "universal quantifier": ["for all", "for every", "for each"],
            "existential quantifier": ["there exists", "for some"],
            "implication": ["implies", "if then"],
            "conjunction": ["and also"],
            "disjunction": ["or else"],
            "negation": ["not"],
            "equivalence": ["if and only if", "iff"]
        }
        
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
                    self.description_to_symbol[description.lower()] = symbol
                    self.name_to_symbol[name.lower()] = symbol
                    
                    # Add synonyms for better matching
                    if description.lower() in synonyms:
                        for synonym in synonyms[description.lower()]:
                            self.description_to_symbol[synonym.lower()] = symbol
        except FileNotFoundError:
            print(f"Error: Dictionary file not found: {dict_path}")
            sys.exit(1)
    
    def health_check(self):
        """Check dictionary and parser health"""
        print(f"Dictionary loaded: {len(self.parser.symbols)} symbols")
        print(f"Mappings created: {len(self.description_to_symbol)} descriptions, {len(self.name_to_symbol)} names")
        return len(self.parser.symbols) > 0
    
    def convert(self, text: str) -> str:
        """Convert natural language to MoonSpeak expression"""
        if not text.strip():
            return ""
        
        # Define common words to skip
        common_words = ['the', 'a', 'an', 'of', 'to', 'in', 'is', 'are', 'that', 'such', 'then']
        
        # Process the input text
        words = text.lower().split()
        i = 0
        result_tokens = []
        
        while i < len(words):
            # Try multi-word phrases first (up to 4 words)
            found_multi_word = False
            for phrase_len in range(4, 0, -1):
                if i + phrase_len <= len(words):
                    phrase = ' '.join(words[i:i+phrase_len])
                    clean_phrase = phrase.strip('.,!?;:')
                    
                    if clean_phrase in self.description_to_symbol:
                        result_tokens.append(self.description_to_symbol[clean_phrase])
                        i += phrase_len
                        found_multi_word = True
                        break
            
            if found_multi_word:
                continue
            
            # Process single word
            word = words[i]
            clean_word = word.strip('.,!?;:')
            
            # Skip common words
            if clean_word in common_words:
                result_tokens.append(clean_word)
            # Check if it's a name
            elif clean_word in self.name_to_symbol:
                result_tokens.append(self.name_to_symbol[clean_word])
            # Keep alphanumeric and parentheses
            elif clean_word.isalnum() or clean_word in ['(', ')']:
                result_tokens.append(clean_word)
            
            i += 1
        
        # Join with spaces and clean up
        result = ' '.join(result_tokens)
        result = result.replace('( ', '(').replace(' )', ')')
        
        return result

def main():
    """Main function"""
    converter = TextToMoonSpeakConverter()
    
    # Health check
    print("=== Health Check ===")
    if not converter.health_check():
        print("ERROR: Dictionary not loaded properly!")
        sys.exit(1)
    print("Health check passed.\n")
    
    # Interactive loop
    while True:
        try:
            text = input("Enter English text (or 'exit' to quit): ")
            if text.lower() in ['exit', 'quit']:
                break
            
            # Convert and display
            result = converter.convert(text)
            print(f"MoonSpeak: {result}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()