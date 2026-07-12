| Column        | Description        | Use in Model? | Reason                                    |
| ------------- | ------------------ | ------------- | ----------------------------------------- |
| `PTS`         | Points scored      | **Target**    | Variable being predicted                  |
| `GAME_DATE`   | Date of game       | Yes           | Used for ordering and feature engineering |
| `MATCHUP`     | Opponent and venue | Yes           | Can derive opponent and home/away         |
| `WL`          | Win/Loss           | No            | Known only after the game (data leakage)  |
| `PLUS_MINUS`  | Plus/minus         | No            | Post-game statistic                       |
| `FANTASY_PTS` | Fantasy scoring    | No            | Derived from post-game statistics         |
| `MIN`         | Minutes PLayed     | No            | Known after the game (data leakage)         
    `3|
