import json
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

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
    password = "amit"
    app = App(uri,user,password)
    tossed_data = open("OutputFiles/toss_data.txt", "r", encoding="utf8")
    stemmed_input = open("OutputFiles/stemmed_input.txt", "r", encoding="utf8")
    severity_json = open("Dataset/JSON/severity.json", "r", encoding="utf8")
    priority_json = open("Dataset/JSON/priority.json", "r", encoding="utf8")
    resolution_json = open("Dataset/JSON/resolution.json", "r", encoding="utf8")
    # gets 
    for line in tossed_data:
        tossInfo = line.split(",")
        # print(tossInfo[1])
        # print(tossInfo[2])
        # app.create_friendship(tossInfo[1],tossInfo[2])

    # read json data
    severity_data = json.load(severity_json)
    priority_data = json.load(priority_json)
    resolution_data = json.load(resolution_json)

    # get bug id, short desc, component, developer assigned to
    for line in stemmed_input:
        bug_info = line.split(",")
        if(len(bug_info)==5):
            bugId= bug_info[0]
            bug_description= bug_info[1]
            component= bug_info[2]
            develoeper= bug_info[3]
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

    tossed_data.close()
    stemmed_input.close()
    severity_json.close()
    priority_json.close()
    app.close()


if __name__ == '__main__':
    buildGraph()