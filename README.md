# Attrib JSON to MongoDB Uploader
After converting raw attrib Lua files to JSON, these JSON files need to be uploaded to a document store DB (MongoDB) 
for use by the web app. 

A document store DB was chosen as attrib JSON files are multi-dimensional JSON with inconsistent
schemas and a large number of key/values. While they could be put in a RDBMS, these value should be read only and relations
between two attribs, like in the case of a reference from an entity to a weapon, are soft references by name and do 
not require foreign keys. A relational DB schema would be bloated and laborious for little gain as the expected retrieval 
pattern will involve almost entirely document retrievals by document key, and should not require any querying by data 
columns.

---
### Note
Version 1.2.11 of the mongodb for PHP package should still support PHP 5.4:\
https://pecl.php.net/package-info.php?package=mongodb&version=1.2.11