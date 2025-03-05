module.exports = {
    publicPath: './',
    outputDir: 'dist',
    assetsDir: 'assets',

    chainWebpack: config => {
      config.plugin('html').tap(args => {
        args[0].title = 'Votre Titre de Projet';
        return args;
      });
    }
  }
