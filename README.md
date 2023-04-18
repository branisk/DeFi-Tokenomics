# DeFi Tokenomics
## Overview

This is a Web3 decentralized finance simulation model of a nodes as a service protocol where rewards are given in the form of the protocol's currency to owners of an NFT. The rewards are given over time, subject to defined mechanics. The model is built into a Python Plotly Dash dashboard where users can change parameters, download parameters and upload them, overwrite the parameters, visualize the results. The dashboard can also be viewed in its entirety at [branisk.pythonanywhere.com].

## Description

The model is built to simulate the DeFi tokenomics of a nodes as a service protocol where rewards are given in the form of the protocol's currency to owners of an NFT. The rewards are given over time, subject to defined mechanics. The dashboard is built in Python Plotly Dash where users can change parameters, download parameters and upload them, overwrite the parameters, visualize the results. The dashboard is built to help users understand how different parameters affect the rewards and the economics of the protocol.

The simulation starts with a presale where investors buy a certain amount of yield gems in exchange for DAI. The protocol then creates a liquidity pool between DEFO and DAI. The next phase is where nodes start giving rewards. The nodes are purchased by investors using DEFO. The rewards are given in DEFO. The rewards taper down as time passes. The investors are required to pay maintenance fees to keep their nodes active. The treasury invests the funds received from investors to make a profit. New investors can also invest in the protocol by buying nodes. The protocol also has a mechanism for price stabilization. The protocol also has a phase 2 where the yield gems can be sold to the protocol for DEFO.
Simulation Process

## The simulation process is as follows:

```
Start Simulation
Complete Presale #1
Complete Presale #2 (Boosters)
Create Liquidity Pool (DEFO/DAI)
Start Phase 1 (Nodes give rewards)
    REPEAT:
        Taper Rewards of eligible nodes
        Investors pay maintenance fee on eligible nodes
        X Investors cash out
        Treasury obtains profits from making investments
        Sell off Daily Node Cap to new investors
        Give rewards in DEFO to active nodes
    CHECK FOR SIMULATION ENDING:
        - If too many rewards are owed
        - If Phase 1 is over
        - If there are not enough tokens left for rewards
```

## Model Parameters

The simulation model is a Python program and consists of the following parameters that can be modified via the dashboard.

   - **defoAllocations**: DEFO allocation array.
   - **taperType**: The type of tapering to be used in the simulation. Either linear or exponential.
   - **days**: The number of days to simulate.
   - **TOKEN_SUPPLY**: The total number of tokens supplied.
   - **rewardCap**: The maximum reward cap.
   - **taperRate**: The taper rate for rewards.
   - **treasuryAPY**: Treasury annual percentage yield.
   - **nodesAvailable**: The number of nodes available for sale.
   - **nodesSoldDaily**: The number of nodes sold daily.
   - **nodeCosts**: The cost of nodes.
   - **monthlyFees**: Monthly fees paid by node owners.
   - **nodeRewards**: The rewards given to node owners.
   - **salesTax**: The sales tax paid by node owners.
   - **charityTax**: The charity tax paid by node owners.
   - **takeProfit**: The take profit amount.
   - **newInvestment**: The amount of new investment.
   - **initialDefoAllocations**: The initial DEFO allocations.
   - **saleAllocations**: The allocation for sale.
   - **weeklyCashout**: The weekly cashout amount.
   - **investorLiquidityFloor**: The liquidity floor for investors.
   - **treasuryLiquidityFloor**: The liquidity floor for the treasury.
   - **daiAllocations**: The DAI allocation array.
   - **initialDaiAllocations**: The initial DAI allocations.
   - **boosterCosts1**: The booster costs array for Presale #1.
   - **boosterCounts1**: The booster counts array for Presale #1.
   - **boosterCosts2**: The booster costs array for Presale #2.
   - **boosterCounts2**: The booster counts array for Presale #2.
   - **boosterRate1**: The booster rate for Presale #1.
   - **boosterRate2**: The booster rate for Presale #2.
   - **stabilize**: The stabilize flag.
   - **holdRate**: The hold rate.
   - **addLiquidity**: The add liquidity flag.
   - **buybackTokens**: The buyback tokens flag.
   - **stabilizationCap**: The stabilization cap.
   - **sellOnNodeCreation**: The sell on node creation flag.
   - **phase2**: The phase 2 flag.
   - **refundTax**: The refund tax.
   - **refundHoldRate**: The percentage of refunds that investors dont sell.
