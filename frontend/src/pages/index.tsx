import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <Heading as="h1" className={styles.heroTitle}>
            {siteConfig.title}
          </Heading>
          <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
          <p className={styles.heroDescription}>
            Dive into the future of robotics and AI with our comprehensive guide to Physical AI,
            humanoid robotics, and embodied intelligence systems.
          </p>
          <div className={styles.buttons}>
            <Link
              className={clsx('button button--lg', styles.primaryButton)}
              to="/docs/book_modules/Module_1/Chapter_1_1_Introduction_to_Physical_AI">
              Start Reading
            </Link>
            <Link
              className={clsx('button button--lg button--outline', styles.secondaryButton)}
              to="/docs/book_modules/Module_1/Chapter_1_2_Sensor_Modalities_for_Robotics">
              Learn More
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

function StatsSection() {
  return (
    <section className={styles.statsSection}>
      <div className="container">
        <div className={styles.statsGrid}>
          <div className={styles.statItem}>
            <span className={styles.statNumber}>3</span>
            <span className={styles.statLabel}>Modules</span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statNumber}>15+</span>
            <span className={styles.statLabel}>Chapters</span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statNumber}>AI</span>
            <span className={styles.statLabel}>Powered Chatbot</span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statNumber}>RAG</span>
            <span className={styles.statLabel}>Enhanced Search</span>
          </div>
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <div className={styles.ctaContent}>
          <Heading as="h2" className={styles.ctaTitle}>
            Ready to Explore Physical AI?
          </Heading>
          <p className={styles.ctaDescription}>
            Start your journey into the world of humanoid robotics and embodied AI systems today.
          </p>
          <Link
            className={clsx('button button--lg', styles.ctaButton)}
            to="/docs/book_modules/Module_1/Chapter_1_1_Introduction_to_Physical_AI">
            Begin Your Journey
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description="The Complete Interactive Book on Physical AI and Humanoid Robotics with Embedded RAG Chatbot">
      <HomepageHeader />
      <main>
        <StatsSection />
        <HomepageFeatures />
        <CTASection />
      </main>
    </Layout>
  );
}
