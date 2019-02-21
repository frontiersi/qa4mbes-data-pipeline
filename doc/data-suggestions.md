# Some derived data guidance

The hydography community has it's own standards and procedures, the following recommendations arrive in a general 'this made life simpler / good data structures' sense.

## Naming things

- avoid spaces in path names. path parsing is much simpler using dashes or under_scores or camelCase word joins
- consistently use either tabs 'ctrl-t' or spaces (one or more) as ASCII file delimiters per-survey. Say which strategy is used in a metadata record
- consitently use file extensions: all `tif` or all `tiff` but not some of each

## Sizing things

- share workloads. QA processing for a single, mulitple gigabyte file is harder than processing for multiple, smaller files covering the same region. The final QA'd result can be joined to a mega file later. 
