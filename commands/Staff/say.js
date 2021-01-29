const { successColor } = require("../../config.json")
const Discord = require("discord.js")

module.exports = {
  name: "say",
  description: "Says something in a specific channel.",
  usage: "+say <message>",
  cooldown: 600,
  aliases: ["parrot", "repeat", "send"],
  roleWhitelist: ["768435276191891456"], //Discord Staff
  async execute(message, strings, args) {
    const executedBy = strings.executedBy.replace("%%user%%", message.author.tag)
    if (!args[0]) return
    const sendTo = message.client.channels.cache.get(args[0].replace(/[\\<>@#&!]/g, ""))
    args.splice(0, 1)
    const toSend = args.join(" ")
    let msg

    if (!sendTo) throw "noChannel"
    if (!toSend) throw "noMessage"
    if (!message.member.permissionsIn(sendTo).has("SEND_MESSAGES")) throw "noPermission"

    if (message.member) if (message.member.hasPermission("MANAGE_ROLES")) {
      msg = await sendTo.send(toSend).catch(() => { throw "noChannel" })
    } else {
      msg = await sendTo.send(">>> " + toSend).catch(() => { throw "noChannel" })
    }
    const embed = new Discord.MessageEmbed()
      .setColor(successColor)
      .setAuthor(strings.moduleName)
      .setTitle(strings.success)
      .setDescription(`${sendTo}:\n${toSend}`)
      .setFooter(executedBy, message.author.displayAvatarURL())
    message.channel.send(embed)
  }
}