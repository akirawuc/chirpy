import { ConnectButton } from '@rainbow-me/rainbowkit';
import type { NextPage } from 'next';
import LensAuthentication from '../components/login';
import {useAccount} from 'wagmi';
import Head from 'next/head';
import { TelegramProvider, useTelegram } from "../components/webapp";
import styles from '../styles/Home.module.css';
import { LensClient, development } from "@lens-protocol/client";


const Home = () => {
  const { user, webApp } = useTelegram();
  console.log(user);
  return (
    <div className={styles.container}>
      <Head>
        <title>RainbowKit App</title>
        <meta
          content="Generated by @rainbow-me/create-rainbowkit"
          name="description"
        />
        <link href="/favicon.ico" rel="icon" />
      </Head>

      <main className={styles.main}>
        <ConnectButton />
          <LensAuthentication />
         {user && (
              <div>
                  {user}
              </div>
            )}

      </main>

      <footer className={styles.footer}>
        <a href="https://rainbow.me" rel="noopener noreferrer" target="_blank">
          Made with ❤️ by your frens at 🌈
        </a>
      </footer>
    </div>
  );
};

export default Home;
