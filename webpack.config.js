const path = require('path')
module.exports = {
    entry: "./taskapp/static/js_input/render_app.js",
    output: {
        path: path.join(__dirname, "taskapp/static/js/"),
        filename: "built.js",
        sourceMapFilename: "built.js.map"
    },
    devtool: "source-map",
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use:{
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/react']
                    }
                }
            }
        ]
    }
}