# tetra-league-stats
A tool to view statistics from TETR.IO's ranked competitive mode TETRA LEAGUE.

## Usage
The program needs a JSON dump of the TETRA LEAGUE data; this can be acquired with `curl https://ch.tetr.io/api/users/lists/league/all -o tetraleaguerankings.json`.

* `python tetra-league-stats.py --get-user USERNAME` gets USERNAME's stats
* `python tetra-league-stats.py --get-rank N` gets the Nth-best player's stats
* `python tetra-league-stats.py --print-ranks` gets a list of the rating required to reach each letter rank

`--input-file PATH` can be used to provide a different input file to the program.

