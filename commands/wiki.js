const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const fetch = require('node-fetch');
const trim = (str, max) => ((str.length > max) ? `${str.slice(0, max - 3)}...` : str);

module.exports = {
	data: new SlashCommandBuilder()
		.setName('wiki')
		.setDescription('Search Wikipedia for a summary!')
		.addStringOption(option =>
			option.setName('input')
				.setDescription('What you want to search for.')
				.setRequired(true)),
	async execute(interaction) {
		await interaction.deferReply();

		const term = interaction.options.getString('input');
		console.log(`Attempting Search with option ${term}.`);

		// Turn into a URL search format so we don't have to do messy formatting ourselves.
		const query = new URLSearchParams(term);

		// Hit Wikipedia's API.
		const result = await fetch(`https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${query}&srlimit=1&srnamespace=0&format=json`).then(response => response.json());

		// On the off-chance nothing is found, say so.
		if (!result) {
			return interaction.editReply(`No results found for **${term}**.`);
		}

		// If something is found, get the main page and the thumbnail.
		const pageTitle = result.query.search[0].title;
		const pageid = result.query.search[0].pageid;
		const resultingPage = await fetch(`https://en.wikipedia.org/w/api.php?action=query&titles=${pageTitle}&prop=extracts&exintro=&explaintext=&format=json`).then(response => response.json());
		const resultingPageImages = await fetch(`https://en.wikipedia.org/w/api.php?action=query&titles=${pageTitle}&prop=pageimages&piprop=thumbnail|original&format=json`).then(response => response.json());

		// Check if a thumbnail exists, and if so, assign it for the embed.
		let pageThumbnail = '';
		if (resultingPageImages.query.pages[pageid].thumbnail) {
			pageThumbnail = resultingPageImages.query.pages[pageid].thumbnail.source;
		}
		else {
			pageThumbnail = 'https://en.wikipedia.org/static/images/project-logos/enwiki.png';
		}

		// Format into an embed

		const embed = new MessageEmbed()
			.setColor('#C0D6E4')
			.setTitle(resultingPage.query.pages[pageid].title)
			.setURL(`https://en.wikipedia.org/?curid=${resultingPage.query.pages[pageid].pageid}`)
			.setAuthor('Wikipedia', 'https://en.wikipedia.org/static/images/project-logos/enwiki.png', 'https://en.wikipedia.org')
			.setThumbnail(`${pageThumbnail}`)
			.addFields(
				{ name: 'Summary', value: trim(resultingPage.query.pages[pageid].extract, 600) },
			)
			.setFooter('This summary is from the first entry from Wikipedia based on your search terms.');

		interaction.editReply({ embeds: [embed] });
	},
};
