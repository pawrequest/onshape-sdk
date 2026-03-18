// @ts-check

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Onshape Python SDK',
  tagline: 'A lightweight, fully-typed Python SDK for the Onshape REST API',
  favicon: 'img/favicon.ico',
  staticDirectories: ['static'],

  url: 'https://zachariah-sharma.github.io',
  baseUrl: '/pyshape/',

  organizationName: 'zachariah-sharma',
  projectName: 'pyshape',

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        defaultMode: 'dark',
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Onshape SDK',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docs',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://github.com/zachariah-sharma/pyshape',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              { label: 'Getting Started', to: '/' },
              { label: 'API Reference', to: '/api/client' },
            ],
          },
          {
            title: 'Resources',
            items: [
              { label: 'GitHub', href: 'https://github.com/zachariah-sharma/pyshape' },
              { label: 'Onshape API Docs', href: 'https://onshape-public.github.io/docs/' },
              { label: 'API Explorer', href: 'https://cad.onshape.com/glassworks/explorer' },
            ],
          },
        ],
        copyright: `Onshape Python SDK Documentation`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
        additionalLanguages: ['python', 'bash', 'json'],
      },
    }),
};

module.exports = config;
