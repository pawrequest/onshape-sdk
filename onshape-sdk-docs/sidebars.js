/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'Guides',
      collapsed: false,
      items: [
        'guides/installation',
        'guides/authentication',
        'guides/url-parsing',
        'guides/error-handling',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      collapsed: false,
      items: [
        'api/client',
        'api/documents',
        'api/parts',
        'api/part-studios',
        'api/assemblies',
        'api/translations',
        'api/drawings',
        'api/blob-elements',
        'api/metadata',
        'api/thumbnails',
        'api/webhooks',
      ],
    },
    'types',
  ],
};

module.exports = sidebars;
