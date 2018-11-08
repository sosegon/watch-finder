var path = require('path');
var webpack = require('webpack');
const HtmlWebPackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  entry: {
    index: path.join(__dirname, './src/js/index.js')
  },
  output: {
    filename: 'build.js',
    path: path.join(__dirname, '/dist/js/')
  },
  module: {
    rules: [
      {
        test: /\.html$/,
        use: [{ loader: "html-loader", options: { minimize: true } }]
      },
      {
        exclude: [/node_modules/, '/src/js/opencv.js'], /*opencv is big and has to be copied*/
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
    new webpack.ProvidePlugin({
      "React" : "react"
    }),
    new CopyWebpackPlugin([
      {from: 'src/assets/', to: '../assets/'},
      {from: 'src/js/opencv.js', to: 'opencv.js'}
    ])
  ]
};