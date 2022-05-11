cd ./input/

wget https://production-media.paperswithcode.com/about/papers-with-abstracts.json.gz
gzip -d papers-with-abstracts.json.gz 

wget https://production-media.paperswithcode.com/about/links-between-papers-and-code.json.gz
gzip -d links-between-papers-and-code.json.gz

wget https://production-media.paperswithcode.com/about/evaluation-tables.json.gz
gzip -d evaluation-tables.json.gz

wget https://production-media.paperswithcode.com/about/methods.json.gz
gzip -d methods.json.gz

wget https://production-media.paperswithcode.com/about/datasets.json.gz
gzip -d datasets.json.gz