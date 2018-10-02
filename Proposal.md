# Project Luther Proposal

### What is the value of your MLB rookie?

Jason Salazer-Adams  

### Scope

Every MLB rookie can be a free agent in 6 years of service time. Each owner would much rather pay their young players long term who will also provide value long-term, rather than waiting until free agency. The inherit risk of waiting until free agency is the rookie underperforms their peers, and thus is over-paid for their value. Ideally, the player over-performs for the contract signed prior to free agency epoch. Can you predict the free-agency value of a rookie batter? The value would be an upper bound salary to then use in negotiations with current rookies.  

### Methodology

1. Get all rookies starting in 1985 to present. Salary information on baseballrefernce.com could be incomplete prior to 1985.  
2. Get all statistics for the rookie players.
3. Build a linear regression model relating batting statistics to salary at year 6.  

### Data

- Salary data by player by year (service term > 5 is free agent contract)
- List of rookies by MLB season
- fangraphs.com / baseballreference.com / http://legacy.baseballprospectus.com/compensation/cots/ (detailed salary data)

### Prediction

Salary of a player after 6 calendar years from MLB debut.

### Features

Features of the rookie player to be predicted.

|Feature|Description
|---|---|
|AVG |Batting average|
|HR |Home runs|
|H |Hits|
|R |Runs|
|SB |Stolen Bases|
|TB |Total Bases|
|2B |Doubles|
|3B |Triples|
|RBI |Runs batted in|
|BB |Walks|
|SO |Strike outs|
|Postion | Main position played (categorical)|

### Things to consider

- Need to adjust for inflation and use a logarithimic scale for salaries.
- Impact of contracts provided prior to the free agency year.
- Adding sabermetric type measurements as features.