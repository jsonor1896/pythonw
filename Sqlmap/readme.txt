# sqlmap/data/xml/boundaries.xml
<root>
    <boundary>
            From which level check for this test.

            Valid values:
            1: Always (<100 requests)
            2: Try a bit harder (100-200 requests)
            3: Good number of requests (200-500 requests)
            4: Extensive test (500-1000 requests)
            5: You have plenty of time (>1000 requests)
        <level>4</level>

            In which clause the payload can work.

            Valid values:
            0: Always
            1: WHERE / HAVING
            2: GROUP BY
            3: ORDER BY
            4: LIMIT
            5: OFFSET
            6: TOP
            7: Table name
            8: Column name
            9: Pre-WHERE (non-query)
        <clause>1</clause>

        Where to add our '<prefix> <payload><comment> <suffix>' string.

        Valid values:
            1: When the value of <test>'s <where> is 1.
            2: When the value of <test>'s <where> is 2.
            3: When the value of <test>'s <where> is 3.
        <where>1,2</where>

        What is the parameter value type.

        Valid values:
            1: Unescaped numeric
            2: Single quoted string
            3: LIKE single quoted string
            4: Double quoted string
            5: LIKE double quoted string
            6: Identifier (e.g. column name)
        <ptype>2</ptype>
        <prefix>')</prefix>
        <suffix>[GENERIC_SQL_COMMENT]</suffix>
    </boundary>


    # 例子
    <boundary>
        <level>2</level>
        <clause>1</clause>
        <where>1,2</where>
        <ptype>1</ptype>
        <prefix>))</prefix>
        <suffix> AND (([RANDNUM]=[RANDNUM]</suffix>
    </boundary>
</root>

# sqlmap/data/xml/payloads/boolean_bind
    <test>
        <title></title>                 # Title of the test.
        <stype></stype>                 # SQL injection family type.
        <level></level>                 # From which level check for this test. 和 boundaries.xml中的level一致
        <risk></risk>                   # likelihood of a payload to damage the data integrity
        <clause></clause>               # In which clause the payload can work. 和 boundraies.xml中的clause一致

        Where to add our '<prefix> <payload><comment> <suffix>' string.

        Valid values:
            1: Append the string to the parameter original value
            2: Replace the parameter original value with a negative random
               integer value and append our string
            3: Replace the parameter original value with our string
        <where></where>
        <vector></vector>               # The payload that will be used to exploit the injection point.
        <request>
            <payload></payload>         # The payload to test for.
            <comment></comment>         # Comment to append to the payload, before the suffix.
            <char></char>               # Character to use to bruteforce number of columns in UNION query SQL injection tests.
            <columns></columns>         # Range of columns to test for in UNION query SQL injection tests.
        </request>
        <response>                      # How to identify if the injected payload succeeded.

            # Perform a request with this string as the payload and compare the response with the <payload> response.
            # Apply the comparison algorithm，useful to test for boolean-based blind SQL injections.
            <comparison></comparison>
            # Regular expression to grep for in the response body.
            # NOTE: useful to test for error-based SQL injection.
            <grep></grep>
            # Time in seconds to wait before the response is returned.
            # NOTE: useful to test for time-based blind and stacked queries
            SQL injections.
            <time></time>
            # Calls unionTest() function.
            # NOTE: useful to test for UNION query (inband) SQL injection.
            <union></union>
        </response>
        <details>
            <dbms></dbms>                           # What is the database management system (e.g. MySQL).
            <dbms_version></dbms_version>           # What is the database management system version (e.g. 5.0.51).
            <os></os>                               # What is the database management system underlying operating system.
        </details>
    </test>



















