# :books:Vocab Learner
A free software for learning vocabularies (Windows only)

# Installation
1. Download the folder **build_v1.1**
2. Run **VocabTrainer.exe** to launch the program

> If the program doesn't run correctly, install this package:\
> [Visual C++ 2010 Redistributable Package (32 bit)](https://www.microsoft.com/en-gb/download/details.aspx?id=5555) or,\
> [Visual C++ 2010 Redistributable Package (64 bit)](https://www.microsoft.com/en-us/download/details.aspx?id=14632)

# Usage
## Program Menu
- Click `Open` to choose a vocabulary list
- Click `Review` to review mistakes from the last practice
- Click `Learn` to practice a vocabulary list without recording mistakes
- Press `esc` to exit the current practice

## Word List
All vocabulary entries should follow the template and save as a **.csv** file:

> Vocabulary lists that contain foreign characters (such as Mandarin, Japanese, etc.) are allowed; however, select **UTF-8** as the file encoding format when saving the file

### Template
Vocabulary, Definition, (n.), (v.), (adj.), (adv.)  `WARNING: Do not modify this row`\
word#1, def#1, 1, , , , \
word#2, def#2, , , 1, 1 \
word#3, def#3, , 1, , \
word#4, def#4, , , , 1 \
word#5, def#5, , , 1, \

### Visual representation
| Vocabulary |	Definition | (n.) | (v.) | (adj.) | (adv.) |
| :--------: | :---------: | :--: | :--: | :----: | :----: |
|   word#1   |    def#1    |   1  |      |        |        |
|   word#2   |    def#2    |      |      |    1   |    1   |
|   word#3   |    def#3    |      |   1  |        |        |
|   word#4   |    def#4    |      |      |        |    1   |
|   word#5   |    def#5    |      |      |    1   |        |
