# Content-addressable storage

Content-addressable storage (CAS) is a type of data storage system that uses unique identifiers called "hashes" to retrieve and manage data. In a CAS system, each piece of data is assigned a unique hash value based on its content. This hash value is used as the data's address, allowing for quick and easy retrieval of the data when needed.

CAS systems typically use algorithms such as SHA-1 or MD5 to generate these unique hashes. These algorithms ensure that each hash is unique, even if two pieces of data have the same content. This means that data can be easily identified and retrieved based on its content, rather than its location within the storage system.

CAS systems are often used in distributed systems where data is stored across multiple locations. Because the data's hash value is used as its address, it can be easily retrieved from any location within the system. This makes CAS systems highly efficient and scalable, allowing for large amounts of data to be quickly and easily accessed.

See also [Content-addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage).

> This page was created with help from OpenAI