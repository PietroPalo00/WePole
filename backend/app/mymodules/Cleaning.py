import pandas as pd


flights_data = pd.read_csv('/app/app/flights.csv', encoding='ISO-8859-1')

# Remove useless columns
df_clean = flights_data.drop(columns=["Number of Travellers", "Customer"])


def clean_cost(value):

    if isinstance(value, str) and '£' in value:
        return float(value.replace('£', '').replace(',', '').strip())
    else:
        return value


df_clean['Price in £'] = df_clean[' Total Cost ex VAT '].apply(clean_cost)

# Renaming the columns for clarity
df_clean.rename(columns={' Total Cost ex VAT ': 'Price in £'}, inplace=True)
df_clean.rename(columns={'Journey Start Point': 'Departure'}, inplace=True)
df_clean.rename(columns={'Journey Finish Point': 'Arrival'}, inplace=True)

# Renaming an Air Carrier
plane = df_clean['Air Carrier']
plane = plane.replace('DO NOT USE - EASYJET - PLEASE ', 'EASYJET')
