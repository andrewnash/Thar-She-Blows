import random
from flask import Flask, request, render_template
from gmplot import gmplot
from map_the_data import create_box
from windmill import generateReport
from table import create_table

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET'])
def create_box_get():
    return render_template('base_page.html')

@app.route('/', methods=['POST'])
def create_box_post():
    # Quick hack to get past flask templating becuase I don't have time to do that
    i = random.randint(1, 9999999999)
   
    # Get response from form
    lat1 = request.form.getlist('lat1')[0]
    lon1 = request.form.getlist('lon1')[0]
    lat2 = request.form.getlist('lat2')[0]
    lon2 = request.form.getlist('lon2')[0]
    
    tower_type = int(request.form.getlist('tower_type')[0])
    
    radioBoxes = dict()
    radioBoxes['heli'] = 'heli' in request.form
    radioBoxes['vessel'] = 'vessel' in request.form
    radioBoxes['diags'] = 'diags' in request.form
    radioBoxes['log'] = 'log' in request.form
    radioBoxes['upgrade'] = 'upgrade' in request.form

    # generate report
    result = generateReport((lon1, lat1), (lon2, lat2), radioBoxes, tower_type)
    
    # map box 
    windmill_lats, windmill_lons = create_box([(lon1, lat1), (lon2, lat2)])
    
    gmap = gmplot.GoogleMapPlotter(43.9, -66.1, 10)
    gmap.plot(windmill_lats, windmill_lons, 'cornflowerblue', edge_width=10)
    

    turbineInfo = result.get('towerList')
    wmLats  = []
    wmLongs = []
    for i in range(0, len(turbineInfo)):
        wmLats.append(turbineInfo[i][0])
        wmLongs.append(turbineInfo[i][1])
    gmap.scatter(wmLats, wmLongs, '#000000', size=400, marker=False)

    file_name = "templates/my_map" + str(i) + ".html"
    gmap.draw(file_name)

    create_table(result)
    
    with open(file_name, 'a') as outfile:
        with open('table.html') as infile:
            outfile.write(infile.read())
    # Return product
    return render_template("my_map" + str(i) + ".html")

