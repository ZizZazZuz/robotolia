��#   R o b o t o l i a  
 

To setup the Bot:
1) Ensure Node.js v16+ is installed
2) Ensure npm is installed
3) Navigate to the Robotolia directory and run `npm install`.

To setup Environment Variables:
1) Create a .env file
2) Add "DISCORD_TOKEN=<bot token here>" to its own line
3) Add "CLIENT_ID=<bot client id here>" to its own line
4) Add "GUILD_ID=<server id here>" to its own line
5) Save

To setup new commands:
1) Create a new <commandname>.js file in the commands directory
2) Create your code for the command within that file.
3) Run `node deploy-commands.js`from the main directory.

To run Robotolia:
1) Run `node anatolia-bot-2_0.js` from the main directory.
2) Ctrl + C to stop.
