MoonSpeak LLM
# MoonSpeak v0.2 - token-efficient reasoning dictionary

**MoonSpeak** is a compact domain specific language (DSL) for symbolic reasoning
and token efficient chain-of-thought inside Large Language Models (LLMs).

# Format: symbol|name|category|priority|description
+|plus|arith|3|addition
-|minus|arith|3|subtraction
*|mul|arith|2|multiplication
/|div|arith|2|division
%|mod|arith|2|modulus
**|pow|arith|1|exponentiation
¬|not|logic|1|negation
∧|and|logic|2|conjunction
∨|or|logic|3|disjunction
→|imp|logic|4|implication
↔|iff|logic|5|equivalence
⊕|xor|logic|4|exclusive-or
⊤|true|logic|1|boolean true
⊥|false|logic|1|boolean false
=|eq|logic|3|equality
≠|ne|logic|3|inequality
∀|forall|quant|1|universal quantifier
∃|exists|quant|1|existential quantifier
□|box|modal|1|necessity
◇|diamond|modal|1|possibility
∴|therefore|reason|1|logical conclusion
∵|because|reason|1|logical premise
⊢|vdash|reason|1|syntactic entailment
⊨|models|reason|1|semantic entailment


# Road map 
moonspeak-v0.2/
├── moonspeak.dict.txt         # Core machine dictionary (symbol|name|category|priority|description)
├── moonspeak.grammar.ebnf     # Optional EBNF grammar
├── README.md                      # Project documentation
├── LICENSE                        # MIT License
└── .gitignore                     # Standard Python / editor ignores

Util/build_dict.py              # Optional YAML → TXT converter
Util/test_parser.py             # Unit tests for CI
