# Solring

Solring is an easy-to-use import tool from solr to local storage. By supporting various options we can create custom
queries and save from a running Solr server to a file.

## How it works

```
$ pip install solring==0.0.2

$ solring --help  
usage: Solring.py [-h] [--version] --url URL [--output OUTPUT]
                  [--save_format {csv,txt}] --core CORE [--rows ROWS] [-fl FL]
                  [-q Q] [-fq FQ] [--score] [--qt QT]
                  {group} ...

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --url URL, -u URL     The host:port of the running solr.
  --output OUTPUT, -o OUTPUT
                        Output file name.
  --save_format {csv,txt}, -sf {csv,txt}
                        File type of saved records. Default is txt.
  --core CORE, -c CORE  The core/collection in solr.
  --rows ROWS, -r ROWS  The number of row numbers returned. By default, Solr
                        returns 5 batches at a time to save records.
  -fl FL                Field list to retrieve. By default, Solr returns the
                        id field.
  -q Q                  Search query. By default, Solr returns all records.
  -fq FQ                Filter queries.
  --score               Learn score of each record in a score field.
  --qt QT               solr request handle to query on, default is '/select'.

group command:
  {group}               group help
```

The group command parameters:

```
$ solring group --help
usage: Solring.py group [-h] --group_fl GROUP_FL --group_agg
                        {mean,min,max,count} --group_column GROUP_COLUMN

optional arguments:
  -h, --help            show this help message and exit
  --group_fl GROUP_FL   The field(s) we want to use to group by.
  --group_agg {mean,min,max,count}
                        Aggregation functions to use in group by. Default is
                        count.
  --group_column GROUP_COLUMN
                        The field(s) where we want to aggregate.
```

Create a custom query where the query we search for is 'boat', we have two filter queries, and we only need to know
their ids and titles as follows:

```
solring --url http://127.0.0.1:8983\ 
 -c boats \
 -fq "cabin:[6 TO *]" \
 -fq harbors:marmaris \
 -q boat \
 -fl id,title,boat_size,group_id

$ ls 
output.txt
```

Let's now aggregate the above request with group options. We can learn the min and max of boats_size of each group:

```
solring --url http://127.0.0.1:8983\ 
 -c boats \
 -fq "cabin:[6 TO *]" \
 -fq harbors:marmaris \
 -q boat \
 -r 100 \
 -fl id,title,boat_size,group_id \
 -o groupby_boats \
 group --group_agg min --group_agg max --group_column boat_size --group_fl group_id

$ ls æ
groupby_boats.txt
```
## LICENSE

MIT


