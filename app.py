import math
import ipywidgets as widgets
from IPython.display import display, clear_output

# Create widgets with wider descriptions and adjust layout
principle_type = widgets.Dropdown(
    options=[("USDT", "usdt"), ("Crypto Coin", "crypto")],
    value="crypto",
    description="Principle Type:",
    style={'description_width': 'initial'}
)

leverage_slider = widgets.FloatSlider(value=5.0000, min=1.0000, max=10.0000, step=0.0001, description="Leverage:",
                                       style={'description_width': 'initial'})
leverage_input = widgets.BoundedFloatText(value=5.0000, min=1.0000, max=10.0000, step=0.0001, description="Leverage:",
                                           style={'description_width': 'initial'})
principle_input = widgets.FloatText(value=100, description="Principle:",
                                    style={'description_width': 'initial'})
price_yx_input = widgets.FloatText(value=1, description="Price (USDT per coin):",
                                   style={'description_width': 'initial'})
new_price_yx_input = widgets.FloatText(value=1.01, description="New Price (USDT per coin):",
                                       style={'description_width': 'initial'})

# Align all text boxes
for widget in [leverage_input, principle_input, price_yx_input, new_price_yx_input]:
    widget.layout = widgets.Layout(width='250px')

# Sync slider and input manually
def sync_leverage(change):
    leverage_slider.value = round(leverage_input.value, 4)  # Round to 4dp

def sync_leverage_slider(change):
    leverage_input.value = round(leverage_slider.value, 4)  # Round to 4dp

leverage_input.observe(sync_leverage, names='value')
leverage_slider.observe(sync_leverage_slider, names='value')

# Function to calculate and display results
def update_results(change=None):
    clear_output(wait=True)  # Prevent excessive prints

    # Get values
    leverage = round(leverage_input.value, 4)
    principle = principle_input.value
    price_yx = price_yx_input.value
    new_price_yx = new_price_yx_input.value

    # Liquidity Calculations
    liquidity = principle * leverage
    liquidity_value_y = liquidity / 2
    liquidity_value_x = liquidity_value_y / price_yx
    k = liquidity_value_x * liquidity_value_y

    # Liquidation Price
    liquidation_price = 1.05 * price_yx * ((liquidity - principle) / liquidity) ** 2

    # Nett & Total Worth
    x1 = math.sqrt(k / new_price_yx)
    y1 = new_price_yx * x1
    total_worth = y1 + x1 * new_price_yx
    debt = liquidity - principle
    nett = total_worth - debt
    final_worth = nett / new_price_yx  # Updated final worth formula

    # Display widgets & results
    display(principle_type, leverage_slider, leverage_input, principle_input, price_yx_input, new_price_yx_input)
    print(f"Liquidation Price : {liquidation_price:.4f} USDT")
    print(f"Final USDT        : {nett:.4f} USDT")
    print(f"Final Coin        : {final_worth:.4f} Coin")

# Observe input changes
for widget in [principle_type, leverage_slider, leverage_input, principle_input, price_yx_input, new_price_yx_input]:
    widget.observe(update_results, names='value')

# Initial display
update_results()
