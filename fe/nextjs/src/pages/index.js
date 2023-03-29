import Head from 'next/head';
import styles from '../styles/Home.module.css';
import Link from 'next/link';
import Header from './components/Header';
import React from 'react';
import useTypewriter from './hooks/useTypewriter';
import Lottie from 'react-lottie';
import githubAnimationData from '../../public/github-animation.json'

export default function Home() {
  const typewriterText = useTypewriter('Generative AI', 100);

  return (
    <div>
      <Header />
      <div className={styles.container}>
        <Head>
          <title>gitr</title>
          <meta name="description" content="Developer tools for documentation" />
        </Head>

        <main className={styles.main}>
          <h1 className={styles.title}>
            {typewriterText}
            <br />in your repository
          </h1>
          <Lottie
            options={{
              loop: true,
              autoplay: true,
              animationData: githubAnimationData,
              rendererSettings: {
                preserveAspectRatio: 'xMidYMid slice',
              },
            }}
            height={175}
            width={175}
          />
          <div className={styles.buttonContainer}>
          <Link href="/write-me">
            <button className={styles.button}>writeme</button>
          </Link>
          <Link href="/auto-api">
            <button className={styles.button}>auto api</button>
          </Link>
          </div>
        </main>
      </div>
    </div>
  );
}
