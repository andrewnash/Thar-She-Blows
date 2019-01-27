# import things
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    name = Col('Infastructure')
    description = Col('Quantity')
    cost = Col('Info')

# Get some objects
class Item(object):
    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost

def create_table(dict):      
 #   dict = {'area': 1, 'millNum': 2, 'nomPower': 3, 'nomPower5': 4, 'maintCost': 5, 'buildCost': 6, 'projTime': 7}
    items = [Item('Windmills', dict.get('millNum'), 'units'),
             Item('Area', dict.get('area'), 'm^2'),
             Item('Nominal Power', dict.get('nomPower'), 'MW'),
             Item('Nominal Power After 5 yr', dict.get('nomPower5'), 'MW'),
             Item('*MaxPower Acheivable', dict.get('powerAfterWind'), 'MW'),
             Item('Preject Time (per tower)', dict.get('projTime'), 'years'),
             Item('Build Cost', dict.get('buildCost'), 'million CAD'),
             Item('Maintenance Cost', dict.get('maintCost'), 'million CAD/yr'),
             Item('Total Cost after 5 yr', str(float(dict.get('buildCost')) + (float(dict.get('maintCost')) * 5)), 'million CAD'),
             Item('Total Cost after 10 yr', str(float(dict.get('buildCost')) + (float(dict.get('maintCost')) * 10)), 'million CAD')
             ]
    
    # Populate the table
    table = ItemTable(items)
    Html_file= open("table2.html","w")
    Html_file.write(table.__html__())
    Html_file.close()
    
    # Print the html
    print(table.__html__())
    
    finalTable = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }
    
    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }
    
    tr:nth-child(even) {
      background-color: #dddddd;
    }
    </style>
    </head>
    <body>
    """
    finalTable += table.__html__()
    finalTable += """
    </body>
    </html>
    """
    
    Html_file= open("table.html","w")
    Html_file.write(finalTable)
    Html_file.close()