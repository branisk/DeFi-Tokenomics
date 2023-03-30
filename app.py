import dash
from dash.dependencies import Output, Input
from dash import dcc, html
import dash_bootstrap_components as dbc

from numpy import dot

from model import *
from parameters import *

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])
app.title = 'DEFO Tokenomics'
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div([
    dcc.Store(id='local', storage_type='local'),
    html.Div(className = "container section rightBlock", children=[
        html.Img(src=app.get_asset_url('logo.jpg'), style={'width:': '5vh', 'height': '5vh', 'position':'absolute', 'left':'12vw', 'radius':'100px'}),
        html.H1('DEFO Tokenomics', className="text-center", id='title'),
        html.Hr(style={"width":"98vw"})
    ]),
    dbc.Tabs(
        style={'position': 'absolute', 'top': '1em', 'right': '20em'},
        children=[
            dbc.Tab(
                html.Div(className = "container-fluid section2", children=[
                    html.Div(className = "row center", children=[
                        html.H4("General Parameters", id='header1'),
                        html.H4("Node Parameters", id='header2'),
                        html.Div(className="col", children=[
                            dash_table.DataTable(
                                id='parameter-table6',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Value', 'name': 'Value'}]
                                ),
                                data=[
                                {
                                    'Blank':'Days',
                                    'Value': days,
                                },
                                {
                                    'Blank':'Token Supply',
                                    'Value': TOKEN_SUPPLY,
                                },
                                {
                                    'Blank':'Sales Tax',
                                    'Value': salesTax,
                                },
                                {
                                    'Blank':'Charity Tax',
                                    'Value': charityTax,
                                },
                                ],
                                editable=True
                            ),
                        ]),
                        html.Div(className="col", children=[
                            dash_table.DataTable(
                                id='parameter-table7',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Value', 'name': 'Value'}]
                                ),
                                data=[
                                {
                                    'Blank':'Investor Liquidity Floor',
                                    'Value': investorLiquidityFloor,
                                },
                                {
                                    'Blank':'Treasury Liquidity Floor',
                                    'Value': treasuryLiquidityFloor,
                                },
                                {
                                    'Blank':'Weekly Cashout Rate',
                                    'Value': weeklyCashout,
                                },
                                {
                                    'Blank':'New Investment',
                                    'Value': newInvestment,
                                },
                                ],
                                editable=True
                            ),
                        ]),
                        html.Div(className="col", children=[
                            dash_table.DataTable(
                                id='parameter-table1',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Sapphire', 'name': 'Sapphire'}] +
                                    [{'id': 'Ruby', 'name': 'Ruby'}] +
                                    [{'id': 'Diamond', 'name': 'Diamond'}]
                                ),
                                data=[{
                                    'Blank':'Daily Sales',
                                    'Sapphire': t1NodesSoldDaily,
                                    'Ruby': t2NodesSoldDaily,
                                    'Diamond': t3NodesSoldDaily,
                                },
                                {
                                    'Blank':'Cost',
                                    'Sapphire': t1Cost,
                                    'Ruby': t2Cost,
                                    'Diamond': t3Cost,
                                },
                                {
                                    'Blank':'Monthly Fee',
                                    'Sapphire': t1Fee,
                                    'Ruby': t2Fee,
                                    'Diamond': t3Fee,
                                },
                                {
                                    'Blank':'Rewards',
                                    'Sapphire': t1Reward,
                                    'Ruby': t2Reward,
                                    'Diamond': t3Reward,
                                },
                                {
                                    'Blank':'Presale',
                                    'Sapphire': MAX_PRESALE_T1_NODES,
                                    'Ruby': MAX_PRESALE_T2_NODES,
                                    'Diamond': MAX_PRESALE_T3_NODES,
                                }
                                ],
                                editable=True
                            ),
                        ]),
                    ]),
                    html.Br(),
                    html.Div(className="row center", children=[
                        html.H4("Booster Parameters", id='header3'),
                        html.Div(className="col", children=[
                            dash_table.DataTable(
                                id='parameter-table8',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Value', 'name': 'Value'}]
                                ),
                                data=[
                                {
                                    'Blank':'Phase 2 Date',
                                    'Value': phase2,
                                },
                                {
                                    'Blank':'Refund Tax',
                                    'Value':refundTax,
                                },
                                {
                                    'Blank':'Refund Hold Rate',
                                    'Value':refundHoldRate,
                                },
                                ],
                                editable=True
                            ),
                        ]),
                        html.Div(className="col", children=[
                            dash_table.DataTable(
                                id='parameter-table5',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Boost Rate', 'name': 'Boost Rate'}]
                                ),
                                data=[
                                {
                                    'Blank':'B1',
                                    'Boost Rate': boosterRate1,
                                },
                                {
                                    'Blank':'B2',
                                    'Boost Rate': boosterRate2,
                                },
                                ],
                                editable=True
                            ),
                        ]),
                        html.Div(className="col", children=[
                            dash_table.DataTable(
                                id='parameter-table2',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Sapphire', 'name': 'Sapphire'}] +
                                    [{'id': 'Ruby', 'name': 'Ruby'}] +
                                    [{'id': 'Diamond', 'name': 'Diamond'}]
                                ),
                                data=[{
                                    'Blank':'B1 Cost',
                                    'Sapphire': boosterCosts1[0],
                                    'Ruby': boosterCosts1[1],
                                    'Diamond': boosterCosts1[2],
                                },
                                {
                                    'Blank':'B1 Count',
                                    'Sapphire': boosterCounts1[0],
                                    'Ruby': boosterCounts1[1],
                                    'Diamond': boosterCounts1[2],
                                },
                                {
                                    'Blank':'B2 Cost',
                                    'Sapphire': boosterCosts2[0],
                                    'Ruby': boosterCosts2[1],
                                    'Diamond': boosterCosts2[2],
                                },
                                {
                                    'Blank':'B2 Count',
                                    'Sapphire': boosterCounts2[0],
                                    'Ruby': boosterCounts2[1],
                                    'Diamond': boosterCounts2[2],
                                },
                                ],
                                editable=True
                            ),
                        ]),
                    ]),
                    html.Br(),
                    html.Div(className="row center", children=[
                        html.Div(className="col", children=[
                            html.H4("DEFO Allocations", id="header4"),
                            dash_table.DataTable(
                                id='parameter-table3',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Initial', 'name': 'Initial'}] +
                                    [{'id': 'Node Creation', 'name': 'Node Creation'}]
                                ),
                                data=[
                                {
                                    'Blank':'Treasury',
                                    'Initial': initialDefoAllocations[1],
                                    'Node Creation': defoAllocations[1]
                                },
                                {
                                    'Blank':'Reward Pool',
                                    'Initial': initialDefoAllocations[0],
                                    'Node Creation': defoAllocations[0]
                                },
                                {
                                    'Blank':'Liquidity',
                                    'Initial': initialDefoAllocations[2],
                                    'Node Creation': defoAllocations[2]
                                },
                                {
                                    'Blank':'Team',
                                    'Initial': initialDefoAllocations[3],
                                    'Node Creation': defoAllocations[3]
                                },
                                {
                                    'Blank':'Marketing',
                                    'Initial': initialDefoAllocations[4],
                                    'Node Creation': defoAllocations[4]
                                },
                                ],
                                editable=True
                            ),
                        ]),
                        html.Div(className="col", children=[
                            html.H4("DAI Allocations", id="header5"),
                            dash_table.DataTable(
                                id='parameter-table4',
                                style_data={"background-color":"gray"},
                                style_cell={"color":"black"},
                                style_header={"background-color":"slategray"},
                                style_data_conditional=[
                                    {
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'slategray',
                                    },
                                    {
                                        "if": {"state": "selected"},
                                        "backgroundColor": "lightgray",
                                        "border": "1px solid black",
                                    },
                                ],
                                columns=(
                                    [{'id': 'Blank', 'name': '', 'editable': False}] +
                                    [{'id': 'Initial', 'name': 'Initial'}] +
                                    [{'id': 'Node Creation', 'name': 'Node Creation'}]
                                ),
                                data=[
                                {
                                    'Blank':'Treasury',
                                    'Initial': initialDaiAllocations[0],
                                    'Node Creation': daiAllocations[0]
                                },
                                {
                                    'Blank':'Buybacks',
                                    'Initial': initialDaiAllocations[1],
                                    'Node Creation': daiAllocations[1]
                                },
                                {
                                    'Blank':'Liquidity',
                                    'Initial': initialDaiAllocations[2],
                                    'Node Creation': daiAllocations[2]
                                },
                                {
                                    'Blank':'Team',
                                    'Initial': initialDaiAllocations[3],
                                    'Node Creation': daiAllocations[3]
                                },
                                {
                                    'Blank':'Marketing',
                                    'Initial': initialDaiAllocations[4],
                                    'Node Creation': daiAllocations[4]
                                },
                                ],
                                editable=True
                            ),
                        ]),
                    ]),
                    html.Br(),
                    html.Div(className="row slider", style={'margin-top':'-1vh'}, children=[
                        html.Div(className="col", children=[
                            html.Div(className="centerBlock", children=[
                                html.H5("Treasury APY", className="text-center slider-text"),
                                dcc.Slider(0, 2, .1, value=treasuryAPY, id='apy',className="text-center slider"),
                                html.Br(),
                                dcc.ConfirmDialog(
                                    id='confirm-danger',
                                    message='This will overwrite the default parameters with these current values.  Are you sure?',
                                ),
                                html.Button('Overwrite Parameters', id='parameters-button', className="btn btn-danger", style={'display':'inline-block'}),
                                html.Button('Download Parameters', id='download-parameters-button', className="btn btn-primary", style={'display':'inline-block'}),
                                dcc.Download(id='download-parameters'),
                                html.Div(style={'display':'inline-block'}, children=[
                                    dcc.Upload(
                                        html.Button('Upload Parameters', id='upload-parameters-button', className="btn btn-primary", style={'display':'inline-block'}),
                                        id='upload-parameters',
                                        style={'display':'inline-block !important', 'padding-left':0}
                                    ),
                                ]),
                            ])
                        ]),
                        html.Div(className="col", children=[
                            html.H5("ROI Cap", className="text-center slider-text"),
                            dcc.Slider(.1, 2, .1, value=rewardCap, id='rewardCap',className="text-center slider"),
                            html.H5("Taper Rate", className="text-center slider-text"),
                            dcc.Slider(0, 1, .05, value=taperRate, id='taperRate',className="text-center slider"),
                        ]),
                    ]),
                ]),
                label="Parameters"
            ),
            dbc.Tab(
                html.Div(className = "container section2 resultsContainer", children=[
                    html.Div(className="row", children=[
                        html.Div(id="results0", className = "col", children=[
                            html.H5('Runaway: ', id="runaway", className="centerBlock"),
                            html.H5('DEFO Price: ', id='defoPrice', className="centerBlock"),
                            dbc.Table(id="costTable", className="centerBlock"),
                            html.Br(),
                        ]),
                    ]),
                    html.Br(),
                    html.Div(className="row", children=[
                        html.Div(id="results3", className = "col", children=[
                            html.H4(f'DAI Distribution for Phase 2', className='centerBlock'),
                            html.Br(),
                            html.H5(f'Treasury: , Profits: , Nodes: ', id='initialResults', className='centerBlock'),
                            html.Br(),
                        ]),
                    ]),

                ]),
                label="Results"
            ),
            dbc.Tab(
                html.Div(className = "container section2", children=[
                    html.Div(id="charts", className = "col", style={'height':'100px'}, children=[
                        html.Div(className="row", children=[
                            dcc.Graph(id='g1', className = "graph1"),
                            dcc.Graph(id='g2', className = "graph1"),
                            dcc.Graph(id='g4', className = "graph1"),
                        ]),
                        html.Div(className="row", children=[
                            dcc.Graph(id='g3', className = "graph"),
                            dcc.Graph(id='g5', className = "graph"),
                        ]),
                    ])
                ]),
                label="Graphs"
            ),
            dbc.Tab(
                html.Div(className = "container section2", children=[
                    html.Div(id="charts2", className = "col", children=[
                        html.Div(className="row", children=[
                            dcc.Graph(id='g7', style={'height':'40vh', 'padding-bottom':'1vh'}),
                        ]),
                        html.Div(className="row", children=[
                            dcc.Graph(id='g6', style={'height':'40vh', 'padding-bottom':'1vh'}),
                        ]),
                        html.Div(className="row", children=[
                            html.H5("Stabilize: "),
                            html.H5("Buyback: ", id='buyback-text'),
                            html.H5("Add Liquidity: ", id='add-liquidity-text'),
                            html.H5("Sell on Node Creation: ", id='sell-on-node-text'),
                            daq.BooleanSwitch(id="stabilize-button", on=stabilize, color="red"),
                            daq.BooleanSwitch(id="buyback-button", on=buybackTokens, color="red"),
                            daq.BooleanSwitch(id="add-liquidity-button", on=addLiquidity, color="red"),
                            daq.BooleanSwitch(id="sell-on-node-button", on=sellOnNodeCreation, color="red"),
                            html.H5("Hold Rate", id='hold-rate-text'),
                            dcc.Slider(min=1, max=8, step=1, marks={i: "{}%".format(round(1/i*100,1)) for i in range(1,9)}, value=holdRate, id='holdRate',className="text-center slider"),
                            html.Div(children=[
                                dcc.Input(id='sell-rate', type='number', value=sellRate)
                            ]),
                            html.Div(children=[
                                html.H5("Cap:", id='capText'),
                                dcc.Input(id='stabilizationCap', type='number', value=stabilizationCap)
                            ]),
                        ])
                    ]),
                ]),
                label="Liquidity Pool"
            ),
        ]
    ),

])

@app.callback(Output('rewardCap', 'value'),
                Output('taperRate', 'value'),
                Output('apy', 'value'),
                Output('parameter-table1', 'data'),
                Output('parameter-table2', 'data'),
                Output('parameter-table3', 'data'),
                Output('parameter-table4', 'data'),
                Output('parameter-table5', 'data'),
                Output('parameter-table6', 'data'),
                Output('parameter-table7', 'data'),
                Output('holdRate', 'value'),
                Output('stabilize-button', 'on'),
                Output('add-liquidity-button', 'value'),
                Output('buyback-button', 'on'),
                Output('sell-on-node-button', 'value'),
                Output('sell-rate', 'value'),
                Output('parameter-table8', 'data'),
                Output('stabilizationCap', 'value'),
                Input('upload-parameters', 'contents'),
                Input('upload-parameters-button', 'n_clicks'),
                Input('upload-parameters-button', 'n_clicks_timestamp'),
                Input('download-parameters-button', 'n_clicks_timestamp'),
                prevent_initial_call=True)
def update_output(content, n_clicks, b1, b2):
    print(dash.callback_context.triggered[0]['prop_id'].split('.')[0])
    b2 = 0 if b2 == None else b2
    if n_clicks is None or content is None or int(b1) < int(b2):
        return dash.no_update
    else:
        decoded = str(base64.b64decode(content)).split('\n')[0].split('days')[1].replace(' ', '').split('=')
        days = int(''.join(filter(str.isdigit, decoded[1])))
        TOKEN_SUPPLY = int(''.join(filter(str.isdigit, decoded[2])))
        rewardCap = literal_eval(decoded[3][:decoded[3].index("n")-1])
        taperRate = literal_eval(decoded[4][:decoded[4].index("n")-1])
        weeklyCashout = literal_eval(decoded[5][:decoded[5].index("n")-1])
        investorLiquidityFloor = literal_eval(decoded[6][:decoded[6].index("n")-1])
        treasuryLiquidityFloor = literal_eval(decoded[7][:decoded[7].index("n")-1])
        initialDefoAllocations = literal_eval(decoded[8][:decoded[8].index("]")+1])
        initialDaiAllocations = literal_eval(decoded[9][:decoded[9].index("]")+1])
        saleAllocations = literal_eval(decoded[10][:decoded[10].index("]")+1])
        defoAllocations = literal_eval(decoded[11][:decoded[11].index("]")+1])
        daiAllocations = literal_eval(decoded[12][:decoded[12].index("]")+1])
        treasuryAPY = literal_eval(decoded[13][:decoded[13].index("n")-1])
        takeProfit = literal_eval(decoded[14][:decoded[14].index("n")-1])
        takeTreasury = literal_eval(decoded[15][:decoded[15].index("n")-2])
        newInvestment = literal_eval(decoded[16][:decoded[16].index("n")-2])
        salesTax = literal_eval(decoded[17][:decoded[17].index("n")-1])
        charityTax = literal_eval(decoded[18][:decoded[18].index("n")-1])
        t1Cost = literal_eval(decoded[19][:decoded[19].index("n")-2])
        t2Cost = literal_eval(decoded[20][:decoded[20].index("n")-2])
        t3Cost = literal_eval(decoded[21][:decoded[21].index("n")-2])
        t1Reward = literal_eval(decoded[22][:decoded[22].index("n")-1])
        t2Reward = literal_eval(decoded[23][:decoded[23].index("n")-1])
        t3Reward = literal_eval(decoded[24][:decoded[24].index("n")-1])
        t1Fee = literal_eval(decoded[25][:decoded[25].index("n")-1])
        t2Fee = literal_eval(decoded[26][:decoded[26].index("n")-2])
        t3Fee = literal_eval(decoded[27][:decoded[27].index("n")-2])
        MAX_PRESALE_T1_NODES = literal_eval(decoded[28][:decoded[28].index("n")-2])
        MAX_PRESALE_T2_NODES = literal_eval(decoded[29][:decoded[29].index("n")-2])
        MAX_PRESALE_T3_NODES = literal_eval(decoded[30][:decoded[30].index("n")-2])
        t1NodesSoldPresale = literal_eval(decoded[31][:decoded[31].index("n")-2])
        t2NodesSoldPresale = literal_eval(decoded[32][:decoded[32].index("n")-2])
        t3NodesSoldPresale = literal_eval(decoded[33][:decoded[33].index("n")-2])
        t1NodesSoldDaily = literal_eval(decoded[34][:decoded[33].index("n")-2])
        t2NodesSoldDaily = literal_eval(decoded[35][:decoded[33].index("n")-2])
        t3NodesSoldDaily = literal_eval(decoded[36][:decoded[33].index("n")-2])
        boosterCounts1 = literal_eval(decoded[37][:decoded[37].index("]")+1])
        boosterCosts1 = literal_eval(decoded[38][:decoded[38].index("n")-1])
        boosterRate1 = literal_eval(decoded[39][:decoded[39].index("n")-1])
        boosterCounts2 = literal_eval(decoded[40][:decoded[40].index("]")+1])
        boosterCosts2 = literal_eval(decoded[41][:decoded[41].index("n")-1])
        boosterRate2 = literal_eval(decoded[42][:decoded[42].index("n")-1])
        stabilize = literal_eval(decoded[43][:decoded[43].index("n")-1])
        holdRate = literal_eval(decoded[44][:decoded[44].index("n")-1])
        addLiquidity = literal_eval(decoded[45][:decoded[45].index('n')-1])
        buybackTokens = literal_eval(decoded[46][:decoded[46].index('n')-1])
        sellOnNodeCreation = literal_eval(decoded[47][:decoded[47].index('n')-1])
        sellRate = literal_eval(decoded[48][:decoded[48].index('n')-1])
        stabilizationCap = literal_eval(decoded[49][:decoded[49].index('n')-1])
        phase2 = literal_eval(decoded[50][:decoded[50].index('n')-2])
        refundTax = literal_eval(decoded[51][:decoded[51].index('n')-1])
        refundHoldRate = literal_eval(decoded[52][:decoded[52].index('"')])

        table1 = [{'Blank': 'Daily Sales', 'Sapphire': t1NodesSoldDaily, 'Ruby': t2NodesSoldDaily, 'Diamond': t3NodesSoldDaily}, {'Blank': 'Cost', 'Sapphire': t1Cost, 'Ruby': t2Cost, 'Diamond': t3Cost}, {'Blank': 'Monthly Fee', 'Sapphire': t1Fee, 'Ruby': t2Fee, 'Diamond': t3Fee}, {'Blank': 'Rewards', 'Sapphire': t1Reward, 'Ruby': t2Reward, 'Diamond': t3Reward}, {'Blank': 'Presale', 'Sapphire': MAX_PRESALE_T1_NODES, 'Ruby': MAX_PRESALE_T2_NODES, 'Diamond': MAX_PRESALE_T3_NODES}]
        table2 = [{'Blank': 'B1 Cost', 'Sapphire': boosterCosts1[0], 'Ruby': boosterCosts1[1], 'Diamond': boosterCosts1[2]}, {'Blank': 'B1 Count', 'Sapphire': boosterCounts1[0], 'Ruby': boosterCounts1[1], 'Diamond': boosterCounts1[2]}, {'Blank': 'B2 Cost', 'Sapphire': boosterCosts2[0], 'Ruby': boosterCosts2[1], 'Diamond': boosterCosts2[2]}, {'Blank': 'B2 Count', 'Sapphire': boosterCounts2[0], 'Ruby': boosterCounts2[1], 'Diamond': boosterCounts2[2]}]
        table3 = [{'Blank': 'Treasury', 'Initial': initialDefoAllocations[1], 'Node Creation': defoAllocations[1]}, {'Blank': 'Reward Pool', 'Initial': initialDefoAllocations[0], 'Node Creation': defoAllocations[0]}, {'Blank': 'Liquidity', 'Initial': initialDefoAllocations[2], 'Node Creation': defoAllocations[2]}, {'Blank': 'Team', 'Initial': initialDefoAllocations[3], 'Node Creation': defoAllocations[3]}, {'Blank': 'Marketing', 'Initial': initialDefoAllocations[4], 'Node Creation': defoAllocations[4]}]
        table4 = [{'Blank': 'Treasury', 'Initial': initialDaiAllocations[0], 'Node Creation': daiAllocations[0]}, {'Blank': 'Buybacks', 'Initial': initialDaiAllocations[1], 'Node Creation': daiAllocations[1]}, {'Blank': 'Liquidity', 'Initial': initialDaiAllocations[2], 'Node Creation': daiAllocations[2]}, {'Blank': 'Team', 'Initial': initialDaiAllocations[3], 'Node Creation': daiAllocations[3]}, {'Blank': 'Marketing', 'Initial': initialDaiAllocations[4], 'Node Creation': daiAllocations[4]}]
        table5 = [{'Blank': 'B1', 'Boost Rate': boosterRate1}, {'Blank': 'B2', 'Boost Rate': boosterRate2}]
        table6 = [{'Blank': 'Days', 'Value': days}, {'Blank': 'Token Supply', 'Value': TOKEN_SUPPLY}, {'Blank': 'Sales Tax', 'Value': salesTax}, {'Blank': 'Charity Tax', 'Value': charityTax}]
        table7 = [{'Blank': 'Investor Liquidity Floor', 'Value': investorLiquidityFloor}, {'Blank': 'Treasury Liquidity Floor', 'Value': treasuryLiquidityFloor}, {'Blank': 'Weekly Cashout Rate', 'Value': weeklyCashout}, {'Blank': 'New Investment', 'Value': newInvestment}]
        table8 = [{'Blank':'Phase 2 Date', 'Value': phase2}, {'Blank':'Refund Tax', 'Value': refundTax}, {'Blank':'Refund Hold Rate', 'Value': refundHoldRate}]

        return rewardCap, taperRate, treasuryAPY, table1, table2, table3, table4, table5, table6, table7, holdRate, stabilize, addLiquidity, buybackTokens, sellOnNodeCreation, sellRate, table8, stabilizationCap

@app.callback(Output('confirm-danger', 'displayed'),
          Input('parameters-button', 'n_clicks'))
def display_confirm(button):
    if button is not None:
        return True
    return False

@app.callback(Output("download-parameters", "data"),
              Input('rewardCap', 'value'),
              Input('taperRate', 'value'),
              Input('apy', 'value'),
              Input('confirm-danger', 'submit_n_clicks'),
              Input('parameter-table1', 'data'),
              Input('parameter-table2', 'data'),
              Input('parameter-table3', 'data'),
              Input('parameter-table4', 'data'),
              Input('parameter-table5', 'data'),
              Input('parameter-table6', 'data'),
              Input('parameter-table7', 'data'),
              Input('stabilize-button', 'on'),
              Input("download-parameters-button", "n_clicks"),
              Input('upload-parameters-button', 'n_clicks_timestamp'),
              Input('download-parameters-button', 'n_clicks_timestamp'),
              Input('holdRate', 'value'),
              Input('add-liquidity-button', 'on'),
              Input('buyback-button', 'on'),
              Input('sell-on-node-button', 'on'),
              Input('sell-rate', 'value'),
              Input('stabilizationCap', 'value'),
              Input('parameter-table8', 'data'),
              prevent_initial_call=True
)
def func(
    value9,
    value10,
    value11,
    dangerConfirmed,
    table1,
    table2,
    table3,
    table4,
    table5,
    table6,
    table7,
    stabilizationValue,
    n_clicks,
    b1,
    b2,
    holdRate,
    addLiquidity,
    buybackTokens,
    sellOnNodeCreation,
    sellRate,
    stabilizationCap,
    table8
):
    b1 = 0 if b1 == None else b1
    if n_clicks is None or int(b2) < int(b1):
        return

    value6 = 'deterministic'

    value7 = int(table6[0]['Value'])
    value8 = int(table6[1]['Value'])
    value28 = float(table6[2]['Value'])
    value29 = float(table6[3]['Value'])

    value43 = float(table7[0]['Value'])
    value44 = float(table7[1]['Value'])
    value42 = float(table7[2]['Value'])
    value31 = float(table7[3]['Value'])


    value12 = float(table1[4]['Sapphire'])
    value13 = float(table1[4]['Ruby'])
    value14 = float(table1[4]['Diamond'])
    value15 = float(table1[0]['Sapphire'])
    value16 = float(table1[0]['Ruby'])
    value17 = float(table1[0]['Diamond'])
    value18 = float(table1[1]['Sapphire'])
    value19 = float(table1[1]['Ruby'])
    value20 = float(table1[1]['Diamond'])
    value21 = float(table1[2]['Sapphire'])
    value22 = float(table1[2]['Ruby'])
    value23 = float(table1[2]['Diamond'])
    value24 = float(table1[3]['Sapphire'])
    value25 = float(table1[3]['Ruby'])
    value26 = float(table1[3]['Diamond'])

    value55 = float(table2[0]['Sapphire'])
    value56 = float(table2[0]['Ruby'])
    value57 = float(table2[0]['Diamond'])
    value58 = float(table2[1]['Sapphire'])
    value59 = float(table2[1]['Ruby'])
    value60 = float(table2[1]['Diamond'])
    value61 = float(table2[2]['Sapphire'])
    value62 = float(table2[2]['Ruby'])
    value63 = float(table2[2]['Diamond'])
    value64 = float(table2[3]['Sapphire'])
    value65 = float(table2[3]['Ruby'])
    value66 = float(table2[3]['Diamond'])

    value32 = float(table3[1]['Initial'])
    value33 = float(table3[0]['Initial'])
    value34 = float(table3[2]['Initial'])
    value35 = float(table3[3]['Initial'])
    value36 = float(table3[4]['Initial'])
    value1 = float(table3[1]['Node Creation'])
    value2 = float(table3[0]['Node Creation'])
    value3 = float(table3[2]['Node Creation'])
    value4 = float(table3[3]['Node Creation'])
    value5 = float(table3[4]['Node Creation'])

    value50 = float(table4[0]['Initial'])
    value51 = float(table4[1]['Initial'])
    value52 = float(table4[2]['Initial'])
    value53 = float(table4[3]['Initial'])
    value54 = float(table4[4]['Initial'])
    value45 = float(table4[0]['Node Creation'])
    value46 = float(table4[1]['Node Creation'])
    value47 = float(table4[2]['Node Creation'])
    value48 = float(table4[3]['Node Creation'])
    value49 = float(table4[4]['Node Creation'])

    value37 = 1
    value38 = 0
    value39 = 0
    value40 = 0
    value41 = 0

    value67 = float(table5[0]['Boost Rate'])
    value68 = float(table5[1]['Boost Rate'])

    phase2 = float(table8[0]['Value'])
    refundTax = float(table8[1]['Value'])
    refundHoldRate = float(table8[2]['Value'])

    print(phase2)
    print(refundTax)

    content = f"taperType = 'deterministic'\ndays = {value7}\nTOKEN_SUPPLY = {value8}\nrewardCap = {value9}\ntaperRate = {value10}\nweeklyCashout = {value42}\ninvestorLiquidityFloor = {value43}\ntreasuryLiquidityFloor = {value44}\ninitialDefoAllocations = {[value32, value33, value34, value35, value36]}\ninitialDaiAllocations = {[value50, value51, value52, value53, value54]}\nsaleAllocations = {[value37, value38, value39, value40, value41]}\ndefoAllocations = {[value1, value2, value3, value4, value5]}\ndaiAllocations = {[value45, value46, value47, value48, value49]}\ntreasuryAPY = {value11}\ntakeProfit = .5\ntakeTreasury = .25\nnewInvestment = {value31}\nsalesTax = {value28}\ncharityTax = {value29}\nt1Cost = {value18}\nt2Cost = {value19}\nt3Cost = {value20}\nt1Reward = {value24}\nt2Reward = {value25}\nt3Reward = {value26}\nt1Fee = {value21}\nt2Fee = {value22}\nt3Fee = {value23}\nMAX_PRESALE_T1_NODES = {value12}\nMAX_PRESALE_T2_NODES = {value13}\nMAX_PRESALE_T3_NODES = {value14}\nt1NodesSoldPresale = {value12}\nt2NodesSoldPresale = {value13}\nt3NodesSoldPresale = {value14}\nt1NodesSoldDaily = {value15}\nt2NodesSoldDaily = {value16}\nt3NodesSoldDaily = {value17}\nboosterCounts1 = {[value58, value59, value60]}\nboosterCosts1 = {[value55, value56, value57]}\nboosterRate1 = {value67}\nboosterCounts2 = {[value64, value65, value66]}\nboosterCosts2 = {[value61, value62, value63]}\nboosterRate2 = {value68}\nstabilize = {stabilizationValue}\nholdRate = {holdRate}\naddLiquidity = {addLiquidity}\nbuybackTokens = {buybackTokens}\nsellOnNodeCreation = {sellOnNodeCreation}\nsellRate = {sellRate}\nstabilizationCap = {stabilizationCap}\nphase2 = {phase2}\nrefundTax = {refundTax}\nrefundHoldRate = {refundHoldRate}"

    return dict(content=content, filename="parameters.txt")

#	Callback for updating the svm graph
@app.callback([Output('g1', 'figure'),
               Output('g2', 'figure'),
               Output('g3', 'figure'),
               Output('g4', 'figure'),
               Output('g5', 'figure'),
               Output('runaway', 'children'),
               Output('initialResults', 'children'),
               Output('defoPrice', 'children'),
               Output('costTable', 'children'),
               Output('g6', 'figure'),
               Output('g7', 'figure')],
              Input('rewardCap', 'value'),
              Input('taperRate', 'value'),
              Input('apy', 'value'),
              Input('confirm-danger', 'submit_n_clicks'),
              Input('parameter-table1', 'data'),
              Input('parameter-table2', 'data'),
              Input('parameter-table3', 'data'),
              Input('parameter-table4', 'data'),
              Input('parameter-table5', 'data'),
              Input('parameter-table6', 'data'),
              Input('parameter-table7', 'data'),
              Input('stabilize-button', 'on'),
              Input('holdRate', 'value'),
              Input('add-liquidity-button', 'on'),
              Input('buyback-button', 'on'),
              Input('sell-on-node-button', 'on'),
              Input('sell-rate', 'value'),
              Input('stabilizationCap', 'value'),
              Input('parameter-table8', 'data'))
def update_graph(
    value9,
    value10,
    value11,
    dangerConfirmed,
    table1,
    table2,
    table3,
    table4,
    table5,
    table6,
    table7,
    stabilizationValue,
    holdRate,
    addLiquidity,
    buybackTokens,
    sellOnNodeCreation,
    sellRate,
    stabilizationCap,
    table8
):
    print(f'hold: {holdRate}')
    value6 = 'deterministic'

    value7 = int(table6[0]['Value'])
    value8 = int(table6[1]['Value'])
    value28 = float(table6[2]['Value'])
    value29 = float(table6[3]['Value'])

    value43 = float(table7[0]['Value'])
    value44 = float(table7[1]['Value'])
    value42 = float(table7[2]['Value'])
    value31 = float(table7[3]['Value'])


    value12 = float(table1[4]['Sapphire'])
    value13 = float(table1[4]['Ruby'])
    value14 = float(table1[4]['Diamond'])
    value15 = float(table1[0]['Sapphire'])
    value16 = float(table1[0]['Ruby'])
    value17 = float(table1[0]['Diamond'])
    value18 = float(table1[1]['Sapphire'])
    value19 = float(table1[1]['Ruby'])
    value20 = float(table1[1]['Diamond'])
    value21 = float(table1[2]['Sapphire'])
    value22 = float(table1[2]['Ruby'])
    value23 = float(table1[2]['Diamond'])
    value24 = float(table1[3]['Sapphire'])
    value25 = float(table1[3]['Ruby'])
    value26 = float(table1[3]['Diamond'])

    value55 = float(table2[0]['Sapphire'])
    value56 = float(table2[0]['Ruby'])
    value57 = float(table2[0]['Diamond'])
    value58 = float(table2[1]['Sapphire'])
    value59 = float(table2[1]['Ruby'])
    value60 = float(table2[1]['Diamond'])
    value61 = float(table2[2]['Sapphire'])
    value62 = float(table2[2]['Ruby'])
    value63 = float(table2[2]['Diamond'])
    value64 = float(table2[3]['Sapphire'])
    value65 = float(table2[3]['Ruby'])
    value66 = float(table2[3]['Diamond'])

    value32 = float(table3[1]['Initial'])
    value33 = float(table3[0]['Initial'])
    value34 = float(table3[2]['Initial'])
    value35 = float(table3[3]['Initial'])
    value36 = float(table3[4]['Initial'])
    value1 = float(table3[1]['Node Creation'])
    value2 = float(table3[0]['Node Creation'])
    value3 = float(table3[2]['Node Creation'])
    value4 = float(table3[3]['Node Creation'])
    value5 = float(table3[4]['Node Creation'])

    value50 = float(table4[0]['Initial'])
    value51 = float(table4[1]['Initial'])
    value52 = float(table4[2]['Initial'])
    value53 = float(table4[3]['Initial'])
    value54 = float(table4[4]['Initial'])
    value45 = float(table4[0]['Node Creation'])
    value46 = float(table4[1]['Node Creation'])
    value47 = float(table4[2]['Node Creation'])
    value48 = float(table4[3]['Node Creation'])
    value49 = float(table4[4]['Node Creation'])

    value37 = 1
    value38 = 0
    value39 = 0
    value40 = 0
    value41 = 0

    value67 = float(table5[0]['Boost Rate'])
    value68 = float(table5[1]['Boost Rate'])

    phase2 = float(table8[0]['Value'])
    refundTax = float(table8[1]['Value'])
    refundHoldRate = float(table8[2]['Value'])

    if dangerConfirmed:
        pass
        content = f"taperType = 'deterministic'\ndays = {value7}\nTOKEN_SUPPLY = {value8}\nrewardCap = {value9}\ntaperRate = {value10}\nweeklyCashout = {value42}\ninvestorLiquidityFloor = {value43}\ntreasuryLiquidityFloor = {value44}\ninitialDefoAllocations = {[value32, value33, value34, value35, value36]}\ninitialDaiAllocations = {[value50, value51, value52, value53, value54]}\nsaleAllocations = {[value37, value38, value39, value40, value41]}\ndefoAllocations = {[value1, value2, value3, value4, value5]}\ndaiAllocations = {[value45, value46, value47, value48, value49]}\ntreasuryAPY = {value11}\ntakeProfit = .5\ntakeTreasury = .25\nnewInvestment = {value31}\nsalesTax = {value28}\ncharityTax = {value29}\nt1Cost = {value18}\nt2Cost = {value19}\nt3Cost = {value20}\nt1Reward = {value24}\nt2Reward = {value25}\nt3Reward = {value26}\nt1Fee = {value21}\nt2Fee = {value22}\nt3Fee = {value23}\nMAX_PRESALE_T1_NODES = {value12}\nMAX_PRESALE_T2_NODES = {value13}\nMAX_PRESALE_T3_NODES = {value14}\nt1NodesSoldPresale = {value12}\nt2NodesSoldPresale = {value13}\nt3NodesSoldPresale = {value14}\nt1NodesSoldDaily = {value15}\nt2NodesSoldDaily = {value16}\nt3NodesSoldDaily = {value17}\nboosterCounts1 = {[value58, value59, value60]}\nboosterCosts1 = {[value55, value56, value57]}\nboosterRate1 = {value67}\nboosterCounts2 = {[value64, value65, value66]}\nboosterCosts2 = {[value61, value62, value63]}\nboosterRate2 = {value68}\nstabilize = {stabilizationValue}\nholdRate = {holdRate}\naddLiquidity = {addLiquidity}\nbuybackTokens = {buybackTokens}\nsellOnNodeCreation = {sellOnNodeCreation}\nsellRate = {sellRate}\nstabilizationCap = {stabilizationCap}\nphase2 = {phase2}\nrefundTax = {refundTax}\nrefundHoldRate = {refundHoldRate}"

        username = ''
        token = ''
        API = ''
        FILEPATH = ''

        response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
                username=username
            ),
            headers={'Authorization': 'Token {token}'.format(token=token)}
        )

        resp = requests.post(
            urljoin(API, FILEPATH),
            files={"content": content},
            headers={"Authorization": "Token {api_token}".format(api_token=token)}
        )

        print(resp.status_code)

        resp = requests.post(
            urljoin(API, ''),
            headers={"Authorization": "Token {api_token}".format(api_token=token)}
        )

        print(resp.status_code)

    return model(
        [value1, value2, value3, value4, value5],
        value6,
        value7,
        value8,
        value9,
        value10,
        value11,
        value12,
        value13,
        value14,
        value15,
        value16,
        value17,
        value18,
        value19,
        value20,
        value21,
        value22,
        value23,
        value24,
        value25,
        value26,
        value28,
        value29,
        takeProfit,
        value31,
        [value32, value33, value34, value35, value36],
        [value37, value38, value39, value40, value41],
        value42,
        value43,
        value44,
        [value45, value46, value47, value48, value49],
        [value50, value51, value52, value53, value54],
        [value55, value56, value57],
        [value58, value59, value60],
        [value61, value62, value63],
        [value64, value65, value66],
        value67,
        value68,
        stabilizationValue,
        holdRate,
        addLiquidity,
        buybackTokens,
        stabilizationCap,
        sellOnNodeCreation,
        sellRate,
        phase2,
        refundTax,
        refundHoldRate
    )
