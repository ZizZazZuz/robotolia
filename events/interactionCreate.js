module.exports = {
	name: 'interactionCreate',
	execute(interaction) {
		if (!interaction.isCommand()) return;

		const command = interaction.client.commands.get(interaction.commandName);

		console.log(`${interaction.user.tag} in #${interaction.channel.name} triggered /${interaction.commandName}.`);

		if (!command) {
			console.log('Command is Null.');
			return;
		}

		try {
			command.execute(interaction);
		}
		catch (error) {
			console.error(error);
			interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
		}
	},
};
