const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('serverinfo')
		.setDescription('Replies with server info!'),
	async execute(interaction) {
		await interaction.reply(`Server Name: ${interaction.guild.name}\nServer Members: ${interaction.guild.memberCount}`);
	},
};
