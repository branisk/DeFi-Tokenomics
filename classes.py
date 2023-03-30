import numpy as np
from numpy import dot, multiply, add, subtract
from numpy.random import normal
from math import floor

class Tokenomics:
    # Model initialization
    def __init__(self, defoAllocations, available, costs, rewards, fees, salesTax, charityTax, tokenSupply, taperType, initialDefoAllocations, daiAllocations, stabilize, addLiquidity, stabilizationCap, buybackTokens, sellOnNodeCreation, phase2):
        self.defo = self.Funds(defoAllocations)
        self.dai = self.Funds(daiAllocations)
        self.nodes = self.Nodes(available, costs, rewards, fees, salesTax, charityTax)
        self.investors = []
        self.dailyRewards = 0
        self.taperType = taperType
        self.stabilize = stabilize
        self.addLiquidity = addLiquidity
        self.stabilizationCap = stabilizationCap
        self.buybackTokens = buybackTokens
        self.sellOnNodeCreation = sellOnNodeCreation
        self.phase2 = phase2
        self.dai.buyback = 0

        # Initial allocation of DEFO supply
        self.defo.rewards += tokenSupply * initialDefoAllocations[0]
        self.defo.treasury += tokenSupply * initialDefoAllocations[1]
        self.defo.liquidity += tokenSupply * initialDefoAllocations[2]
        self.defo.team += tokenSupply * initialDefoAllocations[3]
        self.defo.marketing += tokenSupply * initialDefoAllocations[4]

    # Adds an investor to the protocol by buying out the entire daily node cap
    def add_investor(self, counts):
        self.investors.append(
            self.Investor(
                counts,
                self.nodes
            )
        )
        self.nodes.sell_nodes(counts)
        self.investors[-1].dailyReturn = self.investors[-1].get_daily_return(self.initialPrice)

        # Calculate how much DEFO and DAI obtained from investor (1:1 DEFO:DAI)
        # We divide by the price to get an even $ amount of defo and dai, based price initialized on liquidity creation
        defoAmount = (self.investors[-1].invested * .5) / self.initialPrice
        daiAmount = self.investors[-1].invested * .5

        # Calculate how much an investor has invested in DEFO
        self.investors[-1].invested = defoAmount
        self.dailyRewards += self.investors[-1].dailyReturn

        # Update liquidity pools with defo bought by investor
        self.lp.defo -= defoAmount
        self.lp.dai = self.lp.invariant / self.lp.defo # x*y=k
        self.lp.update_price()

        # Allocate funds to respective pools
        self.defo.allocate_defo(defoAmount)
        self.dai.allocate_dai(daiAmount)

        if self.addLiquidity:
            self.add_liquidity(self.dai.liquidity, self.defo.liquidity)

        if self.stabilize:
            self.stabilize_price(defoAmount)

    # Calculate the daily rewards given to each investor based on the yield gems they own
    def calculate_daily_rewards(self):
        total = 0
        for investor in self.investors:
            total += investor.dailyReturn

        return total

    # Calculate the total owed rewards by the protocol to investors
    def calculate_owed_rewards(self):
        total = 0
        for investor in self.investors:
            total += investor.returns

        return total

    # Cashes out an investor with the rewards they are owed
    # We skip investors based on the holdRate to get a ratio of holders to sellers
    # If an investor is not holding, we sell out the proportion defined by weeklyCashout
    def cashout_investors(self, weeklyCashout, saleAllocations, holdRate):
        for investor in self.investors:
            if (investor.days > 0 and investor.days % 7 == 0):
                # Investor gets given rewards and pays taxes
                value = investor.returns * weeklyCashout

                investor.returns -= value
                investor.returnsTaken += value
                valueAfterTax = (value) * (1 - self.nodes.salesTax)
                charityAmount = value * self.nodes.charityTax

                self.defo.rewards -= (valueAfterTax + charityAmount)

                # These investors claim rewards but hold them
                if (self.investors.index(investor) % holdRate == 0):
                    self.defo.vault += valueAfterTax
                    self.lp.defo += charityAmount
                    self.lp.dai = self.lp.invariant / self.lp.defo
                    self.lp.update_price()

                    self.dai.charity += charityAmount * self.lp.defoPrice

                    continue
                # These investors claim rewards and sell them
                else:
                    # Investor sells rewards
                    self.lp.defo += valueAfterTax + charityAmount
                    self.lp.dai = self.lp.invariant / self.lp.defo
                    self.lp.update_price()

                    self.dai.charity += charityAmount * self.lp.defoPrice

                if self.buybackTokens:
                    self.buyback_tokens(valueAfterTax)

    # In the event that the protocol owes more rewards than cashed out, all investors cash out
    def cashout_all_investors(self):
        for investor in self.investors:
            # Investor gets given rewards and pays taxes
            value = investor.returns
            investor.returns -= value
            valueAfterTax = (value) * (1 - self.nodes.salesTax)
            charityAmount = value * self.nodes.charityTax
            self.defo.rewards -= (valueAfterTax + charityAmount)

            # Investor sells rewards
            self.lp.defo += valueAfterTax + charityAmount
            self.lp.dai = self.lp.invariant / self.lp.defo
            self.lp.update_price()

            self.dai.charity += charityAmount * self.lp.defoPrice

            if self.stabilize:
                self.stabilize_price(valueAfterTax)

    # Checks if a node has been active for a month, and pays maintanence fee
    def check_monthly_fees(self):
        for investor in self.investors:
            if (investor.days > 0 and investor.days % 30 == 0):
                cost = dot(investor.counts, self.nodes.fees)
                self.dai.treasury += cost

    # Check if an investor has reached ROI, and tapers their yield gems if so
    def check_reward_tapers(self, rewardTapers, taperRate):
        for investor in self.investors:
            if (investor.currentReturnCycle >= investor.invested):
                investor.currentReturnCycle = 0
                investor.rewards = multiply(investor.rewards, taperRate)
                investor.dailyReturn = investor.get_daily_return(self.initialPrice)
                self.dailyRewards = self.calculate_daily_rewards()

    # Ends phase 1 in the event that the days until phase 2 has been reached
    def end_phase_1(self, refundHoldRate, refundTax):
        returnTotal = 0

        for investor in self.investors:
            if investor.returnsTaken < investor.invested:
                deficit = (investor.invested - investor.returnsTaken)
                investor.returnsTaken += deficit

                # Logarithmic math wizardry to check whether an investor is holding their phase2 refund
                # We set the maximum skipped investors to 10, since 1/rate can be arbitrarily large
                if (self.investors.index(investor) % round(min(10, 1/refundHoldRate)) == 0):
                    returnTotal += deficit * self.lp.defoPrice * (1 - refundTax)

                    # Investor sells rewards
                    self.dai.treasury -= deficit * self.lp.defoPrice * (1 - refundTax)
                else:
                    self.defo.vault += deficit

        self.lp.update_price()

    # Gets the treasury profits made from investments by the treasury
    def get_treasury_returns(self, apy, newInvestment):
        # Calculate amount of investments made
        profit = floor(self.dai.treasury / newInvestment) * newInvestment * apy / 365

        # Add investment returns to treasury
        self.dai.profits += profit

    # Error check to see how many returns the protocol owes daily
    def get_total_investor_returns(self):
        total = 0
        for investor in self.investors:
            total += investor.returns

        return total

    # Payout rewards to investors (not to be confused with cashing out)
    def payout_rewards(self):
        for investor in self.investors:
            investor.returns += investor.dailyReturn
            investor.currentReturnCycle += investor.dailyReturn

    # Sells off the presale nodes
    def populate_presale(self, daiAllocations):
        while (np.sum(self.nodes.numAvailable) > 0):
            numT1, numT2, numT3 = 0,0,0

            if (self.nodes.numAvailable[0] > 0):
                numT1 = abs(int(normal(9, 3)))
                if (numT1 > self.nodes.numAvailable[0]):
                    numT1 = self.nodes.numAvailable[0]

            if (self.nodes.numAvailable[1] > 0):
                numT2 = abs(int(normal(5, 3)))
                if (numT2 > self.nodes.numAvailable[1]):
                    numT2 = self.nodes.numAvailable[1]

            if (self.nodes.numAvailable[2] > 0):
                numT3 = abs(int(normal(2, 1)))
                if (numT3 > self.nodes.numAvailable[2]):
                    numT3 = self.nodes.numAvailable[2]

            counts = [numT1, numT2, numT3]

            if (numT1 > 0 or numT2 > 0 or numT3 > 0):
                self.investors.append(
                    self.Investor(
                        counts,
                        self.nodes
                    )
                )
                self.nodes.sell_nodes(counts)

    # Sells off the booster presale nodes
    def populate_boosters(self, daiAllocations, boosterCounts1, boosterRate1, boosterCosts1, boosterCounts2, boosterRate2, boosterCosts2):
        boosterCounts = [boosterCounts1, boosterCounts2]
        boosterRates = [boosterRate1, boosterRate2]

        for i in range(2):
            numT1, numT2, numT3 = 0,0,0
            while (True):
                if (numT1 < boosterCounts[i][0]):
                    counts = [1,0,0]
                    numT1 += 1
                elif (numT2 < boosterCounts[i][1]):
                    counts = [0,1,0]
                    numT2 += 1
                elif (numT3 < boosterCounts[i][2]):
                    counts = [0,0,1]
                    numT3 +=1
                else:
                    break

                self.investors.append(
                    self.Investor(
                        counts,
                        self.nodes
                    )
                )
                self.nodes.sell_nodes(counts)
                self.investors[-1].rewards = multiply(self.investors[-1].rewards, boosterRates[i])

        total = dot(boosterCounts1, boosterCosts1) + dot(boosterCounts2, boosterCosts2)

        self.dai.treasury += daiAllocations[0] * total
        self.dai.buyback += daiAllocations[1] * total
        self.dai.liquidity += daiAllocations[2] * total
        self.dai.marketing += daiAllocations[3] * total
        self.dai.team += daiAllocations[4] * total

    # Simply adds 1 to the days the investor has been active
    def update_days(self):
        for investor in self.investors:
            investor.days += 1

    # Creates an instance of a liquidity pool paired by DEFO and DAI
    def create_liquidity_pool(self, dai, defo):
        self.lp = self.LiquidityPool()

        self.dai.liquidity -= dai
        self.lp.dai += dai

        self.defo.liquidity -= defo
        self.lp.defo += defo

        self.lp.invariant = defo * dai
        self.lp.defoPrice = dai / defo

        self.initialPrice = self.lp.defoPrice # Get the initial price

    # Adds liquidity paired by DEFO and DAI based on the current price
    def add_liquidity(self, dai, defo):
        if (self.lp.defoPrice > 100):
            return

        if (self.lp.defoPrice * defo >= self.lp.daiPrice * dai):
            daiAmount = dai
            defoAmount = dai / self.lp.defoPrice
        else:
            defoAmount = defo
            daiAmount = defo * self.lp.defoPrice

        self.lp.dai += daiAmount
        self.dai.liquidity -= daiAmount

        self.lp.defo += defoAmount
        self.defo.liquidity -= defoAmount

        self.lp.invariant = self.lp.defo * self.lp.dai

    # Stabilizes the price by selling defo
    def stabilize_price(self, defo):
        if not self.sellOnNodeCreation:
            if (self.lp.defoPrice >= self.initialPrice * self.stabilizationCap and self.defo.treasury >= defo):
                self.defo.treasury -= defo
                self.lp.defo += defo

                previousDai = self.lp.dai
                self.lp.dai = self.lp.invariant / (self.lp.defo)

                self.dai.liquidity += (previousDai - self.lp.dai)
        else:
            if (self.defo.treasury >= self.sellAmount):
                self.defo.treasury -= self.sellAmount
                self.lp.defo += self.sellAmount

                previousDai = self.lp.dai
                self.lp.dai = self.lp.invariant / (self.lp.defo)

                self.dai.liquidity += (previousDai - self.lp.dai)

    # Buys back tokens from liquidity funds to increase price
    def buyback_tokens(self, defo):
        if (self.lp.defoPrice < self.initialPrice and self.dai.liquidity >= self.lp.defoPrice * defo):
            self.lp.defo -= defo
            self.dai.liquidity -= defo * self.lp.defoPrice
            self.lp.dai = self.lp.invariant / (self.lp.defo)
            self.defo.treasury += defo

        self.lp.update_price()

    class LiquidityPool:
        def __init__(self):
            self.defo = 0
            self.dai = 0
            self.defoPrice = 0
            self.daiPrice = 1
            self.invariant = 0

        # See uniswap v1 whitepaper for details
        # x = amount of DEFO, X = price of DEFO
        # y = amount of DAI,  Y = price of DAI = 1
        #
        # x*y = k    =>   y = k/x
        # X*x = Y*y  =>  X=(Y*y)/x
        #   => X=(Y*(k/x))/x=(1(k/x)/x)=k/x^2
        def update_price(self):
            self.defoPrice = self.invariant / (self.defo ** 2)

    class Funds:
        def __init__(self, allocations):
            self.allocations = allocations
            self.rewards = 0
            self.treasury = 0
            self.liquidity = 0
            self.marketing = 0
            self.team = 0
            self.profits = 0
            self.charity = 0
            self.buyback = 0
            self.vault = 0

        # Distributes DEFO to respective "contracts"
        def allocate_defo(self, funds):
            allocations = self.allocations

            self.rewards += allocations[0] * funds
            self.treasury += allocations[1] * funds
            self.liquidity += allocations[2] * funds
            self.marketing += allocations[3] * funds
            self.team += allocations[4] * funds

        # Distributes DAI to respective "contracts"
        def allocate_dai(self, funds):
            allocations = self.allocations

            self.treasury += allocations[0] * funds
            self.buyback += allocations[1] * funds
            self.liquidity += allocations[2] * funds
            self.marketing += allocations[3] * funds
            self.team += allocations[4] * funds

        # Calculate how much total funds are in the desired pool
        def get_total_funds(self):
            return self.rewards+self.treasury+self.liquidity+self.marketing+self.team+self.charity

    class Nodes:
        def __init__(self, available, costs, rewards, fees, salesTax, charityTax):
            self.numTiers = 3
            self.numAvailable = available
            self.numSold = [0,0,0]
            self.costs = costs.copy()
            self.rewards = rewards.copy()
            self.fees = fees
            self.salesTax = salesTax
            self.charityTax = charityTax

        # Sells out nodes from the protocol
        def sell_nodes(self, counts):
            self.numSold = add(self.numSold, counts)
            self.numAvailable = subtract(self.numAvailable, counts)

    class Investor:
        def __init__(self, counts, nodes):
            self.counts = counts
            self.costs = nodes.costs.copy()
            self.rewards = nodes.rewards.copy()
            self.invested = dot(nodes.costs, counts)
            self.dailyReturn = 0
            self.returns = 0
            self.days = 0
            self.returnsTaken = 0 # Used for ending phase 1 to check unclaimed rewards
            self.currentReturnCycle = 0
            self.vault = 0

        # Calculate how much DEFO an investors' yield gems acquire daily
        def get_daily_return(self, tokenPrice):
            total = 0

            # Loop through each yield gem
            for i in range(3):
                total += self.rewards[i] * self.counts[i] * self.costs[i]

            # Uses the initial DEFO price to calculate correct amount of DEFO
            # Example: DEFO $5, for a node costing $50, need $25 DAI and $25 DEFO
            #          So, divide rewards by $5, and take half, ie the ratio of DEFO to DAI
            return total * .5 / tokenPrice
