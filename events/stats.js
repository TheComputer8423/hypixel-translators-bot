const { workingColor, errorColor, successColor, neutralColor, langdb } = require("../config.json");
const Discord = require("discord.js");
const fetch = require("node-fetch");

module.exports = {
    execute(client, manual) {
        var d = new Date();
        var n = d.getMinutes();
        if (n == "0" || n == "20" || n == "40" || manual) {
            get(client)
        }
    }
}

async function get(client) {
    let url = "https://api.crowdin.com/api/project/hypixel/status?login=qkeleq10&account-key=8205d22af119c4233b1940265bdd77d9&json"
    let settings = { method: "Get" }
    var index = 0
    fetch(url, settings)
        .then(res => res.json())
        .then((json) => {
            json.reverse()
            client.channels.cache.get("748538826003054643").messages.fetch({ limit: 100 })
                .then(messages => {
                    fiMessages = messages.filter(msg => msg.author.bot)
                    fiMessages.forEach(async (msg) => {
                        var r = json[index]
                        var langdbEntry = langdb.find(o => o.name === r.name)
                        const embed = new Discord.MessageEmbed()
                            .setColor(langdbEntry.colour)
                            .setTitle(langdbEntry.emoji + " | " + r.name)
                            .addFields({ name: (r.translated_progress + "% translated (" + r.translated + "/" + r.phrases + " strings)"), value: (r.approved_progress + "% approved (" + r.approved + "/" + r.phrases + " strings)\n\nTranslate on https://crowdin.com/project/hypixel/" + r.code + "") })
                            //.addFields({ name: r.name, value: ("**" + r.translated + " translated** (" + Math.round((100 * r.translated) / r.phrases) + "% from " + r.phrases + ")\n**" + r.approved + " approved** (" + Math.round((100 * r.approved) / r.phrases) + "% from " + r.phrases + ")"), inline: true })
                            .setTimestamp()
                        msg.edit("", embed)
                        index++
                    })
                })
            client.channels.cache.get("730042612647723058").messages.fetch("748584877921796146")
                .then(stringCount => {
                    if (stringCount.content !== json[0].phrases) {
                        client.channels.cache.get("549503985501995011").send("> <a:coolparty:728990234930315344> **New Strings!**\n" + Number(Number(json[0].phrases) - Number(stringCount.content)) + " strings have been added to the Hypixel project.")
                        stringCount.edit(json[0].phrases)
                    }
                })
        })
}