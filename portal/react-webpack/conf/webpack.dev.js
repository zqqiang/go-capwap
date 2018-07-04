const merge = require('webpack-merge')
const common = require('../webpack.config.js')
const path = require("path");
const webpack = require("webpack");

module.exports = merge(common, {
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: ['style-loader', "css-loader", "sass-loader"]
            }
        ]
    },
    plugins: [new webpack.HotModuleReplacementPlugin()],
    devServer: {
        contentBase: path.join(__dirname, '../dist'),
        port: 3000
    }
})