# BugInjector

generate 810-v4.ipynb
- tokenizer (pretrained)
- dataloader
- compute bleu score
- evaluate the model
- training
- generate bug
- evaluate the generated bugs

after24epoch _train_samples.txt
Some generated bugs using patched code in training dataset as input.

after24epoch _val_samples.txt
Some generated bugs using patched code in validation dataset as input.

star.csv
The gathered list of top c/cpp projects on GitHub.


moststarORfork.py
This is used to collect the list.


About data Collection.
1. DownloadFromGithub.py
To download the github project and get the code before committed and after committed.
The code will be stored in diff.

2. Remove Header(#include), so that the file can be processed with gcc compiler without too many errors.

3. Processed by GCC to remove the useless part in gcc.

4.Transfer to CSV file. There are several variables. UP is the number of Added lines. Down is the number of Deleted lines. Index is the start of commit
