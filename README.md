# NLP Project
The purpose of this program is twofold:  
  * Calculate parameters for a known, translated language pair.   
  * Infer the language pair for an unknown, translated language pair.     

# Usage
To calculate the parameters for a known, translated language pair:  
`python main.py --param --source <language_corpus.txt> --target <language_corpus.txt> --output <output_parameters.txt> [--groups <int, int, int>] [--plot]`

To infer the language pair for an unknown, translated language pair:  
`python main.py --infer --source <language_corpus.txt> -- target <language_corpus.txt> -o <output_inference.txt>`

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
