const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const max_dice = 10; // Set maximum number of Dice so as to avoid troll spam

module.exports = {
	data: new SlashCommandBuilder()
		.setName('roll')
		.setDescription('Roll a number of configurable dice!')
		.addIntegerOption(option =>
			option.setName('sides')
				.setDescription('Number of sides for the die.')
				.setRequired(true))
		.addIntegerOption(option =>
			option.setName('dice')
				.setDescription('Total number of dice to roll. Default: 1'))
		.addStringOption(option =>
			option.setName('verbosity')
				.setDescription('Show each individual roll (Verbose) or a simple sum (Simple). Default: Simple')
				.addChoice('Verbose', 'verbose')
				.addChoice('Simple', 'simple')),
	async execute(interaction) {

		// Get our options
		const sides = interaction.options.getInteger('sides');
		let dice = interaction.options.getInteger('dice');
		let verbosity = interaction.options.getString('verbosity');

		// Check if we have < 2 Sides to prevent trolling
		if (sides < 2) {
			return interaction.reply({content: 'Not enough sides to roll! You must have more than 1 side.', ephemeral: true});
		}

		// Set Dice to 1 if not chosen. Else, prevent trolling of max dice number.
		if (!dice) {
			dice = 1;
		}
		else if (dice < 1) {
			return interaction.reply({content: 'Cannot roll less than 1 die.', ephemeral:true});
		}
		else {
			dice = Math.min(dice, max_dice);
		}

		// Format a simple roll function
		if (dice === 1) {
			await interaction.deferReply();

			// Roll our die
			let result = RollDice(sides);

			// Format into a pretty embed
			const embed = new MessageEmbed()
				.setColor('#E61313')
				.setTitle(`:game_die: Roll Results (1d${sides.toString()}) :game_die:`)
				.addFields(
					{ name: 'Total', value: result.toString()},
				);

			// Send the embed to our reply.
			interaction.editReply({ embeds: [embed] });
		}
		else {
			await interaction.deferReply();

			// Create our results array and total
			const results_array = new Array();
			let results_total = 0;

			// Roll our dice.
			for (i = 0; i < dice; i++) {
				results_array[i] = RollDice(sides);
				results_total = results_total + results_array[i];
			}

			// Format into a pretty embed
			const embed = new MessageEmbed()
				.setColor('#E61313')
				.setTitle(`:game_die: Roll Results (${dice}d${sides.toString()}) :game_die:`)
				.addFields(
					{ name: 'Total', value: results_total.toString()},
				);
			// Expound if Verbose was requested.
			if (verbosity === 'Verbose' || verbosity === 'verbose') {
				let results_string = '';

				// Construct a string of results based on the length of the array
				for(j=0; j < results_array.length; j++) {
					results_string = results_string + results_array[j].toString() + ' ';
				 }
				 // Add our Rolls field to the existing embed.
				 embed.addFields(
						 { name: `Rolls`, value: results_string}
					 );
			}

			// Send the embed to our reply.
			interaction.editReply({ embeds: [embed] });
		}

		function RollDice(num_of_sides){
			let result = Math.random() * ((num_of_sides + 1) - 1) + 1;
			return Math.floor(result);
		}

	},
};
