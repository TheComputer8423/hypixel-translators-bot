const { workingColor, errorColor, successColor, neutralColor } = require("../config.json");
const Discord = require("discord.js");

module.exports = {
  name: "permission",
  description: "See if the bot and author have a specified permission or lists all permissions.",
  aliases: ["perm", "perms", "gotperm", "hasperm", "permissions"],
  usage: "permission [name of permission]",
  channelWhiteList: ["549894938712866816", "624881429834366986", "730042612647723058"], // bots staff-bots bot-development
  execute(strings, message, args) {
    try {
      const executedBy = strings.executedBy.replace("%%user%%", message.author.tag)
      const embed = new Discord.MessageEmbed()
        .setColor(workingColor)
        .setAuthor(strings.moduleName)
        .setTitle(strings.loading)
        .setFooter(executedBy)
      message.channel.send(embed).then(msg => {
        if (args[0]) { //Argument given - show if bot and author have specific permission
          const perm = args[0].toUpperCase()
          const authorPerm = message.member.hasPermission(perm)
          const botPerm = msg.member.hasPermission(perm)
          const embed = new Discord.MessageEmbed()
            .setColor(successColor)
            .setAuthor(strings.moduleName)
            .setTitle(strings.specific.replace("%%perm%%", strings.perms[perm]))
            .addFields(
              { name: msg.author.tag, value: strings[botPerm], inline: true },
              { name: message.author.tag, value: strings[authorPerm], inline: true }
            )
            .setFooter(executedBy)
          msg.edit(embed)
        } else { //No argument given - show all bot and author permissions
          var authorP = []
          var botP = []
          const authorPerms = message.member.permissions.toArray().forEach(e => { authorP.push(strings.perms[e]) })
          const botPerms = msg.member.permissions.toArray().forEach(e => { botP.push(strings.perms[e]) })
          const embed = new Discord.MessageEmbed()
            .setColor(successColor)
            .setAuthor(strings.moduleName)
            .setTitle(strings.list)
            .addFields(
              { name: msg.author.tag, value: botP.join(", ") },
              { name: message.author.tag, value: authorP.join(", ") }
            )
            .setFooter(executedBy)
          msg.edit(embed)
        }
      })
    } catch (err) { throw err }
  }
}