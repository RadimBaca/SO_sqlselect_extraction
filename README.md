# SQL Select Extraction and Analysis
This repository provides tools for straightforward extraction of the SQL Select statements from the [Posts.xml](https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z) file and their subsequent analysis. `Posts.xml` is a StackOverflow file that contains all the questions and answers in XML format.

## Usage
Pass a path to the `Posts.xml` file to the `postsxml_sql_extract.py` program. The program will generate `sqlcommands.txt` file with SQL Select on each line. 

```bash
python postsxml_sql_extract.py <path_to_posts.xml_file> 
```

The creation of `sqlcommands.txt` is a mandatory step for any subsequent SQL Select analysis. Once `sqlcommands.txt` is created you may collect different statistics.

### Percent of Window Function per Thousand Queries

```bash
python sql_WF_analysis.py sqlcommands.txt
``` 
