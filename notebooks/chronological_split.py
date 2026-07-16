import pandas as pd

def chronological_split(df, train_size):

    train_parts = []
    test_parts = []

    for _, player in df.groupby("PLAYER_ID"):

        split = int(len(player) * train_size)

        train_parts.append(player.iloc[:split])
        test_parts.append(player.iloc[split:])

    train = pd.concat(train_parts, ignore_index=True)
    test = pd.concat(test_parts, ignore_index=True)

    return train, test