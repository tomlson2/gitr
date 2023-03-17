import Head from 'next/head';
import styles from '../styles/Home.module.css';
import Link from 'next/link';
import Header from './components/Header';
import React from 'react';
import useTypewriter from './hooks/useTypewriter';

export default function Home() {
  const typewriterText = useTypewriter('Generative AI', 100);

  return (
    <div>
      <Header />
      <div className={styles.container}>
        <Head>
          <title>Documatic</title>
          <meta name="description" content="Developer tools for documentation" />
        </Head>

        <main className={styles.main}>
          <h1 className={styles.title}>
            {typewriterText}
            <br />in your repository
          </h1>
          <div className={styles.buttonContainer}>
            <Link href="/write-me">
              <button className={styles.button}>Try it out</button>
            </Link>
          </div>
        </main>
      </div>
    </div>
  );
}
