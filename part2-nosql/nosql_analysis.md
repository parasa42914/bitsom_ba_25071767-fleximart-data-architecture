## Section A: 
Limitations of RDBMS
The current relational database (MySQL/PostgreSQL) struggles with highly diverse product catalogs due to its **rigid schema**. When products have unique attributes (like RAM for laptops vs. size for shoes), an RDBMS requires either a "Sparse Table" with many NULL values or a complex "Entity-Attribute-Value" (EAV) model, which degrades performance and complicates queries.

Frequent schema changes become a bottleneck; adding a new product category requires an ALTER TABLE command, which can lock the database during production. Furthermore, storing customer reviews requires a separate table and expensive JOIN operations. This "impedance mismatch" between application objects and database rows makes it difficult to retrieve a product and all its nested reviews in a single, efficient operation.

##

## Section B: 
NoSQL Benefits
MongoDB solves these issues through its **document-oriented model**. Its **flexible schema** allows each document (product) to have its own unique set of fields without affecting other records. This enables "polymorphic" data where electronics and apparel coexist in the same collection seamlessly.

By using **embedded documents**, FlexiMart can store reviews as an array directly within the product document. This allows for "single-document atomicity," where a single read operation retrieves the product and all its metadata/reviews. Finally, MongoDB’s **horizontal scalability** (sharding) allows the system to distribute data across multiple servers, handling massive growth in traffic and data volume much more effectively than the vertical scaling typical of RDBMS.

##
## Section C: Trade-offs
**Lack of Complex Joins:** MongoDB does not support traditional relational joins efficiently. While $lookup exists, it is an aggregation stage and is significantly slower than SQL joins for complex, multi-table reporting.

**Data Redundancy:** To maintain performance, MongoDB often requires "denormalization" (duplicating data). This increases storage requirements and makes it harder to ensure data consistency across multiple documents when a shared attribute (like a category name) changes.