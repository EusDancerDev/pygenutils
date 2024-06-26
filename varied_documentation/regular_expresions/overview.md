Types of Regular Expressions

    Basic Regular Expressions (BRE):
        Used in older Unix tools like grep (default mode) and sed.
        Limited features compared to modern regex engines.
        Example: grep '^from\s' filename

    Extended Regular Expressions (ERE):
        Used in egrep or grep -E.
        More features than BRE, like +, ?, |, and () without escaping.
        Example: grep -E '^from\s' filename

    Perl-Compatible Regular Expressions (PCRE):
        Used in many modern tools and languages, including grep -P, Perl, Python, etc.
        Supports advanced features like lookaheads, lookbehinds, non-capturing groups, etc.
        Example: grep -P '^from\s(?!pytools)' filename

Common Tools and Their Default Regex Types

    grep: Uses BRE by default.
    egrep: Uses ERE.
    grep -E: Uses ERE.
    grep -P: Uses PCRE (if supported, as not all grep implementations support -P).
    sed: Uses BRE by default.
    awk: Uses ERE by default.
    Perl: Uses PCRE.
    Python re module: Uses PCRE-like regex.

Practical Tips

    * Always check the documentation: When working with a new tool or language, 
 	  review the documentation to understand what type of regex it supports.
    * Use flags appropriately: Many tools offer flags to switch between 
	  regex types (-E for ERE, -P for PCRE in grep).
    * Test incrementally: Start with simpler expressions and gradually 
	  add complexity to ensure each part works as expected.
