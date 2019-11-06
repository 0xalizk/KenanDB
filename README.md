# KenanDB 

The case study networks in all our works correspond to experimentally observed physical interactions. Non of the networks contain computationally-inferred or functional (non-physical) interactions. The complete datasets is under /NETWORKs. 

The "input/" subdirectory for each network contains (1) source code (Python) used to curate/clean the source data and (2) detailed documentation (txt) describing where the network dataset was obtained, which interactions were excluded (due to weak experimental evidence for example), and whether the interaction type (positive or negative) is known or was randomly assigned. Networks obtained from databases come with source code (in Python) that can be used to regenerate those networks anew from the a single source (BioGrid) or from multiple sources simultaneously (PSIQUICK).

The network files are simple 2- or 3-column txt files, first column=source, 2nd column=target, and 3rd column=interaction sign (promotional or inhibitory) if the network is signed. If you just want to collect all network files, grab all txt files under 'input' directory. 

Note: you can find useful network utilities (in Python) under the repository: https://github.com/aliatiia/utilities

TODO: 1-click by-{organism,context} download util. 
