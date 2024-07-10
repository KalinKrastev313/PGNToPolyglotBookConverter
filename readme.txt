This is a python only way to create a polyglot chess opening book from a pgn file, without using additional software.
As this is python implementation, it is slower than some other options.
More efficient, but requiring several software installations method is described here:
https://www.youtube.com/watch?v=rskcUNoirPU&ab_channel=SteveMaughan by Steve Maughan

This project uses the polyglot writer written by Torsten Hellwig:
https://github.com/Torom/polyglot-writer/blob/main/polyglot_writer.py
Slight tweaks on it are possible.

In order to use the converter, you should first paste a .pgn file in the project directory.
For example, you can create a PGN file from your lichess game, when you open your profile there and go to "export games".
Note that polyglot books are made for standard games, so it is wise to exclude other chess variants from the export.
Nevertheless, the converter would ignore entries where other than the classic starting position is specified.
Next step is to run the main.py file. Before this, you can manually change the names of the input (pgn_file_name) and
output (result_file_name) in the main.py file.

Polyglot entries have chess position, corresponding move to it, weight, and learn attributes.
In this implementation, the weight is simply derived from the number of occurrences of a (position, move) pair.

The converter is practical to use with only a few thousand games and the execution might take 10-15 minutes.
All the data is stored in the working memory, before being written down in the book.
This means that if the converter is used for a base of several million games with size of several GBs,
substantial amount of RAM would be needed.

If there are any bad pgn entries, they would be printed in the console and further investigation might be needed if you insist on including them.

