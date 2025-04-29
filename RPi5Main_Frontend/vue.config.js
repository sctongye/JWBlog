const path = require("path");

module.exports = {
  transpileDependencies: [],
  outputDir: path.resolve(__dirname, "../static/blog"),
  assetsDir: "",
  indexPath: "index.html",
  publicPath: process.env.NODE_ENV === "production" ? "/blog/" : "/",
  productionSourceMap: false,
  configureWebpack: {
    output: {
      filename: "static/js/[name].[hash].js",
      chunkFilename: "static/js/[name].[hash].js",
    },
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
};
