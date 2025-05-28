# web_challs

1. set up the website at your kali:
   gcc -o program program.c

2. run it: ./nameofprogram
3. go at: http://127.0.0.1:<port_that_runs_it>

4. try to find a vulnerability :)
-------------------------------------------------------------------------
examples:
1. usage of rand() or srand(): those provides the same random numbers every time you start the instance.
2. if there is a mechanism that sanitise the curl commands avoiding traversal dirs like /../.. try the:
   curl --path-as-is "http://94.237.51.19:43420/stats//../../../flag.txt"

the curl --path-as-is  στέλνει ακριβώς αυτό που γράφεις στο path, χωρίς να το καθαρίσει!!
