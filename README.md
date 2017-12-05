# NLP Project
The purpose of this program is twofold:  
  * Calculate parameters for a known, translated language pair.   
  * Infer the language pair for an unknown, translated language pair.     

# Usage
To calculate the parameters for a known, translated language pair:  
`python main.py --param [--batch] --source <language_corpus.txt> --target <language_corpus.txt> [--groups <int, int, int>] [--plot]`

To infer the language pair for an unknown, translated language pair:  
`python main.py --infer [--batch] --source <language_corpus.txt> -- target <language_corpus.txt> [--groups <int, int, int>] [--plot]`

# Arguments
--source: The source language corpus file. The number of lines in this file must match the target language file.  

--target: The target language corpus file. The number of lines in this file must match the source language file.  

--batch: Starts `n` proceses, where `n` is the number of the computer's available CPUs on which this program is run, to speed up the time it takes to calculate the edit distances for a language pair. It may be used for either `--param` or `--infer`.  

--param: Calculates the edit distances for a known, translated language pair specified by `--source` and `--target`. The edit distances are used to calaculate four parameters, explained in more detail in the README's section `Parameters`. The parameters are then written to a file specified by `--output`.  

--infer: Calculates the edit distances for an unkown, translated language pair specified by `--source` and `--target`. The edit distances are used to calculate four parameters, which are compared against the parameters for a known set of translated languages. The inferred probability for each language is written to a file specified by `--output`.  

--groups: Comma separated integers by which the edit distances will be grouped and counted. For example, if you specify the numbers `5, 10, 15, 25, 100`, then all edit distances of five or less will be counted in group `5`, all edit distances of 10 or less will be counted in group `10`, and so on. 

--plot: Plots the edit distances calculated for the source and target languages. A link to the charts on plot.ly should be automatically generated. Please ignore the `UserWarnings` posted by the plot.ly API.  


# Parameters
The four parameters calculated by this program are listed below. More information about the parameters may be found in the PDF entitled 'Project Details':
* Worst Expanding Factor
* Worst Contracting Factor
* Worst Stretching Factor
* Average Stretching Factor

# Plotting a Graph - Maximum Account Storage
If you choose to generate a graph, please note that a maximum of 25 graphs may be stored at any given time. If you exceed this limit, please inform me so that I may delete one of the older graphs are your request. 

# Python Version
* Python2.7: yes, it is supported
* Python3: unknown, there is no guarantee the program will work because it was neither tested nor run for this version.

# Python Libraries
* nltk: used to calculate edit distance 
* plotly: used to plot a graph via https://plot.ly/
* linecache: used to improve performance when reading text from file
