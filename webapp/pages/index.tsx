import { ConnectButton } from '@rainbow-me/rainbowkit';
import VerifyWorldId from "../../components/worldcoinVerify";
import type { NextPage } from 'next';
import LensAuthentication from '../components/login';
import {useAccount} from 'wagmi';
import Head from 'next/head';
import { TelegramProvider, useTelegram } from "../components/webapp";
import styles from '../styles/Home.module.css';
import { LensClient, development } from "@lens-protocol/client";
const action = "mint-collab-nft";
const app_id = "app_staging_7d739ad0b13ae36395a73a4c9e8fa198";



const Home = () => {
  const [verified, setVerified] = useState(false);
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
      </main>

      <footer className={styles.footer}>
        <a href="https://rainbow.me" rel="noopener noreferrer" target="_blank">
          Made with ❤️ by your frens at 🌈
        </a>
      </footer>
    </div>
  );
};

const WithTelegramProvider = () => {
  return (
    <TelegramProvider>
      <Home />
    </TelegramProvider>
  );
};

export default WithTelegramProvider;
