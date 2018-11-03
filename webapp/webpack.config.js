var path = require('path');
var webpack = require('webpack');
const HtmlWebPackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: {
    index: path.join(__dirname, './src/index.js')
  },
  output: {
    filename: 'build.js',
    path: path.join(__dirname, '/dist')
  },
  module: {
    rules: [
      {
        test: /\.html$/,
        use: [{ loader: "html-loader", options: { minimize: true } }]
      },
      {
        exclude: /node_modules/,
        test: /\.js$/,
        loader: 'babel-loader'
      },
      {
        test: /\.scss$/,
        use: [
          "style-loader",
          "css-loader",
          "sass-loader"
        ]
      },
      {
        test: /\.(png|jpg)$/,
        loader: 'url-loader'
      }
    ]
  },
  plugins: [
    new HtmlWebPackPlugin({
      template: "src/index.html",
      filename: "./index.html"
    }),
    new webpack.ProvidePlugin({
      "React" : "react"
    })
  ]
};