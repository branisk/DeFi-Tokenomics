import matplotlib.pyplot as plt
import numpy as np
from numpy import dot, multiply, add, subtract
from numpy.random import normal
from numpy.linalg import multi_dot
from math import floor, ceil
import pandas as pd
from helpers import *
from classes import *
from app import *

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

#####################################################
#                   SIMULATION PROCESS              #
#####################################################
#            Start Simulation                       #
#                   |                               #
#           Complete Presale #1                     #
#                   |                               #
#           Complete Presale #2 (Boosters)          #
#                   |                               #
#          Create Liquidity Pool (DEFO/DAI)         #
#                   |                               #
#            Start Phase 1 (Nodes give rewards)     #
#                   |                               #
#                REPEAT:                            #
#     Taper Rewards of elligible nodes              #
# Investors pay maintanence fee on elligble nodes   #
#          X Investors cash out                     #
# Treasury obtains profits from making investments  #
#   Sell off Daily Node Cap to new investors        #
#     Give rewards in DEFO to active nodes          #
#                   |                               #
#        CHECK FOR SIMULATION ENDNG:                #
# - If too many rewards are owed                    #
# - If Phase 1 is over                              #
# - If there are not enough tokens left for rewards #
#                                                   #
#####################################################

def model(
    defoAllocations,
    taperType,
    days,
    TOKEN_SUPPLY,
    rewardCap,
    taperRate,
    treasuryAPY,
    nodesAvailable,
    nodesSoldDaily,
    nodeCosts,
    monthlyFees,
    nodeRewards,
    salesTax,
    charityTax,
    takeProfit,
    newInvestment,
    initialDefoAllocations,
    saleAllocations,
    weeklyCashout,
    investorLiquidityFloor,
    treasuryLiquidityFloor,
    daiAllocations,
    initialDaiAllocations,
    boosterCosts1,
    boosterCounts1,
    boosterCosts2,
    boosterCounts2,
    boosterRate1,
    boosterRate2,
    stabilize,
    holdRate,
    addLiquidity,
    buybackTokens,
    stabilizationCap,
    sellOnNodeCreation,
    sellRate,
    phase2,
    refundTax,
    refundHoldRate
):
    ###########################
    #        DONT TOUCH       #
    ###########################

    labels = ['Sapphire', 'Ruby', 'Diamond']
    dailyReturns, totalReturn = [0,0,0], [0,0,0]
    nodesSoldPresale = [t1NodesSoldPresale, t2NodesSoldPresale, t3NodesSoldPresale]
    rewardTapers = [[0],[0],[0]]
    runaway = 0
    initialRunawayTreasury = 0
    initialRunawayProfits = 0
    initialRunawayCounts = [0,0,0]
    sapphireAllocation = 0
    rubyAllocation = 0
    diamondAllocation = 0
    calculated = False
    t1Amount = 0
    t2Amount = 0
    t3Amount = 0
    t1Percentage = 0
    t2Percentage = 0
    t3Percentage = 0

    x1, x2, y1, y2 ,y3, y4, y5, y6, y7, y8 = [], [], [], [], [], [], [], [], [], []
    y9, y10, y11, y12, y13, y14, y15, y16 = [], [], [], [], [], [], [], []
    xarray, yarray, yarray1, yarray2 = [], [], [], []

    roi1x, roi2x = [], []

    rewardArray = [[],[],[]]
    returnArray = [[],[],[]]

    g1 = go.Figure()
    g2 = go.Figure()

    #################################
    #       BEGIN SIMULATIONS       #
    #################################

    # Calculates the roi for each respective yield gem, for a certain amount of ROIs
    # First loop goes through each yield gem
    for i in range(3):
        currentReward = nodeRewards[i]

        # Loops through jth multiple of ROI
        for j in range(1, numberOfRois := 5):
            # Calculate how much reward the node earns daily
            reward = ((1 - salesTax - charityTax) * (nodeCosts[i] * currentReward * (stabilizationCap / (stabilizationCap + 1)))) -  (monthlyFees[i]/31)

            # Calculate day that roi is achieved based on daily reward
            roi = ceil(nodeCosts[i] * j / reward)

            # Update arrays for graphs
            rewardTapers[i].append(roi)
            returnArray[i].append((nodeCosts[i]*(j-1)) - nodeCosts[i])
            rewardArray[i].append(currentReward)

            # Save roi1x and roi2x for evaluating metrics
            if (len(roi1x) == i):
                roi1x.append(roi)
            elif (len(roi2x) == i):
                roi2x.append(roi)

            # Taper rewards to calculate the next achieved roi
            currentReward *= taperRate

        # Update graphs
        g1.add_trace(go.Scatter(x=rewardTapers[i],y=returnArray[i], name=f'{labels[i]}'))
        g2.add_trace(go.Scatter(x=rewardTapers[i],y=rewardArray[i], name=f'{labels[i]}', mode='markers'))

    # INVESTMENT POOL SIMULATION
    print("****BEGINNING SIMULATION****\n")

    # Initialize model object
    model = Tokenomics(
        defoAllocations = defoAllocations,
        available = nodesAvailable,
        costs = nodeCosts,
        rewards = nodeRewards,
        fees = monthlyFees,
        salesTax = salesTax,
        charityTax = charityTax,
        tokenSupply = TOKEN_SUPPLY,
        taperType = taperType,
        initialDefoAllocations = initialDefoAllocations,
        daiAllocations = daiAllocations,
        stabilize = stabilize,
        addLiquidity = addLiquidity,
        stabilizationCap = stabilizationCap,
        buybackTokens = buybackTokens,
        sellOnNodeCreation = sellOnNodeCreation,
        phase2 = phase2,
    )

    # Adds first and second presale investors/yield gems to the simulation
    model.populate_presale(initialDaiAllocations)
    model.populate_boosters(initialDaiAllocations, boosterCounts1, boosterRate1, boosterCosts1,
                                                    boosterCounts2, boosterRate2, boosterCosts2)

    # Initialize an instance of a liquidity pool paired by DEFO and DAI
    model.create_liquidity_pool(model.dai.liquidity, model.defo.liquidity)

    # Initialize amount for investors to sell given price stabilization based on constant sell rate on node creation
    model.sellAmount = int(sellRate * dot(nodesSoldDaily, nodeCosts) / model.initialPrice)

    # After presale, and the liquidity pool is created, calculate the rewards given to presale investors
    for investor in model.investors:
        investor.invested = dot(boosterCosts2, investor.counts) * .5 / model.initialPrice
        investor.dailyReturn = investor.get_daily_return(model.initialPrice)
        model.dailyRewards += investor.dailyReturn

    for i in range(days):
        xarray, yarray, yarray1, yarray2, x2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, model = update_arrays(i, xarray, yarray, yarray1, yarray2, x2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, model)

        # Add 1 to each investors days since mint
        model.update_days()

        # DEFO Callbacks
        model.check_reward_tapers(rewardTapers, taperRate)
        model.cashout_investors(weeklyCashout, saleAllocations, holdRate)

        # DAI Callbacks
        model.check_monthly_fees()
        model.get_treasury_returns(treasuryAPY, newInvestment)

        # Update current price
        model.currentPrice = model.lp.defoPrice
        model.lp.update_price()

        # Introduce a new investor if theres enough DEFO in liquidity to buy in
        if (model.lp.defo >= investorLiquidityFloor and model.lp.defo >= dot(model.nodes.costs, nodesSoldDaily) * .5 / model.initialPrice and np.sum(nodesSoldDaily) > 0):
            model.add_investor(nodesSoldDaily)

        # Cash out all investors and end the simulation if the protocol owes too many rewards
        if (model.calculate_owed_rewards() >= model.defo.rewards):
            model.cashout_all_investors()
            runaway = i
            break

        # Ends the simulation if it's time for phase 2
        if (i == model.phase2):
            model.end_phase_1(refundHoldRate, refundTax)
            break

        # Check if we have enough rewards to payout
        if (model.defo.rewards >= model.dailyRewards):
            model.payout_rewards()
        # Otherwise, end the simulation
        else:
            runaway = i
            break

    print("****SIMULATION COMPLETE****\n")

    # Update our results
    if (runaway == 0):
        runaway = "Sustainable"
    else:
        runaway = f"{runaway} Day "

    sapphireAllocation, rubyAllocation, diamondAllocation = calculate_phase2_allocations(model)
    g3, g4, g5, g6, g7 = graph_plotly(x2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, xarray, yarray, yarray1, yarray2)
    g1, g2, g3, g4, g5, g6, g7 = update_plotly(g1, g2, g3, g4, g5, g6, g7)

    # Dataframe for results table
    df = pd.DataFrame(
        {
            "": ["Sapphire", "Ruby", "Diamond"],
            "$ Cost": nodeCosts,
            "DEFO Cost": [round((nodeCosts[0] * .5) / model.initialPrice, 0).astype(int), round((nodeCosts[1] * .5) / round(model.initialPrice, 0), 0).astype(int), round((nodeCosts[2] * .5) / round(model.initialPrice, 0), 0).astype(int)],
            "DAI Cost": [int(nodeCosts[0] * .5), int(nodeCosts[1] * .5), int(nodeCosts[2] * .5)],
            "1x ROI": [roi for roi in roi1x],
            "2x ROI": [roi for roi in roi2x],
            "Total Nodes": [count for count in model.nodes.numSold],
            "Phase2 ($)": [round(sapphireAllocation,2), round(rubyAllocation,2), round(diamondAllocation,2)],
            "Phase2 (%)": [round(100*sapphireAllocation/model.nodes.costs[0],1), round(100*rubyAllocation/model.nodes.costs[1],1), round(100*diamondAllocation/model.nodes.costs[2],1)]
        }
    )

    return (
        g1,
        g2,
        g3,
        g4,
        g5,
        html.H4(f'{runaway} Runaway', id="initialRunaway"),
        html.H4(f'Treasury: {round(model.dai.treasury,0)}, Profits: {round(model.dai.profits,0)}', id='initialResults'),
        html.H4(f'DEFO Price: ${round(model.initialPrice)}', id='defoPrice'),
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
        g6,
        g7
    )
