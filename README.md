# Solring

Solring is an easy-to-use import tool from solr to local storage. By supporting various options we can create custom queries and save from a running Solr server to a file.    

## How it works

```
$ pip install solring

$ solring --help                                                                                                                [20:30:23]
usage: solring [-h] [--version] --url URL [--output OUTPUT] [--save_format {csv,txt}] --core CORE [--rows ROWS] [-fl FL] [-q Q] [-fq FQ] [--score] [--qt QT]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --url URL, -u URL     The host:port of the running solr
  --output OUTPUT, -o OUTPUT
                        Output file name
  --save_format {csv,txt}, -sf {csv,txt}
                        File type of saved records
  --core CORE, -c CORE  The core/collection in solr
  --rows ROWS, -r ROWS  The number of row numbers returned
  -fl FL                Field list to retrieve
  -q Q                  Search query
  -fq FQ                Filter queries
  --score               Learn score of each record
  --qt QT               solr request handle to query on, default is '/select'
```

Create a custom query where the query we search for is 'boat', we have two filter queries, and we only need to know their ids and titles as follows:

```
solring --url http://127.0.0.1:8983\ 
 -c boats \
 -fq "cabin:[6 TO *]" \
 -fq harbors:marmaris \
 -q boat \
 -fl id,title

$ ls 
output.txt
```


