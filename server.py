from flask import Flask        # to be installed
from flask import request
import mysql.connector

##
#   Create "server" item from Flask
#

app = Flask(__name__, static_folder="./build", static_url_path="/")

##
#   Create an object to be able to comunicate to the database, reader.
#   If there are problems, log and quit
#

try:
    conn = mysql.connector.connect(host="192.168.0.2", database="Covid-data", user="prova", password="prova")
    if conn.is_connected():
        print('Connected to MySQL database')
    else:
        print("Error while connecting to the database")
        quit()

    reader = conn.cursor()

except Exception:
    print("Error while connecting to the database")
    quit()

##
#   Create response for the GET "/api/raw" request
#

@app.route("/api/raw", methods=["GET"])
def raw():
    try:
        values = {
            "data": [],
            "variation": []
        }

        ##
        #   Get all the data from STORICO
        #

        reader.execute("SELECT * FROM STORICO ORDER BY Data")

        fields = [x[0] for x in reader.description][1:]

        for value in reader.fetchall():
            append = {}
            i = 0

            for item in value[1:]:
                append[fields[i]] = item
                i = i+1

            values["data"].append(append)

        ##
        #   Get all the data from VARIATION
        #

        reader.execute("SELECT * FROM VARIAZIONE ORDER BY Data")

        for value in reader.fetchall():
            append = {}
            i = 0

            for item in value[1:]:
                append[fields[i]] = str(item)
                i = i+1

            values["variation"].append(append)

        return values

    except Exception as e:
        print(e)
        return "error"

@app.route("/api/values", methods=["GET"])
def values():
    try:
        if "from" in request.args:
            fromDate = request.args.get("from")
        else:
            fromDate = False

        if "to" in request.args:
            toDate = request.args.get("to")
        else:
            toDate = False

        if "params" in request.args:
            params = request.args.get("params").split(",")
        else:
            return {}

        if "table" in request.args:
            table = request.args.get("table")
        else:
            return {}

        resultObj = {}

        for param in params:
            query = f"SELECT Data, Regione, {param} FROM {table}"
            if fromDate and toDate:
                query = f"{query} WHERE Data >= '{fromDate}' AND Data <= '{toDate}'"
            elif fromDate:
                query = f"{query} WHERE Data >= '{fromDate}'"
            elif toDate:
                query = f"{query} WHERE Data <= '{toDate}'"

            query = f"{query} ORDER BY Data"

            reader.execute(query)
            result = reader.fetchall()

            date = result[0][0]
            thisDate = {
                "data": date
            }
            paramReturn = []

            for i in range(len(result)):
                if result[i][0] == date:
                    thisDate[result[i][1]] = result[i][2]
                else:
                    date = result[i][0]
                    paramReturn.append(thisDate)
                    thisDate = {
                        "data": date,
                        result[i][1]: result[i][2]
                    }

            paramReturn.append(thisDate)

            resultObj[param] = paramReturn

        return resultObj

    except Exception as e:
        print(e)
        return "error"

@app.route("/")
def staticFolder():
	return app.send_satic_file("index.html")
