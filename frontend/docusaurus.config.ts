import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'AI Powered Book',
  tagline: 'The Complete Interactive Book + Embedded RAG Chatbot',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  // UPDATE: Replace with your GitHub Pages URL
  url: process.env.SITE_URL || 'https://your-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: process.env.BASE_URL || '/hackathon-book/',

  // GitHub pages deployment config.
  // UPDATE: Replace with your GitHub username and repo name
  organizationName: process.env.GITHUB_ORG || 'your-username', // Your GitHub username
  projectName: process.env.GITHUB_REPO || 'hackathon-book', // Your repo name
  trailingSlash: false,

  // Custom fields for runtime configuration
  customFields: {
    apiUrl: process.env.API_URL || 'http://localhost:8000',
  },

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // Remove edit URL as it points to external Docusaurus repo
        // editUrl:
        //     'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [
    // Search plugin commented out due to network connectivity issues
    // Uncomment and run `npm install` when network is available
    // [
    //   require.resolve('@easyops-cn/docusaurus-search-local'),
    //   {
    //     hashed: true,
    //     language: ['en'],
    //     highlightSearchTermsOnTargetPage: true,
    //     explicitSearchResultPath: true,
    //   },
    // ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'AI Powered Book',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          type: 'search',
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
            {
              label: 'Book',
              to: '/docs/book_modules/Module_1/Chapter_1_1_Introduction_to_Physical_AI',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI Powered Book. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
