![alt text](https://github.com/M4t1ss/C-3MA/blob/master/C-3MA.png?raw=true "C-3MA")
# Scripts for Tartu Neural MT systems for WMT 17
This repository contains scripts and an example configuration files used for the Tartu Neural MT submission (C-3MA) for the shared translation task at 
the 2017 Workshops on Statistical Machine Translation [http://www.statmt.org/wmt17/](http://www.statmt.org/wmt17/)
* NMT-combination - scripts for combining output of NMT systems
* NMT-config - example configuration files for training NMT systems with [Neural Monkey](https://github.com/ufal/neuralmonkey/) and [Nematus](https://github.com/rsennrich/nematus/)
* named-entity-translation - scripts for prepairing parallel corpora with named entity tags 
* filtering - scripts for filtering parallel text files 
* scoring - scripts for scoring translations with language models
* post-processing - scripts for post-processing output translations
* shuffle_parallel.sh - shuffle two files of parallel sentences

The title is derrived from the authors first names (Chantal, and three Ma's - Maksym, Mark, Matiss). It's also a reference to 
[C-3PO](https://en.wikipedia.org/wiki/C-3PO) - the translation droid from Star Wars.
	
	
Publications
---------

If you use this tool, please cite the following paper:

Matīss Rikters, Chantal Amrhein, Maksym Del, Mark Fishel (2017). "[C-3MA: Tartu-Riga-Zurich Translation Systems for WMT17.](http://www.statmt.org/wmt17/papers.html)" In Proceedings of the Second Conference on Machine Translation (WMT17) (2017).

```
@inproceedings{Rikters-etal:2017:WMT,
	author = {Rikters, Matīss and Amrhein, Chantal and Del, Maksym and Fishel, Mark},
	booktitle = {Proceedings of the Second Conference on Machine Translation},
	title = {{C-3MA: Tartu-Riga-Zurich Translation Systems for WMT17}},
	publisher = {Association for Computational Linguistics},
	address={Copenhagen, Denmark},
	year = {2017}
}
```