import json
from neo4j import GraphDatabase
import logging
import csv
from neo4j.exceptions import ServiceUnavailable

class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

# ! For tossing graph
    def create_friendship(self, dev1, dev2):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, dev1,dev2)
            for row in result:
                print("Created Node between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, dev1,dev2):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MERGE (p1:Dev { name: $dev1 }) "
            "MERGE (p2:Dev { name: $dev2 }) "
        )

        relationQuery=(
            "CREATE (p1)-[:issue_tossed_to]->(p2)"
        )

        returnQueryVar="RETURN p1,p2"

        query+=relationQuery
        result = tx.run(query,dev1=dev1,dev2=dev2)
        query+=returnQueryVar
      
        
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
        
    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    # ! for bug info
    def create_bug_info(self, bugId,component,develoeper,severity,priority,resolvedBy):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_bugfriendship, bugId,component,develoeper,severity,priority,resolvedBy)
            for row in result:
                print("Created Node between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_bugfriendship(tx, bugId,component,develoeper,severity,priority,resolvedBy):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MERGE (p1:bugId { name: $bugId }) "
            "MERGE (p2:component { name: $component }) "
            "MERGE (p3:Dev { name: $develoeper }) "
            "MERGE (p4:severity { name: $severity }) "
            "MERGE (p5:priority { name: $priority }) "
            "MERGE (p6:Dev { name: $resolvedBy }) "
        )

        relationQuery=(
            "CREATE (p6)-[:resolved]->(p1)"
            "CREATE (p1)-[:has_component]->(p2)"
            "CREATE (p1)-[:has_severity]->(p4)"
            "CREATE (p1)-[:priority]->(p5)"
        )

        returnQueryVar="RETURN p1,p2"

        query+=relationQuery
        result = tx.run(query,bugId=bugId,component=component,develoeper=develoeper,severity=severity,priority=priority,resolvedBy=resolvedBy)
        query+=returnQueryVar
      
        
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
        
    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    # ! for adding resolved property
    def addPropertyResolved(self, dev, resolved_count):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_bugfriendship, dev, resolved_count)
            for row in result:
                print("Created Node between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_bugfriendship(tx, dev, resolved_count):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MATCH (p1:Dev{name:$dev})"
            
        )

        relationQuery=(
            "SET p1.resolved_count = $resolved_count"
        )

        returnQueryVar="RETURN p1"

        query+=relationQuery
        result = tx.run(query,dev=dev,resolved_count=resolved_count)
        query+=returnQueryVar
      
        
        try:
            return [{"p1": row["p1"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
        
    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))
    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]
    


def buildGraph():
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "EAFSDd8zrRrc66g"
    app = App(uri,user,password)
    tossed_data = open("OutputFiles/toss_data.txt", "r", encoding="utf8")
    stemmed_input = open("OutputFiles/stemmed_input.txt", "r", encoding="utf8")
    severity_json = open("Dataset/JSON/severity.json", "r", encoding="utf8")
    priority_json = open("Dataset/JSON/priority.json", "r", encoding="utf8")
    resolution_json = open("Dataset/JSON/resolution.json", "r", encoding="utf8")
    
    output_file = open("curatedInput/toss_data.txt", "w", encoding="utf8")
    textclass_file = open("curatedInput/text_class.txt", "w", encoding="utf8")
    
    

    set_of_tossed_develoeprs =set()
    
    # read json data
    severity_data = json.load(severity_json)
    priority_data = json.load(priority_json)
    resolution_data = json.load(resolution_json)

    #  Build graph for top 100 entires for which we have reasonable data
    count =0;
    # get bug id, short desc, component, developer assigned to
    for line in stemmed_input:
        bug_info = line.split(",")
        if(len(bug_info)==5):
            bugId= bug_info[0]
            bug_description= bug_info[1]
            component= bug_info[2]
            develoeper= bug_info[3].lower().strip()
            # find seviarity
            try:
                severity = severity_data["severity"][bugId.strip()][0]['what'] 
            except KeyError: 
                pass
            # find priority
            try:
                priority = priority_data["priority"][bugId.strip()][0]['what']
                if(priority==None):
                    priority="P0"    
            except KeyError: 
                pass
            # find who resolved which bug
            try:
             resolvedBy = resolution_data["resolution"][bugId.strip()][0]['who']
            except KeyError: 
                pass
            if(severity!=None and priority!=None ):
                count+=1;
                # build relations here
                print(bug_info)
                # print(severity)
                # print(priority)
                # print(resolvedBy)
                set_of_tossed_develoeprs.add(develoeper)
                # print(develoeper)
                entry=bug_description+","+component
                entry+="\n"
                textclass_file.write(entry)  
                # app.create_bug_info(bugId,component,develoeper,severity,priority,develoeper)
                if(count>=100):
                    break
                

        # for buidling tossing graph between develeopers 
    print(len(set_of_tossed_develoeprs))
    counter =0;
    for line in tossed_data:
        tossInfo = line.split(",")

        if(tossInfo[1].lower().strip() in set_of_tossed_develoeprs or tossInfo[1].lower().strip() in set_of_tossed_develoeprs):
        # if(1):
            entry = ""+tossInfo[1]+"," +tossInfo[2]
            counter+=1
            entry+="\n"
            output_file.write(entry)  
            # app.create_friendship(tossInfo[1],tossInfo[2])
            print(entry)
        if(counter>100):
            output_file.write(entry)
            break
    print(counter)
    tossed_data.close()
    stemmed_input.close()
    severity_json.close()
    priority_json.close()
    app.close()

def assignResolved():
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "amit"
    app = App(uri,user,password)
    developer_resolved_count = open("OutputFiles/developer_resolved_count.txt", "r", encoding="utf8")
    app.close()
    for line in developer_resolved_count:
        but_toss_info = line.split(",")
        dev_name = but_toss_info[0]
        total_tosses = but_toss_info[1]
        total_assignments = but_toss_info[2]
        total_resolved = but_toss_info[3]
        app.addPropertyResolved(dev_name,total_resolved)
        print(dev_name,total_resolved)

if __name__ == '__main__':
    # buildGraph()
    assignResolved()