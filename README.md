# AI-1

# PA-1

Goal: The goal of this assignment is to take a complex new problem and formulate and solve it as a search. Formulation as search is an integral skill of AI that will come in handy whenever you are faced with a new problem. Heuristic search will allow you to find optimal solutions. Local search may not find the optimal solution, but is usually able to find good solutions for really large problems.

Scenario: Optimization of Conference Schedules
Assume that a conference has n papers accepted. Our job is to organize them in the best possible schedule. Let the
schedule have p parallel sessions at any given time, where each session has k papers, and there are a total of t time slots. We can safely assume that n = (t * p * k). For example, as per the figure below t = 3, p = 2 and k = 4.

Papers : 1,2,3,4
Papers : 5,6,7,8
Papers : 9,10,11,12
Papers : 13,14,15,16
Papers : 17,18,19,20
Papers : 21,22,23,24


Now a good schedule is one where most people would feel no conflict about which session to attend => (1) all papers in a session should be related to a single theme and (2) all papers in parallel sessions should be semantically as far away as possible to avoid conflicts.
To operationalize this intuition let us assume we are given a function representing the distance between two types/categories: d(t1, t2), such that d is between 0 and 1. We can similarly define a similarity between two, s(t1, t2) = 1 - d(t1, t2). 
Now we can define the goodness of a schedule as follows:
Sum(similarities of all pairs within a single time slot in the same session) + C.Sum(distances of all pairs within a single time slot in the parallel session).
In our example, the goodness will be computed as
G(Schedule) = s(1,2) + s(1,3) + s(1,4) + s(2,3) + s(2,4) + s(3,4) + s(5,6) + s(5,7) + s(5,8)
                        + s(6,7) + s(6,8) + s(7,8) + ……. + s(13,14) + …. + s(21,22) + ….. 
  + C x [d(1,13) + d(1,14)… d(2,13) + d(2,14) + … + d(5,17) + d(5,18) + …]

The constant C tradeoff between the importance of semantic coherence of one session versus reducing conflict across parallel sessions.

Your goal is to find a schedule with the maximum goodness.

Input:
Line 1: k: the number of papers per session
Line 2: p: number of parallel sessions
Line 3: t: number of time slots
Line 4: C: trade-off constant
Starting on the fifth line, we have space-separated lists of distances between every paper.
[Note: dist(x, y) = dist(y, x), and dist(x, x) = 0]


Sample Input:
2
2
1
1
0 0.4 0.8 1
0.4 0 0.6 0.7
0.8 0.6 0 0.3
1 0.7 0.3 0

Output:  
Your algorithm should return the max-goodness schedule as found within the desired time limit. The output format is a space-separated list of paper ids, where time slots are separated by bars, and parallel sessions are on different lines.

For the problem shown above, the optimal solution is clearly p1 and p2 in one session; and p3 and p4 in another. This will be represented as:
0 1 
2 3
Other equivalent ways to represent this same solution are:
1 0 
2 3 or
3 2 
0 1 or
2 3 
1 0 (etc)
All of these alternatives are equally valid.
Verify that for this problem the total goodness is 4.4.


# PA-2

Objective: Bayesian inference on the given data. 
Problem: Bayesian network is a directed acyclic graphical representation of a set of variables and their conditional dependencies. Each variable is represented as a node in the graph and a directed edge between the nodes represents the parent-child relationship between the considered nodes. In this assignment we will estimate probability distributions or parameters of a given network. For this, we will make use of a dataset containing samples of values observed for different variables. 
Input 
• Line 1: n : no. of variable or nodes (N1, N2, ...., Nn) 
• Line 2 to Line n + 1: Comma separated list of all possible values of variables N1 to Nn • Line n + 2 to Line 2n + 1: n × n matrix of 1’s and 0’s representing conditional dependencies, e.g. a value 1 at location (3,2) shows that N2 is conditionally dependent on N3 
• Line 2n + 2: m : no. of samples 
• Line 2n + 3 to Line 2n + 2 + m: Comma separated values observed for all variables (N1, N2, ...., Nn) for each sample. It may have some missing values denoted by ‘?’.
Sample input: 
3 
TRUE, FALSE 
TRUE, FALSE 
TRUE, FALSE 
0 0 1 
0 0 1 
0 0 0 
100 
TRUE, FALSE, TRUE 
FALSE, TRUE, FALSE 
. 
. 
. 
. 
There are three binary variables (N1, N2, N3) in this Bayesian network where N3 is conditionally dependent on N1 and N2. In other words, N1 and N2 are the parents of N3. 
Output 
Your program should learn the parameters (probability distributions of each variable) of the given network and return them in the following format 
Output format: Print n lines where Line 1 will contain probability distribution of variable N1, Line 2 will contain probability distribution of variable N2 and so on. Round off the probability value upto 4 decimal places. 
For the above problem the output is 
0.2 0.8 
0.4 0.6 
0.2 0.4 0.3 0.5 0.8 0.6 0.7 0.5 
This implies P(N1=TRUE) = 0.2, and P(N1=FALSE) = 0.8. Similarly P(N2=TRUE) = 0.4, and P(N2=FALSE) = 0.6. Further, P(N3=TRUE|N1=TRUE, N2=TRUE) = 0.2, P(N3=TRUE|N1=TRUE, N2=FALSE) = 0.4, P(N3=TRUE|N1=FALSE, N2=TRUE) = 0.3 and so on.
