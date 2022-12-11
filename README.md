# Bug Triager using Knowledge Graph

## Problem Statement
Recently, bug fixing has become an important part of software maintenance. In large-scale projects, devs rely on bug reports to guide any bug-fixing activities. In our project, we are going to recommend a suitable dev who could resolve the bug in the most efficient way; such that the tossing length is minimized along with a knowledgeable dev who matches the requirements of solving a particular bug. 
## Significance of the problem
Due to a great number of bug reports submitted into the bug repository, the workload of the triagers who are responsible for arranging devs to fix the given bugs is very high. In order to reduce the triagers' workload, a number of approaches (e.g. ML algorithms and social network metrics) were proposed to study who should fix the bug report.
Surveys suggest that making the bug fixing process more efficient would reduce evolution effort and lower software production costs.
### Empirical Study
Reports indicate that, on average, the Eclipse project takes about 40 days to assign a bug to the first dev, and then it takes an additional 100 days or more to reassign the bug to the second dev. Similarly, in the Mozilla project, on average, it takes 180 days for the first assignment and then an additional 250 days if the first assigned dev is unable to fix it. These numbers indicate that the lack of effective, automatic assignment and toss reduction techniques results in considerably high effort associated with bug resolution.
## Brief Description of the Solution Approach
The basis of our work starts with using a graph based approach by creating a more visual notation of bugs and devs. We have three kinds of connections between bugs, skills and devs. The bugs and skills required to solve it, dev to dev showing who tossed the bug to whom, bugs initially assigned to which dev and the dev who solved it. We run Cypher Queries to return the ranked list of devs to recommend to a bug. A dev with who tosses less bugs is allotted higher rank in the list. 


## Building the KG 
Connect to the Neo4j database using the Python driver.
![image](https://user-images.githubusercontent.com/54329870/206886945-2d76dd19-5843-45f3-8d6f-cca96af4a635.png)

Defining the nodes and relationships to create in the graph using Cypher query language. This can include creating nodes for developers, bugs, priorities, components, and severities, as well as defining the relationships between these nodes.
![image](https://user-images.githubusercontent.com/54329870/206886965-5592255c-1d76-4d41-85ff-7cdcfe853dc4.png)

Execute the Cypher queries using the Python driver to create the nodes and relationships in the graph.
Use additional Cypher queries to query the graph and retrieve information about the relationships between the nodes.
![image](https://user-images.githubusercontent.com/54329870/206886968-4f29f33b-aaef-45d9-91b4-a8c75dae601f.png)


## 4.2.5  Cypher Queries Answered 
4.2.5.1. get all the dev who can solve swt issues
This Cypher query is used to find all developers who have resolved bugs related to the "swt" component. The query first matches the component node, bug node, and developer node that are relevant to the "swt" component. It then returns the developer node, which represents the developers who have resolved bugs related to the "swt" component. This query can be used to identify the developers who have expertise in fixing bugs related to the "swt" component, which can be useful for assigning new bugs to the most suitable developers.
![image](https://user-images.githubusercontent.com/54329870/206886972-152aa7db-4785-4a26-b579-1c90649cea82.png)

Fig 4.8
4.2.5 .2. get all the dev who can solve “swt” issues considering  priority and severity
This Cypher query is similar to the previous one, but it adds additional criteria to rank the recommended developers. The query first matches the component node, bug node, and developer node that are relevant to the "swt" component. It then matches the priority and severity nodes for each of these bugs, and uses these nodes to rank the recommended developers.

The developers are ranked based on the priority and severity of the bugs that they have resolved, with developers who have resolved higher priority and higher severity bugs being ranked higher. The results are then returned in descending order based on this ranking, so that the developers who have resolved the most critical bugs are returned first. This query can be used to identify the most experienced and skilled developers for fixing bugs related to the "swt" component, which can be useful for assigning new bugs to the most suitable developers.
![image](https://user-images.githubusercontent.com/54329870/206886978-9c99a91b-8e02-4bdb-a45b-b1f56d6974de.png)


Fig 4.9
4.2.5.3.get all the dev who can solve swt issues order by severity & priority and No total tosses done

This Cypher query is similar to the previous ones, but it adds another criterion for ranking the recommended developers. The query first matches the component node, bug node, and developer node that are relevant to the "swt" component. It then calculates the degree of the developer node, which represents the number of times that the developer has tossed a bug to another developer.

Next, the query matches the priority and severity nodes for each of these bugs, and uses these nodes to rank the recommended developers. The developers are ranked based on the priority and severity of the bugs that they have resolved, as well as the number of times that they have tossed a bug to another developer. Developers who have resolved higher priority and higher severity bugs, and have tossed fewer bugs to other developers, are ranked higher. The results are then returned in descending order based on this ranking, so that the developers who have resolved the most critical bugs and tossed the fewest bugs are returned first. This query can be used to identify the most experienced, skilled, and reliable developers for fixing bugs related to the "swt" component, which can be useful for assigning new bugs to the most suitable developers.




![image](https://user-images.githubusercontent.com/54329870/206886983-964df817-f80f-42cd-8f0c-ed56a60bba90.png)


Fig 4.10
4.2.5.4. get all the dev who can solve swt issues order by severity & priority & no of resolved bug
This Cypher query is similar to the previous ones, but it adds another criterion for ranking the recommended developers. The query first matches the component node, bug node, and developer node that are relevant to the "swt" component. It then calculates the degree of the developer node, which represents the number of times that the developer has tossed a bug to another developer.

Next, the query matches the priority and severity nodes for each of these bugs, and uses these nodes to rank the recommended developers. The developers are ranked based on the priority and severity of the bugs that they have resolved, the number of times that they have tossed a bug to another developer, and the total number of bugs that they have resolved. Developers who have resolved higher priority and higher severity bugs, have tossed fewer bugs to other developers, and have resolved more bugs overall, are ranked higher. The results are then returned in descending order based on this ranking, so that the developers who have the most experience, skill, reliability, and success in resolving bugs related to the "swt" component are returned first. This query can be used to identify the most suitable developers for fixing bugs related to the "swt" component, which can be useful for assigning new bugs to the most appropriate developers.

![image](https://user-images.githubusercontent.com/54329870/206886987-63418674-db72-4d7c-9210-b67d225d56d6.png)

Fig 4.11
4.2.5.5. adamic adar on “swt: component and developer
the "swt" component and the developer nodes. The Adamic-Adar score is a measure of the similarity between the two nodes based on their connections to other nodes in the graph.

The query first matches the "swt" component node and the developer nodes. It then filters these nodes to only include pairs of nodes where the ID of the "swt" component node is less than the ID of the developer node, and where there is no existing relationship between the two nodes. This is to avoid calculating the Adamic-Adar score for the same pair of nodes multiple times, or for relationships that already exist in the graph.

Next, the query calculates the Adamic-Adar score for the relationship between the "swt" component node and the developer node, using the gds.alpha.linkprediction.adamicAdar function. This function takes two nodes as input, and returns the Adamic-Adar score for the relationship between them.

Finally, the query returns the calculated Adamic-Adar scores, along with the "swt" component node and the developer node, in descending order based on the Adamic-Adar score. The results are limited to the top 10 pairs of nodes with the highest Adamic-Adar score, to make it easier to view and interpret the results.


![image](https://user-images.githubusercontent.com/54329870/206886992-aef595b8-1312-4306-bbc1-975ac3eccc45.png)

Fig 4.12
Table 4.1 Ranking of Developers according to adamic adar score
![image](https://user-images.githubusercontent.com/54329870/206886998-997e6023-f929-4c2b-b0dc-4a681b13f7e3.png)


4.2.5.6. common neighbors b/w swt and   dev          
This Cypher query is used to calculate the number of common neighbors for the relationship between the "swt" component and the developer nodes. The number of common neighbors is a measure of the similarity between the two nodes based on the nodes that they share connections with in the graph.

The query first matches the "swt" component node and the developer nodes. It then calculates the number of common neighbors for the relationship between the "swt" component node and the developer node, using the gds.alpha.linkprediction.commonNeighbors function. This function takes two nodes as input, and returns the number of common neighbors for the relationship between them.

Finally, the query returns the calculated number of common neighbors, along with the "swt" component node and the developer node, in descending order based on the number of common neighbors. The results are limited to the top 10 pairs of nodes with the highest number of common neighbors, to make it easier to view and interpret the results.

This query can be useful for identifying the developers who have the most similar interests and expertise to the "swt" component, based on the shared connections between these nodes in the graph. The number of common neighbors can be used as a measure of the similarity between the two nodes, which can be useful for recommending developers to work on bugs related to the "swt" component.
                         
![image](https://user-images.githubusercontent.com/54329870/206887023-4f95428e-31de-4460-b6f1-23e8592230ff.png)
  
Fig 4.13
![image](https://user-images.githubusercontent.com/54329870/206887037-493e6116-6e78-45a4-baf5-93dc9f8eb967.png)

Table 4.2 common neighbors b/w swt and   dev  

4.2.5.7.
This Cypher query is used to recommend developers for a particular bug based on the component, priority, and severity of the bug. The query first matches the component node, bug node, and developer node that are relevant to the given bug. It then calculates the degree of the developer node, which represents the number of times that the developer has tossed a bug to another developer.

Next, the query matches the priority and severity nodes for the given bug, as well as any developer nodes that have been tossed to by the current developer. It then calculates the Adamic-Adar score for the relationship between the component node and the developer node, which is a measure of the similarity between the two nodes based on their connections to other nodes in the graph.

Finally, the query returns the recommended developers, along with their Adamic-Adar score, the number of times that the developer has resolved bugs with the same severity as the given bug, and the total number of times that the developer has tossed a bug to another developer. The recommended developers are ranked based on a combination of these three factors, with developers who have a higher Adamic-Adar score, have resolved more bugs with the same severity, and have tossed fewer bugs to other developers being ranked higher. The results are then returned in descending order based on this ranking.

Query
![image](https://user-images.githubusercontent.com/54329870/206887045-98ad783a-1014-40da-98d0-e6a65e5cf986.png)

Fig 4.14
Graph 
![image](https://user-images.githubusercontent.com/54329870/206887049-78a8347a-69a7-4701-86ad-ee29e206f2ba.png)

Fig 4.15





![image](https://user-images.githubusercontent.com/54329870/206887052-cce53c41-560d-4f0f-9714-2c6b10203288.png)

Table 4.3 Ranked Result

