from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
from werkzeug.datastructures import FileStorage
import pandas
import datetime
import zipfile
import os
from flaskwebgui import FlaskUI


app = Flask(__name__)

# ui = FlaskUI(app)

# app.secret_key = "secret key" # for encrypting the session#It will allow below 16MB contents only, you can change it
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success/", methods=['POST'])
def success():
    if request.method=='POST':
        file=request.files["file"]
        # print(file)

        file_name = secure_filename(file.filename)
        # print(file_name)

        if file_name.endswith(".csv"):
            df = pandas.read_csv(file)
        else:
            df = pandas.read_excel(file, sheet_name=0)

        df2 = df[['Name', 'Lineitem name', 'Shipping Name', 'Shipping Address1', 
        'Shipping Address2', 'Shipping City', 'Shipping Zip', 'Shipping Province', 
        'Shipping Country']].copy()

        df2.set_index("Name", inplace=True, drop=True)

        con = []
        # print(df2.columns)
        df2["Shipping Country"].fillna(" ", inplace=True)
        

        for c in df2["Shipping Country"].unique():
            con.append(c)
            # print(c)
        

        for i in range(0, len(con)-1):
            for val in df2["Shipping Country"]:
                if val == con[i]:
                    with open("tmp/file_{}.csv".format(val), 'w') as file:
                        df = df2.loc[df2['Shipping Country'] == val]
                        df.to_csv(file)
                    


        return render_template("index.html", btn="download.html")


@app.route("/download-file")
def download():
    d = "tmp"
    file_list = []
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            file_list.append(full_path)
        zipobj = zipfile.ZipFile('tmp/files.zip', 'w')
    for f in file_list:
        zipobj.write(f)
    zipobj.close()
    for f in file_list:
        if f != 'tmp\\files.zip':
            os.remove(f)


    return send_file('tmp/files.zip', attachment_filename='files.zip', as_attachment=True, cache_timeout=0)




if __name__ == "__main__":
    app.debug = True
    app.run()
    # FlaskUI(app).run()

    	
