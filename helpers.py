import plotly.graph_objects as go
import numpy as np

def graph_pyplot(axs, x, y1, y2, y3, y4):
    axs[1,0].plot(x,y1, label=f"Rewards")
    axs[1,0].plot(x,y2, label=f"Treasury")
    axs[1,0].plot(x,y4, label=f"Liquidity")
    axs[1,1].plot(x,y3)

    return axs

def graph_plotly(x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14):
    g3 = go.Figure(data=[go.Scatter(x=x,y=y1, name="Reward Pool"),
                            go.Scatter(x=x,y=y2, name="Treasury"),
                            go.Scatter(x=x,y=y4, name="Liquidity"),
                            go.Scatter(x=x,y=y12, name="Team/Marketing"),
                            go.Scatter(x=x,y=y6, name="Charity"),
                            go.Scatter(x=x, y=y14, name="Vault")])

    g4 = go.Figure(data=[go.Scatter(x=x,y=y3)])

    g5 = go.Figure(data=[go.Scatter(x=x,y=y7, name="Buyback"),
                            go.Scatter(x=x,y=y8, name="Treasury"),
                            go.Scatter(x=x,y=y9, name="Liquidity"),
                            go.Scatter(x=x,y=y13, name="Team/Marketing"),
                            go.Scatter(x=x,y=y11, name="Charity"),
                            go.Scatter(x=x,y=y10, name="Treasury Profits")])


    return g3, g4, g5

def update_plotly(g1, g2, g3, g4, g5, g6, g7):
        g1.update_layout(
            title={
                'text': "Node Investment Returns",
                'y':.9,
                'x':.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Days Passed",
            yaxis_title="Total Returns (DEFO)",
            template="plotly_dark"
        )

        g2.update_layout(
            title={
                'text': "Node Reward Tapering",
                'y':.9,
                'x':.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Days Passed",
            yaxis_title="Reward Percentage",
            template="plotly_dark"
        )

        g3.update_layout(
            title={
                'text': "DEFO Funds",
                'y':.9,
                'x':.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Days Passed",
            yaxis_title="Pool Funds (DEFO)",
            template="plotly_dark"
        )

        g4.update_layout(
            title={
                'text': "Daily Reward Payouts",
                'y':.9,
                'x':.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Days Passed",
            yaxis_title="Daily Rewards (DEFO)",
            template="plotly_dark"
        )

        g5.update_layout(
            title={
                'text': "DAI Funds",
                'y':.9,
                'x':.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Days Passed",
            yaxis_title="Pool Funds (DAI)",
            template="plotly_dark"
        )

        g6.update_layout(
            title={
                'text': "Price Action",
                'y':.9,
                'x':.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Days Passed",
            yaxis_title="DEFO Value ($)",
            template="plotly_dark"
        )

        g7.update_layout(
            title={
                'text': "Liquidity Pool",
                'y':.9,
                'x':.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Days Passed",
            yaxis_title="Token Amounts",
            template="plotly_dark"
        )

        return g1, g2, g3, g4, g5, g6, g7

def print_group_results(investors, nodes, rewards):
  length = len(investors)
  print(f'Number of Investors: {length}')
  print(f'Number of Nodes Sold: {nodes.numSold}')
  print(f'Daily Rewards: {rewards} USD')

def print_investment_results_initial(daily, model):
  print(f"Nodes sold daily: {daily}\n")
  print(f"Total DEFO: {model.defo.get_total_funds()}")
  print(f"Reward Pool: {model.defo.rewards} USD")
  print(f"Treasury: {model.defo.treasury} USD\n")
  print(f"Starting Node Counts: {model.nodes.numSold}")
  print(f"Starting Investor Count: {len(model.investors)}")
  print(f"Daily Rewards: {model.dailyRewards} DEFO\n")

def print_investment_results_final(model, roi1x, roi2x, initialRunaway, extendedRunaway, totalFunds):

    print(f"Final Node Counts: {model.nodes.numSold}")
    print(f"Final Investor Count: {len(model.investors)}")
    print(f"Final Daily Rewards: {model.dailyRewards} USD\n")
    print(f"Initial Runaway: {initialRunaway}")
    print(f"Extended Runaway: {extendedRunaway}")
    print(f"1x ROI: {roi1x}")
    print(f"2x ROI: {roi2x}")
    print(f"Liquidity: {model.defo.liquidity}")
    print(f'funds: {totalFunds}')


def update_ax(axs, days):
  axs[0,0].set_title("Node Rewards")
  axs[0,1].set_title("Node Tapering")
  axs[0,0].set_xlabel("Days Passed")
  axs[0,0].set_ylabel("Total Reward")
  axs[0,1].set_xlabel("Days Passed")
  axs[0,1].set_ylabel("Daily Reward (%)")
  axs[0,0].legend()
  axs[0,1].legend()

  #axs[1,0].legend()
  axs[1,0].set_title("Reward Pool/Treasury Runaway")
  axs[1,1].set_title("Daily Reward Payouts")
  axs[1,0].set_xlabel("Days Passed")
  axs[1,0].set_ylabel("Pool Funds")
  axs[1,1].set_xlabel("Days Passed")
  axs[1,1].set_ylabel("Daily Rewards")
  axs[1,0].set_xlim([0, days])
  axs[1,1].set_xlim([0, days])
  axs[1,0].legend()
  return axs

def sma(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
