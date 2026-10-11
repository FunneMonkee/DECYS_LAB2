# DECYS_LAB2

Arduino 35

## Development password / Dan's Password
Answer:

To get Dan's password a timing attack was used.
Starting from the length, we created a python script to send N requests to the arduino and measure the time each response took.
For the length we could infer based on a boxplot created from the request/response data from an earlier version of the script, where we simply timed each request and got the median of the mins (5-20 requests per length) and.
For the actual password the script used for the length was not enough. So we altered it to create deltas based on the timing difference of a full string (length 13 all 'z') and each attempt/request.
This new version of the script also made measuring the legnth a lot faster than before.

## Firmware

## Confidential Information / Alan's Password
Answer:

To get Alan's password, after logging in with Dan's password, we dumped the data and simply looked for Alan's name, the password was the string that followed.

## Identify Cryptographic Assets

## Find the pot of gold / c&c Password
Answer:

The hash has a single result in the rainbow table, so a quick search got to the result.
