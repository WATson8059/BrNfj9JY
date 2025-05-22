# Introduction

Let's compare the most common surrogate primary key strategies:

IDENTITY
SEQUENCE


The IDENTITY generator allows an integer/bigint column to be auto-incremented on demand. 
The increment process happens outside of the current running transaction, 

The increment process is very efficient since it uses a database internal lightweight 
locking mechanism as opposed to the more heavyweight transactional course-grain locks.

statement. This restriction is hindering the transactional write-behind strategy adopted by Hibernate. 
> For this reason, Hibernate cannot use JDBC batching when persisting entities that are using the IDENTITY generator.
> Also the IDENTITY generator strategy doesn’t work with the TABLE_PER_CLASS inheritance model because there could be 
> multiple subclass entities having the same identifier and a base class query will end up retrieving 
> entities with the same identifier (even if belonging to different types).

## SEQUENCE

SEQUENCES are much more flexible than IDENTIFIER columns because:

- A SEQUENCE is table free and the same sequence can be assigned to multiple columns or tables
- A SEQUENCE may preallocate values to improve performance
- A SEQUENCE may define an incremental step, allowing us to benefit from a “pooled” Hilo algorithm
- A SEQUENCE doesn’t restrict Hibernate JDBC batching
- A SEQUENCE doesn’t restrict Hibernate inheritance models

There is another database-independent alternative to generating sequences. One or multiple tables can be used to hold 

for synchronizing multiple concurrent id generation requests.

This is made possible by using row-level locking which comes at a higher cost than IDENTITY or SEQUENCE generators.

The sequence must be calculated in a separate database transaction and this requires the IsolationDelegate mechanism, 
For local transactions, it must open a new JDBC connection, therefore putting more pressure on the current connection pooling mechanism.
For global transactions, it requires suspending the current running transaction. 
After the sequence value is generated, the actual transaction has to be resumed. This process has its own cost, 

[Why you should never use the TABLE identifier generator with JPA and Hibernate](https://vladmihalcea.com/why-you-should-never-use-the-table-identifier-generator-with-jpa-and-hibernate/)

    @GeneratedValue(strategy = GenerationType.AUTO)
To fix that we could use

    @GeneratedValue(
        strategy= GenerationType.AUTO,
        generator="native"
    )
    @GenericGenerator(
        name = "native",
    )
    private Long id;

## Conclusion

Our services need to run on MySQL (which does not support database sequences), 
as well as Oracle and SQL Server, so portability is our primary concern.
As previously explained, the TABLE identifier generator is database-independent but 
does not scale, so we will avoid it. 

Check how we achieve that:

