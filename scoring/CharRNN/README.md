# CharRNN scripts
Scripts for getting perplexity from [CharRNN](https://github.com/karpathy/char-rnn)

### measure_file_perplexity.lua
Scores an input text file by line and outputs tab separated sentence numbers and perpelxity scores one per line.

Usage:
	th measure_file_perplexity.lua \
	-data_path <input_text_file> \
	<language_model> \
	> <output_perplexity_file>


Example:
	th measure_file_perplexity.lua \
	-data_path ./news.NMT.en.ab \
	cv/lm_4M3_epoch4.45_0.9295.t7 \
	> ./news.NMT.en.ab.ppl