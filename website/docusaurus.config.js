const repository = process.env.GITHUB_REPOSITORY || "skorbiz/compliance-as-code";
const [owner, repo] = repository.split("/");
const repoUrl = `https://github.com/${repository}`;
const isCi = process.env.CI === "true";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Compliance as Code",
  tagline: "Minimal web documentation generated from shared YAML data",
  url: `https://${owner}.github.io`,
  baseUrl: isCi ? `/${repo}/` : "/",
  organizationName: owner,
  projectName: repo,
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },
  presets: [
    [
      "classic",
      {
        docs: {
          routeBasePath: "/",
          sidebarPath: require.resolve("./sidebars.js"),
        },
        blog: false,
        pages: false,
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
  themeConfig: {
    navbar: {
      title: "Compliance as Code",
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Docs",
        },
        {
          href: repoUrl,
          label: "GitHub",
          position: "right",
        },
      ],
    },
  },
};

module.exports = config;
