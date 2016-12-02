var debug = false;
// var debug = process.env.NODE_ENV !== "production";
var webpack = require('webpack');
var path = require('path');

var webpack = require('webpack');
var path = require('path');

var STATIC_DIR = path.resolve(__dirname, 'static');

module.exports = {
  entry: path.resolve(STATIC_DIR, 'client.js'),
  output: {
    path: STATIC_DIR,
    filename: "client.bundle.js"
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015']
        }
      }
    ]
  },
  resolve: {
    extensions: ['', '.js', '.json']
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': '"production"'
      }
    }),
    new webpack
      .optimize
      .DedupePlugin(),
    new webpack
      .optimize
      .UglifyJsPlugin({
        mangle: false,
        sourcemap: false,
        output: {
          comments: false
        },
        compress: {
          warnings: false
        }
      })
  ]
};