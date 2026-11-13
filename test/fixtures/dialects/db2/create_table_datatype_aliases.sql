-- Db2 data type aliases for CREATE TABLE.
-- https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table

CREATE TABLE t_char_aliases (
    a CHAR VARYING(10),
    b CHAR LARGE OBJECT(1M),
    c VARCHAR(10) FOR BIT DATA,
    d CHAR(10) FOR BIT DATA
);

CREATE TABLE t_national (
    a NATIONAL CHAR(10),
    b NATIONAL CHARACTER(10),
    c NATIONAL CHAR VARYING(10),
    d NATIONAL CHARACTER VARYING(10),
    e NATIONAL CHAR LARGE OBJECT(1M),
    f NATIONAL CHARACTER LARGE OBJECT(1M)
);

CREATE TABLE t_nchar (
    a NCHAR(10),
    b NCHAR VARYING(10),
    c NCHAR LARGE OBJECT(1M),
    d NVARCHAR(10),
    e NCLOB(1M)
);

CREATE TABLE t_binary (
    a BINARY(10),
    b VARBINARY(10),
    c BINARY VARYING(10),
    d BLOB(1M),
    e BINARY LARGE OBJECT(1M)
);

SELECT CAST(a AS CHAR VARYING(10)) AS a FROM s;
