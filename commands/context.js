const { workingColor, errorColor, successColor, neutralColor } = require("../config.json");
const Discord = require("discord.js");
const { GoogleSpreadsheet } = require('google-spreadsheet')
const { promisify } = require('util')
const creds = require('../service-account.json')

module.exports = {
    name: "context",
    description: "Does nothing for now!",
    usage: "context <link/ID>",
    channelWhiteList: ["549894938712866816", "624881429834366986", "730042612647723058"],
    cooldown: 3,
    execute(message, args) {
        accessSpreadsheet()
    }
}

async function accessSpreadsheet() {
    const doc = new GoogleSpreadsheet('8f8057b93cce4dda659f117b0401582414e10637')
    doc.useServiceAccountAuth(creds)
        .then(() => {
            doc.getInfo()
                .then(info => {
                    console.log(`Loaded doc: ` + info.title + ` by ` + info.author.email)
                    const sheet = info.worksheets[0]
                    console.log(
                        `sheet 1: ` + sheet.title + ` ` + sheet.rowCount + `x` + sheet.colCount
                    )
                })
        })
}