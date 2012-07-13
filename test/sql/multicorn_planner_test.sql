CREATE EXTENSION multicorn;
CREATE server multicorn_srv foreign data wrapper multicorn options (
    wrapper 'multicorn.testfdw.TestForeignDataWrapper'
);
CREATE user mapping for postgres server multicorn_srv options (usermapping 'test');

-- Test for two thing: first, that when a low total row count, 
-- a full seq scan is used on a join.
CREATE foreign table testmulticorn (
    test1 character varying,
    test2 character varying
) server multicorn_srv options (
    option1 'option1'
);

explain select * from testmulticorn;

explain select * from testmulticorn m1 inner join testmulticorn m2 on m1.test1 = m2.test1;

DROP foreign table testmulticorn;

-- Second, when a total row count is high 
-- a parameterized path is used on the test1 attribute.
CREATE foreign table testmulticorn (
    test1 character varying,
    test2 character varying
) server multicorn_srv options (
    option1 'option1',
    test_type 'planner'
);

explain select * from testmulticorn;

explain select * from testmulticorn m1 inner join testmulticorn m2 on m1.test1 = m2.test1;


DROP EXTENSION multicorn cascade;
