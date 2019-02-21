import os
import asyncio  # noqa: F401
import datetime
import discord
from redbot.core import commands, checks, Config

@on('messageReactionAdd')
private async _onReaction(reaction: MessageReaction, user: User): Promise<any> {
    if (user.id === this._client.user.id)
        return;

    const guildmember: GuildMember = await reaction.message.guild.members.fetch(user);
    let guildStorage: GuildStorage = await this._client.storage.guilds.get(reaction.message.guild.id);
    let channel = <TextChannel> await reaction.message.channel;
    let role: Role;

    if (!user.bot && reaction.message.channel.id !== Constants.assignmentChannelId) {
        const logs: TextChannel = <TextChannel> reaction.message.guild.channels.find(chan => chan.name === 'reaction-logs');
        const embed: MessageEmbed = new MessageEmbed()
            .setColor(Constants.reactionAdd)
            .setAuthor(`${user.tag} (${user.id})`, user.avatarURL())
            .setThumbnail(reaction.emoji.url)
            .setDescription(`**Reason:** A reaction was added\n`
                + `**Channel:** #${channel.name} (${channel.id})\n`
                + `**Message:** (${reaction.message.id})\n`
                + `**Emoji:** ${reaction.emoji.name} (${reaction.emoji.id})\n`
                + `**Message Link:** https://discordapp.com/channels/${channel.guild.id}/${channel.id}/${reaction.message.id}`)
            .setTimestamp();
        if (logs) {
            logs.send({embed});
        }
    }
