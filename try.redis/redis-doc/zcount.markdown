# ZCOUNT *key min max*

**TIME COMPLEXITY**:
O(log(N)+M) with N being the number of elements in the sorted set and M being the number of elements between min and max.

**DESCRIPTION**:
Returns the number of elements in the sorted set at key with a score between min and max.
The min and max arguments have the same semantic as described for ZRANGEBYSCORE.

**RETURN VALUE**: Integer reply: the number of elements in the specified score range.
